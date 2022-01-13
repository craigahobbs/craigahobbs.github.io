# Conway's Game of Life

~~~ markdown-script
// Licensed under the MIT License
// https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

function main()
    // Application inputs
    size = if(vSize, vSize, 8)
    gap = if(vGap, vGap, 1)
    color = if(vColor, vColor, 'forestgreen')
    background = if(vBackground, vBackground, 'white')
    init = if(vInit, vInit, 0.2)
    border = if(vBorder, vBorder, 0.1)

    // Initialize or decode the life board
    jumpif (vLife) lifeInitDecode
        life = lifeNew(50, 50)
        lifeInit(life, init, border)
    jump lifeInitDone
    lifeInitDecode:
        life = lifeDecode(vLife, init, border)
    lifeInitDone:

    next = lifeNext(life)

    resetLife = arrayGet(life, 'width') + '-' + arrayGet(life, 'height')
    markdownPrint( \
        "[Next](#var.vLife='" + lifeEncode(next) + "') |", \
        "[Reset](#var.vLife='" + resetLife + if(resetLife == vLife, '-', '') + "')" \
    )
    drawLife(life, size, gap, color, background)
endfunction


function lifeNew(width, height)
    life = objectNew()
    objectSet(life, 'width', width)
    objectSet(life, 'height', height)
    objectSet(life, 'cells', arrayNew(width * height))
    lifeInit(life)
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
            jumpif ((ix < border) || (ix >= (width - border))) skipSet
            jumpif ((iy < border) || (iy >= (height - border))) skipSet
            lifeSet(life, ix, iy, rand() < initRatio)
            skipSet:
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


function lifeDecode(lifeStr, initRatio, borderRatio)
    parts = arraySplit(lifeStr, '-')
    width = value(arrayGet(parts, 0))
    height = value(arrayGet(parts, 1))
    cellsStr = arrayGet(parts, 2)
    life = lifeNew(width, height)

    // Init on empty cells string
    jumpif (cellsStr) skipInit
    return lifeInit(life, initRatio, borderRatio)
    skipInit:

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


function drawLife(life, size, gap, color, background)
    width = objectGet(life, 'width')
    height = objectGet(life, 'height')

    setDrawingWidth((width * (gap + size)) + gap)
    setDrawingHeight((height * (gap + size)) + gap)

    drawStyle('black', 2, background)
    drawRect(0, 0, getDrawingWidth(), getDrawingHeight())

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
