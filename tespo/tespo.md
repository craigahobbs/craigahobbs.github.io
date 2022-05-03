~~~ markdown-script
# TESPO schemas
tespoTypes = schemaParse( \
    '# The Tesla Energy Self-Powered Optimizer (TESPO) service input', \
    'struct TespoInput', \
    '', \
    '    # The current average solar power generation, in kWh', \
    '    float(>= 0) solarPower', \
    '', \
    '    # The current average home power usage, in kWh', \
    '    float(>= 0) homePower', \
    '', \
    '    # The home battery power percentage', \
    '    float(>= 0, <= 100) homeBattery', \
    '', \
    '    # The connected battery-powered electric vehicles', \
    '    Vehicle[] vehicles', \
    '', \
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
    '    # The available charging rates, in amps', \
    '    int(> 0)[len > 0] chargingRates', \
    '', \
    '    # The available charging power (corresponding to the "chargingRates"), in kWh', \
    '    float(>= 0, <= 100)[len > 0] chargingPowers', \
    '', \
    '', \
    '# The Tesla Energy Self-Powered Optimizer (TESPO) service output', \
    'struct TespoOutput', \
    '', \
    '    # The TESPO actions', \
    '    TespoAction[] actions', \
    '', \
    '', \
    '# A TESPO action', \
    'union TespoAction', \
    '', \
    '    # Turn vehichle charging on or off', \
    '    VehicleCharging vehicleCharging', \
    '', \
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


# Input scenarios
scenarios = objectNew( \
    'HomeCharged', 'data/homeCharged.json', \
    'HomeUncharged', 'data/homeUncharged.json' \
)
scenarioNames = objectKeys(scenarios)


# Main entry point
async function main()
    # Input schema documentation?
    jumpif (!vDocInput) noInputDoc
        markdownPrint('[Home](#var=)', '')
        schemaPrint(tespoTypes, 'TespoInput')
        return
    noInputDoc:

    # Output schema documentation?
    jumpif (!vDocOutput) noOutputDoc
        markdownPrint('[Home](#var=)', '')
        schemaPrint(tespoTypes, 'TespoOutput')
        return
    noOutputDoc:

    # Determine the scenario input URL
    scenarioName = if(vScenario != null, vScenario, 'HomeCharged')
    inputURL = objectGet(scenarios, scenarioName)
    inputURL = if(inputURL != null, inputURL, objectGet(scenarios, 'HomeCharged'))

    # Create the scenario links markdown
    scenarioLinks = ''
    ixScenario = 0
    ixScenarioMax = arrayLength(scenarioNames)
    scenarioLinksLoop:
        scenarioLinkName = arrayGet(scenarioNames, ixScenario)
        scenarioLinkURL = objectGet(scenarios, scenarioLinkName)
        scenarioLinks = scenarioLinks + if(ixScenario != 0, ' | ', '') + \
            if(scenarioLinkName == scenarioName, scenarioLinkName, '[' + scenarioLinkName + "](#var.vScenario='" + scenarioLinkName + "')")
        ixScenario = ixScenario + 1
    jumpif (ixScenario < ixScenarioMax) scenarioLinksLoop

    # Fetch the TESPO input
    await input = schemaValidate(tespoTypes, 'TespoInput', fetch(inputURL))

    # Compute the TESPO output
    output = schemaValidate(tespoTypes, 'TespoOutput', tespo(input))

    # Main display
    markdownPrint( \
        '# T.E.S.P.O. (Tesla Energy Self-Powered Optimizer)', \
        '', \
        scenarioLinks, \
        '', \
        '**Scenario:** ' + scenarioName, \
        '', \
        '### Output', \
        '', \
        '~~~', \
        jsonStringify(output, 4), \
        '~~~', \
        '', \
        '### Input', \
        '', \
        '~~~', \
        jsonStringify(input, 4), \
        '~~~', \
        '', \
        '## Schema Documentation', \
        '', \
        '[Input Schema Documentation](#var.vDocInput=1)', \
        '', \
        '[Output Schema Documentation](#var.vDocOutput=1)' \
    )
endfunction


# TESPO constants
spillLimit = 90
minChargingLimit = 50
maxChargingLimit = 90


# The TESPO algorithm
function tespo(input)
    solarPower = objectGet(input, 'solarPower')
    homePower = objectGet(input, 'homePower')
    homeBattery = objectGet(input, 'homeBattery')
    vehicles = objectGet(input, 'vehicles')
    vehiclesLength = arrayLength(vehicles)

    # Compute the available solar power (remove current vehicle charging power)
    availableSolar = solarPower - homePower
    ixVehicle = 0
    availableSolarLoop:
        vehicle = arrayGet(vehicles, ixVehicle)
        chargingRate = objectGet(vehicle, 'chargingRate')
        chargingRates = objectGet(vehicle, 'chargingRates')
        chargingPowers = objectGet(vehicle, 'chargingPowers')
        chargingPower = if(arrayGet(vehicle, 'charging'), arrayGet(chargingPowers, arrayNearest(chargingRates, chargingRate)), 0)
        availableSolar = availableSolar + chargingPower
        ixVehicle = ixVehicle + 1
    jumpif (ixVehicle < vehiclesLenght) availableSolarLoop

    # Add the charging action for each vehicle
    actions = arrayNew()
    output = objectNew('actions', actions)
    ixVehicle = 0
    vehicleLoop:
        vehicle = arrayGet(vehicles, ixVehicle)
        battery = objectGet(vehicle, 'battery')
        chargingRates = objectGet(vehicle, 'chargingRates')
        chargingPowers = objectGet(vehicle, 'chargingPowers')

        # Set vehicle charging off
        actionCharging = false
        actionChargingRate = arrayGet(chargingRates, arrayLength(chargingRates) - 1)
        actionChargingLimit = minChargingLimit

        # Home battery not yet fully charged?
        jumpif (homeBattery < spillLimit) vehicleDone

        # Vehicle fully charged?
        jumpif (battery >= maxChargingLimit) vehicleDone

        # Enough solar power to charge the vehicle?
        jumpif (arrayGet(chargingPowers, 0) >= availableSolar) vehicleDone

        # Compute the vehicle charging power
        ixChargingPower = arrayNearest(chargingPowers, availableSolar)
        chargingPower = arrayGet(chargingPowers, ixChargingPower)

        # Reduce the available solar power
        availableSolar = availableSolar - chargingPower

        # Charge the vehicle
        actionCharging = true
        actionChargingRate = arrayGet(chargingRates, ixChargingPower)
        actionChargingLimit = maxChargingLimit

        vehicleDone:
        arrayPush(actions, objectNew('vehicleCharging', objectNew( \
            'id', objectGet(vehicle, 'id'), \
            'charging', actionCharging, \
            'chargingRate', actionChargingRate, \
            'chargingLimit', actionChargingLimit \
        )))
        ixVehicle = ixVehicle + 1
    jumpif (ixVehicle < vehiclesLength) vehicleLoop
    return output
endfunction


function arrayNearest(array, value)
    arrayLen = arrayLength(array)
    ixValue = 0
    arrayLoop:
        arrayValue = arrayGet(array, ixValue)
        jumpif (arrayValue == value) found
        jumpif (arrayValue > value) foundNear
        ixValue = ixValue + 1
    jumpif (ixValue < arrayLen) arrayLoop
    foundNear:
    return ixValue - 1

    found:
    return ixValue
endfunction


await main()
~~~
