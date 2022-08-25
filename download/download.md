~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


async function main(packages)
    # Package menu
    markdownPrint('**Packages:**')
    ixPackage = 0
    packageLoop:
        packageName = arrayGet(packages, ixPackage)
        packageURL = "#var.vName='" + packageName + "'" + if(vWindow == null, '', '&var.vWindow=' + vWindow)
        if(ixPackage != 0, markdownPrint('**|**'))
        markdownPrint('[' + packageName + '](' + packageURL + ')')
        ixPackage = ixPackage + 1
    jumpif (ixPackage < arrayLength(packages)) packageLoop

    # Set the document title
    title = 'PyPI Download Stats' + if(vName != null, ' - ' + vName, '')
    markdownPrint('# ' + title)
    setDocumentTitle(title)

    if(vName != null, downloadDashboard(vName), markdownPrint('', 'No package selected'))
endfunction


async function downloadDashboard(packageName)
    chartWidth = 1000
    chartHeight = 250

    # Load and validate the package "overall" data
    dataURL = 'data/' + packageName + '.json'
    data = dataValidate(objectGet(fetch(dataURL), 'data'))

    # Compute the with-mirrors three-week daily running average
    windowSize = if(vWindow != null, vWindow, 21)
    windowSizeHalf = (windowSize - 1) / 2
    ixDay = windowSizeHalf
    dataAvg = arrayNew()
    dataWithMirrors = dataFilter(data, 'category == "with_mirrors"')
    dataSort(dataWithMirrors, arrayNew(arrayNew('date')))
    dayLoop:
        avgSum = 0
        ixDayAvg = ixDay - windowSizeHalf
        dayAvgLoop:
            avgSum = avgSum + objectGet(arrayGet(dataWithMirrors, ixDayAvg), 'downloads')
            ixDayAvg = ixDayAvg + 1
        jumpif (ixDayAvg < ixDay + windowSizeHalf + 1) dayAvgLoop
        arrayPush(dataAvg, objectNew( \
            'date', objectGet(arrayGet(dataWithMirrors, ixDay), 'date'), \
            'downloads', avgSum / windowSize \
        ))
        ixDay = ixDay + 1
    jumpif (ixDay < arrayLength(dataWithMirrors) - windowSizeHalf) dayLoop

    # Render the daily running average chart
    dataLineChart(dataAvg, objectNew( \
        'title', 'Average Daily Downloads (' + windowSize + ' day window) - ' + packageName, \
        'width', chartWidth - mathFloor(1.5 * getTextWidth('with_mirrors', getTextHeight('', 0))), \
        'height', chartHeight, \
        'x', 'date', \
        'y', arrayNew('downloads'), \
        'ytick', objectNew('start', 0), \
        'datetime', 'Day', \
        'precision', 0 \
    ))

    # Render the daily line chart
    dataLineChart(data, objectNew( \
        'title', 'Daily Downloads - ' + packageName, \
        'width', chartWidth, \
        'height', chartHeight, \
        'x', 'date', \
        'y', arrayNew('downloads'), \
        'color', 'category', \
        'ytick', objectNew('start', 0), \
        'datetime', 'Day', \
        'precision', 0 \
    ))

    # Aggregate by month
    dataCalculatedField(data, 'month', 'dateFn(year(date), month(date), 1)', objectNew('dateFn', datetimeNew))
    dataMonth = dataAggregate(data, objectNew( \
        'categories', arrayNew('month', 'category'), \
        'measures', arrayNew( \
            objectNew( \
                'field', 'downloads', \
                'function', 'Sum' \
            ) \
        ) \
    ))

    # Render the monthly line chart
    dataLineChart(dataMonth, objectNew( \
        'title', 'Monthly Downloads - ' + packageName, \
        'width', chartWidth, \
        'height', chartHeight, \
        'x', 'month', \
        'y', arrayNew('downloads'), \
        'color', 'category', \
        'ytick', objectNew('start', 0), \
        'datetime', 'Month', \
        'precision', 0 \
    ))

    # Render the monthly table by most recent
    dataSort(dataMonth, arrayNew(arrayNew('month', true), arrayNew('category')))
    dataTable(dataMonth, objectNew( \
        'categoryFields', arrayNew('month', 'category'), \
        'datetime', 'Month' \
    ))
endfunction


main(arrayNew( \
    'chisel', \
    'markdown-up', \
    'schema-markdown', \
    'simple-git-changelog', \
    'template-specialize', \
    'unittest-parallel' \
))
~~~
