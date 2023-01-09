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

    # Display Chaos Ball model documentation?
    jumpif (!vDoc) docDone
        setDocumentTitle('Chaos Balls Specification')
        elementModelRender(schemaElements(chaosBallsTypes, 'ChaosBalls'))
        return
    docDone:

    # Fetch the Chaos Balls model, if requested
    jumpif (vURL == null) fetchDone
        modelJSON = fetch(vURL)
        model = if(modelJSON != null, schemaValidate(chaosBallsTypes, 'ChaosBalls', modelJSON))
        jumpif (model != null) fetchOK
            markdownPrint('Error: Could not fetch/validate Chaos Balls model, "' + vURL + '"')
            return
        fetchOK:

        # Same as session model? If so, don't reset...
        session = chaosBallsGetSession()
        jumpif (session == null || jsonStringify(objectGet(session, 'model')) == jsonStringify(model)) fetchDone

        # Create the new session
        chaosBallsSetSession(chaosBallsNewSession(model))
    fetchDone:

    # Render the Chaos Balls
    chaosBallsResize()

    # Set the window resize handler
    setWindowResize(chaosBallsResize)
endfunction


# Chaos Balls window resize handler
function chaosBallsResize()
    chaosBallsTimeout(true)
endfunction


# Chaos Balls animation timeout handler
function chaosBallsTimeout(noMove)
    # Get the session state
    session = chaosBallsGetSession()

    # Render the menu (unless in full screen mode)
    if(!vFullScreen, chaosBallsMenu())

    # Move the session balls (if necessary)
    period = 0.05
    if(!noMove, chaosBallsMove(session, period))

    # Render the balls
    documentReset()
    chaosBallsRender(session)

    # Start the timer (unless paused)
    if(!vPause, setWindowTimeout(chaosBallsTimeout, period * 1000))
endfunction


# Render the menu
function chaosBallsMenu()
    items = arrayNew()

    if(!vPause, arrayPush(items, '[Pause](#var.vPause=1)'))
    if(vPause, arrayPush(items, '[Play](#var=)'))
    if(vPause, arrayPush(items, '[Step](#var=)'))
    arrayPush(items, '[Reset](#var=)')
    arrayPush(items, '[Default](#var=)')
    arrayPush(items, '[<<](#var=) 22 Hz [>>](#var=)')
    arrayPush(items, '[Full](#var.vFullScreen=1)')
    arrayPush(items, '[About](#url=README.md)')

    # Render the menu items
    markdownPrint(arrayJoin(items, ' | '), '')
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
    sessionJSON = sessionStorageGet('chaosBalls')
    session = if(sessionJSON != null, schemaValidate(chaosBallsTypes, 'ChaosBallsSession', jsonParse(sessionJSON)))

    # If there is no session, create a default session
    jumpif (session != null) sessionDone
        session = chaosBallsNewSession(chaosBallsDefaultModel)
        sessionStorageSet('chaosBalls', jsonStringify(session))
    sessionDone:

    return session
endfunction


# Set the Chaos= Balls session object
function chaosBallsSetSession(session)
    sessionStorageSet('chaosBalls', jsonStringify(session))
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
        dx = dxParam * period * widthHeight
        dyParam = objectGet(ball, 'dy')
        dy = dyParam * period * widthHeight

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
    chaosBallsSetSession(session)
endfunction


# The Chaos Balls model
chaosBallsTypes = schemaParse( \
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
    '    # The ball delta-x, as a ratio of the width/height', \
    '    float dx', \
    '', \
    '    # The ball delta-y, as a ratio of the width/height', \
    '    float dy' \
)


# The default Chaos Balls configuration
chaosBallsDefaultModel = schemaValidate(chaosBallsTypes, 'ChaosBalls', objectNew( \
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
