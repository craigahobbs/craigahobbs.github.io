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
        markdownPrint('[Home](#url=README.md)', '')
        elementModelRender(schemaElements(chaosBallsTypes, 'ChaosBalls'))
        return
    docDone:

    # Set the Chaos Balls model, if requested
    jumpif (vURL == null) fetchDone
        # Default model?
        jumpif (vURL == '') modelDefault
            # Fetch and validate the Chaos Balls JSON model
            modelJSON = fetch(vURL)
            model = if(modelJSON != null, schemaValidate(chaosBallsTypes, 'ChaosBalls', modelJSON))
            jumpif (model != null) modelDone

            # Report the fetch or validation error
            markdownPrint('Error: Could not fetch/validate Chaos Balls model, "' + vURL + '"')
            return
        modelDefault:
            # Set the default model
            model = chaosBallsDefaultModel
        modelDone:

        # Same as session model? If so, don't reset...
        session = chaosBallsGetSession()
        jumpif (jsonStringify(objectGet(session, 'model')) == jsonStringify(model)) fetchDone

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
function chaosBallsTimeout(isResize)
    # Get the session state
    startTime = datetimeNow()
    session = chaosBallsGetSession()

    # Render the menu
    chaosBallsMenu(!isResize)
    if(!isResize, setDocumentReset(chaosBallsMenuResetID))

    # Move the session balls
    period = chaosBallsGetPeriod()
    if(!isResize, chaosBallsMove(session, period))

    # Render the balls
    chaosBallsRender(session)

    # Start the timer (unless paused)
    endTime = datetimeNow()
    ellapsedMs = endTime - startTime
    if(!vPause, setWindowTimeout(chaosBallsTimeout, mathMax(0, period * 1000 - ellapsedMs)))
endfunction


# Menu step button on-click handler
function chaosBallsStep()
    session = chaosBallsGetSession()
    chaosBallsMove(session, chaosBallsGetPeriod())
    chaosBallsResize()
endfunction


# Menu reset button on-click handler
function chaosBallsReset()
    session = chaosBallsGetSession()
    session = chaosBallsNewSession(objectGet(session, 'model'))
    chaosBallsSetSession(session)
    chaosBallsResize()
endfunction


# Render the menu
function chaosBallsMenu(noMenu)
    # Create the menu elements
    items = arrayNew()
    elements = arrayNew()
    if(!noMenu && !vFullScreen, arrayPush(elements, objectNew('html', 'p', 'elem', arrayNew( \
        objectNew('html', 'b', 'elem', objectNew('text', 'Chaos Balls')), \
        objectNew('html', 'br'), \
        items \
    ))))
    arrayPush(elements, objectNew('html', 'div', 'attr', objectNew('id', chaosBallsMenuResetID, 'style', 'display=none')))

    # Get the frame rate
    rateIndex = chaosBallsGetRate()
    rateArg = if(rateIndex != chaosBallsMenuRateDefault, '&var.vRate=' + rateIndex, '')

    # Paused?
    jumpif (vPause) menuPaused
        chaosBallsMenuLink(items, 'Pause', '#var.vPause=1' + rateArg)
        jump menuDone
    menuPaused:
        nbsp = stringFromCharCode(160)
        rateDown = if(rateIndex > 0, rateIndex - 1, null)
        rateUp = if(rateIndex < arrayLength(chaosBallsMenuRates) - 1, rateIndex + 1, null)
        chaosBallsMenuLink(items, 'Play', '#var.vPause=0' + rateArg)
        chaosBallsMenuLink(items, 'Step', chaosBallsStep)
        chaosBallsMenuLink(items, 'Reset', chaosBallsReset)
        chaosBallsMenuLink(items, '<<', if(rateDown != null, '#var.vPause=1&var.vRate=' + rateDown))
        chaosBallsMenuLink(items, arrayGet(chaosBallsMenuRates, rateIndex) + nbsp + 'Hz', null, true)
        chaosBallsMenuLink(items, '>>', if(rateUp != null, '#var.vPause=1&var.vRate=' + rateUp), true)
        chaosBallsMenuLink(items, 'Full', '#var.vFullScreen=1' + rateArg)
        chaosBallsMenuLink(items, 'About', '#url=README.md')
    menuDone:

    # Render the menu items
    elementModelRender(elements)
endfunction


# Helper for adding menu links
function chaosBallsMenuLink(items, text, url, noSeparator)
    nbsp = stringFromCharCode(160)
    arrayPush(items, arrayNew( \
        if(arrayLength(items) > 0, objectNew('text', if(noSeparator, nbsp, nbsp + '|' + nbsp)), null), \
        if(url != null, \
            if(stringLength(url) != null, \
                objectNew( \
                    'html', 'a', \
                    'attr', objectNew('href', documentURL(url)), \
                    'elem', objectNew('text', text) \
                ), \
                objectNew( \
                    'html', 'a', \
                    'attr', objectNew('style', 'cursor: pointer; user-select: none;'), \
                    'elem', objectNew('text', text), \
                    'callback', objectNew('click', url) \
                ) \
            ), \
            objectNew('text', text) \
        ) \
    ))
endfunction


# The below-menu document reset ID
chaosBallsMenuResetID = 'chaosBallsMenu'


# List of available menu frame rates, in Hz
chaosBallsMenuRates = arrayNew(10, 15, 20, 30, 45, 60)
chaosBallsMenuRateDefault = 2


# Get the current rate
function chaosBallsGetRate()
    rateMax = arrayLength(chaosBallsMenuRates) - 1
    return if(vRate != null, mathMax(0, mathMin(rateMax, vRate)), chaosBallsMenuRateDefault)
endfunction


# Get the current period, in seconds
function chaosBallsGetPeriod()
    return 1 / arrayGet(chaosBallsMenuRates, chaosBallsGetRate())
endfunction


# Chaos Balls width helper
function chaosBallsWidth()
    return getWindowWidth() - 3 * getTextHeight()
endfunction


# Chaos Balls height helper
function chaosBallsHeight()
    return getWindowHeight() - if(vFullScreen, 3, 6) * getTextHeight()
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
