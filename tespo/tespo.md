~~~ markdown-script
# The TESPO JSON data schema
tespoDataTypes = schemaParse( \
    '# The TESPO data struct', \
    'struct TespoData', \
    '', \
    '    # Most recent by-minute solar power generation in kWh', \
    '    float[len > 0] solar', \
    '', \
    '    # Most recent by-minute home power consumption in kWh', \
    '    float[len > 0] home' \
)


# Main entry point
function main()
    # Data schema documentation?
    jumpif (!vData) main
    markdownPrint('[Home](#var=)', '')
    schemaPrint(tespoDataTypes, 'TespoData')
    return

    # Main display
    main:
    markdownPrint( \
        '# T.E.S.P.O. (Tesla Energy Self-Powered Optimizer)', \
        '', \
        'Coming soon!', \
        '', \
        '[Data Schema Documentation](#var.vData=1)' \
    )
endfunction


main()
~~~
