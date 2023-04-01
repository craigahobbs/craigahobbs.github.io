# Tesla Energy System Calibration

~~~ markdown-script
# Load the data
data = dataParseCSV(fetch('data-raw/2023-03-25.csv', null, true))

# Data field names
batteryField = 'Battery (kWh)'
batteryPercentField = 'Energy Remaining (%)'
dateField = 'Date time'
gridField = 'Grid (kW)'
homeField = 'Home (kW)'
powerwallField = 'Powerwall (kW)'
solarField = 'Solar (kW)'

# Predicted field names
predBatteryField = 'Pred Battery (kWh)'
predBatteryPercentField = 'Pred Battery (%)'
predGridField = 'Pred Grid (kWh)'
predPowerwallField = 'Pred Powerwall (kWh)'

# Difference field names
diffBatteryField = 'Diff Battery (kWh)'
diffGridField = 'Diff Grid (kWh)'
diffPowerwallField = 'Diff Powerwall (kWh)'

# Battery specifications
batterySizeKWh = 40
batteryMininumPercent = 20
batteryMininumKWh = (batteryMininumPercent / 100) * batterySizeKWh
batteryChargeRatio = 1.489
batteryDischargeRatio = 0.575

# Compute the data duration (hours)
dataDurationMs = objectGet(arrayGet(data, 1), dateField) - objectGet(arrayGet(data, 0), dateField)
dataDuration = dataDurationMs / (60 * 60 * 1000)

# Fill-in battery data holes
batteryPercentPrev = null
foreach row in data do
    batteryPercent = objectGet(row, batteryPercentField)
    if batteryPercent != null then
        batteryPercentPrev = batteryPercent
    else then
        batteryPercent = batteryPercentPrev
        objectSet(row, batteryPercentField, batteryPercent)
    endif
    battery = (batteryPercent / 100) * batterySizeKWh
    objectSet(row, batteryField, battery)
endforeach

# Generate predicted fields for powerwall, grid, and battery
battery = objectGet(arrayGet(data, 0), batteryField)
foreach row in data do
    home = objectGet(row, homeField)
    solar = objectGet(row, solarField)
    powerwall = home - solar

    # Are we generating more solar energy than we're currently using?
    if solar >= home then
        # Yes, add the excess energy to the battery
        excess = (solar - home) * dataDuration
        batteryCharged = batteryChargeRatio * excess
        batteryNew = battery + batteryCharged

        # Did we exceed the battery's capacity?
        if batteryNew > batterySizeKWh then
            # Yes, output excess energy to the grid
            powerwall = (1 / batteryChargeRatio) * (battery - batterySizeKWh) / dataDuration
            grid = powerwall - solar
            battery = batterySizeKWh
        else then
            # No, there is no grid activity
            grid = 0
            battery = batteryNew
        endif

    # No, we are using more energy than we are generating
    else then
        # Discharge the necessary energy from the battery
        needed = (home - solar) * dataDuration
        batteryDischarged = needed / batteryDischargeRatio
        batteryNew = battery - batteryDischarged

        # Do we need to pull additional energy from the grid?
        if batteryNew < batteryMininumKWh then
            # Yes, pull needed energy from the grid
            powerwall = batteryDischargeRatio * (battery - batteryMininumKWh) / dataDuration
            grid = home - powerwall
            battery = batteryMininumKWh
        else then
            # No, there is no grid activity
            grid = 0
            battery = batteryNew
        endif
    endif
    batteryPercent = 100 * battery / batterySizeKWh

    objectSet(row, predBatteryField, battery)
    objectSet(row, predBatteryPercentField, batteryPercent)
    objectSet(row, predGridField, grid)
    objectSet(row, predPowerwallField, powerwall)

    objectSet(row, diffBatteryField, battery - objectGet(row, batteryField))
    objectSet(row, diffGridField, grid - objectGet(row, gridField))
    objectSet(row, diffPowerwallField, powerwall - objectGet(row, powerwallField))
endforeach

# Chart constants
chartWidth = 1000
chartHeight = 210
fontSize = getDocumentFontSize()

# Home/Solar
dataLineChart(data, objectNew( \
    'title', 'Home/Solar', \
    'width', chartWidth - mathFloor(6 * fontSize), \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(homeField, solarField), \
    'yTicks', objectNew('start', 0, 'end', 12) \
))
markdownPrint('', '---')

# Powerwall/Grid
dataLineChart(data, objectNew( \
    'title', 'Powerwall/Grid', \
    'width', chartWidth - mathFloor(3.5 * fontSize), \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(powerwallField, gridField), \
    'yTicks', objectNew('start', -10, 'end', 10) \
))
dataLineChart(data, objectNew( \
    'title', 'Predicted Powerwall/Grid', \
    'width', chartWidth, \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(predPowerwallField, predGridField), \
    'yTicks', objectNew('start', -10, 'end', 10) \
))
markdownPrint('', '---')

# Battery
dataLineChart(data, objectNew( \
    'title', 'Battery', \
    'width', chartWidth - mathFloor(14 * fontSize), \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(batteryField), \
    'yTicks', objectNew('start', 0, 'end', batterySizeKWh), \
    'yLines', arrayNew(objectNew('value', (batteryMininumPercent / 100) * batterySizeKWh)) \
))
dataLineChart(data, objectNew( \
    'title', 'Predicted Battery', \
    'width', chartWidth - mathFloor(14 * fontSize), \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(predBatteryField), \
    'yTicks', objectNew('start', 0, 'end', batterySizeKWh), \
    'yLines', arrayNew(objectNew('value', (batteryMininumPercent / 100) * batterySizeKWh)) \
))
markdownPrint('', '---')

# Battery %
dataLineChart(data, objectNew( \
    'title', 'Battery %', \
    'width', chartWidth - mathFloor(14 * fontSize), \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(batteryPercentField), \
    'yTicks', objectNew('start', 0, 'end', 100), \
    'yLines', arrayNew(objectNew('value', batteryMininumPercent)) \
))
dataLineChart(data, objectNew( \
    'title', 'Predicted Battery %', \
    'width', chartWidth - mathFloor(14 * fontSize), \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(predBatteryPercentField), \
    'yTicks', objectNew('start', 0, 'end', 100), \
    'yLines', arrayNew(objectNew('value', batteryMininumPercent)) \
))
markdownPrint('', '---')

# Differences
dataLineChart(data, objectNew( \
    'title', 'Differences', \
    'width', chartWidth, \
    'height', chartHeight, \
    'x', dateField, \
    'y', arrayNew(diffBatteryField, diffGridField, diffPowerwallField), \
    'yLines', arrayNew(objectNew('value', 0)) \
))

# Compute the average battery percentage difference
diffBatteryAbsField = diffBatteryField + 'Abs'
dataCalculatedField(data, diffBatteryAbsField, 'abs([' + diffBatteryField + '])')
dataAverageDiff = dataAggregate(data, objectNew( \
    'measures', arrayNew( \
        objectNew('field', diffBatteryAbsField, 'function', 'average') \
    ) \
))
averageDiffBatteryPercent = 100 * objectGet(arrayGet(dataAverageDiff, 0), diffBatteryAbsField) / batterySizeKWh
markdownPrint('', '**Battery Difference:** ' + numberToFixed(averageDiffBatteryPercent , 2) + '%')
markdownPrint('', '---')

# Data table
dataTable(data)
~~~
