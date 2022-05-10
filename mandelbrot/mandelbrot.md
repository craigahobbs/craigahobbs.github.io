# Mandelbrot Set Explorer

~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


function main()
    # Image size
    width = if(vWidth, vWidth, 150)
    height = if(vHeight, vHeight, 100)
    pixelSize = if(vSize, vSize, 4)

    # Maximum Mandelbrot set computation iterations
    iter = if(vIter, vIter, 60)

    # Mandelbrot point extents
    x = if(vX, vX, -0.5)
    y = if(vY, vY, 0)
    xRange = if(vXR, vXR, 2.6)

    # Mandelbrot color cycle
    cycle = if(vCycle, vCycle, 0) % 4

    # Menu
    menuXYDelta = 0.1 * xRange
    menuIterDelta = 10
    menuWHDelta = 20
    markdownPrint( \
        menuLinkPair('X', menuLink('Left', vWidth, vHeight, vSize, vIter, x - menuXYDelta, vY, vXR, vCycle), \
            menuLink('Right', vWidth, vHeight, vSize, vIter, x + menuXYDelta, vY, vXR, vCycle)) + \
            ': ' + x + '  ', \
        menuLinkPair('Y', menuLink('Up', vWidth, vHeight, vSize, vIter, vX, y + menuXYDelta, vXR, vCycle), \
            menuLink('Down', vWidth, vHeight, vSize, vIter, vX, y - menuXYDelta, vXR, vCycle)) + \
            ': ' + y + '  ', \
        menuLinkPair('Zoom', menuLink('In', vWidth, vHeight, vSize, vIter, vX, vY, xRange - menuXYDelta, vCycle), \
            menuLink('Out', vWidth, vHeight, vSize, vIter, vX, vY, xRange + menuXYDelta, vCycle)) + \
            ': ' + xRange + '  ', \
        menuLinkPair('Iter', menuLink('Up', vWidth, vHeight, vSize, iter + menuIterDelta, vX, vY, vXR, vCycle), \
            menuLink('Down', vWidth, vHeight, vSize, max(20, iter - menuIterDelta), vX, vY, vXR, vCycle)) + \
            ': ' + iter, \
        '', \
        menuLink('Cycle', vWidth, vHeight, vSize, vIter, vX, vY, vXR, cycle + 1) + ' |', \
        '[Reset](#var=) | ', \
        menuLinkPair('Width', menuLink('Up', width + menuWHDelta, vHeight, vSize, vIter, vX, vY, vXR, vCycle), \
            menuLink('Down', max(menuWHDelta, width - menuWHDelta), vHeight, vSize, vIter, vX, vY, vXR, vCycle)) + ' |', \
        menuLinkPair('Height', menuLink('Up', vWidth, height + menuWHDelta, vSize, vIter, vX, vY, vXR, vCycle), \
            menuLink('Down', vWidth, max(menuWHDelta, height - menuWHDelta), vSize, vIter, vX, vY, vXR, vCycle)) + ' |', \
        menuLinkPair('Size', menuLink('Up', vWidth, vHeight, pixelSize + 1, vIter, vX, vY, vXR, vCycle), \
            menuLink('Down', vWidth, vHeight, max(1, pixelSize - 1), vIter, vX, vY, vXR, vCycle)) \
    )

    # Draw the Mandelbrot set
    colors = arrayNew('#17becf', '#2ca02c', '#98df8a', '#1f77b4')
    mandelbrotSet(width, height, pixelSize, colors, cycle, x, y, xRange, iter)
endfunction


function menuLink(text, w, h, s, i, x, y, xr, vc)
    args = if(w, '&var.vWidth=' + w, '') + \
        if(h != null, '&var.vHeight=' + h, '') + \
        if(s != null, '&var.vSize=' + s, '') + \
        if(i != null, '&var.vIter=' + i, '') + \
        if(x != null, '&var.vX=' + x, '') + \
        if(y != null, '&var.vY=' + y, '') + \
        if(xr != null, '&var.vXR=' + xr, '') + \
        if(vc != null, '&var.vCycle=' + vc, '')
    return '[' + text + '](#' + slice(args, 1) + ')'
endfunction


function menuLinkPair(text, link1, link2)
    return '**' + text + '** (' + link1 + ' | ' + link2 + ')'
endfunction


function mandelbrotSet(width, height, pixelSize, colors, colorCycle, x, y, xRange, iter)
    # Set the drawing size
    setDrawingSize(width * pixelSize, height * pixelSize)

    # Compute the set extents
    yRange = (height / width) * xRange
    xMin = x - 0.5 * xRange
    yMin = y - 0.5 * yRange

    # Draw each pixel in the set
    x = 0
    loopX:
        y = 0
        loopY:
            n = mandelbrotValue(xMin + (x / (width - 1)) * xRange, yMin + (y / (height - 1)) * yRange, iter)
            drawStyle('none', 0, if(n == 0, 'black', arrayGet(colors, (n + colorCycle) % len(colors))))
            drawRect(x * pixelSize, (height - y - 1) * pixelSize, pixelSize, pixelSize)
            y = y + 1
        jumpif (y < height) loopY

        x = x + 1
    jumpif (x < width) loopX
endfunction


function mandelbrotValue(x, y, maxIterations)
    # c1 = complex(x, y)
    # c2 = complex(0, 0)
    c1r = x
    c1i = y
    c2r = 0
    c2i = 0

    # Iteratively compute the next c2 value
    n = 1
    loop:
        # Done?
        jumpif (sqrt(c2r * c2r + c2i * c2i) > 2) loopDone

        # c2 = c2 * c2 + c1
        c2rNew = c2r * c2r - c2i * c2i + c1r
        c2i = 2 * c2r * c2i + c1i
        c2r = c2rNew

        n = n + 1
        jumpif (n <= maxIterations) loop

    # Hit max iterations - the point is in the Mandelbrot set
    return 0

    loopDone:
    return n
endfunction


# Execute main
main()
~~~
