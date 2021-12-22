# Drawing Test

~~~ drawing
drawingWidth = if(size, size, 400)
drawingHeight = if(size, size, 300)

# Render a randomly-placed, randomly-sized shape
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

# Render a "skinny star"
function skinnyStar(x, y, size)
    setStyle('gray')
    moveTo(x + (0.5 * size), y)
    lineTo(x + (0.5 * size), y + size)
    moveTo(x + (0.35 * size), y + (0.5 * size))
    lineTo(x + (0.65 * size), y + (0.5 * size))
endfunction

# Render a "chubby star"
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

# Render the stars
shapes(skinnyStar, 10, 0.10)
shapes(chubbyStar, 30, 0.05)
shapes(grayBall, 15, 0.02)
~~~
