# Mandelbrot Set Explorer

~~~ markdown-script
// Image size
pixelWidth = if(vWidth, vWidth, 150)
pixelHeight = if(vHeight, vHeight, 100)
pixelSize = if(vSize, vSize, 4)

// Compute the drawing size
setDrawingWidth(pixelWidth * pixelSize)
setDrawingHeight(pixelHeight * pixelSize)

// Maximum Mandelbrot set computation iterations
mandelbrotIterations = if(vIter, vIter, 60)

// Mandelbrot point extents
mandelbrotX = if(vX, vX, 0.5)
mandelbrotY = if(vY, vY, 0)
mandelbrotXRange = if(vXR, vXR, 2.6)

// Additional Mandelbrot extent variables
mandelbrotYRange = (pixelHeight / pixelWidth) * mandelbrotXRange
mandelbrotXMin = mandelbrotX - (0.5 * mandelbrotXRange)
mandelbrotYMin = mandelbrotY - (0.5 * mandelbrotYRange)

// Mandelbrot color cycle
mandelbrotCycle = if(vCycle, vCycle, 0) % 4


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

// Menu
menuXYDelta = 0.1 * mandelbrotXRange
menuIterDelta = 10
menuWHDelta = 20
markdownPrint( \
    '**X** (' + \
        menuLink('Left', vWidth, vHeight, vSize, vIter, mandelbrotX - menuXYDelta, vY, vXR, vCycle) + \
        ' | ' + \
        menuLink('Right', vWidth, vHeight, vSize, vIter, mandelbrotX + menuXYDelta, vY, vXR, vCycle) + \
        '): ' + mandelbrotX + '  ', \
    '**Y** (' + \
        menuLink('Up', vWidth, vHeight, vSize, vIter, vX, mandelbrotY + menuXYDelta, vXR, vCycle) + \
        ' | ' + \
        menuLink('Down', vWidth, vHeight, vSize, vIter, vX, mandelbrotY - menuXYDelta, vXR, vCycle) + \
        ': ' + mandelbrotY + '  ', \
    '**Zoom** (' + \
        menuLink('In', vWidth, vHeight, vSize, vIter, vX, vY, mandelbrotXRange - menuXYDelta, vCycle) + \
        ' | ' + \
        menuLink('Out', vWidth, vHeight, vSize, vIter, vX, vY, mandelbrotXRange + menuXYDelta, vCycle) + \
        '): ' + mandelbrotXRange + '  ', \
    '**Iter** (' + \
        menuLink('Up', vWidth, vHeight, vSize, mandelbrotIterations + menuIterDelta, vX, vY, vXR, vCycle) + \
        ' | ' + \
        menuLink('Down', vWidth, vHeight, vSize, max(20, mandelbrotIterations - menuIterDelta), vX, vY, vXR, vCycle) + \
        '): ' + mandelbrotIterations + '  ', \
    '', \
    menuLink('Cycle', vWidth, vHeight, vSize, vIter, vX, vY, vXR, mandelbrotCycle + 1) + ' |', \
    '[Reset](' + hashURL('#var=') + ') | ', \
    '**Width** (' + \
        menuLink('Up', pixelWidth + menuWHDelta, vHeight, vSize, vIter, vX, vY, vXR, vCycle), \
        ' | ' + \
        menuLink('Down', max(menuWHDelta, pixelWidth - menuWHDelta), vHeight, vSize, vIter, vX, vY, vXR, vCycle), \
        ' ) |', \
    '**Height** (' + \
        menuLink('Up', vWidth, pixelHeight + menuWHDelta, vSize, vIter, vX, vY, vXR, vCycle), \
        ' | ' + \
        menuLink('Down', vWidth, max(menuWHDelta, pixelHeight - menuWHDelta), vSize, vIter, vX, vY, vXR, vCycle), \
        ' ) |', \
    '**Size** (' + \
        menuLink('Up', vWidth, vHeight, pixelSize + 1, vIter, vX, vY, vXR, vCycle) + \
        ' | ' + \
        menuLink('Down', vWidth, vHeight, max(1, pixelSize - 1), vIter, vX, vY, vXR, vCycle) + \
        ' )' \
)


// Compute the number of iterations to determine in-out of Mandelbrot set
function mandelbrotSet(x, y, maxIterations)
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
    colorIndex = (n + mandelbrotCycle) % 4
    if(n == 0, 'black', \
        if(colorIndex == 0, '#17becf', \
        if(colorIndex == 1, '#2ca02c', \
        if(colorIndex == 2, '#98df8a', '#1f77b4'))))
endfunction


// Compute the color of each pixel and render it
x = 0
loopX:
    y = 0
    loopY:
        n = mandelbrotSet(mandelbrotXMin + ((x / (pixelWidth - 1)) * mandelbrotXRange), \
                          mandelbrotYMin + ((y / (pixelHeight - 1)) * mandelbrotYRange), \
                          mandelbrotIterations)
        drawStyle('none', 0, mandelbrotColor(n))
        drawRect(x * pixelSize, (pixelHeight - y - 1) * pixelSize, pixelSize, pixelSize)

        y = y + 1
        jumpif (y < pixelHeight) loopY

    x = x + 1
    jumpif (x < pixelWidth) loopX
~~~
