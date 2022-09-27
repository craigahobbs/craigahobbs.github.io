# Bets

~~~ markdown-script
# Load the bets data
data = dataParseCSV(fetch('bets.csv', null, true))

# Compute the results
dataCalculatedField(data, 'Score', '(HomeScore + Line - AwayScore)')
dataCalculatedField(data, 'Result', \
    'if(Score == 0, "Draw", if((Pick == Home && Score > 0) || (Pick == Away && Score < 0), "Win", "Lose"))')
dataCalculatedField(data, 'Win', 'if(Result == "Win", 1, 0)')
dataCalculatedField(data, 'LockWin', 'if(Lock && Result == "Win", 1, 0)')
results = dataAggregate(data, objectNew( \
    'categories', arrayNew('Result'), \
    'measures', arrayNew( \
        objectNew('field', 'Result', 'function', 'count', 'name', 'Count'), \
        objectNew('field', 'Lock', 'function', 'sum', 'name', 'LockCount') \
    ) \
))
dataSort(results, arrayNew(arrayNew('Result')))

# Compute the underdog breakdown
dataCalculatedField(data, 'WinType', \
    'if(Line < 0, if(Score == 0, "HomeScratch", if(Score > 0, "HomeFavorite", "AwayUnderdog")), ' + \
    'if(Line > 0, if(Score == 0, "AwayScratch", if(Score > 0, "HomeUnderdog", "AwayFavorite")), "Scratch"))' \
)
winTypes = dataAggregate(data, objectNew( \
    'categories', arrayNew('WinType'), \
    'measures', arrayNew( \
        objectNew('field', 'WinType', 'function', 'count', 'name', 'Count'), \
        objectNew('field', 'Win', 'function', 'sum', 'name', 'WinCount'), \
        objectNew('field', 'LockWin', 'function', 'sum', 'name', 'LockCount') \
    ) \
))

# Report
dataTable(results)
dataTable(winTypes)
dataTable(data)
~~~
