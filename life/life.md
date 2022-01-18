# Conway's Game of Life

~~~ markdown-script
// Licensed under the MIT License
// https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

function main()
    // Application inputs
    play = if(vPlay, vPlay, 0)
    defaultWidthHeight = 50
    minWidthHeight = 20
    minPeriod = 250
    period = max(minPeriod, if(vPeriod, vPeriod, 1000))
    defaultSize = 10
    minSize = 1
    size = max(minSize, if(vSize, vSize, defaultSize))
    gap = if(vGap, vGap, 1)
    colors = arraySplit('green,white,fuchsia,gold,gray,greenyellow,indigo,lavender,lawngreen', ',')
    defaultColor = 1
    colorIndex = max(1, 1 + ((if(vColor, vColor, defaultColor) - 1) % len(colors)))
    color = arrayGet(colors, colorIndex - 1)
    defaultBackground = 2
    backgroundIndex = max(1, 1 + ((if(vBackground, vBackground, defaultBackground) - 1) % len(colors)))
    background = arrayGet(colors, backgroundIndex - 1)
    defaultBorder = 0
    border = if(vBorder, 1, defaultBorder)
    initRatio = if(vInitRatio, vInitRatio, 0.2)
    borderRatio = if(vBorderRatio, vBorderRatio, 0.1)

    // Initialize or decode the life board
    jumpif (vLife) lifeInitDecode
        life = lifeNew(defaultWidthHeight, defaultWidthHeight, initRatio, borderRatio)
    jump lifeInitDone
    lifeInitDecode:
        life = lifeDecode(vLife)
    lifeInitDone:
    lifeWidth = objectGet(life, 'width')
    lifeHeight = objectGet(life, 'height')

    // Menu
    nextLife = lifeNext(life)
    randomLife = lifeInit(lifeCopy(life), initRatio, borderRatio)
    widthMoreLife = lifeNew(max(minWidthHeight, ceil(1.1 * lifeWidth)), lifeHeight, initRatio, borderRatio)
    widthLessLife = lifeNew(max(minWidthHeight, ceil(0.9 * lifeWidth)), lifeHeight, initRatio, borderRatio)
    heightMoreLife = lifeNew(lifeWidth, max(minWidthHeight, ceil(1.1 * lifeHeight)), initRatio, borderRatio)
    heightLessLife = lifeNew(lifeWidth, max(minWidthHeight, ceil(0.9 * lifeHeight)), initRatio, borderRatio)
    nextColorIndex = 1 + (colorIndex % arrayLength(colors))
    nextColorIndex = if(nextColorIndex != backgroundIndex, nextColorIndex, 1 + (nextColorIndex % arrayLength(colors)))
    nextBackgroundIndex = 1 + (backgroundIndex % arrayLength(colors))
    nextBackgroundIndex = if(nextBackgroundIndex != colorIndex, nextBackgroundIndex, 1 + (nextBackgroundIndex % arrayLength(colors)))
    markdownPrint( \
        if(play, lifeLink('Pause', life, 0), lifeLink('Play', nextLife, 1)) + \
            if(play, '', ' | ' + lifeLink('Step', nextLife, 0)) + \
            if(play, '', ' ' + lifeLink('Random', randomLife, 0)) + \
            if(play, '', ' | ' + lifeLink('Background', life, 0, 0, 0, 0, nextBackgroundIndex)) + \
            if(play, '', ' ' + lifeLink('Cell', life, 0, 0, 0, nextColorIndex)) + \
            if(play, '', ' ' + lifeLink('Border', life, 0, 0, 0, 0, 0, if(border, 1, 2))) + \
            if(play, '', ' [Reset](#var=)') + \
            if(play, ' | **Speed:** ' + lifeLink('More', life, 1, max(minPeriod, fixed(0.75 * period, 2))) + \
                ' ' + lifeLink('Less', life, 1, fixed(1.25 * period, 2)), '') + \
            if(play, '', ' | **Width:** ' + lifeLink('More', widthMoreLife, 0) + ' ' + lifeLink('Less', widthLessLife, 0)) + \
            if(play, '', ' | **Height:** ' + lifeLink('More', heightMoreLife, 0) + ' ' + lifeLink('Less', heightLessLife, 0)) + \
            if(play, '', ' | **Size:** ' + lifeLink('More', life, 0, 0, max(minSize, size + 1)) + \
                ' ' + lifeLink('Less', life, 0, 0, max(minSize, size - 1))) \
    )

    // Life board
    drawLife(life, size, gap, color, background, if(border, 2, 0))

    // Play?
    jumpif (!play) skipPlay
    setNavigateTimeout(lifeURL(nextLife, 1), period)
    skipPlay:
endfunction


function lifeURL(life, play, period, size, color, bkgnd, border, gap, initRatio, borderRatio)
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
        if(life, "&var.vLife='" + lifeEncode(life) + "'", '')
    return '#' + slice(args, 1)
endfunction


function lifeLink(text, life, play, period, size, color, bkgnd, border, gap, initRatio, borderRatio)
    return '[' + text + '](' + lifeURL(life, play, period, size, color, bkgnd, border, gap, initRatio, borderRatio) + ')'
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
            alive = if((ix < border) || (ix >= (width - border)), 0, \
                if((iy < border) || (iy >= (height - border)), 0, rand() < initRatio))
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
            lt = if(ix > 0 && iy > 0, lifeGet(life, ix - 1, iy - 1), 0)
            mt = if(iy > 0, lifeGet(life, ix, iy - 1), 0)
            rt = if(ix < width - 1 && iy > 0, lifeGet(life, ix + 1, iy - 1), 0)
            lm = if(ix > 0, lifeGet(life, ix - 1, iy), 0)
            mm = lifeGet(life, ix, iy)
            rm = if(ix < width - 1, lifeGet(life, ix + 1, iy), 0)
            lb = if(ix > 0 && iy < height - 1, lifeGet(life, ix - 1, iy + 1), 0)
            mb = if(iy < height - 1, lifeGet(life, ix, iy + 1), 0)
            rb = if(ix < width - 1 && iy < height - 1, lifeGet(life, ix + 1, iy + 1), 0)
            nc = lt + mt + rt + lm + rm + lb + mb + rb
            alive = if(mm, if(nc < 2, 0, if(nc > 3, 0, 1)), if(nc == 3, 1, 0))
            lifeSet(nextLife, ix, iy, alive)

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
    lifeStr = width + '-' + height + '-'

    alive = 0
    count = 0
    maxCount = len(lifeEncodeChars) - 1
    ixCell = 0
    cellLoop:
        curAlive = arrayGet(cells, ixCell)
        jumpif (curAlive != alive) cellLoopAlive

        count = count + 1
        jumpif (count < maxCount) cellLoopNext

        lifeStr = lifeStr + slice(lifeEncodeChars, count, count + 1)
        alive = if(alive, 0, 1)
        count = 0
        jump cellLoopNext

        cellLoopAlive:
        lifeStr = lifeStr + slice(lifeEncodeChars, count, count + 1)
        alive = if(alive, 0, 1)
        count = 1

        cellLoopNext:
        ixCell = ixCell + 1
    jumpif (ixCell < arrayLength(cells)) cellLoop

    jumpif (!count) skipLast
    lifeStr = lifeStr + slice(lifeEncodeChars, count, count + 1)
    skipLast:

    return lifeStr
endfunction


function lifeDecode(lifeStr)
    parts = arraySplit(lifeStr, '-')
    width = value(arrayGet(parts, 0))
    height = value(arrayGet(parts, 1))
    cellsStr = arrayGet(parts, 2)
    life = lifeNew(width, height)

    // Decode the cell string
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

    setDrawingSize(((width * (gap + size)) + gap) + borderSize, ((height * (gap + size)) + gap) + borderSize)

    drawStyle(if(borderSize, 'black', 'none'), borderSize, background)
    drawRect(0.5 * borderSize, 0.5 * borderSize, getDrawingWidth() - borderSize, getDrawingHeight() - borderSize)

    drawStyle('none', 0, color)
    iy = 0
    yLoop:
        ix = 0
        xLoop:
            jumpif (!lifeGet(life, ix, iy)) skipCell
            drawRect(gap + (ix * (gap + size)), gap + (iy * (gap + size)), size, size)
            skipCell:
            ix = ix + 1
        jumpif (ix < width) xLoop
        iy = iy + 1
    jumpif (iy < height) yLoop
endfunction


// Execute the main entry point
main()
~~~
