# Conway's Game of Life

~~~ markdown-script
// Licensed under the MIT License
// https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

function main()
    // Defaults
    defaultWidth = 50
    defaultHeight = 50
    defaultPeriod = 1000
    defaultSize = 10
    defaultColorIndex = 0
    defaultBackgroundIndex = 1
    defaultBorder = 0
    defaultDepth = 6

    // Limits
    minWidth = 20
    minHeight = 20
    minPeriod = 200
    minSize = 1
    minDepth = 0

    // Cell and background colors
    colors = arraySplit('forestgreen,white,lightgray,greenyellow,gold,magenta,cornflowerblue', ',')
    borderColor = 'black'

    // Application variables
    play = if(vPlay != null, vPlay, 0)
    period = max(minPeriod, if(vPeriod != null, vPeriod, defaultPeriod))
    size = max(minSize, if(vSize != null, vSize, defaultSize))
    gap = if(vGap != null, vGap, 1)
    depth = max(minDepth, if(vDepth != null, vDepth, defaultDepth))
    colorIndex = if(vColor != null, vColor, defaultColorIndex) % len(colors)
    backgroundIndex = if(vBackground != null, vBackground, defaultBackgroundIndex) % len(colors)
    border = if(vBorder != null, vBorder, defaultBorder)
    initRatio = if(vInitRatio != null, vInitRatio, 0.2)
    borderRatio = if(vBorderRatio != null, vBorderRatio, 0.1)

    // Initialize or decode the life board
    jumpif (vLife) lifeInitDecode
        life = lifeNew(defaultWidth, defaultHeight, initRatio, borderRatio)
    jump lifeInitDone
    lifeInitDecode:
        life = lifeDecode(vLife)
    lifeInitDone:
    lifeWidth = objectGet(life, 'width')
    lifeHeight = objectGet(life, 'height')

    // Is there a cycle?
    nextLife = lifeNext(life)
    encodedLife = lifeEncode(life)
    encodedNext = lifeEncode(nextLife)
    jumpif (!play) cycleDone
        lifeCycle = nextLife
        encodedCycle = encodedNext
        iCycle = 1
        cycleLoop:
            jumpif (iCycle > depth) cycleDone
            jumpif (encodedLife == encodedCycle) cycleDetected
            lifeCycle = lifeNext(lifeCycle)
            encodedCycle = lifeEncode(lifeCycle)
            iCycle = iCycle + 1
        jump cycleLoop
    jump cycleDone
    cycleDetected:
        life = lifeNew(lifeWidth, lifeHeight, initRatio, borderRatio)
        nextLife = lifeNext(life)
        encodedLife = lifeEncode(life)
        encodedNext = lifeEncode(nextLife)
    cycleDone:

    // Pause menu
    jumpif (play) skipPauseMenu
        nextColorIndex = (colorIndex + 1) % arrayLength(colors)
        nextColorIndex = if(nextColorIndex != backgroundIndex, nextColorIndex, (nextColorIndex + 1) % arrayLength(colors))
        nextBackgroundIndex = (backgroundIndex + 1) % arrayLength(colors)
        nextBackgroundIndex = if(nextBackgroundIndex != colorIndex, nextBackgroundIndex, (nextBackgroundIndex + 1) % arrayLength(colors))
        encodedRandom = lifeEncode(lifeNew(lifeWidth, lifeHeight, initRatio, borderRatio))
        encodedWidthMore = lifeEncode(lifeNew(max(minWidth, ceil(1.1 * lifeWidth)), lifeHeight, initRatio, borderRatio))
        encodedWidthLess = lifeEncode(lifeNew(max(minWidth, ceil(0.9 * lifeWidth)), lifeHeight, initRatio, borderRatio))
        encodedHeightMore = lifeEncode(lifeNew(lifeWidth, max(minHeight, ceil(1.1 * lifeHeight)), initRatio, borderRatio))
        encodedHeightLess = lifeEncode(lifeNew(lifeWidth, max(minHeight, ceil(0.9 * lifeHeight)), initRatio, borderRatio))
        markdownPrint( \
            lifeLink('Play', encodedNext, 1), \
            ' | ' + lifeLink('Step', encodedNext, 0), \
            ' ' + lifeLink('Random', encodedRandom, 0), \
            ' | ' + lifeLink('Background', encodedLife, 0, null, null, null, nextBackgroundIndex), \
            ' ' + lifeLink('Cell', encodedLife, 0, null, null, nextColorIndex), \
            ' ' + lifeLink('Border', encodedLife, 0, null, null, null, null, if(border, 0, 1)), \
            ' [Reset](#var=)', \
            ' | **Width:** ' + lifeLink('More', encodedWidthMore, 0) + ' ' + lifeLink('Less', encodedWidthLess, 0), \
            ' | **Height:** ' + lifeLink('More', encodedHeightMore, 0) + ' ' + lifeLink('Less', encodedHeightLess, 0), \
            ' | **Size:** ' + lifeLink('More', encodedLife, null, null, max(minSize, size + 1)) + \
                ' ' + lifeLink('Less', encodedLife, null, null, max(minSize, size - 1)) \
        )
    skipPauseMenu:

    // Play menu
    jumpif (!play) skipPlayMenu
        markdownPrint( \
            lifeLink('Pause', encodedLife, 0), \
            ' | **Speed:** ' + lifeLink('More', encodedNext, 1, max(minPeriod, fixed(0.75 * period, 2))) + \
                ' ' + lifeLink('Less', encodedNext, 1, fixed(1.25 * period, 2)) \
        )
    skipPlayMenu:

    // Life board
    lifeDraw(life, size, gap, arrayGet(colors, colorIndex), arrayGet(colors, backgroundIndex), borderColor, if(border, 2, 0), !play)

    // Play?
    jumpif (!play) skipPlay
        setNavigateTimeout(lifeURL(encodedNext, 1), period)
    skipPlay:
endfunction


function lifeLink(text, encodedLife, play, period, size, color, bkgnd, border)
    return '[' + text + '](' + lifeURL(encodedLife, play, period, size, color, bkgnd, border) + ')'
endfunction


function lifeURL(encodedLife, play, period, size, color, bkgnd, border)
    period = if(period != null, period, vPeriod)
    size = if(size != null, size, vSize)
    color = if(color != null, color, vColor)
    bkgnd = if(bkgnd != null, bkgnd, vBackground)
    border = if(border != null, border, vBorder)
    args = if(play, '&var.vPlay=1', '') + \
        if(period != null, '&var.vPeriod=' + period, '') + \
        if(size != null, '&var.vSize=' + size, '') + \
        if(color != null, '&var.vColor=' + color, '') + \
        if(bkgnd != null, '&var.vBackground=' + bkgnd, '') + \
        if(border != null, '&var.vBorder=' + border, '') + \
        if(vGap != null, '&var.vGap=' + vGap, '') + \
        if(vDepth != null, '&var.vDepth=' + vDepth, '') + \
        if(vInitRatio != null, '&var.vInitRatio=' + vInitRatio, '') + \
        if(vBorderRatio != null, '&var.vBorderRatio=' + vBorderRatio, '') + \
        if(encodedLife != null, "&var.vLife='" + encodedLife + "'", '')
    return '#' + slice(args, 1)
endfunction


function lifeNew(width, height, initRatio, borderRatio)
    life = objectNew()
    objectSet(life, 'width', width)
    objectSet(life, 'height', height)
    cells = arrayNew(width * height)
    objectSet(life, 'cells', cells)

    // Initialize the life
    jumpif (!initRatio || !borderRatio) skipInit
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


function lifeNext(life)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')

    // Compute the next life generation
    nextLife = lifeNew(width, height, 0, 0)
    nextCells = objectGet(nextLife, 'cells')
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

    return nextLife
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

    jumpif (!count) skipLast
    arrayPush(lifeChars, slice(lifeEncodeChars, count, count + 1))
    skipLast:

    return width + '-' + height + '-' + arrayJoin(lifeChars, '')
endfunction


function lifeDecode(lifeStr)
    // Split the encoded life string into width, height, and cell string
    parts = arraySplit(lifeStr, '-')
    width = value(arrayGet(parts, 0))
    height = value(arrayGet(parts, 1))
    cellsStr = arrayGet(parts, 2)

    // Decode the cell string
    life = lifeNew(width, height, 0, 0)
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


function lifeDraw(life, size, gap, color, background, borderColor, borderSize, isEdit)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    cells = objectGet(life, 'cells')

    // Set the drawing size
    setDrawingSize(width * (gap + size) + gap + borderSize, height * (gap + size) + gap + borderSize)
    jumpif (!isEdit) skipEdit
        setGlobal('lifeOnClickLife', life)
        setGlobal('lifeOnClickBorder', borderSize)
        setGlobal('lifeOnClickGap', gap)
        setGlobal('lifeOnClickSize', size)
        drawOnClick(lifeOnClick)
    skipEdit:

    // Draw the background
    drawStyle(borderColor, borderSize, background)
    drawRect(0.5 * borderSize, 0.5 * borderSize, getDrawingWidth() - borderSize, getDrawingHeight() - borderSize)

    // Draw the cells
    drawStyle('none', 0, color)
    y = 0
    yLoop:
        x = 0
        xLoop:
            jumpif (!arrayGet(cells, y * width + x)) skipCell
                px = 0.5 * borderSize + gap + x * (size + gap)
                py = 0.5 * borderSize + gap + y * (size + gap)
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


function lifeOnClick(px, py)
    // Compute the cell index to toggle
    x = max(0, floor((px - lifeOnClickBorder) / (lifeOnClickSize + lifeOnClickGap)))
    y = max(0, floor((py - lifeOnClickBorder) / (lifeOnClickSize + lifeOnClickGap)))
    iCell = y * objectGet(lifeOnClickLife, 'width') + x

    // Toggle the cell
    cells = objectGet(lifeOnClickLife, 'cells')
    arraySet(cells, iCell, if(arrayGet(cells, iCell), 0, 1))
    setNavigateTimeout(lifeURL(lifeEncode(lifeOnClickLife), 0))
endfunction


// Execute the main entry point
main()
~~~
