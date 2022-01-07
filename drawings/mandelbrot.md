# The Mandelbrot Set

~~~ markdown-script
// Image size
pixelWidth = if(width, width, 150)
pixelHeight = if(height, height, 100)
pixelSize = if(size, size, 4)

// Compute the drawing size
setDrawingWidth(pixelWidth * pixelSize)
setDrawingHeight(pixelHeight * pixelSize)

// Maximum Mandelbrot set computation iterations
mandelbrot_iterations = if(iter, iter, 60)

// Mandelbrot point extents
mandelbrot_x = if(x, x, 0.5)
mandelbrot_y = if(y, y, 0)
mandelbrot_x_range = if(xr, xr, 2.6)

// Additional Mandelbrot extent variables
mandelbrot_y_range = (pixelHeight / pixelWidth) * mandelbrot_x_range
mandelbrot_x_min = mandelbrot_x - (0.5 * mandelbrot_x_range)
mandelbrot_y_min = mandelbrot_y - (0.5 * mandelbrot_y_range)


// Compute the number of iterations to determine in-out of Mandelbrot set
function mandelbrotSet(x, y, maxIterations)
    // c1 = complex(x, y)
    // c2 = complex(0, 0)
    c1_r = x
    c1_i = y
    c2_r = 0
    c2_i = 0

    // Iteratively compute the next c2 value
    n = 1
    loop:
        // Done?
        jumpif (sqrt((c2_r * c2_r) + (c2_i * c2_i)) > 2) loopDone

        // c2 = c2 * c2 + c1
        c2_r_new = (c2_r * c2_r) - (c2_i * c2_i) + c1_r
        c2_i = (2 * c2_r * c2_i) + c1_i
        c2_r = c2_r_new

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
    colorIndex = n % 4
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
loop_x:
    y = 0
    loop_y:
        n = mandelbrotSet(mandelbrot_x_min + ((x / (pixelWidth - 1)) * mandelbrot_x_range), \
                          mandelbrot_y_min + ((y / (pixelHeight - 1)) * mandelbrot_y_range), \
                          mandelbrot_iterations)
        drawStyle('none', 0, mandelbrotColor(n))
        drawRect(x * pixelSize, y * pixelSize, pixelSize, pixelSize)

        y = y + 1
        jumpif (y < pixelHeight) loop_y

    x = x + 1
    jumpif (x < pixelWidth) loop_x
~~~
