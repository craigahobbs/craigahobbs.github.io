~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


async function main(packages)
    # Package menu
    markdownPrint('**Packages:**')
    ixPackage = 0
    packageLoop:
        packageName = arrayGet(packages, ixPackage)
        if(ixPackage != 0, markdownPrint('**|**'))
        markdownPrint(if(vName == packageName, packageName, '[' + packageName + '](' + downloadLink(packageName) + ')'))
        ixPackage = ixPackage + 1
    jumpif (ixPackage < arrayLength(packages)) packageLoop

    # Window menu
    markdownPrint('', '**Window:**')
    windows = arrayNew(7, 15, 21, 31, 45)
    ixWindow = 0
    windowLoop:
        window = arrayGet(windows, ixWindow)
        if(ixWindow != 0, markdownPrint('**|**'))
        markdownPrint(if(vWindow == window, window + ' days', '[' + window + ' days](' + downloadLink(null, window) + ')'))
        ixWindow = ixWindow + 1
    jumpif (ixWindow < arrayLength(windows)) windowLoop

    # Set the document title
    title = 'PyPI Download Stats' + if(vName != null, ' - ' + vName, '')
    markdownPrint('', '# ' + title)
    setDocumentTitle(title)

    if(vName != null, downloadDashboard(vName), markdownPrint('', 'No package selected'))
endfunction


function downloadLink(name, window)
    name = if(name != null, name, vName)
    window = if(window != null, window, vWindow)
    parts = arrayNew()
    if(name != null, arrayPush(parts, "var.vName='" + name + "'"))
    if(window != null, arrayPush(parts, 'var.vWindow=' + window))
    return if(arrayLength(parts) == 0, '#var=', '#' + arrayJoin(parts, '&'))
endfunction


async function downloadDashboard(packageName)
    chartWidth = 1000
    chartHeight = 250

    # Load and validate the package "overall" data
    # dataURL = 'https://pypistats.org/api/packages/' + packageName + '/overall'
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
