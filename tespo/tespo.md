~~~ markdown-script
# TESPO schemas
tespoTypes = schemaParse( \
    '# The Tesla Energy Self-Powered Optimizer (TESPO) data API response', \
    'struct TespoData', \
    '', \
    '    # The current average solar power generation, in kWh', \
    '    float(>= 0) solarPower', \
    '', \
    '    # The current average home power usage, in kWh', \
    '    float(>= 0) homeUsage', \
    '', \
    '    # The home battery power percentage', \
    '    float(>= 0, <= 100) homeBattery', \
    '', \
    '    # The connected battery-powered electric vehicles', \
    '    Vehicle[] vehicles', \
    '', \
    '# A battery-powered electric vehicle', \
    'struct Vehicle', \
    '', \
    '    # The vehicle ID', \
    '    string(len > 0) id', \
    '', \
    "    # The vehicle's friendly name", \
    '    string(len > 0) name', \
    '', \
    "    # The vehicle's battery power percentage", \
    '    float(>= 0, <= 100) battery', \
    '', \
    '    # If true, the car is charging', \
    '    bool charging', \
    '', \
    '    # The charging rate, in amps', \
    '    int(> 0) chargingRate', \
    '', \
    '    # The charging limit, as a percentage', \
    '    float(>= 0, <= 100) chargingLimit', \
    '', \
    '# The TESPO algorithm response', \
    'struct TespoResponse', \
    '', \
    '    # The TESPO actions', \
    '    TespoAction[] actions', \
    '', \
    '# A TESPO algorithm response action', \
    'union TespoAction', \
    '', \
    '    # Turn vehichle charging on or off', \
    '    VehicleCharging vehicleCharging', \
    '', \
    "# Set a vehicle's charging on or off", \
    'struct VehicleCharging', \
    '', \
    '    # The vehicle ID', \
    '    string(len > 0) id', \
    '', \
    '    # If true, the car is charging', \
    '    bool charging', \
    '', \
    '    # The charging rate, in amps', \
    '    int(> 0) chargingRate', \
    '', \
    '    # The charging limit, as a percentage', \
    '    float(>= 0, <= 100) chargingLimit' \
)


# Data scenarios
scenarios = objectNew( \
    'HomeCharged', 'data/homeCharged.json', \
    'HomeUncharged', 'data/homeUncharged.json' \
)
scenarioNames = objectKeys(scenarios)


# Main entry point
async function main()
    # Data schema documentation?
    jumpif (!vDocData) noDataDoc
        markdownPrint('[Home](#var=)', '')
        schemaPrint(tespoTypes, 'TespoData')
        return
    noDataDoc:

    # Response schema documentation?
    jumpif (!vDocResponse) noResponseDoc
        markdownPrint('[Home](#var=)', '')
        schemaPrint(tespoTypes, 'TespoResponse')
        return
    noResponseDoc:

    # Determine the scenario data URL
    scenario = getGlobal('vScenario')
    scenario = if(scenario != null, scenario, 'HomeCharged')
    dataURL = objectGet(scenarios, scenario)
    dataURL = if(dataURL != null, dataURL, objectGet('HomeCharged'))

    # Fetch the data API
    await dataResponse = schemaValidate(tespoTypes, 'TespoData', fetch(dataURL))

    # Compute the TESPO response
    tespoResponse = tespo(dataResponse)

    # Create the scenario links markdown
    scenarioLinks = ''
    ixScenario = 0
    ixScenarioMax = arrayLength(scenarioNames)
    scenarioLinksLoop:
        scenarioName = arrayGet(scenarioNames, ixScenario)
        scenarioURL = objectGet(scenarios, scenarioName)
        scenarioLinks = scenarioLinks + if(ixScenario != 0, ' | ', '') + \
            if(scenarioName == scenario,scenarioName, '[' + scenarioName + "](#var.vScenario='" + scenarioName + "')")
        ixScenario = ixScenario + 1
    jumpif (ixScenario < ixScenarioMax) scenarioLinksLoop

    # Main display
    markdownPrint( \
        '# T.E.S.P.O. (Tesla Energy Self-Powered Optimizer)', \
        '', \
        scenarioLinks, \
        '', \
        '**Scenario:** ' + scenario, \
        '', \
        '### Data Response', \
        '', \
        '~~~', \
        jsonStringify(dataResponse, 4), \
        '~~~', \
        '', \
        '### TESPO Response', \
        '', \
        '~~~', \
        jsonStringify(tespoResponse, 4), \
        '~~~', \
        '', \
        '## Schema Documentation', \
        '', \
        '[Data Schema Documentation](#var.vDocData=1)', \
        '', \
        '[Response Schema Documentation](#var.vDocResponse=1)' \
    )
endfunction


# The TESPO algorithm
function tespo()
    return objectNew('actions', arrayNew())
endfunction


await main()
~~~
