~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


# Defaults
defaultBackground = 1
defaultBorderRatio = 0.1
defaultBorderSize = 5
defaultColor = 0
defaultDepth = 6
defaultGap = 1
defaultHeight = 50
defaultInitRatio = 0.2
defaultPeriod = 1000
defaultWidth = 50

# Limits
minimumGap = 1
minimumPeriod = 100
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
    gap = objectGet(args, 'gap')
    load = objectGet(args, 'load')
    period = objectGet(args, 'period')
    play = objectGet(args, 'play')
    save = objectGet(args, 'save')

    # Title
    title = "Conway's Game of Life"
    setDocumentTitle(title)
    markdownPrint('**' + title + '**  ')

    # Load?
    jumpif (load == null) noLoad
        lifeSave(lifeDecode(load))
        setWindowLocation(lifeURL(argsRaw))
        return
    noLoad:

    # Load the life state
    life = lifeLoad()

    # Save menu
    jumpif (!save) menuSaveEnd
        markdownPrint( \
            '**Save:** ', \
            lifeLink('Load', lifeURL(argsRaw, 0, null, null, null, null, null, lifeEncode(life))) \
        )
    menuSaveEnd:

    # Pause menu
    jumpif (save || play) menuPauseEnd
        nextColor = (color + 1) % arrayLength(lifeColors)
        nextColor = if(nextColor != background, nextColor, (nextColor + 1) % arrayLength(lifeColors))
        nextBackground = (background + 1) % arrayLength(lifeColors)
        nextBackground = if(nextBackground != color, nextBackground, (nextBackground + 1) % arrayLength(lifeColors))
        linkSeparator = objectNew('text', ' ')
        linkSection = objectNew('text', ' | ')
        elementModelRender(arrayNew( \
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
            arrayNew(linkSection, objectNew('html', 'b', 'elem', objectNew('text', 'Width: '))), \
            lifeButtonElements('More', lifeOnClickWidthMore), \
            linkSeparator, \
            lifeButtonElements('Less', lifeOnClickWidthLess), \
            arrayNew(linkSection, objectNew('html', 'b', 'elem', objectNew('text', 'Height: '))), \
            lifeButtonElements('More', lifeOnClickHeightMore), \
            linkSeparator, \
            lifeButtonElements('Less', lifeOnClickHeightLess) \
        ))
    menuPauseEnd:

    # Play menu
    jumpif (save || !play) menuPlayEnd
        markdownPrint( \
            lifeLink('Pause', lifeURL(argsRaw, 0)), \
            ' | **Speed:** ' + lifeLink('More', lifeURL(argsRaw, 1, mathMax(minimumPeriod, numberToFixed(0.75 * period, 2)))) + \
                ' ' + lifeLink('Less', lifeURL(argsRaw, 1, numberToFixed(1.25 * period, 2))) \
        )
    menuPlayEnd:

    # Life board
    size = lifeSize(args, life)
    lifeDraw(life, size, gap, arrayGet(lifeColors, color), arrayGet(lifeColors, background), lifeBorderColor, border, !play)

    # Play?
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
        'gap', if(vGap != null, mathMax(minimumGap, vGap), if(!raw, defaultGap)), \
        'initRatio', if(vInitRatio != null, mathMax(0, mathMin(1, vInitRatio)), if(!raw, defaultInitRatio)), \
        'load', vLoad, \
        'period', if(vPeriod != null, mathMax(minimumPeriod, vPeriod), if(!raw, defaultPeriod)), \
        'play', if(vPlay != null, if(vPlay, 1, 0), if(!raw, 0)), \
        'save', if(vSave != null, if(vSave, 1, 0), if(!raw, 0)) \
    )
endfunction


function lifeURL(argsRaw, play, period, color, background, border, save, load)
    # URL args
    play = if(play != null, play, objectGet(argsRaw, 'play'))
    period = if(period != null, period, objectGet(argsRaw, 'period'))
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
        if(period != null, '&var.vPeriod=' + period, '') + \
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
    lifeJSON = jsonStringify(life)
    lifeCycle = nextLife
    iCycle = 0
    cycleLoop:
        jumpif (lifeJSON != jsonStringify(lifeCycle)) cycleNone
            nextLife = lifeNew(objectGet(life, 'width'), objectGet(life, 'height'))
            jump cycleDone
        cycleNone:
        lifeCycle = lifeNext(lifeCycle)
        iCycle = iCycle + 1
    jumpif (iCycle < depth) cycleLoop
    cycleDone:

    # Update the life state and re-render
    lifeSave(nextLife)
    main()
endfunction


function lifeOnClickStep()
    lifeSave(lifeNext(lifeLoad()))
    main()
endfunction


function lifeOnClickRandom()
    life = lifeLoad()
    lifeSave(lifeNew(objectGet(life, 'width'), objectGet(life, 'height')))
    main()
endfunction


function lifeOnClickReset()
    lifeSave(lifeNew())
    main()
    setWindowLocation('#var=')
endfunction


function lifeOnClickWidthLess()
    lifeUpdateWidthHeight(0.9, 1)
endfunction


function lifeOnClickWidthMore()
    lifeUpdateWidthHeight(1.1, 1)
endfunction


function lifeOnClickHeightLess()
    lifeUpdateWidthHeight(1, 0.9)
endfunction


function lifeOnClickHeightMore()
    lifeUpdateWidthHeight(1, 1.1)
endfunction


function lifeUpdateWidthHeight(widthRatio, heightRatio)
    life = lifeLoad()
    width = mathMax(minimumWidthHeight, mathCeil(widthRatio * objectGet(life, 'width')))
    height = mathMax(minimumWidthHeight, mathCeil(heightRatio * objectGet(life, 'height')))
    lifeSave(lifeNew(width, height))
    main()
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
    main()
endfunction


# Life session state object schema
lifeTypes = schemaParse( \
    'struct Life', \
    '    int(>= ' + minimumWidthHeight + ') width', \
    '    int(>= ' + minimumWidthHeight + ') height', \
    '    int(>= 0, <= 1)[len > 0] cells' \
)


function lifeNew(width, height, noInit)
    width = if(width != null, width, defaultWidth)
    height = if(height != null, height, defaultHeight)

    # Create the blank life object
    life = objectNew()
    objectSet(life, 'width', width)
    objectSet(life, 'height', height)
    cells = arrayNewSize(width * height)
    objectSet(life, 'cells', cells)

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
    lifeNext = lifeNew(width, height, true)
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
    life = lifeNew(width, height, true)
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
