~~~ markdown-script
# The Chaos Balls model
ballsTypes = schemaParse( \
    '# The Chaos Balls Model', \
    'struct ChaosBalls', \
    '', \
    '    # The background color', \
    '    string backgroundColor', \
    '', \
    '    # The border color', \
    '    string borderColor', \
    '', \
    '    # The border size, as a ratio of width/height', \
    '    float(>= 0, <= 0.2) borderSize', \
    '', \
    '    # The change period, in seconds', \
    '    float period', \
    '', \
    '    # The ball groups', \
    '    BallGroup[len > 0] groups', \
    '', \
    '# A Chaos Ball Group', \
    'struct BallGroup', \
    '', \
    '    # The ball count', \
    '    int count', \
    '', \
    '    # The ball color', \
    '    string color', \
    '', \
    '    # The minimum size, as a ratio of the width/height', \
    '    float(> 0, <= 0.5) minSize', \
    '', \
    '    # The maximum size, as a ratio of the width/height', \
    '    float(> 0, <= 0.5) maxSize', \
    '', \
    '    # The minimum speed, as a ratio of the width/height per second', \
    '    float(> 0, <= 0.5) minSpeed', \
    '', \
    '    # The maximum speed, as a ratio of the width/height per second', \
    '    float(> 0, <= 0.5) maxSpeed', \
    '', \
    '# The Chaos Balls runtime model', \
    'struct RuntimeBalls', \
    '', \
    '    # The Chaos Balls model', \
    '    ChaosBalls chaosBalls', \
    '', \
    '    # The runtime balls', \
    '    RuntimeBall[len > 0] balls', \
    '', \
    '# The runtime ball model', \
    'struct RuntimeBall', \
    '', \
    '    # The ball color', \
    '    string color', \
    '', \
    '    # The ball size, as a ratio of the width/height', \
    '    float size', \
    '', \
    '    # The ball x-position, as a ratio of the width', \
    '    float x', \
    '', \
    '    # The ball y-position, as a ratio of the height', \
    '    float y', \
    '', \
    '    # The ball delta-x, as a ratio of the width', \
    '    float dx', \
    '', \
    '    # The ball delta-y, as a ratio of the width', \
    '    float dy', \
    '' \
)


# The default Chaos Balls configuration
ballsDefault = schemaValidate(ballsTypes, 'ChaosBalls', objectNew( \
    'backgroundColor', 'white', \
    'borderColor', 'blue', \
    'borderSize', 0.05, \
    'period', 0.05, \
    'groups', arrayNew( \
        objectNew('count', 10, 'color', '#0000ff40', 'minSize', 0.3, 'maxSize', 0.4, 'minSpeed', 0.1, 'maxSpeed', 0.15), \
        objectNew('count', 20, 'color', '#00ff0040', 'minSize', 0.2, 'maxSize', 0.3, 'minSpeed', 0.15, 'maxSpeed', 0.2), \
        objectNew('count', 30, 'color', '#ff000040', 'minSize', 0.1, 'maxSize', 0.2, 'minSpeed', 0.2, 'maxSpeed', 0.25) \
    ) \
))


async function ballsMain()
    if(vURL != null, ballsOpen(vURL), ballsResize())
    setWindowResize(ballsResize)
endfunction


async function ballsOpen(url)
    chaosBalls = if(!url, ballsDefault, schemaValidate(ballsTypes, 'ChaosBalls', fetch(url)))
    balls = if(chaosBalls != null, ballsRuntime(chaosBalls))
    if(balls != null, sessionStorageSet('balls', jsonStringify(balls)))
    setWindowLocation('#var=')
endfunction


function ballsResize()
    ballsTimeout(true)
endfunction


function ballsTimeout(noMove)
    balls = ballsLoad()
    if(!noMove, ballsMove(balls))
    ballsDraw(balls)
    documentReset()
    if(vPlay, setWindowTimeout(ballsTimeout, objectGet(objectGet(balls, 'chaosBalls'), 'period') * 1000))
endfunction


function ballsWidth()
    return getWindowWidth() - 4 * getTextHeight()
endfunction


function ballsHeight()
    return getWindowHeight() - 4 * getTextHeight()
endfunction


function ballsLoad()
    balls = sessionStorageGet('balls')
    balls = if(balls != null, schemaValidate(ballsTypes, 'RuntimeBalls', jsonParse(balls)))
    jumpif (balls != null) ballsDone
        balls = ballsRuntime(ballsDefault)
        sessionStorageSet('balls', jsonStringify(balls))
    ballsDone:
    return balls
endfunction


function ballsRuntime(chaosBalls)
    ballsBalls = arrayNew()
    balls = objectNew('chaosBalls', chaosBalls, 'balls', ballsBalls)

    # Iterate the ball groups
    ixGroup = 0
    groups = objectGet(chaosBalls, 'groups')
    borderSize = objectGet(chaosBalls, 'borderSize')
    groupLoop:
        group = arrayGet(groups, ixGroup)
        groupCount = objectGet(group, 'count')
        groupColor = objectGet(group, 'color')
        groupMinSize = objectGet(group, 'minSize')
        groupMaxSize = objectGet(group, 'maxSize')
        groupMinSpeed = objectGet(group, 'minSpeed')
        groupMaxSpeed = objectGet(group, 'maxSpeed')

        # Create the group's balls
        ixBall = 0
        ballLoop:
            # Compute a random size
            size = groupMinSize + mathRandom() * (groupMaxSize - groupMinSize)

            # Compute a random x and y
            xMin = borderSize + 0.5 * size
            xMax = 1 - xMin
            yMin = borderSize + 0.5 * size
            yMax = 1 - yMin
            x = xMin + mathRandom() * (xMax - xMin)
            y = yMin + mathRandom() * (yMax - yMin)

            # Compute a random dx and dy
            speed = groupMinSpeed + mathRandom() * (groupMaxSpeed - groupMinSpeed)
            speedAngle = mathRandom() * 2 * mathPi()
            dx = speed * mathCos(speedAngle)
            dy = speed * mathSin(speedAngle)

            # Add the ball
            arrayPush(ballsBalls, objectNew('color', groupColor, 'size', size, 'x', x, 'y', y, 'dx', dx, 'dy', dy))

            ixBall = ixBall + 1
        jumpif (ixBall < groupCount) ballLoop

        ixGroup = ixGroup + 1
    jumpif (ixGroup < arrayLength(groups)) groupLoop

    # Validate the runtime balls model
    return schemaValidate(ballsTypes, 'RuntimeBalls', balls)
endfunction


function ballsDraw(balls)
    width = ballsWidth()
    height = ballsHeight()
    widthHeight = mathMin(width, height)

    chaosBalls = objectGet(balls, 'chaosBalls')
    backgroundColor = objectGet(chaosBalls, 'backgroundColor')
    borderColor = objectGet(chaosBalls, 'borderColor')
    borderSize = objectGet(chaosBalls, 'borderSize')
    borderSizePx = borderSize * widthHeight

    setDrawingSize(width, height)
    drawStyle(borderColor, borderSizePx, backgroundColor)
    drawRect(0.5 * borderSizePx, 0.5 * borderSizePx, width - borderSizePx, height - borderSizePx)

    ixBall = 0
    ballsBalls = objectGet(balls, 'balls')
    ballLoop:
        ball = arrayGet(ballsBalls, ixBall)
        drawStyle(null, 0, objectGet(ball, 'color'))
        drawCircle(objectGet(ball, 'x') * width, objectGet(ball, 'y') * height, 0.5 * objectGet(ball, 'size') * widthHeight)
        ixBall = ixBall + 1
    jumpif (ixBall < arrayLength(ballsBalls)) ballLoop
endfunction


function ballsMove(balls)
    width = ballsWidth()
    height = ballsHeight()
    widthHeight = mathMin(width, height)

    chaosBalls = objectGet(balls, 'chaosBalls')
    borderSize = objectGet(chaosBalls, 'borderSize') * widthHeight
    period = objectGet(chaosBalls, 'period')

    ixBall = 0
    ballsBalls = objectGet(balls, 'balls')
    ballLoop:
        ball = arrayGet(ballsBalls, ixBall)
        size = objectGet(ball, 'size') * widthHeight
        x = objectGet(ball, 'x') * width
        y = objectGet(ball, 'y') * height
        dxR = objectGet(ball, 'dx')
        dx = dxR * period * width
        dyR = objectGet(ball, 'dy')
        dy = dyR * period * height

        xMin = borderSize + 0.5 * size
        xMax = width - xMin
        yMin = borderSize + 0.5 * size
        yMax = height - yMin

        x = x + dx
        dxR = if(x < xMin || x > xMax, -dxR, dxR)
        x = if(x < xMin, xMin + (xMin - x), if(x > xMax, xMax - (x - xMax), x))

        y = y + dy
        dyR = if(y < yMin || y > yMax, -dyR, dyR)
        y = if(y < yMin, yMin + (yMin - y), if(y > yMax, yMax - (y - yMax), y))

        objectSet(ball, 'x', x / width)
        objectSet(ball, 'y', y / height)
        objectSet(ball, 'dx', dxR)
        objectSet(ball, 'dy', dyR)

        ixBall = ixBall + 1
    jumpif (ixBall < arrayLength(ballsBalls)) ballLoop

    sessionStorageSet('balls', jsonStringify(schemaValidate(ballsTypes, 'RuntimeBalls', balls)))
endfunction


ballsMain()
~~~
