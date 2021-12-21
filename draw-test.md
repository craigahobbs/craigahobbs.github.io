# Drawing Test

~~~ drawing
drawingWidth = 300
drawingHeight = 300

function shapeX(x, y, size)
    pathMoveTo([x], [y])
    pathLineTo([x] + [size], [y] + [size])
    pathMoveTo([x] + [size], [y])
    pathLineTo([x], [y] + [size])
endfunction

function shapeRect(x, y, width, height)
    pathMoveTo([x], [y])
    pathLineTo([x] + [width], [y])
    pathLineTo([x] + [width], [y] + [height])
    pathLineTo([x], [y] + [height])
    pathClose()
endfunction

shapeRect(0.5, 0.5, [drawingWidth] - 1, [drawingHeight] - 1)
shapeX(0.1 * [drawingWidth], 0.1 * [drawingHeight], 0.2 * [drawingWidth])
shapeX(0.35 * [drawingWidth], 0.35 * [drawingHeight], (0.1 + (0.4 * rand())) * [drawingWidth])
shapeX(0.8 * [drawingWidth], 0.2 * [drawingHeight], 0.1 * [drawingWidth])
shapeX(0.15 * [drawingWidth], 0.5 * [drawingHeight], 0.4 * [drawingWidth])
shapeX(0.45 * [drawingWidth], 0.2 * [drawingHeight], 0.3 * [drawingWidth])
~~~
