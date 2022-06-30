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
    input = schemaValidate(tespoTypes, 'TespoInput', fetch(inputURL))

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
        '# Tesla Energy Self-Powered Optimizer', \
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
        '~~~' \
    )
endfunction


# Input scenario name to URL map
scenarios = objectNew( \
    'AllCharged', 'input/allCharged.json', \
    'HomeCharged', 'input/homeCharged.json', \
    'HomeCharged-LowSolar', 'input/homeCharged-lowSolar.json', \
    'HomeCharged-MedSolar', 'input/homeCharged-medSolar.json', \
    'HomeCharged-ZeroSolar', 'input/homeCharged-zeroSolar.json', \
    'NoneCharged', 'input/noneCharged.json' \
)
scenarioNames = objectKeys(scenarios)
defaultScenarioName = 'AllCharged'


# The percentage at which the home battery is considered full
homeLimit = 90

# The minimum/maximum charging limits for vehicles
minChargingLimit = 50
maxChargingLimit = 90

# The minimum solar power, in kWh, that is considered excess solar power
minSolarExcess = 1


# The TESPO algorithm
function tespo(input)
    solarPower = objectGet(input, 'solarPower')
    homePower = objectGet(input, 'homePower')
    homeBattery = objectGet(input, 'homeBattery')
    vehicles = objectGet(input, 'vehicles')

    # Compute the available solar power (remove current vehicle charging power)
    availableSolar = solarPower - homePower
    ixVehicle = 0
    availableSolarLoop:
        vehicle = arrayGet(vehicles, ixVehicle)
        # P = V * I
        chargingPower = objectGet(vehicle, 'chargingRate') * objectGet(vehicle, 'chargingVoltage') / 1000
        availableSolar = availableSolar + if(objectGet(vehicle, 'chargingEnabled'), chargingPower, 0)
        ixVehicle = ixVehicle + 1
    jumpif (ixVehicle < vehiclesLenght) availableSolarLoop

    # Is the home battery charged?
    isHomeBatteryCharged = homeBattery >= homeLimit
    allBatteriesCharged = isHomeBatteryCharged

    # Add the charging action for each vehicle
    vehicleChargings = arrayNew()
    output = objectNew('vehicles', vehicleChargings)
    ixVehicle = 0
    vehicleLoop:
        vehicle = arrayGet(vehicles, ixVehicle)
        battery = objectGet(vehicle, 'battery')
        minChargingRate = objectGet(vehicle, 'minChargingRate')
        maxChargingRate = objectGet(vehicle, 'maxChargingRate')

        # Set vehicle charging off
        actionCharging = false
        actionChargingRate = maxChargingRate
        actionChargingLimit = minChargingLimit

        # Home battery not yet fully charged?
        jumpif (!isHomeBatteryCharged) vehicleDone

        # Vehicle fully charged?
        isVehicleCharged = battery >= maxChargingLimit
        allBatteriesCharged = allBatteriesCharged && isVehicleCharged
        jumpif (isVehicleCharged) vehicleDone

        # Enough solar power to charge the vehicle?
        # I = P / V
        availableSolarRate = (availableSolar * 1000) / objectGet(vehicle, 'chargingVoltage')
        bestChargingRate = 0
        chargingRateTest = minChargingRate
        chargingRateLoop:
            bestChargingRate = if(chargingRateTest <= availableSolarRate, max(bestChargingRate, chargingRateTest), bestChargingRate)
            chargingRateTest = chargingRateTest + 1
        jumpif (chargingRateTest <= maxChargingRate) chargingRateLoop
        jumpif (bestChargingRate == 0) vehicleDone

        # Charge the vehicle
        actionCharging = true
        actionChargingRate = bestChargingRate
        actionChargingLimit = maxChargingLimit

        # Reduce the available solar power
        chargingPower = actionChargingRate * chargingVoltage / 1000
        availableSolar = availableSolar - chargingPower

        vehicleDone:
        arrayPush(vehicleChargings, objectNew( \
            'id', objectGet(vehicle, 'id'), \
            'chargingEnabled', actionCharging, \
            'chargingRate', actionChargingRate, \
            'chargingLimit', actionChargingLimit \
        ))
        ixVehicle = ixVehicle + 1
    jumpif (ixVehicle < arrayLength(vehicles)) vehicleLoop

    # Set the excess solar power
    excessSolar = if(allBatteriesCharged && availableSolar > minSolarExcess, availableSolar, 0)
    objectSet(output, 'availableSolar', if(isHomeBatteryCharged, round(max(availableSolar, 0), 3), 0))
    objectSet(output, 'excessSolar', round(excessSolar, 3))

    return output
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
    '    # If true, car charging is enabled', \
    '    bool chargingEnabled', \
    '', \
    '    # The charging rate, in amps', \
    '    int(> 0) chargingRate', \
    '', \
    '    # The charging limit, as a percentage', \
    '    float(>= 0, <= 100) chargingLimit', \
    '', \
    '    # The minimum charging rate, in amps', \
    '    int(> 0) minChargingRate', \
    '', \
    '    # The maximum charging rate, in amps', \
    '    int(> 0) maxChargingRate', \
    '', \
    '    # The charging voltage, in volts', \
    '    int(> 0) chargingVoltage', \
    '', \
    '', \
    '# The Tesla Energy Self-Powered Optimizer (TESPO) service output', \
    'struct TespoOutput', \
    '', \
    '    # The vehicle-charging actions', \
    '    VehicleCharging[] vehicles', \
    '', \
    '    # The available solar power, in kWh', \
    '    float(>= 0) availableSolar', \
    '', \
    '    # The excess solar power, in kWh', \
    '    float(>= 0) excessSolar', \
    '', \
    '', \
    "# Set a vehicle's charging on or off", \
    'struct VehicleCharging', \
    '', \
    '    # The vehicle ID', \
    '    string(len > 0) id', \
    '', \
    '    # If true, car charging is enabled', \
    '    bool chargingEnabled', \
    '', \
    '    # The charging rate, in amps', \
    '    int(> 0) chargingRate', \
    '', \
    '    # The charging limit, as a percentage', \
    '    float(>= 0, <= 100) chargingLimit' \
)


# Execute the main entry point
main()
~~~
