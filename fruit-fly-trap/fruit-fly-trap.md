~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include <args.mds>


function main():
    # Parse arguments
    args = argsParse(lifeArguments)
    isMetric = objectGet(args, 'metric')
    height = objectGet(args, 'height', if(isMetric, 11.5, 4.5))
    diameter = objectGet(args, 'diameter', if(isMetric, 7.5, 3))
    bottom = objectGet(args, 'bottom', if(isMetric, 2, 0.75))
    offset = objectGet(args, 'offset', if(isMetric, 2.5, 1))

    # Computed values
    precision = 3
    units = if(isMetric, 'cm', 'in')
    delta = if(isMetric, 0.1, 0.125)
    flapLength = if(isMetric, 0.5, 0.2)
    coneExtraLength = if(isMetric, 1.25, 0.5)
    coneHeight = height - offset

    # Set the title
    title = 'The Fruit Fly Trap Maker'
    documentSetTitle(title)

    # Print the cone form?
    if objectGet(args, 'print'):
        # Print close link
        elementModelRender(objectNew( \
            'html', 'p', \
            'attr', objectNew('class', 'markdown-model-no-print'), \
            'elem', objectNew( \
                'html', 'a', \
                'attr', objectNew('href', documentURL(argsURL(lifeArguments))), \
                'elem', objectNew('text', 'Close') \
            ) \
        ))

        # Render the cone form
        pixelsPerPoint = 4 / 3
        pointsPerCm = 28.3464567
        pointsPerInch = 72
        pixelsPerUnit = if(isMetric, pointsPerCm, pointsPerInch) * pixelsPerPoint
        coneForm(diameter * pixelsPerUnit, bottom * pixelsPerUnit, coneHeight * pixelsPerUnit, \
            flapLength * pixelsPerUnit, 1, coneExtraLength * pixelsPerUnit)
        return
    endif

    # Introduction
    markdownPrint( \
        '# ' + title, \
        '', \
        '**The Fruit Fly Trap Maker** rids your home of annoying fruit flies using only a drinking glass,', \
        'your computer printer, and a small amount of apple cider vinegar (or similar).', \
        '', \
        'The trap is made by placing a custom-fitted cone (based on your measurements) into a drinking glass', \
        'containing a small amount of apple cider vinegar (see below). The fruit flies fly in through the', \
        'cone opening and become trapped between the cone and the liquid.' \
    )

    # Fruit-fly trap diagram
    fruitFlyTrapDiagram()

    # Instructions
    markdownPrint( \
        '## Instructions', \
        '', \
        argsLink(lifeArguments, 'Reset', objectNew('metric', isMetric), true), \
        ' | ', \
        argsLink(lifeArguments, if(isMetric, 'Imperial', 'Metric'), objectNew('metric', !isMetric), true), \
        '', \
        '1. Take the following measurements from a drinking glass (see diagram above).', \
        '', \
        '    **Top diameter (d)** (' + \
            if(isValidConeForm(diameter - delta, bottom, coneHeight, flapLength), \
                argsLink(lifeArguments, 'Less', objectNew('diameter', mathRound(diameter - delta, precision))), 'Less') + ' | ' + \
            if(isValidConeForm(diameter + delta, bottom, coneHeight, flapLength), \
                argsLink(lifeArguments, 'More', objectNew('diameter', mathRound(diameter + delta, precision))), 'More') + \
            '): ' + diameter + ' ' + units, \
        '', \
        '    **Height (h)** (' + \
            if(isValidConeForm(diameter, bottom, coneHeight - delta, flapLength), \
                argsLink(lifeArguments, 'Less', objectNew('height', mathRound(height - delta, precision))), 'Less') + ' | ' + \
            if(isValidConeForm(diameter, bottom, coneHeight + delta, flapLength), \
                argsLink(lifeArguments, 'More', objectNew('height', mathRound(height + delta, precision))), 'More') + \
            '): ' + height + ' ' + units, \
        '', \
        '    **Bottom offset (o)** (' + \
            if(isValidConeForm(diameter, bottom, coneHeight + delta, flapLength), \
                argsLink(lifeArguments, 'Less', objectNew('offset', mathRound(offset - delta, precision))), 'Less') + ' | ' + \
            if(isValidConeForm(diameter, bottom, coneHeight - delta, flapLength), \
                argsLink(lifeArguments, 'More', objectNew('offset', mathRound(offset + delta, precision))), 'More') + \
            '): ' + offset + ' ' + units, \
        '', \
        '    **Bottom diameter (b)** (' + \
            if(isValidConeForm(diameter, bottom - delta, coneHeight, flapLength), \
                argsLink(lifeArguments, 'Less', objectNew('bottom', mathRound(bottom - delta, precision))), 'Less') + ' | ' + \
            if(isValidConeForm(diameter, bottom + delta, coneHeight, flapLength), \
                argsLink(lifeArguments, 'More', objectNew('bottom', mathRound(bottom + delta, precision))), 'More') + \
            '): ' + bottom + ' ' + units, \
        '', \
        '2. Print the cone form using the link below.', \
        '', \
        '   ' + argsLink(lifeArguments, 'Print Cone Form', objectNew('print', true), false, argsTopHeaderId), \
        '', \
        "3. Cut out the cone form carefully using scissors and tape the cone together along the cone form's flap line.", \
        '', \
        '4. Pour a small amount of fruit-fly-attracting liquid (e.g., apple cider vinegar) into the glass. Be', \
        '   sure the liquid level is at least ' + if(isMetric, '1/2 cm.', '1/4 in.') + ' below the cone-bottom.', \
        '', \
        '5. Place the cone form in the glass. It may help to rub some water around the top rim of the glass', \
        '   to form a seal.', \
        '', \
        '6. Set the trap near where you have fruit flies.' \
    )
endfunction


lifeArguments = argsValidate(arrayNew( \
    objectNew('name', 'bottom', 'type', 'float'), \
    objectNew('name', 'diameter', 'type', 'float'), \
    objectNew('name', 'height', 'type', 'float'), \
    objectNew('name', 'metric', 'type', 'bool', 'default', false), \
    objectNew('name', 'offset', 'type', 'float'), \
    objectNew('name', 'print', 'type', 'bool', 'default', false, 'explicit', true) \
))


function isValidConeForm(diameterTop, diameterBottom, height, flapLength):
    formRadius = (height * diameterBottom) / (diameterTop - diameterBottom)
    formTheta = mathPi() * (diameterBottom / formRadius)
    flapTheta = formTheta + (flapLength / formRadius)
    return (diameterBottom < (0.9 * diameterTop)) && (flapTheta < (0.9 * (2 * mathPi())))
endfunction


function coneForm(diameterTop, diameterBottom, height, flapLength, lineWidth, extraLength):
    # Compute the cone form's radii and theta
    formRadius = height * diameterBottom / (diameterTop - diameterBottom)
    formRadiusOuter = formRadius + height + extraLength
    formTheta = mathPi() * diameterBottom / formRadius

    # Compute the flap angle
    flapTheta = formTheta + flapLength / formRadius

    # Compute the SVG extents
    formMinX = 0
    formMaxX = 0
    formMinY = 0
    formMaxY = 0
    flapInnerX = formRadius * mathSin(flapTheta)
    flapInnerY = formRadius * mathCos(flapTheta)
    flapOuterX = formRadiusOuter * mathSin(flapTheta)
    flapOuterY = formRadiusOuter * mathCos(flapTheta)

    if flapTheta < 0.5 * mathPi():
        formMinX = 0
        formMinY = flapInnerY
        formMaxX = flapOuterX
        formMaxY = formRadiusOuter
    elif flapTheta < mathPi():
        formMinX = 0
        formMinY = flapOuterY
        formMaxX = formRadiusOuter
        formMaxY = formRadiusOuter
    elif flapTheta < 1.5 * mathPi():
        formMinX = flapOuterX
        formMinY = -formRadiusOuter
        formMaxX = formRadiusOuter
        formMaxY = formRadiusOuter
    else:
        formMinX = -formRadiusOuter
        formMinY = -formRadiusOuter
        formMaxX = formRadiusOuter
        formMaxY = formRadiusOuter
    endif

    # Expand the form bounding box by one line width (to accomodate lines)
    formMinX = formMinX - lineWidth
    formMinY = formMinY - lineWidth
    formMaxX = formMaxX + lineWidth
    formMaxY = formMaxY + lineWidth

    # Compute the cone form guide line
    guideInnerX = formRadius * mathSin(formTheta)
    guideInnerY = formRadius * mathCos(formTheta)
    guideOuterX = formRadiusOuter * mathSin(formTheta)
    guideOuterY = formRadiusOuter * mathCos(formTheta)

    # Draw the cone form
    edge = 5 * lineWidth
    drawNew(2 * edge + formMaxX - formMinX, 2 * edge + formMaxY - formMinY)
    drawStyle('none', 0, 'white')
    drawRect(0, 0, drawWidth(), drawHeight())
    drawStyle('black', lineWidth, 'none', 3 * lineWidth + ' ' + 3 * lineWidth)
    drawMove(edge - formMinX, edge)
    drawArc(formRadiusOuter, formRadiusOuter, 0, flapTheta > mathPi(), 1, edge + flapOuterX - formMinX, edge + formMaxY - flapOuterY)
    drawLine(edge + flapInnerX - formMinX, edge + formMaxY - flapInnerY)
    drawArc(formRadius, formRadius, 0, flapTheta > mathPi(), 0, edge - formMinX, edge + formRadiusOuter - formRadius)
    drawClose()
    drawStyle('lightgray', lineWidth, 'none')
    drawMove(edge + guideInnerX - formMinX, edge + formMaxY - guideInnerY)
    drawLine(edge + guideOuterX - formMinX, edge + formMaxY - guideOuterY)
endfunction


function fruitFlyTrapDiagram():
    annotationTextSize = documentFontSize()
    width = 16 * annotationTextSize
    height = 14  * annotationTextSize

    imageMargin = mathCeil(0.7 * annotationTextSize)
    lineWidth = 1
    glassLineWidth = 5 * lineWidth
    annotationWidth = mathCeil(1.2 * annotationTextSize)
    annotationBarWidth = 0.5 * annotationWidth
    annotationTextHeight = 1.2 * annotationWidth
    airHeight = annotationWidth
    liquidHeight = 1.5 * airHeight

    # Glass position
    glassTop = 0.2 * height
    glassLeft = imageMargin + annotationWidth + 0.5 * glassLineWidth
    glassLeftRight = glassLeft + 0.5 * glassLineWidth
    glassBottom = height - imageMargin - 0.5 * glassLineWidth
    glassRight = width - glassLeft
    glassRightLeft = glassRight - 0.5 * glassLineWidth

    # Cone position
    coneBottom = height - imageMargin - glassLineWidth - liquidHeight - airHeight
    coneBottomLeft = 0.5 * width - annotationWidth
    coneBottomRight = width - coneBottomLeft
    coneTop = imageMargin
    coneTopLeft = (coneBottomLeft * (glassTop - coneTop) + glassLeftRight * (coneTop - coneBottom)) / (glassTop - coneBottom)
    coneTopRight = width - coneTopLeft

    # Draw the fruit fly trap diagram
    drawNew(width, height)
    drawStyle('none', 0, 'white')
    drawRect(0, 0, width, height)

    # Liquid
    drawStyle('none', 0, '#cc99ff80')
    drawRect(glassLeft, glassBottom - liquidHeight, glassRight - glassLeft, liquidHeight)

    # Glass
    drawStyle('black', glassLineWidth)
    drawMove(glassLeft, glassTop)
    drawVLine(glassBottom)
    drawHLine(glassRight)
    drawVLine(glassTop)

    # Cone
    drawStyle('black', lineWidth, 'none')
    drawMove(coneTopLeft, coneTop)
    drawLine(coneBottomLeft, coneBottom)
    drawHLine(coneBottomRight)
    drawLine(coneTopRight, coneTop)
    drawClose()

    # Annotations
    verticalAnnotation('h', imageMargin + 0.5 * annotationBarWidth, glassTop, glassBottom, \
        annotationBarWidth, annotationTextHeight, annotationTextSize)
    verticalAnnotation('o', width - imageMargin - 0.5 * annotationBarWidth, coneBottom, glassBottom, \
        annotationBarWidth, annotationTextHeight, annotationTextSize)
    horizontalAnnotation('d', glassTop - annotationWidth + 0.5 * annotationBarWidth, glassLeftRight, glassRightLeft, \
        annotationBarWidth, annotationTextHeight, annotationTextSize)
    horizontalAnnotation('b', coneBottom - annotationWidth + 0.5 * annotationBarWidth, coneBottomLeft, coneBottomRight, \
        annotationBarWidth, annotationTextHeight, annotationTextSize)
endfunction


function verticalAnnotation(text, xcoord, top, bottom, annotationBarWidth, annotationTextHeight, annotationTextSize):
    drawMove(xcoord - 0.5 * annotationBarWidth, top)
    drawHLine(xcoord + 0.5 * annotationBarWidth)
    drawMove(xcoord, top)
    drawVLine(0.5 * (top + bottom) - 0.5 * annotationTextHeight)
    drawMove(xcoord, bottom)
    drawVLine(0.5 * (top + bottom) + 0.5 * annotationTextHeight)
    drawMove(xcoord - 0.5 * annotationBarWidth, bottom)
    drawHLine(xcoord + 0.5 * annotationBarWidth)
    drawTextStyle(annotationTextSize)
    drawText(text, xcoord, 0.5 * (top + bottom))
endfunction


function horizontalAnnotation(text, ycoord, left, right, annotationBarWidth, annotationTextHeight, annotationTextSize):
    drawStyle('black', 1)
    drawMove(left, ycoord - 0.5 * annotationBarWidth)
    drawVLine(ycoord + 0.5 * annotationBarWidth)
    drawMove(left, ycoord)
    drawHLine(0.5 * (left + right) - 0.5 * annotationTextHeight)
    drawMove(right, ycoord)
    drawHLine(0.5 * (left + right) + 0.5 * annotationTextHeight)
    drawMove(right, ycoord - 0.5 * annotationBarWidth)
    drawVLine(ycoord + 0.5 * annotationBarWidth)
    drawTextStyle(annotationTextSize)
    drawText(text, 0.5 * (left + right), ycoord)
endfunction


# Execute the main entry point
main()
~~~
