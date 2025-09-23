~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include <args.bare>
include <forms.bare>


# Chaos Balls application main entry point
async function chaosBallsMain():
    # Parse arguments
    args = argsParse(chaosBallsArguments)
    objectSet(args, 'rate', mathMax(0, mathMin(arrayLength(chaosBallsRates) - 1, objectGet(args, 'rate'))))

    # Display Chaos Ball model documentation?
    if objectGet(args, 'doc'):
        documentSetTitle('Chaos Balls JSON Format')
        markdownPrint('[Home](#url=README.md)', '')
        elementModelRender(schemaElements(chaosBallsTypes, 'ChaosBalls'))
        return
    endif

    # Set the title
    documentSetTitle('Chaos Balls')

    # Load the session
    session = chaosBallsGetSession()

    # Set the Chaos Balls model, if requested
    url = objectGet(args, 'url')
    if url != null:
        # Set the default model?
        if url == '':
            model = chaosBallsDefaultModel
        else:
            # Fetch and validate the Chaos Balls JSON model
            modelJSON = jsonParse(systemFetch(url))
            model = if(modelJSON != null, schemaValidate(chaosBallsTypes, 'ChaosBalls', modelJSON))
            if model == null:
                markdownPrint('Error: Could not fetch/validate Chaos Balls model, "' + url + '"')
                return
            endif
        endif

        # Create a new, random session from the model (unless its the same as the session's model)
        if jsonStringify(model) != jsonStringify(objectGet(session, 'model')):
            session = chaosBallsNewSession(model)
            chaosBallsSetSession(session)
        endif
    endif

    # Render the application
    chaosBallsRender(session, args)

    # Set the keydown callback
    documentSetKeyDown(systemPartial(chaosBallsKeyDown, args))

    # Set the window resize handler
    windowSetResize(systemPartial(chaosBallsRender, session, args))
endfunction


# The Chaos Balls application arguments
chaosBallsArguments = argsValidate(arrayNew( \
    objectNew('name', 'doc', 'type', 'bool'), \
    objectNew('name', 'fullScreen', 'type', 'bool', 'default', false), \
    objectNew('name', 'play', 'type', 'bool', 'default', true), \
    objectNew('name', 'rate', 'type', 'int', 'default', 3), \
    objectNew('name', 'url', 'global', 'vURL') \
))


# Render the Chaos Balls application
function chaosBallsRender(session, args):
    # Render the menu
    elementModelRender(arrayNew( \
        if(!objectGet(args, 'fullScreen'), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'b', 'elem', objectNew('text', "Chaos Balls")), \
                objectNew('html', 'br'), \
                chaosBallsMenuElements(session, args) \
            )) \
        ), \
        objectNew('html', 'div', 'attr', objectNew('id', chaosBallsDocumentResetID, 'style', 'display: none;')) \
    ))

    # Render the balls
    chaosBallsDraw(session, args)

    # Set the timeout handler
    chaosBallsSetTimeout(session, args)
endfunction


# Helper to set the timeout handler
function chaosBallsSetTimeout(session, args, startTime, endTime):
    ellapsedMs = if(startTime != null && endTime != null, endTime - startTime, 0)
    periodMs = mathMax(0, 1000 / arrayGet(chaosBallsRates, objectGet(args, 'rate')) - ellapsedMs)
    if objectGet(args, 'play'):
        windowSetTimeout(systemPartial(chaosBallsTimeout, session, args), periodMs)
    endif
endfunction


# Chaos Balls timeout handler
function chaosBallsTimeout(session, args):
    startTime = datetimeNow()

    # Move the session balls
    chaosBallsMove(session, args)

    # Render the balls
    documentSetReset(chaosBallsDocumentResetID)
    chaosBallsDraw(session, args)

    # Set the timeout handler
    endTime = datetimeNow()
    chaosBallsSetTimeout(session, args, startTime, endTime)
endfunction


# Chaos Balls document keydown handler
function chaosBallsKeyDown(args, event):
    key = objectGet(event, 'key')

    # Play/Pause
    if key == ' ':
        windowSetLocation(argsURL(chaosBallsArguments, objectNew('play', !objectGet(args, 'play'))))
        return
    endif

    # Re-render the current state
    chaosBallsRender(chaosBallsGetSession(), args)
endfunction


# Create the Chaos Balls application menu element model
function chaosBallsMenuElements(session, args):
    # Menu separators
    nbsp = stringFromCharCode(160)
    linkSeparator = objectNew('text', ' ')
    linkSection = objectNew('text', nbsp + '| ')

    # Create the menu element model
    play = objectGet(args, 'play')
    rate = objectGet(args, 'rate')
    return arrayNew( \
        if(play, formsLinkElements('Pause', argsURL(chaosBallsArguments, objectNew('play', 0)))), \
        if(!play, formsLinkElements('Play', argsURL(chaosBallsArguments, objectNew('play', 1)))), \
        linkSection, \
        formsLinkButtonElements('Step', systemPartial(chaosBallsStep, session, args)), \
        linkSeparator, \
        formsLinkButtonElements('Reset', systemPartial(chaosBallsReset, session, args)), \
        linkSection, \
        formsLinkElements('<<', if(rate > 0, argsURL(chaosBallsArguments, objectNew('rate', rate - 1)))), \
        objectNew('text', nbsp + arrayGet(chaosBallsRates, rate) + nbsp + 'Hz' + nbsp), \
        formsLinkElements('>>', if(rate < arrayLength(chaosBallsRates) - 1, argsURL(chaosBallsArguments, objectNew('rate', rate + 1)))), \
        linkSection, \
        formsLinkElements('Full', argsURL(chaosBallsArguments, objectNew('fullScreen', true))), \
        linkSection, \
        formsLinkElements('About', '#url=README.md') \
    )
endfunction


# The Chaos Balls menu frame rates, in Hz
chaosBallsRates = arrayNew(10, 15, 20, 30, 45, 60)

# The Chaos Balls document reset ID
chaosBallsDocumentResetID = 'chaosBallsMenu'


# Chaos Balls step click handler
function chaosBallsStep(session, args):
    chaosBallsMove(session, args)
    if objectGet(args, 'play'):
        windowSetLocation(argsURL(chaosBallsArguments, objectNew('play', 0)))
    else:
        chaosBallsRender(session, args)
    endif
endfunction


# Chaos Balls reset click handler
function chaosBallsReset(session, args):
    session = chaosBallsNewSession(objectGet(session, 'model'))
    chaosBallsSetSession(session)
    chaosBallsRender(session, args)
endfunction


# Create a new Chaos Balls session object
function chaosBallsNewSession(model):
    balls = arrayNew()
    session = objectNew('model', model, 'balls', balls)

    # Iterate the ball groups
    for group in objectGet(model, 'groups'):
        groupCount = objectGet(group, 'count')
        groupColor = objectGet(group, 'color')
        groupMinSize = objectGet(group, 'minSize')
        groupMaxSize = objectGet(group, 'maxSize')
        groupMinSpeed = objectGet(group, 'minSpeed')
        groupMaxSpeed = objectGet(group, 'maxSpeed')

        # Create the group's balls
        ixBall = 0
        while ixBall < groupCount:
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
        endwhile
    endfor

    return session
endfunction


# Get the Chaos Balls session object
function chaosBallsGetSession():
    # Parse and validate the session object
    sessionJSON = sessionStorageGet('chaosBalls')
    session = null
    if sessionJSON != null:
        session = jsonParse(sessionJSON)
        if session != null:
            session = schemaValidate(chaosBallsTypes, 'ChaosBallsSession', session)
        endif
    endif

    # If there is no session, create a default session
    if session == null:
        session = chaosBallsNewSession(chaosBallsDefaultModel)
        sessionStorageSet('chaosBalls', jsonStringify(session))
    endif

    return session
endfunction


# Set the Chaos= Balls session object
function chaosBallsSetSession(session):
    sessionStorageSet('chaosBalls', jsonStringify(session))
endfunction


# Draw the Chaos Balls
function chaosBallsDraw(session, args):
    # Compute the width/height
    width = chaosBallsWidth()
    height = chaosBallsHeight(args)
    widthHeight = mathMin(width, height)

    # Render the background
    model = objectGet(session, 'model')
    drawNew(width, height)
    drawStyle('none', 0, objectGet(model, 'backgroundColor'))
    drawRect(0, 0, width, height)

    # Render the balls
    for ball in objectGet(session, 'balls'):
        drawStyle('black', 0, objectGet(ball, 'color'))
        drawCircle(objectGet(ball, 'x') * width, objectGet(ball, 'y') * height, 0.5 * objectGet(ball, 'size') * widthHeight)
    endfor
endfunction


# Get the Chaos Balls drawing width
function chaosBallsWidth():
    return windowWidth() - 3 * documentFontSize()
endfunction


# Get the Chaos Balls drawing height
function chaosBallsHeight(args):
    return windowHeight(args) - if(objectGet(args, 'fullScreen'), 3, 6) * documentFontSize()
endfunction


# Move the Chaos Balls
function chaosBallsMove(session, args):
    # Compute the width/height
    width = chaosBallsWidth()
    height = chaosBallsHeight(args)
    widthHeight = mathMin(width, height)

    # Move each ball
    period = 1 / arrayGet(chaosBallsRates, objectGet(args, 'rate'))
    for ball in objectGet(session, 'balls'):
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
        if x < xMin:
            dxParam = -dxParam
            x = xMin + (xMin - x)
        elif x > xMax:
            dxParam = -dxParam
            x = xMax - (x - xMax)
        endif

        # Compute the new Y coordinate - adjust if out of bounds
        y = y + dy
        if y < yMin:
            dyParam = -dyParam
            y = yMin + (yMin - y)
        elif y > yMax:
            dyParam = -dyParam
            y = yMax - (y - yMax)
        endif

        # Update the ball position and direction
        objectSet(ball, 'x', x / width)
        objectSet(ball, 'y', y / height)
        objectSet(ball, 'dx', dxParam)
        objectSet(ball, 'dy', dyParam)
    endfor

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
