# Drawing Testb

~~~ drawing
drawingWidth = 300
drawingHeight = 300

# Star sizes
star1Size = 0.15 * if([drawingWidth] < [drawingHeight], [drawingWidth], [drawingHeight])
star2Size = 0.1 * if([drawingWidth] < [drawingHeight], [drawingWidth], [drawingHeight])

# Render a randomly-placed, randomly-sized "skinny star"
function star1()
    size = (1.25 - (0.5 * rand())) * [star1Size]
    minX = 0.5 * [size]
    maxX = [drawingWidth] - (0.5 * [size])
    minY = 0.5 * [size]
    maxY = [drawingHeight] - (0.5 * [size])
    x = [minX] + (rand() * ([maxX] - [minX]))
    y = [minY] + (rand() * ([maxY] - [minY]))

    pathMoveTo([x] + (0.5 * [size]), [y])
    pathLineTo([x] + (0.5 * [size]), [y] + [size])
    pathMoveTo([x] + (0.33 * [size]), [y] + (0.5 * [size]))
    pathLineTo([x] + (0.67 * [size]), [y] + (0.5 * [size]))
endfunction

# Render a randomly-placed, randomly-sized "chubby star"
function star2()
    size = (1.25 - (0.5 * rand())) * [star2Size]
    minX = 0.5 * [size]
    maxX = [drawingWidth] - (0.5 * [size])
    minY = 0.5 * [size]
    maxY = [drawingHeight] - (0.5 * [size])
    x = [minX] + (rand() * ([maxX] - [minX]))
    y = [minY] + (rand() * ([maxY] - [minY]))

    pathMoveTo([x], [y])
    pathLineTo([x] + (0.5 * [size]), [y] + (0.33 * [size]))
    pathLineTo([x] + [size], [y])
    pathLineTo([x] + (0.67 * [size]), [y] + (0.5 * [size]))
    pathLineTo([x] + [size], [y] + [size])
    pathLineTo([x] + (0.5 * [size]), [y] + (0.67 * [size]))
    pathLineTo([x], [y] + [size])
    pathLineTo([x] + (0.33 * [size]), [y] + (0.5 * [size]))
    pathClose()
endfunction

# Render 5 skinny stars
function star1_5()
    star1()
    star1()
    star1()
    star1()
    star1()
endfunction

# Render 5 chubby stars
function star2_5()
    star2()
    star2()
    star2()
    star2()
    star2()
endfunction

# Draw a starscape
star1_5()
star1_5()
star1_5()
star2_5()
star2_5()
star2_5()
~~~
