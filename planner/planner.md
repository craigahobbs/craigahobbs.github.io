~~~ markdown-script
# Unit conversion
pixelsPerPoint = 4 / 3
pointsPerInch = 72
pixelsPerInch = pointsPerInch * pixelsPerPoint

# Text
titleFontSize = (24 / pointsPerInch) * pixelsPerInch
headerFontSize = (16 / pointsPerInch) * pixelsPerInch
textColor = 'black'

# Page
pageMargin = 0.65 * pixelsPerInch
pageWidth = 8.5 * pixelsPerInch - 2 * pageMargin
pageHeight = 11 * pixelsPerInch - 2 * pageMargin
pageInnerMargin = 0.5 * headerFontSize
pageColor = 'white'
pageDividerX = 0.33 * pageWidth
pageDividerY = 0.5 * pageHeight

# Tables
lineSize = 1
lineColor = 'black'

# Draw the page background
setDrawingSize(pageWidth, pageHeight)
drawStyle('none', 0, pageColor)
drawRect(0, 0, pageWidth, pageHeight)

# Draw the header
drawTextStyle(titleFontSize, textColor, true)
drawText('HOURLY SCHEDULE', pageDividerX + titleFontSize, pageInnerMargin, 'start', 'hanging')
drawTextStyle(headerFontSize, textColor, true)
drawText('DATE:', pageInnerMargin, pageInnerMargin + titleFontSize - headerFontSize, 'start', 'hanging')

# Draw the todo table
todoX = pageInnerMargin
todoY = pageInnerMargin + 1.2 * titleFontSize
todoWidth = pageDividerX - 0.5 * headerFontSize - todoX
todoHeight = pageDividerY - todoY
drawStyle(lineColor, lineSize, 'none')
drawRect(todoX + 0.5 * lineSize, todoY + 0.5 * lineSize, todoWidth - lineSize, todoHeight - lineSize)

# Draw the notes table
notesX = todoX
notesY = todoY + todoHeight + headerFontSize
notesWidth = todoWidth
notesHeight = pageHeight - notesY - pageInnerMargin
drawStyle(lineColor, lineSize, 'none')
drawRect(notesX + 0.5 * lineSize, notesY + 0.5 * lineSize, notesWidth - lineSize, notesHeight - lineSize)

# Draw the hourly schedule table
hoursX = pageDividerX + 0.5 * headerFontSize
hoursY = todoY
hoursWidth = pageWidth - hoursX - pageInnerMargin
hoursHeight = pageHeight - hoursY - pageInnerMargin
drawStyle(lineColor, lineSize, 'none')
drawRect(hoursX + 0.5 * lineSize, hoursY + 0.5 * lineSize, hoursWidth - lineSize, hoursHeight - lineSize)
~~~
