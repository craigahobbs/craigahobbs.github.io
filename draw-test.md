# Drawing Test

~~~ drawing
drawingWidth = 300
drawingHeight = 300

# Star sizes
skinnyStarSize = 0.12 * if([drawingWidth] < [drawingHeight], [drawingWidth], [drawingHeight])
chubbyStarSize = 0.08 * if([drawingWidth] < [drawingHeight], [drawingWidth], [drawingHeight])

# Render a randomly-placed, randomly-sized "skinny star"
function skinnyStar()
    size = (1.25 - (0.5 * rand())) * [skinnyStarSize]
    minX = 0
    maxX = [drawingWidth] - [size]
    minY = 0
    maxY = [drawingHeight] - [size]
    x = [minX] + (rand() * ([maxX] - [minX]))
    y = [minY] + (rand() * ([maxY] - [minY]))

    pathMoveTo([x] + (0.5 * [size]), [y])
    pathLineTo([x] + (0.5 * [size]), [y] + [size])
    pathMoveTo([x] + (0.33 * [size]), [y] + (0.5 * [size]))
    pathLineTo([x] + (0.67 * [size]), [y] + (0.5 * [size]))
endfunction

# Render a randomly-placed, randomly-sized "chubby star"
function chubbyStar()
    size = (1.25 - (0.5 * rand())) * [chubbyStarSize]
    minX = 0
    maxX = [drawingWidth] - [size]
    minY = 0
    maxY = [drawingHeight] - [size]
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

# Render several skinny stars
function skinnyStars()
    skinnyStar()
    skinnyStar()
    skinnyStar()
endfunction

# Render several chubby stars
function chubbyStars()
    chubbyStar()
    chubbyStar()
    chubbyStar()
    chubbyStar()
    chubbyStar()
endfunction

# Draw a starscape
skinnyStars()
skinnyStars()
skinnyStars()
skinnyStars()
skinnyStars()
chubbyStars()
chubbyStars()
chubbyStars()
chubbyStars()
chubbyStars()
~~~
