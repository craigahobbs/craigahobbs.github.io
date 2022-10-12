# GitHub Flavored Markdown (GFM)

## Links

- [Edit](https://github.com/craigahobbs/craigahobbs.github.io/edit/main/gfm/README.md)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

~~~ markdown-script
data = dataParseCSV( \
    'Done,Priority,Effort,Description', \
    '0,2,1,bold/italic - underscores', \
    "0,2,1,\"strikethrough\"", \
    '0,2,2,markdown spec review and unit tests', \
    '0,1,1,code review and performance testing', \
    '0,1,1,update readme with markdown flavor information', \
    '1,3,2,code spans', \
    '1,3,3,tables', \
    '1,3,3,block quotes' \
)

dataCalculatedField(data, 'DescriptionLower', 'lower(Description)')
dataSort(data, arrayNew(arrayNew('Priority', true), arrayNew('Effort'), arrayNew('DescriptionLower')))
dataNotDone = dataFilter(data, '!Done')
dataDone = dataFilter(data, 'Done')

totalEffort = dataAggregate(data, objectNew('measures', arrayNew(objectNew('field', 'Effort', 'function', 'sum'))))
doneEffort = dataAggregate(dataDone, objectNew('measures', arrayNew(objectNew('field', 'Effort', 'function', 'sum'))))
donePercent = 100 * objectGet(arrayGet(doneEffort, 0), 'Effort') / objectGet(arrayGet(totalEffort, 0), 'Effort')

jumpif (arrayLength(dataNotDone) == 0) notDoneNone
    markdownPrint('', '## Tasks')
    dataTable(dataNotDone, objectNew('fields', arrayNew('Priority', 'Effort', 'Description')))
notDoneNone:

jumpif (arrayLength(dataDone) == 0) doneNone
    markdownPrint('', '## Completed Tasks', '', 'The project is **' + numberToFixed(donePercent, 1) + '%** complete.')
    dataTable(dataDone, objectNew('fields', arrayNew('Priority', 'Effort', 'Description')))
doneNone:
~~~
