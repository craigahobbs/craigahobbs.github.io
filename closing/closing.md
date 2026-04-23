```markdown-script
include <draw.bare>


function closingMain():
    # Compute the days to closing
    closingDatetime = datetimeNew(2026, 5, 27)
    daysToClose = (closingDatetime - datetimeToday()) / (24 * 60 * 60 * 1000)

    # Compute the sign size
    fontSizePx = documentFontSize()
    width = windowWidth() - 3 * fontSizePx
    height = windowHeight() - 3 * fontSizePx

    # Compute the font sizes
    daysText = stringNew(daysToClose)
    labelText = 'Days to Closing'
    labelFontSize = mathMin(0.2 * height, drawTextHeight(labelText, 0.9 * width))
    daysFontSize = mathMin(0.8 * height, drawTextHeight(daysText, 0.9 * width))

    # Draw the sign
    drawNew(width, height)
    drawStyle('none', 1, 'white')
    drawRect(0, 0, width, height)
    drawTextStyle(daysFontSize, 'red')
    drawText(daysText, 0.5 * width, 0.45 * height)
    drawTextStyle(labelFontSize)
    drawText(labelText, 0.5 * width, 0.85 * height)
    drawRender()

    # Set the resize event
    windowSetResize(closingMain)
endfunction


closingMain()
```
