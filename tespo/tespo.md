~~~ markdown-script
# The TESPO data API schema
tespoDataTypes = schemaParse( \
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
    '    float(>= 0, <= 100) chargingLimit' \
)


# Main entry point
async function main()
    # Data schema documentation?
    jumpif (!vData) noDataDoc
        markdownPrint('[Home](#var=)', '')
        schemaPrint(tespoDataTypes, 'TespoData')
        return
    noDataDoc:

    # Fetch the data API
    await data = schemaValidate(tespoDataTypes, 'TespoData', fetch('data'))

    # Main display
    markdownPrint( \
        '# T.E.S.P.O. (Tesla Energy Self-Powered Optimizer)', \
        '', \
        '**Current Solar Power:**  ' + objectGet(data, 'solarPower'), \
        '', \
        '[Data Schema Documentation](#var.vData=1)' \
    )
endfunction


await main()
~~~
