# Mandelbrot Set Explorer

~~~ markdown-script
// Main entry point
function main()
    // Image size
    pixelWidth = if(vWidth, vWidth, 150)
    pixelHeight = if(vHeight, vHeight, 100)
    pixelSize = if(vSize, vSize, 4)

    // Maximum Mandelbrot set computation iterations
    mandelbrotIterations = if(vIter, vIter, 60)

    // Mandelbrot point extents
    mandelbrotX = if(vX, vX, 0.5)
    mandelbrotY = if(vY, vY, 0)
    mandelbrotXRange = if(vXR, vXR, 2.6)

    // Mandelbrot color cycle
    mandelbrotCycle = if(vCycle, vCycle, 0) % 4

    // Menu
    menuXYDelta = 0.1 * mandelbrotXRange
    menuIterDelta = 10
    menuWHDelta = 20
    markdownPrint( \
        menuLinkPair('X', menuLink('Left', vWidth, vHeight, vSize, vIter, mandelbrotX - menuXYDelta, vY, vXR, vCycle), \
            menuLink('Right', vWidth, vHeight, vSize, vIter, mandelbrotX + menuXYDelta, vY, vXR, vCycle)) + \
            ': ' + mandelbrotX + '  ', \
        menuLinkPair('Y', menuLink('Up', vWidth, vHeight, vSize, vIter, vX, mandelbrotY + menuXYDelta, vXR, vCycle), \
            menuLink('Down', vWidth, vHeight, vSize, vIter, vX, mandelbrotY - menuXYDelta, vXR, vCycle)) + \
            ': ' + mandelbrotY + '  ', \
        menuLinkPair('Zoom', menuLink('In', vWidth, vHeight, vSize, vIter, vX, vY, mandelbrotXRange - menuXYDelta, vCycle), \
            menuLink('Out', vWidth, vHeight, vSize, vIter, vX, vY, mandelbrotXRange + menuXYDelta, vCycle)) + \
            ': ' + mandelbrotXRange + '  ', \
        menuLinkPair('Iter', menuLink('Up', vWidth, vHeight, vSize, mandelbrotIterations + menuIterDelta, vX, vY, vXR, vCycle), \
            menuLink('Down', vWidth, vHeight, vSize, max(20, mandelbrotIterations - menuIterDelta), vX, vY, vXR, vCycle)) + \
            ': ' + mandelbrotIterations, \
        '', \
        menuLink('Cycle', vWidth, vHeight, vSize, vIter, vX, vY, vXR, mandelbrotCycle + 1) + ' |', \
        '[Reset](' + hashURL('#var=') + ') | ', \
        menuLinkPair('Width', menuLink('Up', pixelWidth + menuWHDelta, vHeight, vSize, vIter, vX, vY, vXR, vCycle), \
            menuLink('Down', max(menuWHDelta, pixelWidth - menuWHDelta), vHeight, vSize, vIter, vX, vY, vXR, vCycle)) + ' |', \
        menuLinkPair('Height', menuLink('Up', vWidth, pixelHeight + menuWHDelta, vSize, vIter, vX, vY, vXR, vCycle), \
            menuLink('Down', vWidth, max(menuWHDelta, pixelHeight - menuWHDelta), vSize, vIter, vX, vY, vXR, vCycle)) + ' |', \
        menuLinkPair('Size', menuLink('Up', vWidth, vHeight, pixelSize + 1, vIter, vX, vY, vXR, vCycle), \
            menuLink('Down', vWidth, vHeight, max(1, pixelSize - 1), vIter, vX, vY, vXR, vCycle)) \
    )

    // Draw the Mandelbrot set
    mandelbrotSet(pixelWidth, pixelHeight, pixelSize, mandelbrotCycle, mandelbrotX, mandelbrotY, mandelbrotXRange, mandelbrotIterations)
endfunction


// Menu URL helper function
function menuLink(text, w, h, s, i, x, y, xr, vc)
    args = if(w, '&var.vWidth=' + w, '') + \
        if(h, '&var.vHeight=' + h, '') + \
        if(s, '&var.vSize=' + s, '') + \
        if(i, '&var.vIter=' + i, '') + \
        if(x, '&var.vX=' + x, '') + \
        if(y, '&var.vY=' + y, '') + \
        if(xr, '&var.vXR=' + xr, '') + \
        if(vc, '&var.vCycle=' + vc, '')
    '[' + text + '](' + hashURL('#' + right(args, len(args) - 1)) + ')'
endfunction


// Menu link pair helper function
function menuLinkPair(text, link1, link2)
    '**' + text + '** (' + link1 + ' | ' + link2 + ')'
endfunction


// Render the Mandelbrot set
function mandelbrotSet(width, height, pixelSize, colorCycle, x, y, xRange, iter)
    // Set the drawing size
    setDrawingWidth(width * pixelSize)
    setDrawingHeight(height * pixelSize)

    // Compute the set extents
    yRange = (height / width) * xRange
    xMin = x - (0.5 * xRange)
    yMin = y - (0.5 * yRange)

    // Draw each pixel in the set
    x = 0
    loopX:
        y = 0
        loopY:
            n = mandelbrotValue(xMin + ((x / (width - 1)) * xRange), yMin + ((y / (height - 1)) * yRange), iter)
            drawStyle('none', 0, mandelbrotColor(if(n, n + colorCycle, 0)))
            drawRect(x * pixelSize, (height - y - 1) * pixelSize, pixelSize, pixelSize)

            y = y + 1
        jumpif (y < height) loopY

        x = x + 1
    jumpif (x < width) loopX
endfunction


// Compute the number of iterations to determine in-out of Mandelbrot set
function mandelbrotValue(x, y, maxIterations)
    // c1 = complex(x, y)
    // c2 = complex(0, 0)
    c1r = x
    c1i = y
    c2r = 0
    c2i = 0

    // Iteratively compute the next c2 value
    n = 1
    loop:
        // Done?
        jumpif (sqrt((c2r * c2r) + (c2i * c2i)) > 2) loopDone

        // c2 = c2 * c2 + c1
        c2rNew = (c2r * c2r) - (c2i * c2i) + c1r
        c2i = (2 * c2r * c2i) + c1i
        c2r = c2rNew

        n = n + 1
        jumpif (n <= maxIterations) loop

    // Hit max iterations - the point is in the Mandelbrot set
    n = 0

    loopDone:
endfunction


// Compute a color from a Mandelbrot set value
function mandelbrotColor(n)
    colorIndex = (n) % 4
    if(n == 0, 'black', \
        if(colorIndex == 0, '#17becf', \
        if(colorIndex == 1, '#2ca02c', \
        if(colorIndex == 2, '#98df8a', '#1f77b4'))))
endfunction


// Execute main
main()
~~~
