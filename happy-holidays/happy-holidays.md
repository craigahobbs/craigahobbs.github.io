~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


function main()
    # Set the title
    titleText = if(vMessage, vMessage, 'Happy Holidays!')
    documentSetTitle(titleText)

    # Menu
    if (!vFullScreen, markdownPrint( \
        '**Happy Holidays**  ', \
        '[Reset](#var=) |', \
        "[Custom](#var.vMessage='Edit%20Message%20in%20URL') |", \
        '[Full](#var.vFullScreen=1' + if(vMessage, "&var.vMessage='" + urlEncodeComponent(vMessage) + "'", '') + ')' \
    ))

    # Compute the drawing width/height
    width = windowWidth() - 3 * documentFontSize()
    height = windowHeight() - if(vFullScreen, 3, 6) * documentFontSize()

    # Measure the title box height
    titleBoxWidth = 0.8 * width
    titleTextWidth = 0.9 * titleBoxWidth
    titleTextHeight = mathMin(drawTextHeight(titleText, titleTextWidth), 0.2 * height)
    titleBoxHeight = 3 * titleTextHeight

    # Set the drawing width/height
    drawNew(width, height)
    drawStyle('none', 0, 'white')
    drawRect(0, 0, width, height)

    # Draw the stars
    baseSize = titleBoxHeight
    shapes(skinnyStar, baseSize, 20, 0.2, 0.3)
    shapes(chubbyStar, baseSize, 50, 0.1, 0.2)
    shapes(grayBall, baseSize, 30, 0.06, 0.12)
    shapes(purpleBall, baseSize, 30, 0.06, 0.12)
    shapes(blueEllipse, baseSize, 30, 0.06, 0.1)

    # Draw the title
    drawStyle('black', 5, '#ff0000f0')
    drawRect(0.5 * width - 0.5 * titleBoxWidth, 0.5 * height - 0.5 * titleBoxHeight, titleBoxWidth, titleBoxHeight)
    drawTextStyle(titleTextHeight, 'white')
    drawText(titleText, 0.5 * width, 0.5 * height)

    # Set the resize handler
    windowSetResize(main)
endfunction


function shapes(shapeFn, baseSize, count, minSize, maxSize)
    width = drawWidth()
    height = drawHeight()
    ix = 0
    while ix < count:
        size = baseSize * (minSize + mathRandom() * (maxSize - minSize))
        minX = size
        maxX = width - size
        minY = size
        maxY = height - size
        x = minX + mathRandom() * (maxX - minX)
        y = minY + mathRandom() * (maxY - minY)
        shapeFn(x, y, size)
        ix = ix + 1
    endwhile
endfunction


function skinnyStar(x, y, size)
    drawStyle('black', 1, 'none')
    drawMove(x + 0.5 * size, y)
    drawVLine(y + size)
    drawMove(x + 0.35 * size, y + 0.5 * size)
    drawHLine(x + 0.65 * size)
endfunction


function chubbyStar(x, y, size)
    fillRand = mathRandom()
    fill = if(fillRand < 0.33, '#ff0000', if(fillRand < 0.67, '#00ff00', '#0060ff'))
    drawStyle('black', 1, fill)
    drawMove(x, y)
    drawLine(x + 0.5 * size, y + 0.33 * size)
    drawLine(x + size, y)
    drawLine(x + 0.67 * size, y + 0.5 * size)
    drawLine(x + size, y + size)
    drawLine(x + 0.5 * size, y + 0.67 * size)
    drawLine(x, y + size)
    drawLine(x + 0.33 * size, y + 0.5 * size)
    drawClose()
endfunction


function grayBall(x, y, size)
    fillRand = mathRandom()
    fill = if(fillRand < 0.5, '#c0c0c0', '#e0e0e0')
    drawStyle('black', 2, fill)
    drawRect(x, y, size, size, 3, 3)
endfunction


function purpleBall(x, y, size)
    fillRand = mathRandom()
    fill = if(fillRand < 0.5, '#c000c0', '#e000e0')
    drawStyle('black', 2, fill)
    drawCircle(x, y, 0.5 * size)
endfunction


function blueEllipse(x, y, size)
    drawStyle('black', 2, '#00c0f0')
    drawEllipse(x, y, size, 0.5 * size)
endfunction


# Execute the main entry point
main()
~~~
