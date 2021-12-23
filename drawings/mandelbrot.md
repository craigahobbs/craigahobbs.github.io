# The Mandelbrot Set

~~~ drawing
function mandelbrotSet(x, y, maxIterations)
    c1_r = x
    c1_i = y
    c2_r = 0
    c2_i = 0

    n = 1
    loop:
        jumpif (sqrt((c2_r * c2_r) + (c2_i * c2_i)) > 2) loopDone

        # c2 = c2 * c2 + c1
        #
        # (c2_r + c2_i * i) * (c2_r + c2_i * i)
        # => (c2_r * c2_r) + (c2_r * c2_i * i) + (c2_r * c2_i * i) * (c2_i * i * c2_i * i)
        # => (c2_r * c2_r) + 2 * (c2_r * c2_i * i) * (-1 * c2_i * c2_i)

        c2_r_new = (c2_r * c2_r) - (c2_i * c2_i) + c1_r
        c2_i = (2 * c2_r * c2_i) + c1_i
        c2_r = c2_r_new

        n = n + 1
        jumpif (n <= maxIterations) loop

    n = 0

    loopDone:
endfunction


function mandelbrotColor(n)
    jumpif (n == 0) black

    colorIndex = n % 4
    jumpif (colorIndex == 0) color0
    jumpif (colorIndex == 1) color1
    jumpif (colorIndex == 2) color2

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


pixelWidth = 300
pixelHeight = 200
pixelSize = 2

drawingWidth = pixelWidth * pixelSize
drawingHeight = pixelHeight * pixelSize

mandelbrot_x_min = -0.75
mandelbrot_x_max = 2
mandelbrot_y_max = 1
mandelbrot_size = (mandelbrot_x_max - mandelbrot_x_min) / pixelWidth
mandelbrot_y_min = mandelbrot_y_max - (pixelHeight * mandelbrot_size)

mandelbrot_iterations = 50


x = 0
loop_x:
    y = 0
    loop_y:
        n = mandelbrotSet(mandelbrot_x_min + ((x / (pixelWidth - 1)) * (mandelbrot_x_max - mandelbrot_x_min)), \
                          mandelbrot_y_max - ((y / (pixelHeight - 1)) * (mandelbrot_y_max - mandelbrot_y_min)), \
                          mandelbrot_iterations)
        setStyle('none', 1, mandelbrotColor(n))
        rect(x * pixelSize, y * pixelSize, pixelSize, pixelSize)

        y = y + 1
        jumpif (y < pixelHeight) loop_y

    x = x + 1
    jumpif (x < pixelWidth) loop_x
~~~