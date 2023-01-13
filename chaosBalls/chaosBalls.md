~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


#
# Chaos Balls - configurable chaos
#


# Chaos Balls application main entry point
async function chaosBallsMain()
    # Display Chaos Ball model documentation?
    jumpif (!vDoc) docDone
        setDocumentTitle('Chaos Balls JSON Format')
        markdownPrint('[Home](#url=README.md)', '')
        elementModelRender(schemaElements(chaosBallsTypes, 'ChaosBalls'))
        return
    docDone:

    # Set the default title
    setDocumentTitle('Chaos Balls')

    # Set the Chaos Balls model, if requested
    jumpif (vURL == null) fetchDone
        # Set the default model?
        jumpif (vURL != '') modelFetch
            model = chaosBallsDefaultModel
            jump modelDone
        modelFetch:
            # Fetch and validate the Chaos Balls JSON model
            modelJSON = fetch(vURL)
            model = if(modelJSON != null, schemaValidate(chaosBallsTypes, 'ChaosBalls', modelJSON))
            jumpif (model != null) modelOK
                markdownPrint('Error: Could not fetch/validate Chaos Balls model, "' + vURL + '"')
                return
            modelOK:
        modelDone:

        # Create a new, random session from the model (unless its the same as the session's model)
        session = chaosBallsGetSession()
        jumpif (jsonStringify(model) == jsonStringify(objectGet(session, 'model'))) fetchDone
        chaosBallsSetSession(chaosBallsNewSession(model))
    fetchDone:

    # Render the balls
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
    # Get the session state
    session = chaosBallsGetSession()

    # Move the session balls
    chaosBallsMove(session, chaosBallsGetPeriod())

    # Render the balls
    chaosBallsResize()

    # Pause playing, if necessary
    if(!vPause, setWindowLocation(chaosBallsMenuURL(1)))
endfunction


# Menu reset button on-click handler
function chaosBallsReset()
    # Get the session state
    session = chaosBallsGetSession()

    # Create a new, random session from the current session model
    session = chaosBallsNewSession(objectGet(session, 'model'))
    chaosBallsSetSession(session)

    # Render the balls
    chaosBallsResize()
endfunction


# Render the menu
function chaosBallsMenu(noMenu)
    # Create the menu elements
    elements = arrayNew()

    # Add the menu elements
    jumpif (noMenu || vFullScreen) menuDone
        # Add the application title
        items = arrayNew()
        arrayPush(elements, objectNew('html', 'p', 'elem', arrayNew( \
            objectNew('html', 'b', 'elem', objectNew('text', 'Chaos Balls')), \
            objectNew('html', 'br'), \
            items \
        )))

        # Add the menu items
        nbsp = stringFromCharCode(160)
        rateIndex = chaosBallsGetRate()
        rateDown = if(rateIndex > 0, rateIndex - 1, null)
        rateUp = if(rateIndex < arrayLength(chaosBallsMenuRates) - 1, rateIndex + 1, null)
        if(!vPause, chaosBallsMenuLink(items, 'Pause', chaosBallsMenuURL(1)))
        if(vPause, chaosBallsMenuLink(items, 'Play', chaosBallsMenuURL(0)))
        chaosBallsMenuButton(items, 'Step', chaosBallsStep)
        chaosBallsMenuButton(items, 'Reset', chaosBallsReset)
        chaosBallsMenuLink(items, '<<', if(rateDown != null, chaosBallsMenuURL(null, rateDown)))
        chaosBallsMenuLink(items, arrayGet(chaosBallsMenuRates, rateIndex) + nbsp + 'Hz', null, true)
        chaosBallsMenuLink(items, '>>', if(rateUp != null, chaosBallsMenuURL(null, rateUp)), true)
        chaosBallsMenuLink(items, 'Full', chaosBallsMenuURL(0, null, true))
        chaosBallsMenuLink(items, 'About', '#url=README.md')
    menuDone:

    # Add the document reset ID
    arrayPush(elements, objectNew('html', 'div', 'attr', objectNew('id', chaosBallsMenuResetID, 'style', 'display=none')))

    # Render the menu elements
    elementModelRender(elements)
endfunction


# Helper for creating menu link URLs
function chaosBallsMenuURL(pause, rate, fullScreen)
    # Compute the URL argument state
    pause = if(pause != null, pause, vPause)
    rate = if(rate != null, rate, vRate)

    # Create the URL
    parts = arrayNew()
    if(vURL != null, arrayPush(parts, "var.vURL='" + encodeURIComponent(vURL) + "'"))
    if(pause != null, arrayPush(parts, 'var.vPause=' + pause))
    if(rate != null, arrayPush(parts, 'var.vRate=' + rate))
    if(fullScreen, arrayPush(parts, 'var.vFullScreen=1'))
    return '#' + arrayJoin(parts, '&')
endfunction


# Helper for creating menu link elements
function chaosBallsMenuLink(items, text, url, noSeparator)
    nbsp = stringFromCharCode(160)
    arrayPush(items, arrayNew( \
        if(arrayLength(items) > 0, objectNew('text', if(noSeparator, ' ', nbsp + '| ')), null), \
        if(url == null, objectNew('text', text), \
            objectNew('html', 'a', 'attr', objectNew('href', documentURL(url)), 'elem', objectNew('text', text))) \
    ))
endfunction


# Helper for creating menu button elements
function chaosBallsMenuButton(items, text, callback, noSeparator)
    nbsp = stringFromCharCode(160)
    arrayPush(items, arrayNew( \
        if(arrayLength(items) > 0, objectNew('text', if(noSeparator, nbsp, nbsp + '|' + nbsp)), null), \
        objectNew( \
            'html', 'a', \
            'attr', objectNew('style', 'cursor: pointer; user-select: none;'), \
            'elem', objectNew('text', text), \
            'callback', objectNew('click', callback) \
        ) \
    ))
endfunction


# The below-menu document reset ID
chaosBallsMenuResetID = 'chaosBallsMenu'


# List of available menu frame rates, in Hz
chaosBallsMenuRates = arrayNew(10, 15, 20, 30, 45, 60)
chaosBallsMenuRateDefault = 2


# Get the current frame rate, in Hz
function chaosBallsGetRate()
    rateMax = arrayLength(chaosBallsMenuRates) - 1
    return if(vRate != null, mathMax(0, mathMin(rateMax, vRate)), chaosBallsMenuRateDefault)
endfunction


# Get the current frame rate period, in seconds
function chaosBallsGetPeriod()
    return 1 / arrayGet(chaosBallsMenuRates, chaosBallsGetRate())
endfunction


# Get the Chaos Balls drawing width
function chaosBallsWidth()
    return getWindowWidth() - 3 * getTextHeight()
endfunction


# Get the Chaos Balls drawing height
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
            xMin = 0.5 * size
            xMax = 1 - xMin
            yMin = 0.5 * size
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

    # Render the background
    model = objectGet(session, 'model')
    setDrawingSize(width, height)
    drawStyle('none', 0, objectGet(model, 'backgroundColor'))
    drawRect(0, 0, width, height)

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
        xMin = 0.5 * size
        xMax = width - xMin
        yMin = 0.5 * size
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
    '    ChaosBallsSessionBall[len > 0] balls', \
    '', \
    '', \
    '# The Chaos Balls session ball model', \
    'struct ChaosBallsSessionBall', \
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


# The default Chaos Balls model
chaosBallsDefaultModel = schemaValidate(chaosBallsTypes, 'ChaosBalls', objectNew( \
    'backgroundColor', '#ffffff', \
    'groups', arrayNew( \
        objectNew('count', 10, 'color', '#0000ff40', 'minSize', 0.3, 'maxSize', 0.4, 'minSpeed', 0.1, 'maxSpeed', 0.15), \
        objectNew('count', 20, 'color', '#00ff0040', 'minSize', 0.2, 'maxSize', 0.3, 'minSpeed', 0.15, 'maxSpeed', 0.2), \
        objectNew('count', 30, 'color', '#ff000040', 'minSize', 0.1, 'maxSize', 0.2, 'minSpeed', 0.2, 'maxSpeed', 0.25) \
    ) \
))


# Call the main entry point
chaosBallsMain()
~~~