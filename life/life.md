~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include <args.mds>
include <forms.mds>


# Life application main entry point
function lifeMain():
    # Set the title
    documentSetTitle("Conway's Game of Life")

    # Parse arguments
    args = argsParse(lifeArguments)
    objectSet(args, 'background', objectGet(args, 'background') % arrayLength(lifeColors))
    objectSet(args, 'border', mathMax(minBorder, objectGet(args, 'border')))
    objectSet(args, 'borderRatio', mathMax(0, mathMin(0.4, objectGet(args, 'borderRatio'))))
    objectSet(args, 'color', objectGet(args, 'color') % arrayLength(lifeColors))
    objectSet(args, 'gap', mathMax(1, objectGet(args, 'gap')))
    objectSet(args, 'initRatio', mathMax(0, mathMin(1, objectGet(args, 'initRatio'))))
    objectSet(args, 'rate', mathMax(0, mathMin(arrayLength(lifeRates) - 1, objectGet(args, 'rate'))))

    # Load the life state
    life = lifeLoad(args)

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
    windowSetResize(systemPartial(lifeRender, life, args))
endfunction


# The Life application arguments
lifeArguments = argsValidate(arrayNew( \
    objectNew('name', 'background', 'type', 'int', 'default', 1), \
    objectNew('name', 'border', 'type', 'int', 'default', 0), \
    objectNew('name', 'borderRatio', 'type', 'float', 'default', 0.1), \
    objectNew('name', 'color', 'type', 'int', 'default', 0), \
    objectNew('name', 'depth', 'type', 'int', 'default', 6), \
    objectNew('name', 'fullScreen', 'type', 'bool', 'default', false), \
    objectNew('name', 'gap', 'type', 'int', 'default', 1), \
    objectNew('name', 'initRatio', 'type', 'float', 'default', 0.2), \
    objectNew('name', 'load', 'explicit', true), \
    objectNew('name', 'play', 'type', 'bool', 'default', true), \
    objectNew('name', 'rate', 'type', 'int', 'default', 2), \
    objectNew('name', 'save', 'type', 'bool', 'default', false, 'explicit', true) \
))


# Render the Life application
function lifeRender(life, args):
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
    lifeSetTimeout(life, args)
endfunction


# Helper to set the timeout handler
function lifeSetTimeout(life, args, startTime, endTime):
    ellapsedMs = if(startTime != null && endTime != null, endTime - startTime, 0)
    periodMs = mathMax(0, 1000 / arrayGet(lifeRates, objectGet(args, 'rate')) - ellapsedMs)
    if objectGet(args, 'play'):
        windowSetTimeout(systemPartial(lifeTimeout, life, args), periodMs)
    endif
endfunction


# Life application timeout handler
function lifeTimeout(life, args):
    startTime = datetimeNow()

    # Compute the next life state
    lifeJSON = jsonStringify(objectGet(life, 'cells'))
    life = lifeNext(life)

    # Is there a cycle?
    depth = objectGet(args, 'depth')
    lifeCycle = life
    iCycle = 0
    while iCycle < depth:
        if lifeJSON == jsonStringify(objectGet(lifeCycle, 'cells')):
            life = lifeNew(args, objectGet(life, 'width'), objectGet(life, 'height'), objectGet(life, 'initial'))
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
    lifeSetTimeout(life, args, startTime, endTime)
endfunction


# Create the Life application menu element model
function lifeMenuElements(life, args):
    # Menu separators
    nbsp = stringFromCharCode(160)
    linkSeparator = objectNew('text', ' ')
    linkSection = objectNew('text', nbsp + '| ')

    # Color menu part
    background = objectGet(args, 'background')
    border = objectGet(args, 'border')
    color = objectGet(args, 'color')
    nextColor = (color + 1) % arrayLength(lifeColors)
    nextColor = if(nextColor != background, nextColor, (nextColor + 1) % arrayLength(lifeColors))
    nextBackground = (background + 1) % arrayLength(lifeColors)
    nextBackground = if(nextBackground != color, nextBackground, (nextBackground + 1) % arrayLength(lifeColors))
    colorElements = arrayNew( \
        formsLinkElements('Ground', argsURL(lifeArguments, objectNew('background', nextBackground))), \
        linkSeparator, \
        formsLinkElements('Cell', argsURL(lifeArguments, objectNew('color', nextColor))), \
        linkSeparator, \
        formsLinkElements('Border', argsURL(lifeArguments, objectNew('border', if(border == 0, 5, 0)))), \
        linkSection, \
        formsLinkElements('Full', argsURL(lifeArguments, objectNew('fullScreen', 1))) \
    )

    # Which menu? (play, save, or pause)
    if objectGet(args, 'play'):
        rate = objectGet(args, 'rate')
        return arrayNew( \
            formsLinkElements('Pause', argsURL(lifeArguments, objectNew('play', 0))), \
            linkSection, \
            colorElements, \
            linkSection, \
            formsLinkElements('<<', if(rate > 0, argsURL(lifeArguments, objectNew('rate', rate - 1)))), \
            arrayNew(objectNew('text', nbsp + arrayGet(lifeRates, rate) + nbsp + 'Hz' + nbsp)), \
            formsLinkElements('>>', if(rate < arrayLength(lifeRates) - 1, argsURL(lifeArguments, objectNew('rate', rate + 1)))) \
        )
    elif objectGet(args, 'save'):
        return arrayNew( \
            objectNew('text', 'Save: '), \
            formsLinkElements('Load', argsURL(lifeArguments, objectNew('load', lifeEncode(life)))) \
        )
    else:
        # Pause menu
        return arrayNew( \
            formsLinkElements('Play', argsURL(lifeArguments, objectNew('play', 1))), \
            linkSection, \
            formsLinkButtonElements('Step', systemPartial(lifeClickStep, life, args)), \
            linkSeparator, \
            formsLinkButtonElements('Random', systemPartial(lifeClickRandom, life, args)), \
            linkSeparator, \
            formsLinkButtonElements('Reset', systemPartial(lifeClickReset, args)), \
            linkSeparator, \
            formsLinkElements('Save', argsURL(lifeArguments, objectNew('play', 0, 'save', 1))), \
            linkSection, \
            colorElements, \
            linkSection, \
            formsLinkButtonElements('<<', systemPartial(lifeClickWidthHeight, life, args, -5, 0)), \
            arrayNew(objectNew('text', nbsp + 'Width' + nbsp)), \
            formsLinkButtonElements('>>', systemPartial(lifeClickWidthHeight, life, args, 5, 0)), \
            linkSection, \
            formsLinkButtonElements('<<', systemPartial(lifeClickWidthHeight, life, args, 0, -5)), \
            arrayNew(objectNew('text', nbsp + 'Height' + nbsp)), \
            formsLinkButtonElements('>>', systemPartial(lifeClickWidthHeight, life, args, 0, 5)) \
        )
    endif
endfunction


# The Life application menu change rates, in Hz
lifeRates = arrayNew(0.5, 1, 2, 4, 6, 8, 10, 20, 30)

# The Life application menu colors
lifeColors = arrayNew('forestgreen', 'white' , 'lightgray', 'greenyellow', 'gold', 'magenta', 'cornflowerblue')

# The Life application menu/board document reset ID
lifeDocumentResetID = 'lifeReset'


# Life application step click handler
function lifeClickStep(life, args):
    life = lifeNext(life)
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Life application random click handler
function lifeClickRandom(life, args):
    life = lifeNew(args, objectGet(life, 'width'), objectGet(life, 'height'))
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Life application reset click handler
function lifeClickReset(args):
    # Create a default life
    life = lifeNew(args)
    lifeSave(life)

    # If we're already at the reset location, just update
    resetLocation = argsURL(lifeArguments, objectNew('play', false), true)
    if resetLocation == argsURL(lifeArguments):
        lifeRender(life, args)
        return
    endif

    windowSetLocation(resetLocation)
endfunction


# Life application width/height click handler
function lifeClickWidthHeight(life, args, widthDelta, heightDelta):
    width = mathMax(10, widthDelta + objectGet(life, 'width'))
    height = mathMax(10, heightDelta + objectGet(life, 'height'))
    life = lifeNew(args, width, height)
    lifeSave(life)
    lifeRender(life, args)
endfunction


# Life application cell click handler
function lifeClickCell(life, args, px, py):
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
function lifeNew(args, width, height, initial):
    width = if(width != null, width, 50)
    height = if(height != null, height, 50)
    cells = arrayNewSize(width * height)

    # Initialize the life
    if args != null:
        initRatio = objectGet(args, 'initRatio')
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
function lifeLoad(args):
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
        life = lifeNew(args)
        lifeSave(life)
    endif

    return life
endfunction


# Save the Life object to session storage
function lifeSave(life):
    sessionStorageSet('life', jsonStringify(life))
endfunction


# Draw the life board
function lifeDraw(life, args):
    # Set the drawing size
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    size = lifeSize(life, args)
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')
    drawNew(width * (gap + size) + gap + 2 * border, height * (gap + size) + gap + 2 * border)

    # Set the cell click handler
    if !objectGet(args, 'play'):
        drawOnClick(systemPartial(lifeClickCell, life, args))
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
function lifeSize(life, args):
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
function lifeNext(life):
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')

    # Compute the next life generation
    lifeNext = lifeNew(null, width, height, objectGet(life, 'initial'))
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
function lifeEncode(life):
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
function lifeDecode(lifeStr):
    # Split the encoded life string into width, height, and cell string
    parts = stringSplit(lifeStr, '-')
    width = numberParseInt(arrayGet(parts, 0))
    height = numberParseInt(arrayGet(parts, 1))
    cellsStr = arrayGet(parts, 2)

    # Decode the cell string
    life = lifeNew(null, width, height, lifeStr)
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
