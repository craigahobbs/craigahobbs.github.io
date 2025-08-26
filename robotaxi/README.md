# Tesla vs Waymo Robotaxi Fleet Size Predictions

```markdown-script
# Load the data
data = dataValidate(dataParseCSV(systemFetch('robotaxi.csv')))

dataFiltered = dataFilter(data, 'Month < monthMax', objectNew('monthMax', datetimeNew(2026, 9, 1)))

dataLineChart(dataFiltered, objectNew( \
    'title', 'Project Robotaxi Fleet Sizes', \
    'width', 1000, \
    'height', 450, \
    'precision', 0, \
    'datetime', 'month', \
    'x', 'Month', \
    'y', arrayNew('Size'), \
    'color', 'Fleet' \
))

dataTable(data)
```
