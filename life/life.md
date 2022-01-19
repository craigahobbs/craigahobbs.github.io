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
    defaultColorIndex = 1
    defaultBackgroundIndex = 2
    defaultBorder = 0

    // Limits
    minWidth = 20
    minHeight = 20
    minPeriod = 100
    minSize = 1
    maxCycle = 6

    // Cell and background colors
    colors = arraySplit('forestgreen,white,lightgray,greenyellow,gold,magenta,cornflowerblue', ',')
    borderColor = 'black'

    // Application variables
    play = if(vPlay, vPlay, 0)
    period = max(minPeriod, if(vPeriod, vPeriod, defaultPeriod))
    size = max(minSize, if(vSize, vSize, defaultSize))
    gap = if(vGap, vGap, 1)
    colorIndex = max(1, 1 + ((if(vColor, vColor, defaultColorIndex) - 1) % len(colors)))
    backgroundIndex = max(1, 1 + ((if(vBackground, vBackground, defaultBackgroundIndex) - 1) % len(colors)))
    border = if(vBorder, 1, defaultBorder)
    initRatio = if(vInitRatio, vInitRatio, 0.2)
    borderRatio = if(vBorderRatio, vBorderRatio, 0.1)

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
        ixCycle = 1
        cycleLoop:
            jumpif (encodedLife == encodedCycle) cycleDetected
            jumpif (ixCycle >= maxCycle) cycleDone
            lifeCycle = lifeNext(lifeCycle)
            encodedCycle = lifeEncode(lifeCycle)
            ixCycle = ixCycle + 1
        jump cycleLoop
    jump cycleDone
    cycleDetected:
        life = lifeInit(life, initRatio, borderRatio)
        nextLife = lifeNext(life)
        encodedLife = lifeEncode(life)
        encodedNext = lifeEncode(nextLife)
    cycleDone:

    // Pause menu
    jumpif (play) skipPauseMenu
        nextColorIndex = 1 + (colorIndex % arrayLength(colors))
        nextColorIndex = if(nextColorIndex != backgroundIndex, nextColorIndex, 1 + (nextColorIndex % arrayLength(colors)))
        nextBackgroundIndex = 1 + (backgroundIndex % arrayLength(colors))
        nextBackgroundIndex = if(nextBackgroundIndex != colorIndex, nextBackgroundIndex, 1 + (nextBackgroundIndex % arrayLength(colors)))
        encodedRandom = lifeEncode(lifeInit(lifeCopy(life), initRatio, borderRatio))
        encodedWidthMore = lifeEncode(lifeNew(max(minWidth, ceil(1.1 * lifeWidth)), lifeHeight, initRatio, borderRatio))
        encodedWidthLess = lifeEncode(lifeNew(max(minWidth, ceil(0.9 * lifeWidth)), lifeHeight, initRatio, borderRatio))
        encodedHeightMore = lifeEncode(lifeNew(lifeWidth, max(minHeight, ceil(1.1 * lifeHeight)), initRatio, borderRatio))
        encodedHeightLess = lifeEncode(lifeNew(lifeWidth, max(minHeight, ceil(0.9 * lifeHeight)), initRatio, borderRatio))
        markdownPrint( \
            lifeLink('Play', encodedNext, 1), \
            ' | ' + lifeLink('Step', encodedNext, 0), \
            ' ' + lifeLink('Random', encodedRandom, 0), \
            ' | ' + lifeLink('Background', encodedLife, 0, 0, 0, 0, nextBackgroundIndex), \
            ' ' + lifeLink('Cell', encodedLife, 0, 0, 0, nextColorIndex), \
            ' ' + lifeLink('Border', encodedLlife, 0, 0, 0, 0, 0, if(border, 1, 2)), \
            ' [Reset](#var=)', \
            ' | **Width:** ' + lifeLink('More', encodedWidthMore, 0) + ' ' + lifeLink('Less', encodedWidthLess, 0), \
            ' | **Height:** ' + lifeLink('More', encodedHeightMore, 0) + ' ' + lifeLink('Less', encodedHeightLess, 0), \
            ' | **Size:** ' + lifeLink('More', encodedLife, 0, 0, max(minSize, size + 1)) + \
                ' ' + lifeLink('Less', encodedLife, 0, 0, max(minSize, size - 1)) \
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
    drawLife(life, size, gap, arrayGet(colors, colorIndex - 1), arrayGet(colors, backgroundIndex - 1), if(border, 2, 0))

    // Play?
    jumpif (!play) skipPlay
    setNavigateTimeout(lifeURL(encodedNext, 1), period)
    skipPlay:
endfunction


function lifeURL(encodedLife, play, period, size, color, bkgnd, border, gap, initRatio, borderRatio)
    size = if(size, size, vSize)
    period = if(period, period, vPeriod)
    gap = if(gap, gap, vGap)
    color = if(color, color, vColor)
    bkgnd = if(bkgnd, bkgnd, vBackground)
    border = if(border, if(border - 1, 1, 0), vBorder)
    initRatio = if(initRatio, initRatio, vInitRatio)
    borderRatio = if(borderRatio, borderRatio, vBorderRatio)
    args = if(play, '&var.vPlay=1', '') + \
        if(size, '&var.vSize=' + size, '') + \
        if(period, '&var.vPeriod=' + period, '') + \
        if(gap, '&var.vGap=' + gap, '') + \
        if(color, '&var.vColor=' + color, '') + \
        if(bkgnd, '&var.vBackground=' + bkgnd, '') + \
        if(border, '&var.vBorder=' + border, '') + \
        if(initRatio, '&var.vInitRatio=' + initRatio, '') + \
        if(borderRatio, '&var.vBorderRatio=' + borderRatio, '') + \
        if(encodedLife, "&var.vLife='" + encodedLife + "'", '')
    return '#' + slice(args, 1)
endfunction


function lifeLink(text, encodedLife, play, period, size, color, bkgnd, border, gap, initRatio, borderRatio)
    return '[' + text + '](' + lifeURL(encodedLife, play, period, size, color, bkgnd, border, gap, initRatio, borderRatio) + ')'
endfunction


function lifeNew(width, height, initRatio, borderRatio)
    life = objectNew()
    objectSet(life, 'width', width)
    objectSet(life, 'height', height)
    objectSet(life, 'cells', arrayNew(width * height))
    lifeInit(life, initRatio, borderRatio)
    return life
endfunction


function lifeCopy(life)
    newLife = objectCopy(life)
    objectSet(newLife, 'cells', arrayCopy(objectGet(life, 'cells')))
    return newLife
endfunction


function lifeGet(life, x, y)
    return arrayGet(objectGet(life, 'cells'), (y * objectGet(life, 'width')) + x)
endfunction


function lifeSet(life, x, y, alive)
    return arraySet(objectGet(life, 'cells'), (y * objectGet(life, 'width')) + x, if(alive, 1, 0))
endfunction


function lifeInit(life, initRatio, borderRatio)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    border = ceil(borderRatio * min(width, height))
    iy = 0
    yLoop:
        ix = 0
        xLoop:
            alive = if((ix < border) || (ix >= (width - border)), 0, if((iy < border) || (iy >= (height - border)), 0, rand() < initRatio))
            lifeSet(life, ix, iy, alive)
            ix = ix + 1
        jumpif (ix < width) xLoop
        iy = iy + 1
    jumpif (iy < height) yLoop
    return life
endfunction


function lifeNext(life)
    nextLife = lifeCopy(life)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')
    iy = 0
    yLoop:
        ix = 0
        xLoop:
            cellAlive = lifeGet(life, ix, iy)
            neighborCount = if(ix > 0 && iy > 0, lifeGet(life, ix - 1, iy - 1), 0) + \
                if(iy > 0, lifeGet(life, ix, iy - 1), 0) + \
                if(ix < width - 1 && iy > 0, lifeGet(life, ix + 1, iy - 1), 0) + \
                if(ix > 0, lifeGet(life, ix - 1, iy), 0) + \
                if(ix < width - 1, lifeGet(life, ix + 1, iy), 0) + \
                if(ix > 0 && iy < height - 1, lifeGet(life, ix - 1, iy + 1), 0) + \
                if(iy < height - 1, lifeGet(life, ix, iy + 1), 0) + \
                if(ix < width - 1 && iy < height - 1, lifeGet(life, ix + 1, iy + 1), 0)
            lifeSet(nextLife, ix, iy, if(cellAlive, if(neighborCount < 2, 0, if(neighborCount > 3, 0, 1)), if(neighborCount == 3, 1, 0)))
            ix = ix + 1
        jumpif (ix < width) xLoop
        iy = iy + 1
    jumpif (iy < height) yLoop

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
    ixCell = 0
    cellLoop:
        curAlive = arrayGet(cells, ixCell)
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
        ixCell = ixCell + 1
    jumpif (ixCell < arrayLength(cells)) cellLoop

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
    life = lifeNew(width, height)
    cells = objectGet(life, 'cells')
    ixCell = 0
    ixChar = 0
    charLoop:
    jumpif (ixChar >= len(cellsStr)) charLoopDone
        char = slice(cellsStr, ixChar, ixChar + 1)
        count = indexOf(lifeEncodeChars, char)
        iCount = 0
        countLoop:
        jumpif (iCount >= count) countLoopDone
            arraySet(cells, ixCell, ixChar % 2)
            iCount = iCount + 1
            ixCell = ixCell + 1
        jump countLoop
        countLoopDone:
        ixChar = ixChar + 1
    jump charLoop
    charLoopDone:

    return life
endfunction


lifeEncodeAlpha = 'abcdefghijklmnopqrstuvwxyz'
lifeEncodeChars = '0123456789' + lifeEncodeAlpha + upper(lifeEncodeAlpha)


function drawLife(life, size, gap, color, background, borderSize)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')

    // Draw the background
    setDrawingSize(((width * (gap + size)) + gap) + borderSize, ((height * (gap + size)) + gap) + borderSize)
    drawStyle(if(borderSize, borderColor, 'none'), borderSize, background)
    drawRect(0.5 * borderSize, 0.5 * borderSize, getDrawingWidth() - borderSize, getDrawingHeight() - borderSize)

    // Draw the cells
    drawStyle('none', 0, color)
    iy = 0
    yLoop:
        ix = 0
        xLoop:
            jumpif (!lifeGet(life, ix, iy)) skipCell
            x = (0.5 * borderSize) + gap + (ix * (size + gap))
            y = (0.5 * borderSize) + gap + (iy * (size + gap))
            drawMove(x, y)
            drawHLine(x + size)
            drawVLine(y + size)
            drawHLine(x)
            drawClose()
            skipCell:
            ix = ix + 1
        jumpif (ix < width) xLoop
        iy = iy + 1
    jumpif (iy < height) yLoop
endfunction


// Execute the main entry point
main()
~~~
