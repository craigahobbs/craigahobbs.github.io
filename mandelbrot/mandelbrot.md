# Mandelbrot Set Explorer

~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include <args.mds>


function mandelbrotMain():
    # Parse arguments
    args = argsParse(mandelbrotArguments)
    cycle = objectGet(args, 'cycle')
    xRange = objectGet(args, 'xRange')

    # Menu
    menuXYDelta = 0.1 * xRange
    menuIterDelta = 10
    menuWHDelta = 20
    markdownPrint( \
        mandelbrotUpDown(args, 'X', 'Left', 'Right', 'x', -menuXYDelta) + ' \\', \
        mandelbrotUpDown(args, 'Y', 'Up', 'Down', 'y', menuXYDelta) + ' \\', \
        mandelbrotUpDown(args, 'Zoom', 'In', 'Out', 'xRange', -menuXYDelta, menuXYDelta) + ' \\', \
        mandelbrotUpDown(args, 'Iter', 'Up', 'Down', 'iter', menuIterDelta, menuIterDelta), \
        '', \
        argsLink(mandelbrotArguments, 'Cycle', objectNew('cycle', cycle + 1)) + ' |', \
        argsLink(mandelbrotArguments, 'Reset', null, true) + ' | ', \
        mandelbrotUpDown(args, 'Width', 'Up', 'Down', 'width', menuWHDelta, menuWHDelta, true) + ' |', \
        mandelbrotUpDown(args, 'Height', 'Up', 'Down', 'height', menuWHDelta, menuWHDelta, true) + ' |', \
        mandelbrotUpDown(args, 'Size', 'Up', 'Down', 'size', 1, 1, true) \
    )

    # Draw the Mandelbrot set
    mandelbrotDraw( \
        objectGet(args, 'width'), \
        objectGet(args, 'height'), \
        objectGet(args, 'size'), \
        arrayNew('#17becf', '#2ca02c', '#98df8a', '#1f77b4'), \
        cycle, \
        objectGet(args, 'x'), \
        objectGet(args, 'y'), \
        xRange, \
        objectGet(args, 'iter') \
    )
endfunction


mandelbrotArguments = argsValidate(arrayNew( \
    objectNew('name', 'cycle', 'type', 'int', 'default', 0), \
    objectNew('name', 'height', 'type', 'int', 'default', 100), \
    objectNew('name', 'iter', 'type', 'int', 'default', 60), \
    objectNew('name', 'size', 'type', 'int', 'default', 4), \
    objectNew('name', 'width', 'type', 'int', 'default', 150), \
    objectNew('name', 'x', 'type', 'float', 'default', -0.5), \
    objectNew('name', 'xRange', 'type', 'float', 'default', 2.6), \
    objectNew('name', 'y', 'type', 'float', 'default', 0) \
))


function mandelbrotUpDown(args, label, labelUp, labelDown, argName, argDelta, argMin, noValue):
    # Get the argument value
    argValue = objectGet(args, argName)
    if argMin != null:
        argValue = mathMax(argMin, argValue)
    endif

    # Compute the up/down links
    linkUp = argsLink(mandelbrotArguments, labelUp, objectNew(argName, argValue + argDelta))
    valueDown = argValue - argDelta
    if argMin == null || valueDown >= argMin:
        linkDown = argsLink(mandelbrotArguments, labelDown, objectNew(argName, valueDown))
    else:
        linkDown = labelDown
    endif

    return '**' + markdownEscape(label) + '**&nbsp;(' + linkUp + '&nbsp;|&nbsp;' + linkDown + ')' + \
        if(noValue, '', ':&nbsp;' + argValue)
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
