# GitHub Flavored Markdown (GFM)

## Links

- [Edit](https://github.com/craigahobbs/craigahobbs.github.io/edit/main/gfm/README.md)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

## Tasks

~~~ markdown-script
data = dataParseCSV( \
    'Done,Priority,Effort,Description', \
    '0,1,1,line-breaks - check', \
    '0,2,1,bold/italic - underscores', \
    '0,3,3,blockquotes', \
    '0,1,1,ordered list - check', \
    '0,1,1,images - check', \
    '1,3,2,code spans (`)', \
    '0,1,1,links - check', \
    '0,2,2,reference-style links', \
    '0,1,1,escapes - check', \
    "0,2,1,\"strikethrough, subscript, superscript\"", \
    '0,2,2,footnotes', \
    '0,2,2,HTML comments', \
    '1,3,3,tables', \
    '0,2,2,entity and numeric character references' \
)

dataCalculatedField(data, 'DescriptionLower', 'lower(Description)')
dataSort(data, arrayNew(arrayNew('Priority', true), arrayNew('Effort'), arrayNew('DescriptionLower')))
dataNotDone = dataFilter(data, '!Done')
dataDone = dataFilter(data, 'Done')

notDoneEffort = dataAggregate(dataNotDone, objectNew('measures', arrayNew(objectNew('field', 'Effort', 'function', 'sum'))))
doneEffort = dataAggregate(dataDone, objectNew('measures', arrayNew(objectNew('field', 'Effort', 'function', 'sum'))))
donePercent = 100 * objectGet(arrayGet(doneEffort, 0), 'Effort') / objectGet(arrayGet(notDoneEffort, 0), 'Effort')

dataTable(dataNotDone, objectNew('fields', arrayNew('Priority', 'Effort', 'Description')))
jumpif (arrayLength(dataDone) == 0) doneNone
    markdownPrint('', '## Completed Tasks', '', 'The project is **' + numberToFixed(donePercent, 1) + '%** complete.')
    dataTable(dataDone, objectNew('fields', arrayNew('Priority', 'Effort', 'Description')))
doneNone:
~~~
