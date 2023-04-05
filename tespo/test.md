# Test

~~~ markdown-script
include 'tesla.mds'

data = dataParseCSV(fetch('data-raw/2023-03-25.csv', null, true))
teslaFillBatteryData(data)
dataLineChart(data, objectNew( \
    'x', teslaFieldDate, \
    'y', arrayNew(teslaFieldBatteryPercent) \
))
dataTable(data)
~~~
