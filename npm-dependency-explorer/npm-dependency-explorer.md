~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include 'forms.mds'
include 'npm.mds'


# The npm Dependency Explorer main entry point
async function ndeMain()
    # Variable arguments
    packageName = if(vName != null && stringLength(vName) > 0, vName, null)
    packageVersion = if(vVersion != null && stringLength(vVersion) > 0, vVersion, null)
    if objectHas(ndeDependencyTypeKeys, vType) then
        dependencyType = vType
        dependencyKey = objectGet(ndeDependencyTypeKeys, vType)
    else then
        dependencyType = 'Package'
        dependencyKey = objectGet(ndeDependencyTypeKeys, dependencyType)
    endif

    # Load the package version dependency data
    cache = npmCacheNew()
    packageJSON = null
    if packageName != null then
        packageJSON = npmLoadPackage(cache, packageName, packageVersion, dependencyKey)
        if packageJSON != null && packageVersion == null then
            packageVersion = objectGet(packageJSON, 'version')
        endif
    endif

    # Render the menu
    currentURL = ndeURL(objectNew())
    markdownPrint(if(currentURL != '#var=', '[Home](#var=)', 'Home') + ' | [About](#url=README.md)')

    # Render the title
    title = 'npm Dependency Explorer'
    markdownPrint('', '# ' + markdownEscape(title))
    setDocumentTitle(title + if(packageJSON != null, ' - ' + packageName, ''))

    # If no package is loaded, render the package selection form
    if packageJSON == null then
        ndeRenderForm(cache, packageName, packageVersion, packageJSON)
        return
    endif

    # Render the package header
    isPackageView = !(vVersionSelect || vVersionChart)
    markdownPrint( \
        '', \
        '## [' + markdownEscape(packageName) + '](' + npmPackagePageURL(packageName) + ')', \
        '', \
        '**Description:** ' + markdownEscape(objectGet(packageJSON, 'description')) + if(isPackageView, ' \\', '') \
    )
    if isPackageView then
        markdownPrint( \
            '**Version:** ' + markdownEscape(packageVersion), \
            '([versions](' + ndeCleanURL(objectNew('name', packageName, 'version', packageVersion, 'versionSelect', 1)) + ') | ', \
            '[chart](' + ndeCleanURL(objectNew('name', packageName, 'version', packageVersion, 'versionChart', 1)) + '))' \
        )
    endif

    # Render the package version selection links, if requested
    if vVersionSelect then
        ndeRenderVersionLinks(cache, packageName, packageVersion)
        return

    # Render the package version dependency chart, if requested
    else if vVersionChart then
        ndeRenderVersionChart(cache, packageName, packageVersion)
        return
    endif

    # Load all dependencies and compute the dependency statistics
    dependencyStats = npmPackageStats(cache, packageName, packageVersion, dependencyKey)
    dependenciesFiltered = objectGet(dependencyStats, if(vDirect, 'dependenciesDirect', 'dependencies'))
    warnings = objectGet(dependencyStats, 'warnings')

    # Filter to dependencies that have a newer version?
    hasLatest = arrayLength(dataFilter(dependenciesFiltered, 'Latest != ""')) > 0
    if hasLatest && vLatest then
        dependenciesFiltered = dataFilter(dependenciesFiltered, "Latest != ''")
    endif

    # Compute the direct filter links
    linkDirectAll = if(!vDirect, 'All', '[All](' + ndeURL(objectNew('direct', 0)) + ')')
    linkDirect = if(vDirect, 'Direct', '[Direct](' + ndeURL(objectNew('direct', 1)) + ')')

    # Compute the latest filter links
    linkLatestAll = if(!vLatest, 'All', '[All](' + ndeURL(objectNew('latest', 0)) + ')')
    linkLatest = if(vLatest, 'Latest', '[Latest](' + ndeURL(objectNew('latest', 1)) + ')')

    # Compute the sort links
    linkSortName = if(vSort != 'Dependencies', 'Name', '[Name](' + ndeURL(objectNew('sort', '')) + ')')
    linkSortDependencies = if(vSort == 'Dependencies', 'Dependencies', '[Dependencies](' + ndeURL(objectNew('sort', 'Dependencies')) + ')')

    # Compute the dependency type links
    linkPackage = if(dependencyType == 'Package', 'Package', '[Package](' + ndeURL(objectNew('type', '')) + ')')
    linkDevelopment = if(dependencyType == 'Development', 'Development', '[Development](' + ndeURL(objectNew('type', 'Development')) + ')')
    linkOptional = if(dependencyType == 'Optional', 'Optional', '[Optional](' + ndeURL(objectNew('type', 'Optional')) + ')')
    linkPeer = if(dependencyType == 'Peer', 'Peer', '[Peer](' + ndeURL(objectNew('type', 'Peer')) + ')')

    # Render the package dependency stats
    dependenciesDescriptor = if(dependencyType != 'Package', '*' + stringLower(dependencyType) + '* ', '')
    markdownPrint( \
        '', \
        '**Direct ' + dependenciesDescriptor + 'dependencies:** ' + objectGet(dependencyStats, 'countDirect') + ' \\', \
        '**Total ' + dependenciesDescriptor + 'dependencies:** ' + objectGet(dependencyStats, 'count'), \
        '', \
        '**Direct:** ' + linkDirectAll + ' | ' + linkDirect + ' \\' \
    )
    if hasLatest then
        markdownPrint('**Latest:** ' + linkLatestAll + ' | ' + linkLatest + ' \\')
    endif
    markdownPrint( \
        '**Sort:** ' + linkSortName + ' | ' + linkSortDependencies + ' \\', \
        '**Type:** ' + linkPackage + ' | ' + linkDevelopment + ' | ' + linkOptional + ' | ' + linkPeer \
    )

    # Render warnings
    if arrayLength(warnings) then
        markdownPrint( \
            '', \
            '### Warnings', \
            '', \
            'There are ' + arrayLength(warnings) + ' warnings.' + stringFromCharCode(160), \
            '[' + if(vWarn, 'Hide', 'Show') + '](' + ndeURL(objectNew('warn', !vWarn)) + ')' \
        )
        if vWarn then
            foreach warning in warnings do
                markdownPrint('', '- ' + markdownEscape(warning))
            endforeach
        endif
    endif

    # Render the dependency table
    dependenciesTable = arrayCopy(dependenciesFiltered)
    if arrayLength(dependenciesTable) then
        # Add the dependency count field
        dataCalculatedField(dependenciesTable, 'Dependencies', 'npmPackageDependencyCount(cache, Package, Version)', \
            objectNew('cache', cache))

        # Sort the table data
        sortFields = arrayNew(arrayNew('Package'), arrayNew('Version'), arrayNew('Dependent'), arrayNew('Dependent Version'))
        if vSort == 'Dependencies' then
            sortFields = arrayExtend(arrayNew(arrayNew('Dependencies', 1)), sortFields)
        endif
        dataSort(dependenciesTable, sortFields)

        # Make the name field links
        dataCalculatedField(dependenciesTable, 'Package', \
            "'[' + markdownEscape(Package) + '](' + ndeCleanURL(objectNew('name', Package, 'version', Version)) + ')'")
        dataCalculatedField(dependenciesTable, 'Dependent', \
            "'[' + markdownEscape(Dependent) + '](' + ndeCleanURL(objectNew('name', Dependent, 'version', [Dependent Version])) + ')'")

        # Render the dependencies table
        markdownPrint('### ' + if(dependencyType != 'Package', dependencyType, '') + ' Dependencies')
        dataTable(dependenciesTable, objectNew( \
            'categories', arrayNew('Package', 'Version'), \
            'fields', if(hasLatest, \
                arrayNew('Latest', 'Range', 'Dependent', 'Dependent Version', 'Dependencies'), \
                arrayNew('Range', 'Dependent', 'Dependent Version', 'Dependencies') \
            ), \
            'markdown', arrayNew('Package', 'Dependent') \
        ))
    endif
endfunction


# Render the package selection form
function ndeRenderForm(cache, packageName, packageVersion, packageJSON)
    # Render the search form
    elementModelRender(arrayNew( \
        objectNew('html', 'p', 'elem', objectNew('html', 'b', 'elem', objectNew('text', 'Package Name:'))), \
        objectNew('html', 'p', 'elem', formsTextElements('package-name-text', packageName, 32, ndePackageNameOnClick)), \
        objectNew('html', 'p', 'elem', formsLinkButtonElements('Explore Dependencies', ndePackageNameOnClick)) \
    ))
    setDocumentFocus('package-name-text')

    # Render error messages
    if packageName != null then
        if npmCacheGetPackage(cache, packageName) == null then
            markdownPrint('', '**Error:** Unknown package "' + markdownEscape(packageName) + '"')
        else if packageJSON == null then
            markdownPrint('', '**Error:** Unknown version "' + markdownEscape(packageVersion) + '" of package "' + \
                markdownEscape(packageName) + '"')
        endif
    endif
endfunction


# Package name button on-click handler
function ndePackageNameOnClick()
    packageName = stringTrim(getDocumentInputValue('package-name-text'))
    setWindowLocation(ndeCleanURL(objectNew('name', packageName)))
endfunction



# Render the package version links
function ndeRenderVersionLinks(cache, packageName, packageVersion)
    markdownPrint( \
        '', \
        '[Back to package](' + ndeCleanURL(objectNew('name', packageName, 'version', packageVersion)) + ')', \
        '', \
        '### Versions' \
    )
    packageSemvers = npmCacheGetPackageVersions(cache, packageName)
    packageVersionLatest = npmPackageVersionLatest(npmCacheGetPackage(cache, packageName))
    foreach packageSemver in packageSemvers do
        packageVersion = semverStringify(packageSemver)
        markdownPrint('', '[' + markdownEscape(packageVersion) + '](' + \
            ndeCleanURL(objectNew('name', packageName, 'version', packageVersion)) + ')' + \
            if(packageVersion == packageVersionLatest, ' (latest)', ''))
    endforeach
endfunction


# Render the package dependencies by version chart
async function ndeRenderVersionChart(cache, packageName, packageVersion)
    markdownPrint( \
        '', \
        '[Back to package](' + ndeCleanURL(objectNew('name', packageName, 'version', packageVersion)) + ')', \
        '', \
        '### Version Dependency Chart' \
    )

    # Load all package version dependencies
    npmLoadPackageAllVersions(cache, packageName, 'dependencies')

    # Compute the version dependency data table
    versionDependencies = arrayNew()
    packageSemvers = npmCacheGetPackageVersions(cache, packageName)
    packageSemverCount = arrayLength(packageSemvers)
    foreach packageSemver, ixSemver in packageSemvers do
        packageVersion = semverStringify(packageSemver)
        arrayPush(versionDependencies, objectNew( \
            'Version Index', packageSemverCount - ixSemver - 1, \
            'Version', packageVersion, \
            'Dependencies', npmPackageDependencyCount(cache, packageName, packageVersion) \
        ))
    endforeach

    # Render the version dependency data as a line chart and as a table
    dataLineChart(versionDependencies, objectNew( \
        'width', 800, \
        'height', 300, \
        'x', 'Version Index', \
        'y', arrayNew('Dependencies'), \
        'xTicks', objectNew('count', 5), \
        'yTicks', objectNew('count', 5), \
        'precision', 0 \
    ))
    dataSort(versionDependencies, arrayNew(arrayNew('Version Index', 1)))
    dataTable(versionDependencies)
endfunction


# Map of type argument string to npm package JSON dependency map key
ndeDependencyTypeKeys = objectNew( \
    'Development', 'devDependencies', \
    'Optional', 'optionalDependencies', \
    'Package', 'dependencies', \
    'Peer', 'peerDependencies' \
)


# Helper to create application links
function ndeURL(args)
    # Arguments overrides
    name = objectGet(args, 'name')
    version = objectGet(args, 'version')
    versionChart = objectGet(args, 'versionChart')
    versionSelect = objectGet(args, 'versionSelect')
    type = objectGet(args, 'type')
    direct = objectGet(args, 'direct')
    latest = objectGet(args, 'latest')
    sort = objectGet(args, 'sort')
    warn = objectGet(args, 'warn')

    # Variable arguments
    name = if(name != null, name, vName)
    version = if(version != null, version, vVersion)
    type = if(type != null, type, vType)
    direct = if(direct != null, direct, vDirect)
    latest = if(latest != null, latest, vLatest)
    sort = if(sort != null, sort, vSort)
    warn = if(warn != null, warn, vWarn)

    # Cleared arguments
    name = if(name != null && stringLength(name) > 0, name)
    version = if(version != null && stringLength(version) > 0, version)
    type = if(type != null && stringLength(type) > 0, type)
    sort = if(sort != null && stringLength(sort) > 0, sort)

    # Create the link
    parts = arrayNew()
    if(direct != null && direct, arrayPush(parts, 'var.vDirect=1'))
    if(latest != null && latest, arrayPush(parts, 'var.vLatest=1'))
    if(name != null, arrayPush(parts, "var.vName='" + encodeURIComponent(name) + "'"))
    if(sort != null, arrayPush(parts, "var.vSort='" + encodeURIComponent(sort) + "'"))
    if(type != null, arrayPush(parts, "var.vType='" + encodeURIComponent(type) + "'"))
    if(version != null, arrayPush(parts, "var.vVersion='" + encodeURIComponent(version) + "'"))
    if(versionChart != null && versionChart, arrayPush(parts, 'var.vVersionChart=1'))
    if(versionSelect != null && versionSelect, arrayPush(parts, 'var.vVersionSelect=1'))
    if(warn != null && warn, arrayPush(parts, 'var.vWarn=1'))
    return if(arrayLength(parts) != 0, '#' + arrayJoin(parts, '&'), '#var=')
endfunction


# Helper to create package/version application links
function ndeCleanURL(args)
    argsClean = objectNew( \
        'name', '', \
        'version', '', \
        'versionChart', 0, \
        'versionSelect', 0, \
        'type', '', \
        'direct', 0, \
        'latest', 0, \
        'sort', '', \
        'warn', 0 \
     )
    return ndeURL(objectAssign(argsClean, args))
endfunction


# Call the main entry point
ndeMain()
~~~
