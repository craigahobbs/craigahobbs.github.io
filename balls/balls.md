~~~ markdown-script
width = 1000
height = 600
borderColor = 'black'
borderSize = 10
ballsTimeoutMs = 25
ballsSpeedX = 500
ballsSpeedY = 300

ballColorCount = 30
ballSizeCount = 10
ballColors = arrayNew('blue', 'green', 'red', 'lightblue', 'lightgreen', 'pink')
ballSizeMin = 30
ballSizeMax = 60

ballsTypes = schemaParse( \
    'struct RandomBalls', \
    '    string(len > 0) borderSize', \
    '    string borderColor', \
    '    RandomBall[len > 0] balls', \
    '', \
    '# The random ball generator model', \
    'struct RandomBall', \
    '', \
    '    # The minimum X-delta as a percentage of the width per second', \
    '    float(>= 0, <= 0.2) minDx', \
    '', \
    '    # The maximum X-delta as a percentage of the width per second', \
    '    float(>= 0, <= 0.2) maxDx', \
    '', \
    '    # The minimum Y-delta as a percentage of the height per second', \
    '    float(>= 0, <= 0.2) minDy', \
    '', \
    '    # The maximum Y-delta as a percentage of the height per second', \
    '    float(>= 0, <= 0.2) maxDy', \
    '', \
    '    # The minimum size as a percentage of the height', \
    '    float(>= 0, <= 0.2) minSize', \
    '', \
    '    # The maximum size as a percentage of the height', \
    '    float(>= 0, <= 0.2) maxSize', \
    '', \
    '    # The list of potential colors', \
    '    string[len > 0] colors', \
    '', \
    'struct Ball', \
    '    float x', \
    '    float y', \
    '    float dx', \
    '    float dy', \
    '    float size', \
    '    string color', \
    '', \
    '    float xMin', \
    '    float yMin', \
    '    float xMax', \
    '    float yMax', \
    '', \
    'struct Balls', \
    '    Ball[] balls' \
)


function ballsMain()
    ballsDraw()
    if(!vReset && vPlay, setWindowTimeout(ballsTimeout, ballsTimeoutMs))
endfunction


function ballsLoad()
    ballsJSON = sessionStorageGet('balls')
    ballsObj = if(ballsJSON != null, schemaValidate(ballsTypes, 'Balls', jsonParse(ballsJSON)))
    jumpif (!vReset && ballsObj != null) ballsDone
        balls = arrayNew()
        ballsObj = objectNew('balls', balls)
        ixColor = 0
        colorLoop:
            ballColor = arrayGet(ballColors, ixColor % arrayLength(ballColors))
            ballSizeDelta = if(ballSizeCount > 1, (ballSizeMax - ballSizeMin) / (ballSizeCount - 1), 0)
            ballSize = ballSizeMin
            sizeLoop:
                xMin = borderSize + 0.5 * ballSize
                xMax = width - borderSize - 0.5 * ballSize
                yMin = borderSize + 0.5 * ballSize
                yMax = height - borderSize - 0.5 * ballSize
                ball = objectNew( \
                    'x', mathRound(xMin + mathRandom() * (xMax - xMin), 0), \
                    'y', mathRound(yMin + mathRandom() * (yMax - yMin), 0), \
                    'dx', if(mathRound(10 * mathRandom(), 0) % 2, 1, -1) * (ballsTimeoutMs / 1000) * ballsSpeedX, \
                    'dy', if(mathRound(10 * mathRandom(), 0) % 2, 1, -1) * (ballsTimeoutMs / 1000) * ballsSpeedY, \
                    'xMin', xMin, \
                    'xMax', xMax, \
                    'yMin', yMin, \
                    'yMax', yMax, \
                    'color', ballColor, \
                    'size', ballSize \
                )
                arrayPush(balls, ball)
                ballSize = ballSize + ballSizeDelta
            jumpif (ballSize <= ballSizeMax) sizeLoop
            ixColor = ixColor + 1
        jumpif (ixColor < ballColorCount) colorLoop

        sessionStorageSet('balls', jsonStringify(schemaValidate(ballsTypes, 'Balls', ballsObj)))
    ballsDone:
    return ballsObj
endfunction


function ballsDraw()
    ballsObj = ballsLoad()
    balls = objectGet(ballsObj, 'balls')

    markdownPrint('# Balls', '', '[Play](#var.vPlay=1&var.vReset=0) | [Reset](#var.vReset=1)', '')
    setDocumentTitle('Balls')

    setDrawingSize(width, height)
    drawStyle(borderColor, borderSize)
    drawRect(0.5 * borderSize, 0.5 * borderSize, width - borderSize, height - borderSize)
    ixBall = 0
    ballLoop:
        ball = arrayGet(balls, ixBall)
        drawStyle(null, 0, objectGet(ball, 'color'))
        drawCircle(objectGet(ball, 'x'), objectGet(ball, 'y'), 0.5 * objectGet(ball, 'size'))
        ixBall = ixBall + 1
    jumpif (ixBall < arrayLength(balls)) ballLoop
endfunction


function ballsTimeout()
    ballsObj = ballsLoad()
    balls = objectGet(ballsObj, 'balls')

    ixBall = 0
    ballLoop:
        ball = arrayGet(balls, ixBall)

        dx = objectGet(ball, 'dx')
        x = objectGet(ball, 'x') + dx
        xMin = objectGet(ball, 'xMin')
        xMax = objectGet(ball, 'xMax')
        dx = if(x >= xMin && x <= xMax, dx, -dx)
        x = if(x >= xMin, x, xMin + (xMin - x))
        x = if(x <= xMax, x, xMax - (x - xMax))

        objectSet(ball, 'x', x)
        objectSet(ball, 'dx', dx)

        dy = objectGet(ball, 'dy')
        y = objectGet(ball, 'y') + dy
        yMin = objectGet(ball, 'yMin')
        yMax = objectGet(ball, 'yMax')
        dy = if(y >= yMin && y <= yMax, dy, -dy)
        y = if(y >= yMin, y, yMin + (yMin - y))
        y = if(y <= yMax, y, yMax - (y - yMax))

        objectSet(ball, 'y', y)
        objectSet(ball, 'dy', dy)

        ixBall = ixBall + 1
    jumpif (ixBall < arrayLength(balls)) ballLoop

    sessionStorageSet('balls', jsonStringify(schemaValidate(ballsTypes, 'Balls', ballsObj)))

    documentReset()
    ballsDraw()
    if(!vReset && vPlay, setWindowTimeout(ballsTimeout, ballsTimeoutMs))
endfunction


ballsMain()
~~~
