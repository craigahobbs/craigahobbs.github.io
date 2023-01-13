~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


function main()
    # Set the title
    titleText = if(vMessage, vMessage, 'Happy Holidays!')
    setDocumentTitle(titleText)

    # Menu
    if (!vFullScreen, markdownPrint( \
        '**Happy Holidays**  ', \
        '[Reset](#var=) |', \
        "[Custom](#var.vMessage='Edit%20Message%20in%20URL') |", \
        '[Full](#var.vFullScreen=1' + if(vMessage, "&var.vMessage='" + encodeURIComponent(vMessage) + "'", '') + ')' \
    ))

    # Compute the drawing width/height
    drawTextStyle()
    width = getWindowWidth() - 3 * getTextHeight()
    height = getWindowHeight() - if(vFullScreen, 3, 6) * getTextHeight()

    # Set the drawing width/height
    setDrawingSize(width, height)
    drawStyle('none', 0, 'white')
    drawRect(0, 0, width, height)

    # Draw the stars
    shapes(skinnyStar, 20, 0.2, 0.3)
    shapes(chubbyStar, 50, 0.05, 0.12)
    shapes(grayBall, 30, 0.02, 0.07)
    shapes(purpleBall, 30, 0.02, 0.07)
    shapes(blueEllipse, 30, 0.02, 0.05)

    # Measure the title box height
    titleBoxWidth = 0.8 * width
    titleTextWidth = 0.9 * titleBoxWidth
    titleTextHeight = mathMin(getTextHeight(titleText, titleTextWidth), 0.2 * height)
    titleBoxHeight = 3 * titleTextHeight

    # Draw the title
    drawStyle('black', 5, '#ff0000f0')
    drawRect(0.5 * width - 0.5 * titleBoxWidth, 0.5 * height - 0.5 * titleBoxHeight, titleBoxWidth, titleBoxHeight)
    drawTextStyle(titleTextHeight, 'white')
    drawText(titleText, 0.5 * width, 0.5 * height)

    # Set the resize handler
    setWindowResize(main)
endfunction


function shapes(shapeFn, count, minSize, maxSize)
    width = getDrawingWidth()
    height = getDrawingHeight()
    widthHeight = mathMin(width, height)
    ix = 0
    loop:
        size = widthHeight * (minSize + mathRandom() * (maxSize - minSize))
        minX = size
        maxX = width - size
        minY = size
        maxY = height - size
        x = minX + mathRandom() * (maxX - minX)
        y = minY + mathRandom() * (maxY - minY)
        shapeFn(x, y, size)
    ix = ix + 1
    jumpif (ix < count) loop
endfunction


function skinnyStar(x, y, size)
    drawStyle('black')
    drawMove(x + 0.5 * size, y)
    drawVLine(y + size)
    drawMove(x + 0.35 * size, y + 0.5 * size)
    drawHLine(x + 0.65 * size)
endfunction


function chubbyStar(x, y, size)
    fillRand = mathRandom()
    fill = if(fillRand < 0.33, '#ff0000', if(fillRand < 0.67, '#00ff00', '#0060ff'))
    drawStyle('black', 2, fill)
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
