~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include <forms.mds>


# Life application main entry point
function lifeMain()
    # Set the title
    documentSetTitle("Conway's Game of Life")

    # Load the life state
    life = lifeLoad()
    args = lifeArgs()

    # Load argument provided?
    load = objectGet(args, 'load')
    if load != null:
        # Decode the load argument
        loadedLife = lifeDecode(load)

        # Save the loaded life (unless its already loaded)
        if load != objectGet(life, 'initial'):
            life = loadedLife
            lifeSave(loadedLife)
        endif
    endif

    # Render the application
    lifeRender(life, args)

    # Set the window resize handler
    windowSetResize(lifeResize)
endfunction


# Render the Life application
function lifeRender(life, args)
    # Render the menu
    elementModelRender(arrayNew( \
        if(!objectGet(args, 'fullScreen'), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'b', 'elem', objectNew('text', "Conway's Game of Life")), \
                objectNew('html', 'br'), \
                lifeMenuElements(life, args) \
            )) \
        ), \
        objectNew('html', 'div', 'attr', objectNew('id', lifeDocumentResetID, 'style', 'display: none;')) \
    ))

    # Render the Life board
    lifeDraw(life, args)

    # Set the timeout handler
    lifeSetTimeout(args)
endfunction


# Helper to set the timeout handler
function lifeSetTimeout(args, startTime, endTime)
    ellapsedMs = if(startTime != null && endTime != null, endTime - startTime, 0)
    periodMs = mathMax(0, 1000 / arrayGet(lifeRates, objectGet(args, 'rate')) - ellapsedMs)
    if objectGet(args, 'play'):
        windowSetTimeout(lifeTimeout, periodMs)
    endif
endfunction


# Life application window resize handler
function lifeResize()
    life = lifeLoad()
    args = lifeArgs()
    lifeRender(life, args)
endfunction


# Life application timeout handler
function lifeTimeout()
    startTime = datetimeNow()
    life = lifeLoad()
    args = lifeArgs()

    # Compute the next life state
    lifeJSON = jsonStringify(objectGet(life, 'cells'))
    life = lifeNext(life)

    # Is there a cycle?
    depth = objectGet(args, 'depth')
    lifeCycle = life
    iCycle = 0
    while iCycle < depth:
        if lifeJSON == jsonStringify(objectGet(lifeCycle, 'cells')):
            life = lifeNew(objectGet(life, 'width'), objectGet(life, 'height'), objectGet(life, 'initial'))
            break
        endif
        lifeCycle = lifeNext(lifeCycle)
        iCycle = iCycle + 1
    endwhile

    # Update the life state
    lifeSave(life)

    # Render the application
    documentSetReset(lifeDocumentResetID)
    lifeDraw(life, args)

    # Set the timeout handler
    endTime = datetimeNow()
    lifeSetTimeout(args, startTime, endTime)
endfunction


# Create the Life application variable-arguments object
function lifeArgs(raw)
    args = objectNew()
    objectSet(args, 'background', if(vBackground != null, vBackground % arrayLength(lifeColors), if(!raw, 1)))
    objectSet(args, 'border', if(vBorder != null, mathMax(minBorder, vBorder), if(!raw, 0)))
    objectSet(args, 'borderRatio', if(vBorderRatio != null, mathMax(0, mathMin(1, vBorderRatio)), if(!raw, 0.1)))
    objectSet(args, 'color', if(vColor != null, vColor % arrayLength(lifeColors), if(!raw, 0)))
    objectSet(args, 'depth', if(vDepth != null, vDepth, if(!raw, 6)))
    objectSet(args, 'fullScreen', if(vFullScreen != null, if(vFullScreen, 1, 0), if(!raw, 0)))
    objectSet(args, 'gap', if(vGap != null, mathMax(1, vGap), if(!raw,  1)))
    objectSet(args, 'initRatio', if(vInitRatio != null, mathMax(0, mathMin(1, vInitRatio)), if(!raw, 0.2)))
    objectSet(args, 'load', vLoad)
    objectSet(args, 'play', if(vPlay != null, if(vPlay, 1, 0), if(!raw, 1)))
    objectSet(args, 'rate', if(vRate != null, mathMax(0, mathMin(arrayLength(lifeRates) - 1, vRate)), if(!raw, 1)))
    objectSet(args, 'save', if(vSave != null, if(vSave, 1, 0), if(!raw, 0)))
    return args
endfunction


# Create the Life application menu element model
function lifeMenuElements(life, args)
    # Menu separators
    nbsp = stringFromCharCode(160)
    linkSeparator = objectNew('text', ' ')
    linkSection = objectNew('text', nbsp + '| ')

    # Color menu part
    argsRaw = lifeArgs(true)
    background = objectGet(args, 'background')
    borderRaw = objectGet(argsRaw, 'border')
    color = objectGet(args, 'color')
    nextColor = (color + 1) % arrayLength(lifeColors)
    nextColor = if(nextColor != background, nextColor, (nextColor + 1) % arrayLength(lifeColors))
    nextBackground = (background + 1) % arrayLength(lifeColors)
    nextBackground = if(nextBackground != color, nextBackground, (nextBackground + 1) % arrayLength(lifeColors))
    colorElements = arrayNew( \
        formsLinkElements('Ground', lifeURL(argsRaw, objectNew('background', nextBackground))), \
        linkSeparator, \
        formsLinkElements('Cell', lifeURL(argsRaw, objectNew('color', nextColor))), \
        linkSeparator, \
        formsLinkElements('Border', lifeURL(argsRaw, objectNew('border', if(borderRaw != null, 0, 5)))), \
        linkSection, \
        formsLinkElements('Full', lifeURL(argsRaw, objectNew('fullScreen', 1))) \
    )

    # Which menu? (play, save, or pause)
    if objectGet(args, 'play'):
        rate = objectGet(args, 'rate')
        return arrayNew( \
            formsLinkElements('Pause', lifeURL(argsRaw, objectNew('play', 0))), \
            linkSection, \
            colorElements, \
            linkSection, \
            formsLinkElements('<<', if(rate > 0, lifeURL(argsRaw, objectNew('rate', rate - 1)))), \
            arrayNew(objectNew('text', nbsp + arrayGet(lifeRates, rate) + nbsp + 'Hz' + nbsp)), \
            formsLinkElements('>>', if(rate < arrayLength(lifeRates) - 1, lifeURL(argsRaw, objectNew('rate', rate + 1)))) \
        )
    elif objectGet(args, 'save'):
        return arrayNew( \
            objectNew('text', 'Save: '), \
            formsLinkElements('Load', lifeURL(argsRaw, objectNew('load', lifeEncode(life)))) \
        )
    else:
        # Pause menu
        return arrayNew( \
            formsLinkElements('Play', lifeURL(argsRaw, objectNew('play', 1))), \
            linkSection, \
            formsLinkButtonElements('Step', lifeClickStep), \
            linkSeparator, \
            formsLinkButtonElements('Random', lifeClickRandom), \
            linkSeparator, \
            formsLinkButtonElements('Reset', lifeClickReset), \
            linkSeparator, \
            formsLinkElements('Save', lifeURL(argsRaw, objectNew('play', 0, 'save', 1))), \
            linkSection, \
            colorElements, \
            linkSection, \
            formsLinkButtonElements('<<', lifeClickWidthLess), \
            arrayNew(objectNew('text', nbsp + 'Width' + nbsp)), \
            formsLinkButtonElements('>>', lifeClickWidthMore), \
            linkSection, \
            formsLinkButtonElements('<<', lifeClickHeightLess), \
            arrayNew(objectNew('text', nbsp + 'Height' + nbsp)), \
            formsLinkButtonElements('>>', lifeClickHeightMore) \
        )
    endif
endfunction


# The Life application menu change rates, in Hz
lifeRates = arrayNew(0.5, 1, 2, 4, 6, 8, 10, 20, 30)

# The Life application menu colors
lifeColors = arrayNew('forestgreen', 'white' , 'lightgray', 'greenyellow', 'gold', 'magenta', 'cornflowerblue')

# The Life application menu/board document reset ID
lifeDocumentResetID = 'lifeReset'


# Helper to create an application URL
function lifeURL(argsRaw, args)
    # URL arguments
    play = objectGet(args, 'play')
    rate = objectGet(args, 'rate')
    color = objectGet(args, 'color')
    background = objectGet(args, 'background')
    border = objectGet(args, 'border')
    save = objectGet(args, 'save')
    load = objectGet(args, 'load')
    fullScreen = objectGet(args, 'fullScreen')

    # Variable arguments
    play = if(play != null, play, objectGet(argsRaw, 'play'))
    rate = if(rate != null, rate, objectGet(argsRaw, 'rate'))
    color = if(color != null, color, objectGet(argsRaw, 'color'))
    background = if(background != null, background, objectGet(argsRaw, 'background'))
    border = if(border != null, if(border, border, null), objectGet(argsRaw, 'border'))
    fullScreen = if(fullScreen != null, fullScreen, objectGet(argsRaw, 'fullScreen'))
    gap = objectGet(argsRaw, 'gap')
    depth = objectGet(argsRaw, 'depth')
    initRatio = objectGet(argsRaw, 'initRatio')
    borderRatio = objectGet(argsRaw, 'borderRatio')

    # Return the URL
    parts = arrayNew()
    if(background != null, arrayPush(parts, 'var.vBackground=' + background))
    if(border != null, arrayPush(parts, 'var.vBorder=' + border))
    if(borderRatio != null, arrayPush(parts, 'var.vBorderRatio=' + borderRatio))
    if(color != null, arrayPush(parts, 'var.vColor=' + color))
    if(depth != null, arrayPush(parts, 'var.vDepth=' + depth))
    if(fullScreen != null, arrayPush(parts, 'var.vFullScreen=' + fullScreen))
    if(gap != null, arrayPush(parts, 'var.vGap=' + gap))
    if(initRatio != null, arrayPush(parts, 'var.vInitRatio=' + initRatio))
    if(load != null, arrayPush(parts, "var.vLoad='" + load + "'"))
    if(play != null, arrayPush(parts, 'var.vPlay=' + play))
    if(rate != null, arrayPush(parts, 'var.vRate=' + rate))
    if(save, arrayPush(parts, 'var.vSave=1'))
    return if(arrayLength(parts), '#' + arrayJoin(parts, '&'), '#var=')
endfunction


# Life application step click handler
function lifeClickStep()
    life = lifeLoad()
    life = lifeNext(life)
    args = lifeArgs()
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Life application random click handler
function lifeClickRandom()
    life = lifeLoad()
    life = lifeNew(objectGet(life, 'width'), objectGet(life, 'height'))
    args = lifeArgs()
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Life application reset click handler
function lifeClickReset()
    life = lifeNew()
    args = lifeArgs()
    lifeSave(life)

    # If we're already at the reset location, just update
    resetLocation = '#var.vPlay=0'
    argsRaw = lifeArgs(true)
    if lifeURL(argsRaw) == resetLocation:
        lifeRender(life, args)
        return
    endif

    windowSetLocation(resetLocation)
endfunction


# Life application width-less click handler
function lifeClickWidthLess()
    lifeRenderWidthHeight(-5, 0)
endfunction


# Life application width-more click handler
function lifeClickWidthMore()
    lifeRenderWidthHeight(5, 0)
endfunction


# Life application height-less click handler
function lifeClickHeightLess()
    lifeRenderWidthHeight(0, -5)
endfunction


# Life application height-more click handler
function lifeClickHeightMore()
    lifeRenderWidthHeight(0, 5)
endfunction


# Helper for width/height less/more click handlers
function lifeRenderWidthHeight(widthDelta, heightDelta)
    life = lifeLoad()
    args = lifeArgs()
    width = mathMax(10, mathCeil(widthDelta + objectGet(life, 'width')))
    height = mathMax(10, mathCeil(heightDelta + objectGet(life, 'height')))
    life = lifeNew(width, height)
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Life application cell click handler
function lifeClickCell(px, py)
    life = lifeLoad()
    args = lifeArgs()
    size = lifeSize(life, args)
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')

    # Compute the cell index to toggle
    x = mathMax(0, mathMin(objectGet(life, 'width') - 1, mathFloor((px - border) / (size + gap))))
    y = mathMax(0, mathMin(objectGet(life, 'height') - 1, mathFloor((py - border) / (size + gap))))
    iCell = y * objectGet(life, 'width') + x

    # Toggle the cell
    cells = objectGet(life, 'cells')
    arraySet(cells, iCell, if(arrayGet(cells, iCell), 0, 1))

    # Update the life state and re-render
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Create a new Life object
function lifeNew(width, height, initial, noInit)
    width = if(width != null, width, 50)
    height = if(height != null, height, 50)
    cells = arrayNewSize(width * height)

    # Initialize the life
    args = lifeArgs()
    initRatio = objectGet(args, 'initRatio')
    if !noInit && initRatio:
        borderRatio = objectGet(args, 'borderRatio')
        border = mathCeil(borderRatio * mathMin(width, height))
        y = 0
        while y < height:
            x = 0
            while x < width:
                arraySet(cells, y * width + x, \
                    if(x >= border && x < width - border && y >= border && y < height - border && mathRandom() < initRatio, 1, 0))
                x = x + 1
            endwhile
            y = y + 1
        endwhile
    endif

    # Create the blank life object
    life = objectNew('width', width, 'height', height, 'initial', initial, 'cells', cells)
    if initial == null:
        objectSet(life, 'initial', lifeEncode(life))
    endif

    return life
endfunction


# Load and validate the Life object from session storage, or create a new one
function lifeLoad()
    # Parse and validate the session storage
    lifeJSON = sessionStorageGet('life')
    life = null
    if lifeJSON != null:
        life = jsonParse(lifeJSON)
        if life != null:
            life = schemaValidate(lifeSession, 'Life', life)
            if life != null && objectGet(life, 'width') * objectGet(life, 'height') != arrayLength(objectGet(life, 'cells')):
                life = null
            endif
        endif
    endif

    # If there is no session, create a default session
    if life == null:
        life = lifeNew()
        lifeSave(life)
    endif

    return life
endfunction


# Save the Life object to session storage
function lifeSave(life)
    sessionStorageSet('life', jsonStringify(life))
endfunction


# Draw the life board
function lifeDraw(life, args)
    # Set the drawing size
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    size = lifeSize(life, args)
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')
    drawNew(width * (gap + size) + gap + 2 * border, height * (gap + size) + gap + 2 * border)

    # Set the cell click handler
    if !objectGet(args, 'play'):
        drawOnClick(lifeClickCell)
    endif

    # Draw the background
    drawStyle('#606060', border, arrayGet(lifeColors, objectGet(args, 'background')))
    drawRect(0.5 * border, 0.5 * border, drawWidth() - border, drawHeight() - border)

    # Draw the cells
    drawStyle('none', 0, arrayGet(lifeColors, objectGet(args, 'color')))
    cells = objectGet(life, 'cells')
    y = 0
    while y < height:
        x = 0
        while x < width:
            if arrayGet(cells, y * width + x):
                drawPathRect(border + gap + x * (size + gap), border + gap + y * (size + gap), size, size)
            endif
            x = x + 1
        endwhile
        y = y + 1
    endwhile
endfunction


# Compute the Life board cell size
function lifeSize(life, args)
    totalWidth = windowWidth() - 3 * documentFontSize()
    totalHeight = windowHeight() - if(objectGet(args, 'fullScreen'), 3, 6) * documentFontSize()
    lifeWidth = objectGet(life, 'width')
    lifeHeight = objectGet(life, 'height')
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')
    sizeWidth = (totalWidth - gap * (lifeWidth + 1) - 2 * border) / lifeWidth
    sizeHeight = (totalHeight - gap * (lifeHeight + 1) - 2 * border) / lifeHeight
    return mathMax(1, mathMin(sizeWidth, sizeHeight))
endfunction


# Compute the next Life object state
function lifeNext(life)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')

    # Compute the next life generation
    lifeNext = lifeNew(width, height, objectGet(life, 'initial'), true)
    nextCells = objectGet(lifeNext, 'cells')
    y = 0
    while y < height:
        x = 0
        while x < width:
            neighbor = if(x > 0 && y > 0, arrayGet(cells, (y - 1) * width + x - 1), 0) + \
                if(y > 0, arrayGet(cells, (y - 1) * width + x), 0) + \
                if(x < width - 1 && y > 0, arrayGet(cells, (y - 1) * width + x + 1), 0) + \
                if(x > 0, arrayGet(cells, y * width + x - 1), 0) + \
                if(x < width - 1, arrayGet(cells, y * width + x + 1), 0) + \
                if(x > 0 && y < height - 1, arrayGet(cells, (y + 1) * width + x - 1), 0) + \
                if(y < height - 1, arrayGet(cells, (y + 1) * width + x), 0) + \
                if(x < width - 1 && y < height - 1, arrayGet(cells, (y + 1) * width + x + 1), 0)
            arraySet(nextCells, y * width + x, \
                if(arrayGet(cells, y * width + x), if(neighbor < 2, 0, if(neighbor > 3, 0, 1)), if(neighbor == 3, 1, 0)))
            x = x + 1
        endwhile
        y = y + 1
    endwhile

    return lifeNext
endfunction


# Encode the Life object
function lifeEncode(life)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')
    lifeChars = arrayNew()

    # Compute runs of alive/not-alive cells
    alive = 0
    count = 0
    maxCount = stringLength(lifeEncodeChars) - 1
    for curAlive, iCell in cells:
        if curAlive == alive:
            count = count + 1
            if count == maxCount:
                arrayPush(lifeChars, stringSlice(lifeEncodeChars, count, count + 1))
                alive = if(alive, 0, 1)
                count = 0
            endif
        else:
            arrayPush(lifeChars, stringSlice(lifeEncodeChars, count, count + 1))
            alive = if(alive, 0, 1)
            count = 1
        endif
    endfor

    # Add the final run
    if count:
        arrayPush(lifeChars, stringSlice(lifeEncodeChars, count, count + 1))
    endif

    return width + '-' + height + '-' + arrayJoin(lifeChars, '')
endfunction


# Decode the Life object
function lifeDecode(lifeStr)
    # Split the encoded life string into width, height, and cell string
    parts = stringSplit(lifeStr, '-')
    width = numberParseInt(arrayGet(parts, 0))
    height = numberParseInt(arrayGet(parts, 1))
    cellsStr = arrayGet(parts, 2)

    # Decode the cell string
    life = lifeNew(width, height, lifeStr, true)
    cells = objectGet(life, 'cells')
    iCell = 0
    iChar = 0
    cellsStrLength = stringLength(cellsStr)
    while iChar < cellsStrLength:
        char = stringSlice(cellsStr, iChar, iChar + 1)
        count = stringIndexOf(lifeEncodeChars, char)
        iCount = 0
        while iCount < count:
            arraySet(cells, iCell, iChar % 2)
            iCount = iCount + 1
            iCell = iCell + 1
        endwhile
        iChar = iChar + 1
    endwhile

    return life
endfunction


# Life encoding characters
lifeEncodeAlpha = 'abcdefghijklmnopqrstuvwxyz'
lifeEncodeChars = '0123456789' + lifeEncodeAlpha + stringUpper(lifeEncodeAlpha)


# Life session state object schema
lifeSession = schemaParse( \
    '# The Life session state', \
    'struct Life', \
    '', \
    '    # The Life board width', \
    '    int(>= 10) width', \
    '', \
    '    # The Life board height', \
    '    int(>= 10) height', \
    '', \
    '    # The Life board cell state array', \
    '    int(>= 0, <= 1)[len > 0] cells', \
    '', \
    "    # The Life board's encoded initial cell state", \
    '    string initial' \
)


# Execute the main entry point
lifeMain()
~~~
