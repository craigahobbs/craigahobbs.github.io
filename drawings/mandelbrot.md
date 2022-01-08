# The Mandelbrot Set

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

// Mandelbrot color cycle
mandelbrotCycle = if(vCycle, vCycle, 0)
mandelbrotCycleCount = 4

// Menu URL helper function
function menuLink(text, sep, w, h, s, i, x, y, xr, vc)
    args = if(w, '&var.vWidth=' + w, '') + \
        if(h, '&var.vHeight=' + h, '') + \
        if(s, '&var.vSize=' + s, '') + \
        if(i, '&var.vIter=' + i, '') + \
        if(x, '&var.vX=' + x, '') + \
        if(y, '&var.vY=' + y, '') + \
        if(xr, '&var.vXR=' + xr, '') + \
        if(vc, '&var.vCycle=' + vc, '')
    '[' + text + '](' + hashURL('#' + right(args, len(args) - 1)) + ')' + if(sep, ' |', '')
endfunction

// Menu
markdownPrint( \
    '[Reset](' + hashURL('#var=') + ') |', \
    menuLink('Up', 0, vWidth, vHeight, vSize, vIter, vX, mandelbrotY - 0.1 * mandelbrotXRange, vXR, vCycle), \
    menuLink('Down', 1, vWidth, vHeight, vSize, vIter, vX, 0.9 * mandelbrotY + 0.1 * mandelbrotXRange, vXR, vCycle), \
    menuLink('Left', 0, vWidth, vHeight, vSize, vIter, mandelbrotX - 0.1 * mandelbrotXRange, vY, vXR, vCycle), \
    menuLink('Right', 1, vWidth, vHeight, vSize, vIter, mandelbrotX + 0.1 * mandelbrotXRange, vY, vXR, vCycle), \
    menuLink('ZoomIn', 0, vWidth, vHeight, vSize, vIter, vX, vY, 0.9 * mandelbrotXRange, vCycle), \
    menuLink('ZoomOut', 1, vWidth, vHeight, vSize, vIter, vX, vY, 1.1 * mandelbrotXRange, vCycle), \
    menuLink('IterUp', 0, vWidth, vHeight, vSize, 1.1 * mandelbrotIterations, vX, vY, vXR, vCycle), \
    menuLink('IterDown', 1, vWidth, vHeight, vSize, 0.9 * mandelbrotIterations, vX, vY, vXR, vCycle), \
    menuLink('SizeUp', 0, vWidth, vHeight, 1.1 * pixelSize, vIter, vX, vY, vXR, vCycle), \
    menuLink('SizeDown', 1, vWidth, vHeight, 0.9 * pixelSize, vIter, vX, vY, vXR, vCycle), \
    menuLink('WidthUp', 0, 1.1 * pixelWidth, vHeight, vSize, vIter, vX, vY, vXR, vCycle), \
    menuLink('WidthDown', 1, 0.9 * pixelWidth, vHeight, vSize, vIter, vX, vY, vXR, vCycle), \
    menuLink('HeightUp', 0, vWidth, 1.1 * pixelHeight, vSize, vIter, vX, vY, vXR, vCycle), \
    menuLink('HeightDown', 1, vWidth, 0.9 * pixelHeight, vSize, vIter, vX, vY, vXR, vCycle), \
    menuLink('Cycle', 0, vWidth, vHeight, vSize, vIter, vX, vY, vXR, (mandelbrotCycle + 1) % mandelbrotCycleCount) \
)

// Additional Mandelbrot extent variables
mandelbrotYRange = (pixelHeight / pixelWidth) * mandelbrotXRange
mandelbrotXMin = mandelbrotX - (0.5 * mandelbrotXRange)
mandelbrotYMin = mandelbrotY - (0.5 * mandelbrotYRange)


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
    // In the Mandelbrot set? If so, the pixel is black
    jumpif (n == 0) black

    // Compute the color from the modulus
    colorIndex = (n + mandelbrotCycle) % 4
    jumpif (colorIndex == 0) color0
    jumpif (colorIndex == 1) color1
    jumpif (colorIndex == 2) color2

    // color4:
    '#1f77b4'
    jump done

color0:
    '#17becf'
    jump done

color1:
    '#2ca02c'
    jump done

color2:
    '#98df8a'
    jump done

black:
    'black'

done:
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
        drawRect(x * pixelSize, y * pixelSize, pixelSize, pixelSize)

        y = y + 1
        jumpif (y < pixelHeight) loopY

    x = x + 1
    jumpif (x < pixelWidth) loopX
~~~
