~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


# Life application main entry point
function lifeMain()
    # Application arguments
    args = lifeArgs()

    # Title
    title = "Conway's Game of Life"
    setDocumentTitle(title)

    # Load the life state
    life = lifeLoad()

    # Load argument provided?
    load = objectGet(args, 'load')
    jumpif (load == null) loadDone
        loadedLife = lifeDecode(load)

        # Save the loaded life (unless its already loaded)
        jumpif (load == objectGet(life, 'initial')) loadDone
            life = loadedLife
            lifeSave(loadedLife)
    loadDone:

    # Render the menu
    elementModelRender(arrayNew( \
        if(!objectGet(args, 'fullScreen'), objectNew('html', 'p', 'elem', arrayNew( \
            objectNew('html', 'b', 'elem', objectNew('text', title)), \
            objectNew('html', 'br'), \
            lifeMenuElements(args, life) \
        ))), \
        objectNew('html', 'div', 'attr', objectNew('id', lifeDocumentResetID, 'style', 'display: none;')) \
    ))

    # Life board
    lifeDraw(life, args)

    # Set the play timeout
    period = 1000 / arrayGet(lifeFrequencies, objectGet(args, 'freq'))
    if(objectGet(args, 'play') && !objectGet(args, 'save'), setWindowTimeout(lifeOnTimeout, period))

    # Set the window resize handler
    setWindowResize(main)
endfunction


# Helper to update the Life application following a Life object state change
function lifeUpdate(periodAdjust)
    periodAdjust = if(periodAdjust != null, periodAdjust, 0)

    # Is there a load argument? If so, delete it and update the window location
    argsRaw = lifeArgs(true)
    jumpif (objectGet(argsRaw, 'load') == null) loadDone
        objectDelete(argsRaw, 'load')
        setWindowLocation(lifeURL(argsRaw))
        return
    loadDone:

    # Re-render
    args = lifeArgs()
    setDocumentReset(lifeDocumentResetID)
    lifeDraw(lifeLoad(), args)

    # Set the play timeout
    period = mathMax(0, 1000 / arrayGet(lifeFrequencies, objectGet(args, 'freq')) - periodAdjust)
    if(objectGet(args, 'play'), setWindowTimeout(lifeOnTimeout, period))
endfunction


# Create the Life application variable-arguments object
function lifeArgs(raw)
    args = objectNew()
    if(vBackground != null || !raw, \
        objectSet(args, 'background', if(vBackground != null, vBackground % arrayLength(lifeColors), 1)))
    if(vBorder != null || !raw, \
        objectSet(args, 'border', if(vBorder != null, mathMax(minBorder, vBorder), 0)))
    if(vBorderRatio != null || !raw, \
        objectSet(args, 'borderRatio', if(vBorderRatio != null, mathMax(0, mathMin(1, vBorderRatio)), 0.1)))
    if(vColor != null || !raw, \
        objectSet(args, 'color', if(vColor != null, vColor % arrayLength(lifeColors), 0)))
    if(vDepth != null || !raw, \
        objectSet(args, 'depth', if(vDepth != null, vDepth, 6)))
    if(vFreq != null || !raw, \
        objectSet(args, 'freq', if(vFreq != null, mathMax(0, mathMin(arrayLength(lifeFrequencies) - 1, vFreq)), 1)))
    if(vFullScreen != null || !raw, \
        objectSet(args, 'fullScreen', if(vFullScreen != null, if(vFullScreen, 1, 0), 0)))
    if(vGap != null || !raw, \
        objectSet(args, 'gap', if(vGap != null, mathMax(1, vGap),  1)))
    if(vInitRatio != null || !raw, \
        objectSet(args, 'initRatio', if(vInitRatio != null, mathMax(0, mathMin(1, vInitRatio)), 0.2)))
    if(vLoad != null, \
        objectSet(args, 'load', vLoad))
    if(vPlay != null || !raw, \
        objectSet(args, 'play', if(vPlay != null, if(vPlay, 1, 0), 1)))
    if(vSave != null || !raw, \
        objectSet(args, 'save', if(vSave != null, if(vSave, 1, 0), 0)))
    return args
endfunction


# Create the Life application menu element model
function lifeMenuElements(args, life)
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
        lifeLinkElements('Ground', lifeURL(argsRaw, objectNew('background', nextBackground))), \
        linkSeparator, \
        lifeLinkElements('Cell', lifeURL(argsRaw, objectNew('color', nextColor))), \
        linkSeparator, \
        lifeLinkElements('Border', lifeURL(argsRaw, objectNew('border', if(borderRaw != null, 0, 5)))), \
        linkSection, \
        lifeLinkElements('Full', lifeURL(argsRaw, objectNew('fullScreen', 1))) \
    )

    # Which menu? (save, play, or pause)
    jumpif (objectGet(args, 'save')) menuSave
    jumpif (objectGet(args, 'play')) menuPlay
        # Pause menu
        return arrayNew( \
            lifeLinkElements('Play', lifeURL(argsRaw, objectNew('play', 1))), \
            linkSection, \
            lifeButtonElements('Step', lifeOnClickStep), \
            linkSeparator, \
            lifeButtonElements('Random', lifeOnClickRandom), \
            linkSeparator, \
            lifeButtonElements('Reset', lifeOnClickReset), \
            linkSeparator, \
            lifeLinkElements('Save', lifeURL(argsRaw, objectNew('play', 0, 'save', 1))), \
            linkSection, \
            colorElements, \
            linkSection, \
            lifeButtonElements('<<', lifeOnClickWidthLess), \
            arrayNew(objectNew('text', nbsp + 'Width' + nbsp)), \
            lifeButtonElements('>>', lifeOnClickWidthMore), \
            linkSection, \
            lifeButtonElements('<<', lifeOnClickHeightLess), \
            arrayNew(objectNew('text', nbsp + 'Height' + nbsp)), \
            lifeButtonElements('>>', lifeOnClickHeightMore) \
        )
        jump menuDone
    menuPlay:
        freq = objectGet(args, 'freq')
        return arrayNew( \
            lifeLinkElements('Pause', lifeURL(argsRaw, objectNew('play', 0))), \
            linkSection, \
            colorElements, \
            linkSection, \
            lifeLinkElements('<<', lifeURL(argsRaw, objectNew('freq', mathMax(0, freq - 1)))), \
            arrayNew(objectNew('text', nbsp + arrayGet(lifeFrequencies, freq) + nbsp + 'Hz' + nbsp)), \
            lifeLinkElements('>>', lifeURL(argsRaw, objectNew('freq', mathMin(arrayLength(lifeFrequencies) - 1, freq + 1)))) \
        )
        jump menuDone
    menuSave:
        return arrayNew( \
            objectNew('text', 'Save: '), \
            lifeLinkElements('Load', lifeURL(argsRaw, objectNew('load', lifeEncode(life)))) \
        )
    menuDone:
endfunction


# The Life application menu change frequencies, in Hz
lifeFrequencies = arrayNew(0.5, 1, 2, 4, 6, 8, 10, 20, 30)

# The Life application menu colors
lifeColors = arrayNew('forestgreen', 'white' , 'lightgray', 'greenyellow', 'gold', 'magenta', 'cornflowerblue')

# The Life application menu/board document reset ID
lifeDocumentResetID = 'lifeReset'


# Create a life application URL
function lifeURL(argsRaw, options)
    # Options
    play = objectGet(options, 'play')
    freq = objectGet(options, 'freq')
    color = objectGet(options, 'color')
    background = objectGet(options, 'background')
    border = objectGet(options, 'border')
    save = objectGet(options, 'save')
    load = objectGet(options, 'load')
    fullScreen = objectGet(options, 'fullScreen')

    # Variable arguments
    play = if(play != null, play, objectGet(argsRaw, 'play'))
    freq = if(freq != null, freq, objectGet(argsRaw, 'freq'))
    color = if(color != null, color, objectGet(argsRaw, 'color'))
    background = if(background != null, background, objectGet(argsRaw, 'background'))
    border = if(border != null, if(border, border, null), objectGet(argsRaw, 'border'))
    fullScreen = if(fullScreen != null, fullScreen, objectGet(argsRaw, 'fullScreen'))
    gap = objectGet(argsRaw, 'gap')
    depth = objectGet(argsRaw, 'depth')
    initRatio = objectGet(argsRaw, 'initRatio')
    borderRatio = objectGet(argsRaw, 'borderRatio')

    # Return the URL
    urlArgs = \
        if(background != null, '&var.vBackground=' + background, '') + \
        if(border != null, '&var.vBorder=' + border, '') + \
        if(borderRatio != null, '&var.vBorderRatio=' + borderRatio, '') + \
        if(color != null, '&var.vColor=' + color, '') + \
        if(depth != null, '&var.vDepth=' + depth, '') + \
        if(freq != null, '&var.vFreq=' + freq, '') + \
        if(fullScreen != null, '&var.vFullScreen=' + fullScreen, '') + \
        if(gap != null, '&var.vGap=' + gap, '') + \
        if(initRatio != null, '&var.vInitRatio=' + initRatio, '') + \
        if(load != null, "&var.vLoad='" + load + "'", '') + \
        if(play != null, '&var.vPlay=' + play, '') + \
        if(save, '&var.vSave=1', '')
    return if(stringLength(urlArgs) > 0, '#' + stringSlice(urlArgs, 1), '#var=')
endfunction


# Create a link element model
function lifeLinkElements(text, url)
    return objectNew( \
        'html', 'a', \
        'attr', objectNew('href', documentURL(url)), \
        'elem', objectNew('text', text) \
    )
endfunction


# Create a link-button element model
function lifeButtonElements(text, onclick)
    return objectNew( \
        'html', 'a', \
        'attr', objectNew('style', 'cursor: pointer; user-select: none;'), \
        'elem', objectNew('text', text), \
        'callback', objectNew('click', onclick) \
    )
endfunction


# Life application timeout handler
function lifeOnTimeout()
    # Get the start time
    startTime = datetimeNow()

    # Compute the next life state
    life = lifeLoad()
    nextLife = lifeNext(life)

    # Is there a cycle?
    args = lifeArgs()
    depth = objectGet(args, 'depth')
    lifeJSON = jsonStringify(objectGet(life, 'cells'))
    lifeCycle = nextLife
    iCycle = 0
    cycleLoop:
        jumpif (lifeJSON != jsonStringify(objectGet(lifeCycle, 'cells'))) cycleNone
            nextLife = lifeNew(objectGet(life, 'width'), objectGet(life, 'height'), objectGet(life, 'initial'))
            jump cycleDone
        cycleNone:
        lifeCycle = lifeNext(lifeCycle)
        iCycle = iCycle + 1
    jumpif (iCycle < depth) cycleLoop
    cycleDone:

    # Update the life state
    lifeSave(nextLife)

    # Compute the ellapsed time and update
    endTime = datetimeNow()
    ellapsedMs = endTime - startTime
    lifeUpdate(ellapsedMs)
endfunction


# Life application step click handler
function lifeOnClickStep()
    lifeSave(lifeNext(lifeLoad()))
    lifeUpdate()
endfunction


# Life application random click handler
function lifeOnClickRandom()
    life = lifeLoad()
    lifeSave(lifeNew(objectGet(life, 'width'), objectGet(life, 'height')))
    lifeUpdate()
endfunction


# Life application reset click handler
function lifeOnClickReset()
    lifeSave(lifeNew())
    resetArgs = (jsonStringify(lifeArgs(true)) == '{"play":0}')
    if(resetArgs, lifeMain())
    if(!resetArgs, setWindowLocation('#var.vPlay=0'))
endfunction


# Life application width-less click handler
function lifeOnClickWidthLess()
    lifeUpdateWidthHeight(-5, 0)
endfunction


# Life application width-more click handler
function lifeOnClickWidthMore()
    lifeUpdateWidthHeight(5, 0)
endfunction


# Life application height-less click handler
function lifeOnClickHeightLess()
    lifeUpdateWidthHeight(0, -5)
endfunction


# Life application height-more click handler
function lifeOnClickHeightMore()
    lifeUpdateWidthHeight(0, 5)
endfunction


# Helper for width/height less/more click handlers
function lifeUpdateWidthHeight(widthDelta, heightDelta)
    life = lifeLoad()
    width = mathMax(10, mathCeil(widthDelta + objectGet(life, 'width')))
    height = mathMax(10, mathCeil(heightDelta + objectGet(life, 'height')))
    lifeSave(lifeNew(width, height))
    lifeUpdate()
endfunction


# Life application cell click handler
function lifeOnClickCell(px, py)
    args = lifeArgs()
    life = lifeLoad()
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
    lifeUpdate()
endfunction


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


# Create a new Life object
function lifeNew(width, height, initial, noInit)
    width = if(width != null, width, 50)
    height = if(height != null, height, 50)
    cells = arrayNewSize(width * height)

    # Initialize the life
    jumpif (noInit) skipInit
        args = lifeArgs()
        initRatio = objectGet(args, 'initRatio')
        jumpif (initRatio == 0) skipInit
        borderRatio = objectGet(args, 'borderRatio')
        border = mathCeil(borderRatio * mathMin(width, height))
        y = 0
        yLoop:
            x = 0
            xLoop:
                arraySet(cells, y * width + x, \
                    if(x >= border && x < width - border && y >= border && y < height - border && mathRandom() < initRatio, 1, 0))
                x = x + 1
            jumpif (x < width) xLoop
            y = y + 1
        jumpif (y < height) yLoop
    skipInit:

    # Create the blank life object
    life = objectNew('width', width, 'height', height, 'initial', initial, 'cells', cells)
    if(initial == null, objectSet(life, 'initial', lifeEncode(life)))
    return life
endfunction


# Load and validate the Life object from session storage, or create a new one
function lifeLoad()
    life = sessionStorageGet('life')
    life = if(life != null, jsonParse(life))
    life = if(life != null, schemaValidate(lifeSession, 'Life', life))
    life = if(life != null && objectGet(life, 'width') * objectGet(life, 'height') == arrayLength(objectGet(life, 'cells')), life)
    jumpif (life != null) done
        life = lifeNew()
        lifeSave(life)
    done:
    return life
endfunction


# Save the Life object to session storage
function lifeSave(life)
    sessionStorageSet('life', jsonStringify(life))
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
    yLoop:
        x = 0
        xLoop:
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
        jumpif (x < width) xLoop
        y = y + 1
    jumpif (y < height) yLoop

    return lifeNext
endfunction


# Draw the life board
function lifeDraw(life, args)
    # Set the drawing size
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    size = lifeSize(life, args)
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')
    setDrawingSize(width * (gap + size) + gap + 2 * border, height * (gap + size) + gap + 2 * border)
    if(!objectGet(args, 'play'), drawOnClick(lifeOnClickCell))

    # Draw the background
    drawStyle('#606060', border, arrayGet(lifeColors, objectGet(args, 'background')))
    drawRect(0.5 * border, 0.5 * border, getDrawingWidth() - border, getDrawingHeight() - border)

    # Draw the cells
    drawStyle('none', 0, arrayGet(lifeColors, objectGet(args, 'color')))
    cells = objectGet(life, 'cells')
    y = 0
    yLoop:
        x = 0
        xLoop:
            jumpif (!arrayGet(cells, y * width + x)) skipCell
                px = border + gap + x * (size + gap)
                py = border + gap + y * (size + gap)
                drawMove(px, py)
                drawHLine(px + size)
                drawVLine(py + size)
                drawHLine(px)
                drawClose()
            skipCell:
            x = x + 1
        jumpif (x < width) xLoop
        y = y + 1
    jumpif (y < height) yLoop
endfunction


# Compute the Life board cell size
function lifeSize(life, args)
    totalWidth = getWindowWidth() - 3 * getDocumentFontSize()
    totalHeight = getWindowHeight() - if(objectGet(args, 'fullScreen'), 3, 6) * getDocumentFontSize()
    lifeWidth = objectGet(life, 'width')
    lifeHeight = objectGet(life, 'height')
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')
    sizeWidth = (totalWidth - gap * (lifeWidth + 1) - 2 * border) / lifeWidth
    sizeHeight = (totalHeight - gap * (lifeHeight + 1) - 2 * border) / lifeHeight
    return mathMax(1, mathMin(sizeWidth, sizeHeight))
endfunction


# Encode the Life object
function lifeEncode(life)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')
    lifeChars = arrayNew()

    alive = 0
    count = 0
    maxCount = stringLength(lifeEncodeChars) - 1
    iCell = 0
    cellLoop:
        curAlive = arrayGet(cells, iCell)
        jumpif (curAlive != alive) cellLoopAlive

        count = count + 1
        jumpif (count < maxCount) cellLoopNext

        arrayPush(lifeChars, stringSlice(lifeEncodeChars, count, count + 1))
        alive = if(alive, 0, 1)
        count = 0
        jump cellLoopNext

        cellLoopAlive:
        arrayPush(lifeChars, stringSlice(lifeEncodeChars, count, count + 1))
        alive = if(alive, 0, 1)
        count = 1

        cellLoopNext:
        iCell = iCell + 1
    jumpif (iCell < arrayLength(cells)) cellLoop

    if(count, arrayPush(lifeChars, stringSlice(lifeEncodeChars, count, count + 1)))

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
    charLoop:
    jumpif (iChar >= stringLength(cellsStr)) charLoopDone
        char = stringSlice(cellsStr, iChar, iChar + 1)
        count = stringIndexOf(lifeEncodeChars, char)
        iCount = 0
        countLoop:
        jumpif (iCount >= count) countLoopDone
            arraySet(cells, iCell, iChar % 2)
            iCount = iCount + 1
            iCell = iCell + 1
        jump countLoop
        countLoopDone:
        iChar = iChar + 1
    jump charLoop
    charLoopDone:

    return life
endfunction


# Life encoding characters
lifeEncodeAlpha = 'abcdefghijklmnopqrstuvwxyz'
lifeEncodeChars = '0123456789' + lifeEncodeAlpha + stringUpper(lifeEncodeAlpha)


# Execute the main entry point
lifeMain()
~~~
