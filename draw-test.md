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
    path('gray')
    pathMoveTo(x + (0.5 * size), y)
    pathLineTo(x + (0.5 * size), y + size)
    pathMoveTo(x + (0.35 * size), y + (0.5 * size))
    pathLineTo(x + (0.65 * size), y + (0.5 * size))
endfunction

# Render a "chubby star"
function chubbyStar(x, y, size)
    fillRand = rand()
    fill = if(fillRand < 0.33, '#ff0000', if(fillRand < 0.67, '#00ff00', '#0060ff'))
    path('black', 2, fill)
    pathMoveTo(x, y)
    pathLineTo(x + (0.5 * size), y + (0.33 * size))
    pathLineTo(x + size, y)
    pathLineTo(x + (0.67 * size), y + (0.5 * size))
    pathLineTo(x + size, y + size)
    pathLineTo(x + (0.5 * size), y + (0.67 * size))
    pathLineTo(x, y + size)
    pathLineTo(x + (0.33 * size), y + (0.5 * size))
    pathClose()
endfunction

# Render the stars
shapes(skinnyStar, 10, 0.10)
shapes(chubbyStar, 30, 0.05)
~~~
