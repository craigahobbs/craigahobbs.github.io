~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


#
# Chaos Balls - configurable chaos
#


# Chaos Balls application main entry point
async function chaosBallsMain()
    # Set the default title
    setDocumentTitle('Chaos Balls')

    # Execute the command - or render the balls
    if(vURL != null, chaosBallsFetch(vURL), \
        if(vDoc, chaosBallsDoc(), \
        chaosBallsResize()))

    # Set the window resize handler
    setWindowResize(chaosBallsResize)
endfunction


# Fetch a Chaos Balls model
async function chaosBallsFetch(url)
    # Fetch and validate the model
    modelJSON = fetch(url)
    model = if(modelJSON != null, schemaValidate(ballsTypes, 'ChaosBalls', modelJSON))
    jumpif (model != null) sessionOK
        markdownPrint('Error: Could not fetch/validate Chaos Balls model, "' + url + '"')
        if(modelJSON != null, markdownPrint('', '~~~', jsonStringify(modelJSON, 4), '~~~'))
        return
    sessionOK:

    # Create the session state
    session = chaosBallsNewSession(model)
    sessionStorageSet(chaosBallsSessionKey, jsonStringify(session))

    # Start the animation
    setWindowLocation('#var=')
endfunction


# Render the Chaos Balls model documentation
function chaosBallsDoc()
    setDocumentTitle('Chaos Balls Specification')
    elementModelRender(schemaElements(ballsTypes, 'ChaosBalls'))
endfunction


# Chaos Balls window resize handler
function chaosBallsResize()
    chaosBallsTimeout(true)
endfunction


# Chaos Balls animation timeout handler
function chaosBallsTimeout(noMove)
    # Get the session state
    session = chaosBallsGetSession()

    # Move the session balls (if necessary)
    period = 0.05
    if(!noMove, chaosBallsMove(session, period))

    # Render the balls
    documentReset()
    chaosBallsRender(session)

    # Start the timer (unless paused)
    if(!vPause, setWindowTimeout(chaosBallsTimeout, period * 1000))
endfunction


# Chaos Balls width helper
function chaosBallsWidth()
    return getWindowWidth() - 4 * getTextHeight()
endfunction


# Chaos Balls height helper
function chaosBallsHeight()
    return getWindowHeight() - 4 * getTextHeight()
endfunction


# Get the Chaos= Balls session object
function chaosBallsGetSession()
    # Parse and validate the session object
    sessionJSON = sessionStorageGet(chaosBallsSessionKey)
    session = if(sessionJSON != null, schemaValidate(ballsTypes, 'ChaosBallsSession', jsonParse(sessionJSON)))

    # If there is no session, create a default session
    jumpif (session != null) sessionDone
        session = chaosBallsNewSession(chaosBallsDefaultModel)
        sessionStorageSet(chaosBallsSessionKey, jsonStringify(session))
    sessionDone:

    return session
endfunction


# Create a new Chaos Balls session object
function chaosBallsNewSession(model)
    balls = arrayNew()
    session = objectNew('model', model, 'balls', balls)

    # Iterate the ball groups
    ixGroup = 0
    groups = objectGet(model, 'groups')
    borderSize = objectGet(model, 'borderSize')
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
            arrayPush(balls, objectNew('color', groupColor, 'size', size, 'x', x, 'y', y, 'dx', dx, 'dy', dy))

            ixBall = ixBall + 1
        jumpif (ixBall < groupCount) ballLoop

        ixGroup = ixGroup + 1
    jumpif (ixGroup < arrayLength(groups)) groupLoop

    return session
endfunction


# Render the Chaos Balls
function chaosBallsRender(session)
    # Compute the width/height
    width = chaosBallsWidth()
    height = chaosBallsHeight()
    widthHeight = mathMin(width, height)

    # Render the background and border
    model = objectGet(session, 'model')
    borderSize = objectGet(model, 'borderSize') * widthHeight
    setDrawingSize(width, height)
    drawStyle(objectGet(model, 'borderColor'), borderSize, objectGet(model, 'backgroundColor'))
    drawRect(0.5 * borderSize, 0.5 * borderSize, width - borderSize, height - borderSize)

    # Render the balls
    ixBall = 0
    balls = objectGet(session, 'balls')
    ballLoop:
        ball = arrayGet(balls, ixBall)
        drawStyle(null, 0, objectGet(ball, 'color'))
        drawCircle(objectGet(ball, 'x') * width, objectGet(ball, 'y') * height, 0.5 * objectGet(ball, 'size') * widthHeight)
        ixBall = ixBall + 1
    jumpif (ixBall < arrayLength(balls)) ballLoop
endfunction


# Move the Chaos Balls
function chaosBallsMove(session, period)
    # Compute the width/height
    width = chaosBallsWidth()
    height = chaosBallsHeight()
    widthHeight = mathMin(width, height)

    # Compute the border size
    model = objectGet(session, 'model')
    borderSize = objectGet(model, 'borderSize') * widthHeight

    # Move each ball
    ixBall = 0
    balls = objectGet(session, 'balls')
    ballLoop:
        ball = arrayGet(balls, ixBall)

        # Compute the ball size, position, and direction
        size = objectGet(ball, 'size') * widthHeight
        x = objectGet(ball, 'x') * width
        y = objectGet(ball, 'y') * height
        dxParam = objectGet(ball, 'dx')
        dx = dxParam * period * width
        dyParam = objectGet(ball, 'dy')
        dy = dyParam * period * height

        # Compute the X and Y extents for this ball
        xMin = borderSize + 0.5 * size
        xMax = width - xMin
        yMin = borderSize + 0.5 * size
        yMax = height - yMin

        # Compute the new X coordinate - adjust if out of bounds
        x = x + dx
        dxParam = if(x < xMin || x > xMax, -dxParam, dxParam)
        x = if(x < xMin, xMin + (xMin - x), if(x > xMax, xMax - (x - xMax), x))

        # Compute the new Y coordinate - adjust if out of bounds
        y = y + dy
        dyParam = if(y < yMin || y > yMax, -dyParam, dyParam)
        y = if(y < yMin, yMin + (yMin - y), if(y > yMax, yMax - (y - yMax), y))

        # Update the ball position and direction
        objectSet(ball, 'x', x / width)
        objectSet(ball, 'y', y / height)
        objectSet(ball, 'dx', dxParam)
        objectSet(ball, 'dy', dyParam)

        ixBall = ixBall + 1
    jumpif (ixBall < arrayLength(balls)) ballLoop

    # Update the session storage
    sessionStorageSet(chaosBallsSessionKey, jsonStringify(session))
endfunction


# The Chaos Balls model
ballsTypes = schemaParse( \
    '# The Chaos Balls model', \
    'struct ChaosBalls', \
    '', \
    '    # The background color', \
    '    string(len > 0) backgroundColor', \
    '', \
    '    # The border color', \
    '    string(len > 0) borderColor', \
    '', \
    '    # The border size, as a ratio of width/height', \
    '    float(>= 0, <= 0.2) borderSize', \
    '', \
    '    # The ball groups', \
    '    ChaosBallsGroup[len > 0] groups', \
    '', \
    '', \
    '# A ball group', \
    'struct ChaosBallsGroup', \
    '', \
    '    # The ball count', \
    '    int(>= 1) count', \
    '', \
    '    # The ball color', \
    '    string(len > 0) color', \
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
    '', \
    '# The Chaos Balls session model', \
    'struct ChaosBallsSession', \
    '', \
    '    # The Chaos Balls model', \
    '    ChaosBalls model', \
    '', \
    '    # The runtime balls', \
    '    ChaosBallsBall[len > 0] balls', \
    '', \
    '', \
    '# The Chaos Balls session ball model', \
    'struct ChaosBallsBall', \
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
    '    float dy' \
)


# The Chaos Ball session storage keys
chaosBallsSessionKey = 'chaosBalls'


# The default Chaos Balls configuration
chaosBallsDefaultModel = schemaValidate(ballsTypes, 'ChaosBalls', objectNew( \
    'backgroundColor', 'white', \
    'borderColor', 'blue', \
    'borderSize', 0.05, \
    'groups', arrayNew( \
        objectNew('count', 10, 'color', '#0000ff40', 'minSize', 0.3, 'maxSize', 0.4, 'minSpeed', 0.1, 'maxSpeed', 0.15), \
        objectNew('count', 20, 'color', '#00ff0040', 'minSize', 0.2, 'maxSize', 0.3, 'minSpeed', 0.15, 'maxSpeed', 0.2), \
        objectNew('count', 30, 'color', '#ff000040', 'minSize', 0.1, 'maxSize', 0.2, 'minSpeed', 0.2, 'maxSpeed', 0.25) \
    ) \
))


# Call the main entry point
chaosBallsMain()
~~~
