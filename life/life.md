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

# Life change frequencies, in Hz
lifeFrequencies = arrayNew(1, 2, 4, 6, 8, 10, 20, 30)

# Limits
minimumGap = 1
minimumWidthHeight = 10

# Life cell and background colors
lifeColors = arrayNew('forestgreen', 'white' , 'lightgray', 'greenyellow', 'gold', 'magenta', 'cornflowerblue')
lifeBorderColor = '#606060'


function main()
    # Application arguments
    argsRaw = lifeArgs(true)
    args = lifeArgs()
    background = objectGet(args, 'background')
    border = objectGet(args, 'border')
    borderRaw = objectGet(argsRaw, 'border')
    color = objectGet(args, 'color')
    freq = objectGet(args, 'freq')
    gap = objectGet(args, 'gap')
    load = objectGet(args, 'load')
    play = objectGet(args, 'play')
    save = objectGet(args, 'save')

    # Title
    title = "Conway's Game of Life"
    setDocumentTitle(title)

    # Load the life state
    life = lifeLoad()

    # Load?
    jumpif (load == null) loadDone
        loadedLife = lifeDecode(load)

        # Save the loaded life (unless its already loaded)
        jumpif (load == objectGet(life, 'initial')) loadDone
            life = loadedLife
            lifeSave(loadedLife)
    loadDone:

    # Save menu
    jumpif (!save) menuSaveEnd
        menuElements = arrayNew( \
            objectNew('text', 'Save: '), \
            lifeLinkElements('Load', lifeURL(argsRaw, 0, null, null, null, null, null, lifeEncode(life))) \
        )
    menuSaveEnd:

    # Pause menu
    nbsp = stringFromCharCode(160)
    linkSeparator = objectNew('text', ' ')
    linkSection = objectNew('text', nbsp + '| ')
    jumpif (save || play) menuPauseEnd
        nextColor = (color + 1) % arrayLength(lifeColors)
        nextColor = if(nextColor != background, nextColor, (nextColor + 1) % arrayLength(lifeColors))
        nextBackground = (background + 1) % arrayLength(lifeColors)
        nextBackground = if(nextBackground != color, nextBackground, (nextBackground + 1) % arrayLength(lifeColors))
        menuElements = arrayNew( \
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
    menuPauseEnd:

    # Play menu
    jumpif (save || !play) menuPlayEnd
        menuElements = arrayNew( \
            lifeLinkElements('Pause', lifeURL(argsRaw, 0)), \
            linkSection, \
            lifeLinkElements('<<', lifeURL(argsRaw, 1, mathMax(0, freq - 1))), \
            arrayNew(objectNew('text', nbsp + arrayGet(lifeFrequencies, freq) + nbsp + 'Hz' + nbsp)), \
            lifeLinkElements('>>', lifeURL(argsRaw, 1, mathMin(arrayLength(lifeFrequencies) - 1, freq + 1))) \
        )
    menuPlayEnd:

    # Render the menu
    elementModelRender(objectNew('html', 'p', 'elem', arrayNew( \
        objectNew('html', 'b', 'elem', objectNew('text', title)), \
        objectNew('html', 'br'), \
        menuElements \
    )))

    # Life board
    size = lifeSize(args, life)
    lifeDraw(life, size, gap, arrayGet(lifeColors, color), arrayGet(lifeColors, background), lifeBorderColor, border, !play)

    # Play?
    period = 1000 / arrayGet(lifeFrequencies, freq)
    if(!save && play, setWindowTimeout(lifeOnTimeout, period))

    # Set the window resize handler
    setWindowResize(main)
endfunction


function lifeSize(args, life)
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


function lifeLink(text, url)
    return '[' + text + '](' + url + ')'
endfunction


function lifeLinkElements(text, url)
    return objectNew( \
        'html', 'a', \
        'attr', objectNew('href', documentURL(url)), \
        'elem', objectNew('text', text) \
    )
endfunction


function lifeButtonElements(text, onclick)
    return objectNew( \
        'html', 'a', \
        'attr', objectNew('style', 'cursor: pointer; user-select: none;'), \
        'elem', objectNew('text', text), \
        'callback', objectNew('click', onclick) \
    )
endfunction


function lifeDraw(life, size, gap, color, background, lifeBorderColor, borderSize, isEdit)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')

    # Set the drawing size
    setDrawingSize(width * (gap + size) + gap + 2 * borderSize, height * (gap + size) + gap + 2 * borderSize)
    if(isEdit, drawOnClick(lifeOnClickCell))

    # Draw the background
    jumpif (border == 0) noBorder
        drawStyle(lifeBorderColor, borderSize, background)
        drawRect(0.5 * borderSize, 0.5 * borderSize, getDrawingWidth() - borderSize, getDrawingHeight() - borderSize)
    noBorder:

    # Draw the cells
    drawStyle('none', 0, color)
    y = 0
    yLoop:
        x = 0
        xLoop:
            jumpif (!arrayGet(cells, y * width + x)) skipCell
                px = borderSize + gap + x * (size + gap)
                py = borderSize + gap + y * (size + gap)
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


function lifeOnClickStep()
    lifeSave(lifeNext(lifeLoad()))
    lifeUpdate()
endfunction


function lifeOnClickRandom()
    life = lifeLoad()
    lifeSave(lifeNew(objectGet(life, 'width'), objectGet(life, 'height')))
    lifeUpdate()
endfunction


function lifeOnClickReset()
    lifeSave(lifeNew())
    emptyArgs = lifeArgsEmpty(lifeArgs(true))
    if(emptyArgs, main())
    if(!emptyArgs, setWindowLocation('#var='))
endfunction


function lifeOnClickWidthLess()
    lifeUpdateWidthHeight(-defaultWidthHeightDelta, 0)
endfunction


function lifeOnClickWidthMore()
    lifeUpdateWidthHeight(defaultWidthHeightDelta, 0)
endfunction


function lifeOnClickHeightLess()
    lifeUpdateWidthHeight(0, -defaultWidthHeightDelta)
endfunction


function lifeOnClickHeightMore()
    lifeUpdateWidthHeight(0, defaultWidthHeightDelta)
endfunction


function lifeUpdateWidthHeight(widthDelta, heightDelta)
    life = lifeLoad()
    width = mathMax(minimumWidthHeight, mathCeil(widthDelta + objectGet(life, 'width')))
    height = mathMax(minimumWidthHeight, mathCeil(heightDelta + objectGet(life, 'height')))
    lifeSave(lifeNew(width, height))
    lifeUpdate()
endfunction


function lifeOnClickCell(px, py)
    args = lifeArgs()
    life = lifeLoad()
    size = lifeSize(args, life)
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


function lifeUpdate()
    # Is there a load argument? If so, delete it and update the window location
    argsRaw = lifeArgs(true)
    jumpif (objectGet(argsRaw, 'load') == null) loadDone
        objectDelete(argsRaw, 'load')
        setWindowLocation(lifeURL(argsRaw))
        return
    loadDone:

    main()
endfunction


# Life session state object schema
lifeTypes = schemaParse( \
    'struct Life', \
    '    int(>= ' + minimumWidthHeight + ') width', \
    '    int(>= ' + minimumWidthHeight + ') height', \
    '    int(>= 0, <= 1)[len > 0] cells', \
    '    string initial' \
)


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


function lifeSave(life)
    sessionStorageSet('life', jsonStringify(life))
endfunction


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


lifeEncodeAlpha = 'abcdefghijklmnopqrstuvwxyz'
lifeEncodeChars = '0123456789' + lifeEncodeAlpha + stringUpper(lifeEncodeAlpha)


# Execute the main entry point
main()
~~~
