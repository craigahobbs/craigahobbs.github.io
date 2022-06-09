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
defaultSize = 10
defaultWidth = 50

# Limits
minimumGap = 1
minimumPeriod = 100
minimumSize = 1
minimumWidthHeight = 10

# Life cell and background colors
lifeColors = arrayNew('forestgreen', 'white' , 'lightgray', 'greenyellow', 'gold', 'magenta', 'cornflowerblue')
lifeBorderColor = 'black'


function main()
    # Title
    title = "Conway's Game of Life"
    setDocumentTitle(title)
    markdownPrint("# " + title, '')

    # Load life
    life = lifeLoad()

    # Application arguments
    argsRaw = lifeArgs(true)
    args = lifeArgs()
    background = objectGet(args, 'background')
    border = objectGet(args, 'border')
    borderRaw = objectGet(argsRaw, 'border')
    color = objectGet(args, 'color')
    gap = objectGet(args, 'gap')
    period = objectGet(args, 'period')
    play = objectGet(args, 'play')
    size = objectGet(args, 'size')

    # Pause menu
    jumpif (play) menuPlay
        nextColor = (color + 1) % arrayLength(lifeColors)
        nextColor = if(nextColor != background, nextColor, (nextColor + 1) % arrayLength(lifeColors))
        nextBackground = (background + 1) % arrayLength(lifeColors)
        nextBackground = if(nextBackground != color, nextBackground, (nextBackground + 1) % arrayLength(lifeColors))
        linkSeparator = objectNew('text', ' ')
        linkSection = objectNew('text', ' | ')
        elementModelRender(objectNew('html', 'p', 'elem', arrayNew( \
            lifeLinkElements('Play', lifeURL(argsRaw, 1)), \
            linkSection, \
            lifeButtonElements('Step', lifeOnClickStep), \
            linkSeparator, \
            lifeButtonElements('Random', lifeOnClickRandom), \
            linkSection, \
            lifeLinkElements('Background', lifeURL(argsRaw, 0, null, null, null, nextBackground)), \
            linkSeparator, \
            lifeLinkElements('Cell', lifeURL(argsRaw, 0, null, null, nextColor)), \
            linkSeparator, \
            lifeLinkElements('Border', lifeURL(argsRaw, 0, null, null, null, null, if(borderRaw != null, 0, defaultBorderSize))), \
            linkSeparator, \
            lifeButtonElements('Reset', lifeOnClickReset), \
            arrayNew(linkSection, objectNew('html', 'b', 'elem', objectNew('text', 'Width: '))), \
            lifeButtonElements('More', lifeOnClickWidthMore), \
            linkSeparator, \
            lifeButtonElements('Less', lifeOnClickWidthLess), \
            arrayNew(linkSection, objectNew('html', 'b', 'elem', objectNew('text', 'Height: '))), \
            lifeButtonElements('More', lifeOnClickHeightMore), \
            linkSeparator, \
            lifeButtonElements('Less', lifeOnClickHeightLess), \
            arrayNew(linkSection, objectNew('html', 'b', 'elem', objectNew('text', 'Size: '))), \
            lifeLinkElements('More', lifeURL(argsRaw, 0, null, max(minimumSize, size + 1))), \
            linkSeparator, \
            lifeLinkElements('Less', lifeURL(argsRaw, 0, null, max(minimumSize, size - 1))) \
        )))
        jump menuDone

    # Play menu
    menuPlay:
        markdownPrint( \
            lifeLink('Pause', lifeURL(argsRaw, 0)), \
            ' | **Speed:** ' + lifeLink('More', lifeURL(argsRaw, 1, max(minimumPeriod, fixed(0.75 * period, 2)))) + \
                ' ' + lifeLink('Less', lifeURL(argsRaw, 1, fixed(1.25 * period, 2))) \
        )
    menuDone:

    # Life board
    lifeDraw(life, size, gap, arrayGet(lifeColors, color), arrayGet(lifeColors, background), lifeBorderColor, border, !play)

    # Play?
    if(play, setWindowTimeout(lifeOnTimeout, period))
endfunction


function lifeArgs(raw)
    return objectNew( \
        'background', if(vBackground != null, vBackground % len(lifeColors), if(!raw, defaultBackground)), \
        'border', if(vBorder != null, max(minBorder, vBorder), if(!raw, 0)), \
        'borderRatio', if(vBorderRatio != null, max(0, min(1, vBorderRatio)), if(!raw, defaultBorderRatio)), \
        'color', if(vColor != null, vColor % len(lifeColors), if(!raw, defaultColor)), \
        'depth', if(vDepth != null, vDepth, if(!raw, defaultDepth)), \
        'gap', if(vGap != null, max(minimumGap, vGap), if(!raw, defaultGap)), \
        'initRatio', if(vInitRatio != null, max(0, min(1, vInitRatio)), if(!raw, defaultInitRatio)), \
        'period', if(vPeriod != null, max(minimumPeriod, vPeriod), if(!raw, defaultPeriod)), \
        'play', if(vPlay != null, if(vPlay, 1, 0), if(!raw, 0)), \
        'size', if(vSize != null, max(minimumSize, vSize), if(!raw, defaultSize)) \
    )
endfunction


function lifeURL(argsRaw, play, period, size, color, background, border)
    # URL args
    period = if(period != null, period, objectGet(argsRaw, 'period'))
    size = if(size != null, size, objectGet(argsRaw, 'size'))
    color = if(color != null, color, objectGet(argsRaw, 'color'))
    background = if(background != null, background, objectGet(argsRaw, 'background'))
    border = if(border != null, if(border, border, null), objectGet(argsRaw, 'border'))
    gap = objectGet(argsRaw, 'gap')
    depth = objectGet(argsRaw, 'depth')
    initRatio = objectGet(argsRaw, 'initRatio')
    borderRatio = objectGet(argsRaw, 'borderRatio')

    # Return the URL
    urlArgs = if(play, '&var.vPlay=1', '') + \
        if(period != null, '&var.vPeriod=' + period, '') + \
        if(size != null, '&var.vSize=' + size, '') + \
        if(color != null, '&var.vColor=' + color, '') + \
        if(background != null, '&var.vBackground=' + background, '') + \
        if(border != null, '&var.vBorder=' + border, '') + \
        if(gap != null, '&var.vGap=' + gap, '') + \
        if(depth != null, '&var.vDepth=' + depth, '') + \
        if(initRatio != null, '&var.vInitRatio=' + initRatio, '') + \
        if(borderRatio != null, '&var.vBorderRatio=' + borderRatio, '')
    return if(len(urlArgs) > 0, '#' + slice(urlArgs, 1), '#var=')
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
    documentReset()
    main()
endfunction


function lifeOnClickStep()
    lifeSave(lifeNext(lifeLoad()))
    documentReset()
    main()
endfunction


function lifeOnClickRandom()
    life = lifeLoad()
    lifeSave(lifeNew(objectGet(life, 'width'), objectGet(life, 'height')))
    documentReset()
    main()
endfunction


function lifeOnClickReset()
    lifeSave(lifeNew())
    documentReset()
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
    width = max(minimumWidthHeight, ceil(widthRatio * objectGet(life, 'width')))
    height = max(minimumWidthHeight, ceil(heightRatio * objectGet(life, 'height')))
    lifeSave(lifeNew(width, height))
    documentReset()
    main()
endfunction


function lifeOnClickCell(px, py)
    args = lifeArgs()
    size = objectGet(args, 'size')
    gap = objectGet(args, 'gap')
    border = objectGet(args, 'border')

    # Compute the cell index to toggle
    life = lifeLoad()
    x = max(0, min(objectGet(life, 'width') - 1, floor((px - border) / (size + gap))))
    y = max(0, min(objectGet(life, 'height') - 1, floor((py - border) / (size + gap))))
    iCell = y * objectGet(life, 'width') + x

    # Toggle the cell
    cells = objectGet(life, 'cells')
    arraySet(cells, iCell, if(arrayGet(cells, iCell), 0, 1))

    # Update the life state and re-render
    lifeSave(life)
    documentReset()
    main()
endfunction


# Life session state object schema
lifeTypes = schemaParse( \
    'struct Life', \
    '    int(>= ' + minimumWidthHeight + ') width', \
    '    int(>= ' + minimumWidthHeight + ') height', \
    '    int(>= 0, <= 1)[len > 0] cells' \
)


function lifeNew(width, height)
    width = if(width != null, width, defaultWidth)
    height = if(height != null, height, defaultHeight)
    args = lifeArgs()
    initRatio = objectGet(args, 'initRatio')
    borderRatio = objectGet(args, 'borderRatio')

    # Create the blank life object
    life = objectNew()
    objectSet(life, 'width', width)
    objectSet(life, 'height', height)
    cells = arrayNewSize(width * height)
    objectSet(life, 'cells', cells)

    # Initialize the life
    jumpif (initRatio == 0) skipInit
        border = ceil(borderRatio * min(width, height))
        y = 0
        yLoop:
            x = 0
            xLoop:
                arraySet(cells, y * width + x, \
                    if(x >= border && x < width - border && y >= border && y < height - border && rand() < initRatio, 1, 0))
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
    lifeNext = lifeNew(width, height, 0)
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
    maxCount = len(lifeEncodeChars) - 1
    iCell = 0
    cellLoop:
        curAlive = arrayGet(cells, iCell)
        jumpif (curAlive != alive) cellLoopAlive

        count = count + 1
        jumpif (count < maxCount) cellLoopNext

        arrayPush(lifeChars, slice(lifeEncodeChars, count, count + 1))
        alive = if(alive, 0, 1)
        count = 0
        jump cellLoopNext

        cellLoopAlive:
        arrayPush(lifeChars, slice(lifeEncodeChars, count, count + 1))
        alive = if(alive, 0, 1)
        count = 1

        cellLoopNext:
        iCell = iCell + 1
    jumpif (iCell < arrayLength(cells)) cellLoop

    if(count, arrayPush(lifeChars, slice(lifeEncodeChars, count, count + 1)))

    return width + '-' + height + '-' + arrayJoin(lifeChars, '')
endfunction


function lifeDecode(lifeStr)
    # Split the encoded life string into width, height, and cell string
    parts = split(lifeStr, '-')
    width = value(arrayGet(parts, 0))
    height = value(arrayGet(parts, 1))
    cellsStr = arrayGet(parts, 2)

    # Decode the cell string
    life = lifeNew(width, height, 0)
    cells = objectGet(life, 'cells')
    iCell = 0
    iChar = 0
    charLoop:
    jumpif (iChar >= len(cellsStr)) charLoopDone
        char = slice(cellsStr, iChar, iChar + 1)
        count = indexOf(lifeEncodeChars, char)
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
lifeEncodeChars = '0123456789' + lifeEncodeAlpha + upper(lifeEncodeAlpha)


# Execute the main entry point
main()
~~~
