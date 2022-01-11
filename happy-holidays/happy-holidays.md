# Happy Holidays

~~~ markdown-script
// Licensed under the MIT License
// https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

function main()
    jumpif (vPrint) skipMenu

    // Menu
    markdownPrint( \
        '[Reset](#var=) |', \
        '[Small](#var.vWidth=400&var.vHeight=250' + if(vMessage, "&var.vMessage='" + vMessage + "'", '') + ') |', \
        '[Medium](#var.vWidth=700&var.vHeight=350' + if(vMessage, "&var.vMessage='" + vMessage + "'", '') + ') |', \
        '[Large](#var.vWidth=1000&var.vHeight=450' + if(vMessage, "&var.vMessage='" + vMessage + "'", '') + ') |', \
        "[Custom Message](#var.vMessage='Hello!'" + if(vWidth, '&var.vWidth=' + vWidth, '') + if(vHeight, '&var.vHeight=' + vHeight, '') + ') |', \
        '[Print](#var.vPrint=1' + if(vWidth, '&var.vWidth=' + vWidth, '') + if(vHeight, '&var.vHeight=' + vHeight, '') + \
            if(vMessage, "&var.vMessage='" + encodeURIComponent(vMessage) + "'", '') + ')' \
    )

    skipMenu:

    // Set the drawing width/height
    setDrawingWidth(if(vWidth, vWidth, 600))
    setDrawingHeight(if(vHeight, vHeight, 300))

    // Draw the stars
    shapes(skinnyStar, 10, 0.10)
    shapes(chubbyStar, 30, 0.05)
    shapes(grayBall, 15, 0.02)
    shapes(purpleBall, 15, 0.01)
    shapes(blueEllipse, 15, 0.015)

    // Measure the title box height
    titleText = if(vMessage, vMessage, 'Happy Holidays!')
    titleBoxWidth = 0.8 * getDrawingWidth()
    titleTextWidth = 0.9 * titleBoxWidth
    titleTextHeight = min(getTextHeight(titleText, titleTextWidth), 0.2 * getDrawingHeight())
    titleBoxHeight = 3 * titleTextHeight

    // Draw the title
    drawStyle('black', 5, '#ff0000f0')
    drawRect((0.5 * getDrawingWidth()) - (0.5 * titleBoxWidth), (0.5 * getDrawingHeight()) - (0.5 * titleBoxHeight), titleBoxWidth, titleBoxHeight)
    drawTextStyle(titleTextHeight, 'white')
    drawText(titleText, 0.5 * getDrawingWidth(), 0.5 * getDrawingHeight())
endfunction


function shapes(shapeFn, count, sizeRatio)
    ix = 0
    loop:
        size = sizeRatio * (1 + (2 * rand())) * if(getDrawingWidth() < getDrawingHeight(), getDrawingWidth(), getDrawingHeight())
        minX = size
        maxX = getDrawingWidth() - size
        minY = size
        maxY = getDrawingHeight() - size
        x = minX + (rand() * (maxX - minX))
        y = minY + (rand() * (maxY - minY))
        shapeFn(x, y, size)
    ix = ix + 1
    jumpif (ix < count) loop
endfunction


function skinnyStar(x, y, size)
    drawStyle('gray')
    drawMove(x + (0.5 * size), y)
    drawVLine(y + size)
    drawMove(x + (0.35 * size), y + (0.5 * size))
    drawHLine(x + (0.65 * size))
endfunction


function chubbyStar(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.33, '#ff0000', if(fillRand < 0.67, '#00ff00', '#0060ff'))
    drawStyle('black', 2, fill)
    drawMove(x, y)
    drawLine(x + (0.5 * size), y + (0.33 * size))
    drawLine(x + size, y)
    drawLine(x + (0.67 * size), y + (0.5 * size))
    drawLine(x + size, y + size)
    drawLine(x + (0.5 * size), y + (0.67 * size))
    drawLine(x, y + size)
    drawLine(x + (0.33 * size), y + (0.5 * size))
    drawClose()
endfunction


function grayBall(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.5, '#c0c0c0', '#e0e0e0')
    drawStyle('black', 2, fill)
    drawRect(x, y, size, size, 3, 3)
endfunction


function purpleBall(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.5, '#c000c0', '#e000e0')
    drawStyle('black', 2, fill)
    drawCircle(x, y, size)
endfunction


function blueEllipse(x, y, size)
    drawStyle('black', 2, '#00c0f0')
    drawEllipse(x, y, size, 0.5 * size)
endfunction


// Execute the main entry point
main()
~~~
