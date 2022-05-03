~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

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
    scenarioName = if(vScenario != null, vScenario, defaultScenarioName)
    inputURL = objectGet(scenarios, scenarioName)
    inputURL = if(inputURL != null, inputURL, objectGet(scenarios, defaultScenarioName))

    # Fetch the TESPO input
    await input = schemaValidate(tespoTypes, 'TespoInput', fetch(inputURL))

    # Compute the TESPO output
    output = schemaValidate(tespoTypes, 'TespoOutput', tespo(input))

    # Create the scenario links markdown
    scenarioLinks = ''
    ixScenario = 0
    ixScenarioMax = arrayLength(scenarioNames)
    scenarioLinksLoop:
        scenarioLinkName = arrayGet(scenarioNames, ixScenario)
        scenarioLinks = scenarioLinks + if(ixScenario != 0, ' | ', '') + \
            if(scenarioLinkName == scenarioName, scenarioLinkName, '[' + scenarioLinkName + "](#var.vScenario='" + scenarioLinkName + "')")
        ixScenario = ixScenario + 1
    jumpif (ixScenario < ixScenarioMax) scenarioLinksLoop

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
        '[Output Schema Documentation](#var.vDocOutput=1)', \
        '', \
        '~~~', \
        jsonStringify(output, 4), \
        '~~~', \
        '', \
        '### Input', \
        '', \
        '[Input Schema Documentation](#var.vDocInput=1)', \
        '', \
        '~~~', \
        jsonStringify(input, 4), \
        '~~~', \
        '', \
        '## Information Placard' \
    )

    # Example information placard
    spillage = objectGet(output, 'spillage')
    statusSize = 100
    borderSize = 5
    setDrawingSize(statusSize, statusSize)
    drawStyle('black', borderSize, if(spillage != 0, 'lawngreen', 'red'))
    drawRect(0.5 * borderSize, 0.5 * borderSize, statusSize - borderSize, statusSize - borderSize)
    statusText = if(spillage != 0, \
        'There is currently surplus solar power (' + spillage + ' kW). Please use power freely.', \
        'Batteries are charging or discharging. Please use power wisely.')
    markdownPrint('**Status:**', statusText)
endfunction


# Input scenario name to URL map
scenarios = objectNew( \
    'AllCharged', 'data/allCharged.json', \
    'HomeCharged', 'data/homeCharged.json', \
    'HomeCharged-LowSolar', 'data/homeCharged-lowSolar.json', \
    'HomeCharged-MedSolar', 'data/homeCharged-medSolar.json', \
    'HomeCharged-ZeroSolar', 'data/homeCharged-zeroSolar.json', \
    'NoneCharged', 'data/noneCharged.json' \
)
scenarioNames = objectKeys(scenarios)
defaultScenarioName = 'AllCharged'


# The TESPO "spill limit", the percentage at which the home battery is considered full.
spillLimit = 90

# The minimum/maximum charging limits for vehicles
minChargingLimit = 50
maxChargingLimit = 90

# The minimum solar power, in kWh, that is considered solar spillage
minSolarSpillage = 2


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

    # Is the home battery charged?
    isHomeBatteryCharged = homeBattery >= spillLimit
    allBatteriesCharged = isHomeBatteryCharged

    # Add the charging action for each vehicle
    chargings = arrayNew()
    output = objectNew('chargings', chargings)
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
        jumpif (!isHomeBatteryCharged) vehicleDone

        # Vehicle fully charged?
        isVehicleCharged = battery >= maxChargingLimit
        allBatteriesCharged = allBatteriesCharged && isVehicleCharged
        jumpif (isVehicleCharged) vehicleDone

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
        arrayPush(chargings, objectNew( \
            'id', objectGet(vehicle, 'id'), \
            'charging', actionCharging, \
            'chargingRate', actionChargingRate, \
            'chargingLimit', actionChargingLimit \
        ))
        ixVehicle = ixVehicle + 1
    jumpif (ixVehicle < vehiclesLength) vehicleLoop

    # Set the solar spillage
    spillage = if(allBatteriesCharged && availableSolar > minSolarSpillage, round(availableSolar, 3), 0)
    objectSet(output, 'spillage', spillage)

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
    '    # The vehicle-charging actions', \
    '    VehicleCharging[] chargings', \
    '', \
    '    # The solar spillage, in kWh. If greater than zero, there is currently solar spillage.', \
    '    float(>= 0) spillage', \
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


# Execute the main entry point
await main()
~~~
