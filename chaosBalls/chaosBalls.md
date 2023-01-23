~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


# Chaos Balls application main entry point
async function chaosBallsMain()
    # Display Chaos Ball model documentation?
    jumpif (!vDoc) docDone
        setDocumentTitle('Chaos Balls JSON Format')
        markdownPrint('[Home](#url=README.md)', '')
        elementModelRender(schemaElements(chaosBallsTypes, 'ChaosBalls'))
        return
    docDone:

    # Set the title
    setDocumentTitle('Chaos Balls')

    # Load the session
    session = chaosBallsGetSession()
    args = chaosBallsArgs()

    # Set the Chaos Balls model, if requested
    url = objectGet(args, 'url')
    jumpif (url == null) fetchDone
        # Set the default model?
        jumpif (url != '') modelFetch
            model = chaosBallsDefaultModel
            jump modelDone
        modelFetch:
            # Fetch and validate the Chaos Balls JSON model
            modelJSON = fetch(url)
            model = if(modelJSON != null, schemaValidate(chaosBallsTypes, 'ChaosBalls', modelJSON))
            jumpif (model != null) modelOK
                markdownPrint('Error: Could not fetch/validate Chaos Balls model, "' + url + '"')
                return
            modelOK:
        modelDone:

        # Create a new, random session from the model (unless its the same as the session's model)
        jumpif (jsonStringify(model) == jsonStringify(objectGet(session, 'model'))) fetchDone
        session = chaosBallsNewSession(model)
        chaosBallsSetSession(session)
    fetchDone:

    # Render the application
    chaosBallsRender(session, args)

    # Set the window resize handler
    setWindowResize(chaosBallsResize)
endfunction


# Render the Chaos Balls application
function chaosBallsRender(session, args)
    # Render the menu
    elementModelRender(arrayNew( \
        if(!objectGet(args, 'fullScreen'), objectNew('html', 'p', 'elem', arrayNew( \
            objectNew('html', 'b', 'elem', objectNew('text', "Chaos Balls")), \
            objectNew('html', 'br'), \
            chaosBallsMenuElements(args) \
        ))), \
        objectNew('html', 'div', 'attr', objectNew('id', chaosBallsDocumentResetID, 'style', 'display: none;')) \
    ))

    # Render the balls
    chaosBallsDraw(session, args)

    # Set the timeout handler
    chaosBallsSetTimeout(args)
endfunction


# Helper to set the timeout handler
function chaosBallsSetTimeout(args, startTime, endTime)
    ellapsedMs = if(startTime != null && endTime != null, endTime - startTime, 0)
    periodMs = mathMax(0, 1000 / arrayGet(chaosBallsRates, objectGet(args, 'rate')) - ellapsedMs)
    if(objectGet(args, 'play'), setWindowTimeout(chaosBallsTimeout, periodMs))
endfunction


# Chaos Balls window resize handler
function chaosBallsResize()
    session = chaosBallsGetSession()
    args = chaosBallsArgs()
    chaosBallsRender(session, args)
endfunction


# Chaos Balls timeout handler
function chaosBallsTimeout()
    startTime = datetimeNow()
    session = chaosBallsGetSession()
    args = chaosBallsArgs()

    # Move the session balls
    chaosBallsMove(session, args)

    # Render the balls
    setDocumentReset(chaosBallsDocumentResetID)
    chaosBallsDraw(session, args)

    # Set the timeout handler
    endTime = datetimeNow()
    chaosBallsSetTimeout(args, startTime, endTime)
endfunction


# Create the Chaos Balls application variable-arguments object
function chaosBallsArgs(raw)
    args = objectNew()
    objectSet(args, 'fullScreen', if(vFullScreen != null, if(vFullScreen, 1, 0), if(!raw, 0)))
    objectSet(args, 'play', if(vPlay != null, if(vPlay, 1, 0), if(!raw, 1)))
    objectSet(args, 'rate', if(vRate != null, mathMax(0, mathMin(arrayLength(chaosBallsRates) - 1, vRate)), if(!raw, 2)))
    objectSet(args, 'url', vURL)
    return args
endfunction


# Create the Chaos Balls application menu element model
function chaosBallsMenuElements(args)
    # Menu separators
    nbsp = stringFromCharCode(160)
    linkSeparator = objectNew('text', ' ')
    linkSection = objectNew('text', nbsp + '| ')

    # Create the menu element model
    argsRaw = chaosBallsArgs(true)
    play = objectGet(args, 'play')
    rate = objectGet(args, 'rate')
    rateDown = if(rate > 0, rate - 1)
    rateUp= if(rate < arrayLength(chaosBallsRates) - 1, rate + 1)
    return arrayNew( \
        if(play, chaosBallsLinkElements('Pause', chaosBallsURL(argsRaw, objectNew('play', 0)))), \
        if(!play, chaosBallsLinkElements('Play', chaosBallsURL(argsRaw, objectNew('play', 1)))), \
        linkSection, \
        chaosBallsButtonElements('Step', chaosBallsStep), \
        linkSeparator, \
        chaosBallsButtonElements('Reset', chaosBallsReset), \
        linkSection, \
        chaosBallsLinkElements('<<', if(rateDown != null, chaosBallsURL(argsRaw, objectNew('rate', rateDown)))), \
        objectNew('text', nbsp + arrayGet(chaosBallsRates, rate) + nbsp + 'Hz' + nbsp), \
        chaosBallsLinkElements('>>', if(rateUp != null, chaosBallsURL(argsRaw, objectNew('rate', rateUp)))), \
        linkSection, \
        chaosBallsLinkElements('Full', chaosBallsURL(argsRaw, objectNew('fullScreen', true))), \
        linkSection, \
        chaosBallsLinkElements('About', '#url=README.md') \
    )
endfunction


# The Chaos Balls menu frame rates, in Hz
chaosBallsRates = arrayNew(10, 15, 20, 30, 45, 60)

# The Chaos Balls document reset ID
chaosBallsDocumentResetID = 'chaosBallsMenu'


# Helper to create an application URL
function chaosBallsURL(argsRaw, args)
    # URL arguments
    fullScreen = objectGet(args, 'fullScreen')
    play = objectGet(args, 'play')
    rate = objectGet(args, 'rate')
    url = objectGet(args, 'url')

    # Variable arguments
    fullScreen = if(fullScreen != null, fullScreen, objectGet(argsRaw, 'fullScreen'))
    play = if(play != null, play, objectGet(argsRaw, 'play'))
    rate = if(rate != null, rate, objectGet(argsRaw, 'rate'))
    url = if(url != null, url, objectGet(argsRaw, 'url'))

    # Create the URL
    parts = arrayNew()
    if(fullScreen, arrayPush(parts, 'var.vFullScreen=1'))
    if(play != null, arrayPush(parts, 'var.vPlay=' + play))
    if(rate != null, arrayPush(parts, 'var.vRate=' + rate))
    if(vURL != null, arrayPush(parts, "var.vURL='" + encodeURIComponent(vURL) + "'"))
    return if(arrayLength(parts), '#' + arrayJoin(parts, '&'), '#var=')
endfunction


# Helper to create a link element model
function chaosBallsLinkElements(text, url)
    return if(url != null, \
        objectNew( \
            'html', 'a', \
            'attr', objectNew('href', documentURL(url)), \
            'elem', objectNew('text', text) \
        ), \
        objectNew( \
            'html', 'span', \
            'attr', objectNew('style', 'user-select: none;'), \
            'elem', objectNew('text', text) \
        ))
endfunction


# Helper to create a link-button element model
function chaosBallsButtonElements(text, callback)
    return objectNew( \
        'html', 'a', \
        'attr', objectNew('style', 'cursor: pointer; user-select: none;'), \
        'elem', objectNew('text', text), \
        'callback', objectNew('click', callback) \
    )
endfunction


# Chaos Balls step click handler
function chaosBallsStep()
    session = chaosBallsGetSession()
    args = chaosBallsArgs()
    chaosBallsMove(session, args)
    if(!objectGet(args, 'play'), chaosBallsRender(session, args))
    if(objectGet(args, 'play'), setWindowLocation(chaosBallsURL(chaosBallsArgs(true), objectNew('play', 0))))
endfunction


# Chaos Balls reset click handler
function chaosBallsReset()
    session = chaosBallsGetSession()
    session = chaosBallsNewSession(objectGet(session, 'model'))
    args = chaosBallsArgs()
    chaosBallsSetSession(session)
    chaosBallsRender(session, args)
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


# Draw the Chaos Balls
function chaosBallsDraw(session, args)
    # Compute the width/height
    width = chaosBallsWidth()
    height = chaosBallsHeight(args)
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


# Get the Chaos Balls drawing width
function chaosBallsWidth()
    return getWindowWidth() - 3 * getDocumentFontSize()
endfunction


# Get the Chaos Balls drawing height
function chaosBallsHeight(args)
    return getWindowHeight(args) - if(objectGet(args, 'fullScreen'), 3, 6) * getDocumentFontSize()
endfunction


# Move the Chaos Balls
function chaosBallsMove(session, args)
    # Compute the width/height
    width = chaosBallsWidth()
    height = chaosBallsHeight(args)
    widthHeight = mathMin(width, height)

    # Move each ball
    ixBall = 0
    balls = objectGet(session, 'balls')
    period = 1 / arrayGet(chaosBallsRates, objectGet(args, 'rate'))
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
