# Happy Holidays 2021

~~~ drawing
drawingWidth = if(width, width, 600)
drawingHeight = if(height, height, 300)

# Render a number of randomly-placed, randomly-sized shapes
function shapes(shapeFn, count, sizeRatio)
    ix = 0
    loop:
        size = sizeRatio * (1 + (2 * rand())) * if(drawingWidth < drawingHeight, drawingWidth, drawingHeight)
        minX = 0
        maxX = drawingWidth - size
        minY = 0
        maxY = drawingHeight - size
        x = minX + (rand() * (maxX - minX))
        y = minY + (rand() * (maxY - minY))
        shapeFn(x, y, size)
    ix = ix + 1
    jumpif (ix < count) loop
endfunction

function skinnyStar(x, y, size)
    setStyle('gray')
    moveTo(x + (0.5 * size), y)
    vlineTo(y + size)
    moveTo(x + (0.35 * size), y + (0.5 * size))
    hlineTo(x + (0.65 * size))
endfunction

function chubbyStar(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.33, '#ff0000', if(fillRand < 0.67, '#00ff00', '#0060ff'))
    setStyle('black', 2, fill)
    moveTo(x, y)
    lineTo(x + (0.5 * size), y + (0.33 * size))
    lineTo(x + size, y)
    lineTo(x + (0.67 * size), y + (0.5 * size))
    lineTo(x + size, y + size)
    lineTo(x + (0.5 * size), y + (0.67 * size))
    lineTo(x, y + size)
    lineTo(x + (0.33 * size), y + (0.5 * size))
    pathClose()
endfunction

function grayBall(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.5, '#c0c0c0', '#e0e0e0')
    setStyle('black', 2, fill)
    rect(x, y, size, size, 3, 3)
endfunction

function purpleBall(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.5, '#c000c0', '#e000e0')
    setStyle('black', 2, fill)
    circle(x, y, size)
endfunction

function blueEllipse(x, y, size)
    setStyle('black', 2, '#00c0f0')
    ellipse(x, y, size, 0.5 * size)
endfunction

# Draw the stars
shapes(skinnyStar, 10, 0.10)
shapes(chubbyStar, 30, 0.05)
shapes(grayBall, 15, 0.02)
shapes(purpleBall, 15, 0.01)
shapes(blueEllipse, 15, 0.015)

# Measure the title box height
titleText = if(message,message,'Happy Holidays!')
titleBoxWidth = 0.8 * drawingWidth
titleTextWidth = 0.9 * titleBoxWidth
titleTextHeight = min(textHeight(titleText, titleTextWidth), 0.2 * drawingHeight)
titleBoxHeight = 3 * titleTextHeight

# Draw the title
setStyle('black', 5, '#ff0000f0')
rect((0.5 * drawingWidth) - (0.5 * titleBoxWidth), (0.5 * drawingHeight) - (0.5 * titleBoxHeight), titleBoxWidth, titleBoxHeight)
setTextStyle(titleTextHeight, 'white')
drawText(titleText, 0.5 * drawingWidth, 0.5 * drawingHeight)
~~~
