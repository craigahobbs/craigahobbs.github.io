# Mandelbrot Set Explorer

~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include <args.mds>


function mandelbrotMain():
    # Parse arguments
    args = argsParse(mandelbrotArguments)
    width = objectGet(args, 'width')
    height = objectGet(args, 'height')
    pixelSize = objectGet(args, 'size')
    iter = objectGet(args, 'iter')
    x = objectGet(args, 'x')
    y = objectGet(args, 'y')
    xRange = objectGet(args, 'xRange')
    cycle = objectGet(args, 'cycle')

    # Menu
    menuXYDelta = 0.1 * xRange
    menuIterDelta = 10
    menuWHDelta = 20
    markdownPrint( \
        mandelbrotMenuPair( \
            'X', \
            argsLink(mandelbrotArguments, 'Left', objectNew('x', x - menuXYDelta)), \
            argsLink(mandelbrotArguments, 'Right', objectNew('x', x + menuXYDelta)) \
        ) + ': ' + x + '  ', \
        mandelbrotMenuPair( \
            'Y', \
            argsLink(mandelbrotArguments, 'Up', objectNew('y', y + menuXYDelta)), \
            argsLink(mandelbrotArguments, 'Down', objectNew('y', y - menuXYDelta)) \
        ) + ': ' + y + '  ', \
        mandelbrotMenuPair( \
            'Zoom', \
            argsLink(mandelbrotArguments, 'In', objectNew('xRange', xRange - menuXYDelta)), \
            argsLink(mandelbrotArguments, 'Out', objectNew('xRange', xRange + menuXYDelta)) \
        ) + ': ' + xRange + '  ', \
        mandelbrotMenuPair( \
            'Iter', \
            argsLink(mandelbrotArguments, 'Up', objectNew('iter', iter - menuIterDelta)), \
            argsLink(mandelbrotArguments, 'Down', objectNew('iter', iter + menuIterDelta)) \
        ) + ': ' + iter, \
        '', \
        argsLink(mandelbrotArguments, 'Cycle', objectNew('cycle', cycle + 1)) + ' |', \
        argsLink(mandelbrotArguments, 'Reset', null, true) + ' | ', \
        mandelbrotMenuPair( \
            'Width', \
            argsLink(mandelbrotArguments, 'Up', objectNew('width', width + menuWHDelta)), \
            argsLink(mandelbrotArguments, 'Down', objectNew('width', mathMax(menuWHDelta, width - menuWHDelta))) \
        ) + ' |', \
        mandelbrotMenuPair( \
            'Height', \
            argsLink(mandelbrotArguments, 'Up', objectNew('height', height + menuWHDelta)), \
            argsLink(mandelbrotArguments, 'Down', objectNew('height', mathMax(menuWHDelta, height - menuWHDelta))) \
        ) + ' |', \
        mandelbrotMenuPair( \
            'Size', \
            argsLink(mandelbrotArguments, 'Up', objectNew('size', pixelSize + 1)), \
            argsLink(mandelbrotArguments, 'Down', objectNew('size', mathMax(1, pixelSize - 1))) \
        ) \
    )

    # Draw the Mandelbrot set
    colors = arrayNew('#17becf', '#2ca02c', '#98df8a', '#1f77b4')
    mandelbrotDraw(width, height, pixelSize, colors, cycle, x, y, xRange, iter)
endfunction


mandelbrotArguments = argsValidate(arrayNew( \
    objectNew('name', 'cycle', 'type', 'int', 'default', 0), \
    objectNew('name', 'height', 'type', 'int', 'default', 100), \
    objectNew('name', 'iter', 'type', 'int', 'default', 60), \
    objectNew('name', 'size', 'type', 'int', 'default', 4), \
    objectNew('name', 'width', 'type', 'int', 'default', 150), \
    objectNew('name', 'x', 'type', 'float', 'default', -0.5), \
    objectNew('name', 'xRange', 'global', 'vXR', 'type', 'float', 'default', 2.6), \
    objectNew('name', 'y', 'type', 'float', 'default', 0) \
))


function mandelbrotMenuPair(text, link1, link2):
    return '**' + text + '** (' + link1 + ' | ' + link2 + ')'
endfunction


function mandelbrotDraw(width, height, pixelSize, colors, colorCycle, x, y, xRange, iter):
    # Set the drawing size
    drawNew(width * pixelSize, height * pixelSize)

    # Compute the set extents
    yRange = (height / width) * xRange
    xMin = x - 0.5 * xRange
    yMin = y - 0.5 * yRange

    # Draw each pixel in the set
    x = 0
    while x < width:
        y = 0
        while y < height:
            n = mandelbrotValue(xMin + (x / (width - 1)) * xRange, yMin + (y / (height - 1)) * yRange, iter)
            drawStyle('none', 0, if(n == 0, 'black', arrayGet(colors, (n + colorCycle) % arrayLength(colors))))
            drawPathRect(x * pixelSize, (height - y - 1) * pixelSize, pixelSize, pixelSize)
            y = y + 1
        endwhile
        x = x + 1
    endwhile
endfunction


function mandelbrotValue(x, y, maxIterations):
    # c1 = complex(x, y)
    # c2 = complex(0, 0)
    c1r = x
    c1i = y
    c2r = 0
    c2i = 0

    # Iteratively compute the next c2 value
    n = 1
    while n <= maxIterations:
        # Done?
        if (mathSqrt(c2r * c2r + c2i * c2i) > 2):
            return n
        endif

        # c2 = c2 * c2 + c1
        c2rNew = c2r * c2r - c2i * c2i + c1r
        c2i = 2 * c2r * c2i + c1i
        c2r = c2rNew

        n = n + 1
    endwhile

    # Hit max iterations - the point is in the Mandelbrot set
    return 0
endfunction


# Execute main
mandelbrotMain()
~~~
