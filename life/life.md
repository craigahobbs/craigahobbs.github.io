~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


# Defaults
defaultBackground = 1
defaultBorderRatio = 0.1
defaultBorderSize = 5
defaultColor = 0
defaultDepth = 6
defaultFreq = 1
defaultGap = 1
defaultHeight = 50
defaultInitRatio = 0.2
defaultWidth = 50
defaultWidthHeightDelta = 5

# Limits
minimumGap = 1
minimumWidthHeight = 10

# Life change frequencies, in Hz
lifeFrequencies = arrayNew(1, 2, 4, 6, 8, 10, 20, 30)

# Life cell and background colors
lifeColors = arrayNew('forestgreen', 'white' , 'lightgray', 'greenyellow', 'gold', 'magenta', 'cornflowerblue')
lifeBorderColor = '#606060'

# The life board document reset ID
lifeDocumentResetID = 'lifeReset'


# Life application main entry point
function main()
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
        objectNew('html', 'p', 'elem', arrayNew( \
            objectNew('html', 'b', 'elem', objectNew('text', title)), \
            objectNew('html', 'br'), \
            lifeMenuElements(args, life) \
        )), \
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
function lifeUpdate()
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
    period = 1000 / arrayGet(lifeFrequencies, objectGet(args, 'freq'))
    if(objectGet(args, 'play'), setWindowTimeout(lifeOnTimeout, period))
endfunction


# Create the Life application variable-arguments object
function lifeArgs(raw)
    return objectNew( \
        'background', if(vBackground != null, vBackground % arrayLength(lifeColors), if(!raw, defaultBackground)), \
        'border', if(vBorder != null, mathMax(minBorder, vBorder), if(!raw, 0)), \
        'borderRatio', if(vBorderRatio != null, mathMax(0, mathMin(1, vBorderRatio)), if(!raw, defaultBorderRatio)), \
        'color', if(vColor != null, vColor % arrayLength(lifeColors), if(!raw, defaultColor)), \
        'depth', if(vDepth != null, vDepth, if(!raw, defaultDepth)), \
        'freq', if(vFreq != null, mathMax(0, mathMin(arrayLength(lifeFrequencies) - 1, vFreq)), if(!raw, defaultFreq)), \
        'gap', if(vGap != null, mathMax(minimumGap, vGap), if(!raw, defaultGap)), \
        'initRatio', if(vInitRatio != null, mathMax(0, mathMin(1, vInitRatio)), if(!raw, defaultInitRatio)), \
        'load', vLoad, \
        'play', if(vPlay != null, if(vPlay, 1, 0), if(!raw, 0)), \
        'save', if(vSave != null, if(vSave, 1, 0), if(!raw, 0)) \
    )
endfunction


# Helper to determine if all variable arguments are empty
function lifeArgsEmpty(args)
    keys = objectKeys(args)
    ixKey = 0
    keyLoop:
        value = objectGet(args, arrayGet(keys, ixKey))
        jumpif (value == null) valueNull
            return false
        valueNull:
        ixKey = ixKey + 1
    jumpif (ixKey < arrayLength(keys)) keyLoop
    return true
endfunction


# Create the Life application menu element model
function lifeMenuElements(args, life)
    # Menu separators
    nbsp = stringFromCharCode(160)
    linkSeparator = objectNew('text', ' ')
    linkSection = objectNew('text', nbsp + '| ')

    # Which menu? (save, play, or pause)
    argsRaw = lifeArgs(true)
    jumpif (objectGet(args, 'save')) menuSave
    jumpif (objectGet(args, 'play')) menuPlay
        # Pause menu
        background = objectGet(args, 'background')
        borderRaw = objectGet(argsRaw, 'border')
        color = objectGet(args, 'color')
        nextColor = (color + 1) % arrayLength(lifeColors)
        nextColor = if(nextColor != background, nextColor, (nextColor + 1) % arrayLength(lifeColors))
        nextBackground = (background + 1) % arrayLength(lifeColors)
        nextBackground = if(nextBackground != color, nextBackground, (nextBackground + 1) % arrayLength(lifeColors))
        return arrayNew( \
            lifeLinkElements('Play', lifeURL(argsRaw, 1)), \
            linkSection, \
            lifeButtonElements('Step', lifeOnClickStep), \
            linkSeparator, \
            lifeButtonElements('Random', lifeOnClickRandom), \
            linkSeparator, \
            lifeLinkElements('Save', lifeURL(argsRaw, 0, null, null, null, null, 1)), \
            linkSection, \
            lifeLinkElements('Background', lifeURL(argsRaw, 0, null, null, nextBackground)), \
            linkSeparator, \
            lifeLinkElements('Cell', lifeURL(argsRaw, 0, null, nextColor)), \
            linkSeparator, \
            lifeLinkElements('Border', lifeURL(argsRaw, 0, null, null, null, if(borderRaw != null, 0, defaultBorderSize))), \
            linkSeparator, \
            lifeButtonElements('Reset', lifeOnClickReset), \
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
            lifeLinkElements('Pause', lifeURL(argsRaw, 0)), \
            linkSection, \
            lifeLinkElements('<<', lifeURL(argsRaw, 1, mathMax(0, freq - 1))), \
            arrayNew(objectNew('text', nbsp + arrayGet(lifeFrequencies, freq) + nbsp + 'Hz' + nbsp)), \
            lifeLinkElements('>>', lifeURL(argsRaw, 1, mathMin(arrayLength(lifeFrequencies) - 1, freq + 1))) \
        )
        jump menuDone
    menuSave:
        return arrayNew( \
            objectNew('text', 'Save: '), \
            lifeLinkElements('Load', lifeURL(argsRaw, 0, null, null, null, null, null, lifeEncode(life))) \
        )
    menuDone:
endfunction


# Create a life application URL
function lifeURL(argsRaw, play, freq, color, background, border, save, load)
    # URL args
    play = if(play != null, play, objectGet(argsRaw, 'play'))
    freq = if(freq != null, freq, objectGet(argsRaw, 'freq'))
    color = if(color != null, color, objectGet(argsRaw, 'color'))
    background = if(background != null, background, objectGet(argsRaw, 'background'))
    border = if(border != null, if(border, border, null), objectGet(argsRaw, 'border'))
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
        if(gap != null, '&var.vGap=' + gap, '') + \
        if(initRatio != null, '&var.vInitRatio=' + initRatio, '') + \
        if(load != null, "&var.vLoad='" + load + "'", '') + \
        if(freq != null, '&var.vFreq=' + freq, '') + \
        if(play, '&var.vPlay=1', '') + \
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
    args = lifeArgs()
    depth = objectGet(args, 'depth')

    # Compute the next life state
    life = lifeLoad()
    nextLife = lifeNext(life)

    # Is there a cycle?
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

    # Update the life state and re-render
    lifeSave(nextLife)
    lifeUpdate()
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
    emptyArgs = lifeArgsEmpty(lifeArgs(true))
    if(emptyArgs, main())
    if(!emptyArgs, setWindowLocation('#var='))
endfunction


# Life application width-less click handler
function lifeOnClickWidthLess()
    lifeUpdateWidthHeight(-defaultWidthHeightDelta, 0)
endfunction


# Life application width-more click handler
function lifeOnClickWidthMore()
    lifeUpdateWidthHeight(defaultWidthHeightDelta, 0)
endfunction


# Life application height-less click handler
function lifeOnClickHeightLess()
    lifeUpdateWidthHeight(0, -defaultWidthHeightDelta)
endfunction


# Life application height-more click handler
function lifeOnClickHeightMore()
    lifeUpdateWidthHeight(0, defaultWidthHeightDelta)
endfunction


# Helper for width/height less/more click handlers
function lifeUpdateWidthHeight(widthDelta, heightDelta)
    life = lifeLoad()
    width = mathMax(minimumWidthHeight, mathCeil(widthDelta + objectGet(life, 'width')))
    height = mathMax(minimumWidthHeight, mathCeil(heightDelta + objectGet(life, 'height')))
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
lifeTypes = schemaParse( \
    '# The Life session state', \
    'struct Life', \
    '', \
    '    # The Life board width', \
    '    int(>= ' + minimumWidthHeight + ') width', \
    '', \
    '    # The Life board height', \
    '    int(>= ' + minimumWidthHeight + ') height', \
    '', \
    '    # The Life board cell state array', \
    '    int(>= 0, <= 1)[len > 0] cells', \
    '', \
    "    # The Life board's encoded initial cell state", \
    '    string initial' \
)


# Create a new Life object
function lifeNew(width, height, initial, noInit)
    width = if(width != null, width, defaultWidth)
    height = if(height != null, height, defaultHeight)
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
    life = if(life != null, schemaValidate(lifeTypes, 'Life', life))
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
    drawStyle(lifeBorderColor, border, arrayGet(lifeColors, objectGet(args, 'background')))
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
    totalHeight = getWindowHeight() - 6 * getDocumentFontSize()
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
main()
~~~
