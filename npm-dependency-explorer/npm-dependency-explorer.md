~~~ markdown-script
# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

include 'semver.mds'


# The npm Dependency Explorer main entry point
async function ndeMain()
    # Variable arguments
    packageName = if(vName != null && stringLength(vName) > 0, vName)
    packageVersion = if(vVersion != null && stringLength(vVersion) > 0, vVersion)
    dependencyKey = objectGet(ndeDependencyTypeKeys, vType)
    dependencyType = if(dependencyKey != null, vType, 'Package')
    dependencyKey = if(dependencyKey != null, dependencyKey, objectGet(ndeDependencyTypeKeys, dependencyType))

    # Fetch the package data
    packageData = if(packageName != null, fetch(ndePackageDataURL(packageName)))
    packages = objectNew(packageName, packageData)
    semvers = objectNew(packageName, semverVersions(objectKeys(objectGet(packageData, 'versions'))))
    packageVersionLatest = ndePackageVersionLatest(packageData)
    packageVersion = if(packageVersion != null, packageVersion, if(packageData != null, packageVersionLatest))
    packageJSON = if(packageData != null && packageVersion != null, ndePackageJSON(packageData, packageVersion))
    if(packageJSON != null, ndeFetchPackageData(packages, semvers, arrayNew(packageJSON), dependencyKey, objectNew()))

    # Render the menu
    currentURL = ndeLink(objectNew())
    markdownPrint(if(currentURL != '#var=', '[Home](#var=)', 'Home') + ' | [About](#url=README.md)')

    # Render the title
    title = 'npm Dependency Explorer'
    markdownPrint('', '# ' + markdownEscape(title))
    setDocumentTitle(title + if(packageJSON != null, ' - ' + packageName, ''))

    # If no package is loaded, render the package selection form
    jumpif (packageJSON != null) packageOK
        # Render the search form
        elementModelRender(arrayNew( \
            objectNew('html', 'p', 'elem', objectNew('html', 'b', 'elem', objectNew('text', 'Package Name:'))), \
            objectNew('html', 'p', 'elem', objectNew( \
                'html', 'input', \
                'attr', objectNew( \
                    'autocomplete', 'off', \
                    'id', 'package-name-text', \
                    'style', 'font-size: inherit; border: thin solid black; padding: 0.4em;', \
                    'type', 'text', \
                    'value', if(packageName != null, packageName, ''), \
                    'size', '32' \
                ), \
                'callback', objectNew('keyup', ndePackageNameOnKeyup) \
            )), \
            objectNew('html', 'p', 'elem', objectNew( \
                'html', 'a', \
                'attr', objectNew('style', 'cursor: pointer; user-select: none;'), \
                'elem', objectNew('text', 'Explore Dependencies'), \
                'callback', objectNew('click', ndePackageNameOnClick) \
            )) \
        ))
        setDocumentFocus('package-name-text')

        # Render error messages
        if(packageName != null && packageData == null, \
            markdownPrint('', '**Error:** Unknown package "' + packageName + '"'))
        if(packageName != null && packageData != null && packageJSON == null, \
            markdownPrint('', '**Error:** Unknown version "' + packageVersion + '" of package "' + packageName + '"'))

        return
    packageOK:

    # Load all dependencies and compute the dependency statistics
    dependencyStats = ndePackageStats(packages, semvers, packageName, packageVersion, dependencyKey)
    dependenciesFiltered = objectGet(dependencyStats, if(vDirect, 'dependenciesDirect', 'dependencies'))
    warnings = objectGet(dependencyStats, 'warnings')

    # Render the package header
    markdownPrint( \
        '', \
        '## [' + markdownEscape(packageName) + '](' + ndePackagePageURL(packageName) + ')', \
        '', \
        '**Description:** ' + markdownEscape(objectGet(packageJSON, 'description')) + if(!vVersionSelect, ' \\', ''), \
        if(!vVersionSelect, '**Version:** ' + markdownEscape(packageVersion), '') + \
            ' ([select](' + ndeLink(objectNew('versionSelect', 1)) + '))' \
    )

    # Render the package version selection links, if requested
    jumpif (!vVersionSelect) versionOK
        markdownPrint('', '### Versions')
        packageSemvers = arrayCopy(objectGet(semvers, packageName))
        packageSemvers = arraySort(packageSemvers, semverCompareReversed)
        ixSemver = 0
        semverLoop:
            semver = semverStringify(arrayGet(packageSemvers, ixSemver))
            markdownPrint('', '[' + markdownEscape(semver) + '](' + ndeLink(objectNew('version', semver)) + ')' + \
                if(semver == packageVersionLatest, ' (latest)', ''))
            ixSemver = ixSemver + 1
        jumpif (ixSemver < arrayLength(packageSemvers)) semverLoop
        return
    versionOK:

    # Compute the showing links
    linkAll = if(!vDirect, 'All', '[All](' + ndeLink(objectNew('direct', 0)) + ')')
    linkDirect = if(vDirect, 'Direct', '[Direct](' + ndeLink(objectNew('direct', 1)) + ')')

    # Compute the sort links
    linkSortName = if(vSort != 'Dependencies', 'Name', '[Name](' + ndeLink(objectNew('sort', '')) + ')')
    linkSortDependencies = if(vSort == 'Dependencies', 'Dependencies', '[Dependencies](' + ndeLink(objectNew('sort', 'Dependencies')) + ')')

    # Compute the dependency type links
    linkPackage = if(dependencyType == 'Package', 'Package', '[Package](' + ndeLink(objectNew('type', '')) + ')')
    linkDevelopment = if(dependencyType == 'Development', 'Development', '[Development](' + ndeLink(objectNew('type', 'Development')) + ')')
    linkOptional = if(dependencyType == 'Optional', 'Optional', '[Optional](' + ndeLink(objectNew('type', 'Optional')) + ')')
    linkPeer = if(dependencyType == 'Peer', 'Peer', '[Peer](' + ndeLink(objectNew('type', 'Peer')) + ')')

    # Render the package dependency stats
    dependenciesDescriptor = if(dependencyType != 'Package', '*' + stringLower(dependencyType) + '* ', '')
    markdownPrint( \
        '', \
        '**Direct ' + dependenciesDescriptor + 'dependencies:** ' + objectGet(dependencyStats, 'countDirect') + ' \\', \
        '**Total ' + dependenciesDescriptor + 'dependencies:** ' + objectGet(dependencyStats, 'count'), \
        '', \
        '**Showing:** ' + linkAll + ' | ' + linkDirect + ' \\',  \
        '**Sort:** ' + linkSortName + ' | ' + linkSortDependencies + ' \\', \
        '**Dependency type:** ' + linkPackage + ' | ' + linkDevelopment + ' | ' + linkOptional + ' | ' + linkPeer \
    )

    # Render warnings
    jumpif (arrayLength(warnings) == 0) warningsDone
        markdownPrint( \
            '', \
            '### Warnings', \
            '', \
            'There are ' + arrayLength(warnings) + ' warnings.' + stringFromCharCode(160), \
            '[' + if(vWarn, 'Hide', 'Show') + '](' + ndeLink(objectNew('warn', !vWarn)) + ')' \
        )
        jumpif (!vWarn) warningsDone
        ixWarning = 0
        warningLoop:
            warning = arrayGet(warnings, ixWarning)
            markdownPrint('', '- ' + warning)
            ixWarning = ixWarning + 1
        jumpif (ixWarning < arrayLength(warnings)) warningLoop
    warningsDone:

    # Render the dependency table
    dependenciesTable = arrayCopy(dependenciesFiltered)
    jumpif (arrayLength(dependenciesTable) == 0) tableDone
        # Add the dependency count field
        dataCalculatedField(dependenciesTable, 'Dependencies', \
            'ndePackageDependencyCount(packages, semvers, Package, Version)', \
            objectNew('packages', packages, 'semvers', semvers))

        # Sort the table data
        sortFields = arrayNew()
        if(vSort == 'Dependencies', arrayPush(sortFields, arrayNew('Dependencies', 1)))
        arrayExtend(sortFields, arrayNew( \
            arrayNew('Package'), \
            arrayNew('Version'), \
            arrayNew('Dependent'), \
            arrayNew('Dependent Version') \
        ))
        dataSort(dependenciesTable, sortFields)

        # Make the name field links
        dataCalculatedField(dependenciesTable, 'Package', \
            "'[' + markdownEscape(Package) + '](' + ndeLink(objectNew('name', Package, 'version', Version, 'type', '')) + ')'")
        dataCalculatedField(dependenciesTable, 'Dependent', \
            "'[' + markdownEscape(Dependent) + '](' + ndeLink(objectNew('name', Dependent, 'version', [Dependent Version], 'type', '')) + ')'")

        # Render the dependencies table
        markdownPrint('### ' + if(dependencyType != 'Package', dependencyType, '') + ' Dependencies')
        dataTable(dependenciesTable, objectNew( \
            'categories', arrayNew('Package', 'Version'), \
            'fields', if(arrayLength(dataFilter(dependenciesTable, 'Latest != ""')) > 0, \
                arrayNew('Latest', 'Range', 'Dependent', 'Dependent Version', 'Dependencies'), \
                arrayNew('Range', 'Dependent', 'Dependent Version', 'Dependencies') \
            ), \
            'markdown', arrayNew('Package', 'Dependent') \
        ))
    tableDone:
endfunction


# Map of type argument string to npm package JSON dependency map key
ndeDependencyTypeKeys = objectNew( \
    'Development', 'devDependencies', \
    'Optional', 'optionalDependencies', \
    'Package', 'dependencies', \
    'Peer', 'peerDependencies' \
)


# Helper to create application links
function ndeLink(args)
    # Arguments overrides
    name = objectGet(args, 'name')
    version = objectGet(args, 'version')
    versionSelect = objectGet(args, 'versionSelect')
    type = objectGet(args, 'type')
    direct = objectGet(args, 'direct')
    sort = objectGet(args, 'sort')
    warn = objectGet(args, 'warn')

    # Variable arguments
    name = if(name != null, name, vName)
    version = if(version != null, version, vVersion)
    type = if(type != null, type, vType)
    direct = if(direct != null, direct, vDirect)
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
    if(name != null, arrayPush(parts, "var.vName='" + encodeURIComponent(name) + "'"))
    if(sort != null, arrayPush(parts, "var.vSort='" + encodeURIComponent(sort) + "'"))
    if(type != null, arrayPush(parts, "var.vType='" + encodeURIComponent(type) + "'"))
    if(version != null, arrayPush(parts, "var.vVersion='" + encodeURIComponent(version) + "'"))
    if(versionSelect != null && versionSelect, arrayPush(parts, 'var.vVersionSelect=1'))
    if(warn != null && warn, arrayPush(parts, 'var.vWarn=1'))
    return if(arrayLength(parts) != 0, '#' + arrayJoin(parts, '&'), '#var=')
endfunction


# Package name button on-click handler
function ndePackageNameOnClick()
    packageName = stringTrim(getDocumentInputValue('package-name-text'))
    setWindowLocation(ndeLink(objectNew('name', packageName, 'version', '', 'type', '', 'direct', 0, 'sort', '')))
endfunction


# Package name text input on-keyup handler
function ndePackageNameOnKeyup(keyCode)
    if(keyCode == 13, ndePackageNameOnClick())
endfunction


# Helper to recursively load package data
async function ndeFetchPackageData(packages, semvers, packageJSONs, dependencyKey, completed)
    # Compute the unloaded dependencies for the given package JSON
    unloaded = objectNew()
    ixPackage = 0
    packageLoop:
        packageJSON = arrayGet(packageJSONs, ixPackage)

        # Get the package dependencies
        packageDependencies = objectGet(packageJSON, dependencyKey)
        jumpif (packageDependencies == null) packageContinue
        dependencyNames = objectKeys(packageDependencies)
        jumpif (arrayLength(dependencyNames) == 0) packageContinue

        # Add to the unloaded dependencies
        ixDependency = 0
        dependencyLoop:
            dependencyName = arrayGet(dependencyNames, ixDependency)
            dependencyRange = objectGet(packageDependencies, dependencyName)

            # Has this dependency/range been processed?
            if(!objectHas(completed, dependencyName), objectSet(completed, dependencyName, objectNew()))
            completedRanges = objectGet(completed, dependencyName)
            jumpif (objectHas(completedRanges, dependencyRange)) dependencyContinue
            objectSet(completedRanges, dependencyRange, true)

            # Add the unloaded dependency range
            if(!objectHas(unloaded, dependencyName), objectSet(unloaded, dependencyName, objectNew()))
            dependencyRanges = objectGet(unloaded, dependencyName)
            objectSet(dependencyRanges, dependencyRange, true)

            dependencyContinue:
            ixDependency = ixDependency + 1
        jumpif (ixDependency < arrayLength(dependencyNames)) dependencyLoop

        packageContinue:
        ixPackage = ixPackage + 1
    jumpif (ixPackage < arrayLength(packageJSONs)) packageLoop

    # Compute the package data URLs for the unloaded dependencies
    unloadedNames = objectKeys(unloaded)
    unloadedURLs = arrayNew()
    unloadedURLNames = arrayNew()
    jumpif (arrayLength(unloadedNames) == 0) unloadedDone
        ixUnloaded = 0
        unloadedLoop:
            unloadedName = arrayGet(unloadedNames, ixUnloaded)
            if(!objectHas(packages, unloadedName), arrayPush(unloadedURLs, ndePackageDataURL(unloadedName)))
            if(!objectHas(packages, unloadedName), arrayPush(unloadedURLNames, unloadedName))
            ixUnloaded = ixUnloaded + 1
        jumpif (ixUnloaded < arrayLength(unloadedNames)) unloadedLoop
    unloadedDone:

    # Fetch the unloaded depedency data
    jumpif (arrayLength(unloadedURLs) == 0) fetchDone
        loaded = fetch(unloadedURLs)
        ixLoaded = 0
        fetchLoop:
            dependencyName = arrayGet(unloadedURLNames, ixLoaded)
            dependencyData = arrayGet(loaded, ixLoaded)
            objectSet(packages, dependencyName, dependencyData)
            objectSet(semvers, dependencyName, semverVersions(objectKeys(objectGet(dependencyData, 'versions'))))
            ixLoaded = ixLoaded + 1
        jumpif (ixLoaded < arrayLength(unloadedURLs)) fetchLoop
    fetchDone:

    # Compute the unloaded dedendencies' depdencies
    jumpif (arrayLength(unloadedNames) == 0) dependsDone
        # Get the array of unloaded package JSON
        unloadedJSONs = arrayNew()
        ixUnloaded = 0
        dependsLoop:
            unloadedName = arrayGet(unloadedNames, ixUnloaded)
            unloadedData = objectGet(packages, unloadedName)
            jumpif (unloadedData == null) dependsContinue
            unloadedSemvers = objectGet(semvers, unloadedName)

            # Iterate each unloaded range
            unloadedRanges = objectKeys(objectGet(unloaded, unloadedName))
            ixRange = 0
            rangeLoop:
                unloadedRange = arrayGet(unloadedRanges, ixRange)
                unloadedVersion = ndePackageVersion(unloadedData, unloadedSemvers, unloadedRange)
                unloadedJSON = if(unloadedVersion != null, ndePackageJSON(unloadedData, unloadedVersion))
                if(unloadedJSON != null, arrayPush(unloadedJSONs, unloadedJSON))
                ixRange = ixRange + 1
            jumpif (ixRange < arrayLength(unloadedRanges)) rangeLoop

            dependsContinue:
            ixUnloaded = ixUnloaded + 1
        jumpif (ixUnloaded < arrayLength(unloadedNames)) dependsLoop

        # Compute the dependencies' dependencies
        ndeFetchPackageData(packages, semvers, unloadedJSONs, 'dependencies', completed)
    dependsDone:
endfunction


# Helper to get a package's total dependency count
function ndePackageDependencyCount(packages, semvers, packageName, packageVersion)
    dependencies = arrayNew()
    warnings = arrayNew()
    ndePackageDependencies(packages, semvers, dependencies, warnings, packageName, packageVersion, 'dependencies', objectNew())
    dependenciesTotal = dataAggregate(dependencies, objectNew( \
        'categories', arrayNew('Package', 'Version'), \
        'measures', arrayNew( \
            objectNew('field', 'Count', 'function', 'count') \
        ) \
    ))
    return arrayLength(dependenciesTotal)
endfunction


# Helper to get a package's total and direct dependencies with warnings
function ndePackageStats(packages, semvers, packageName, packageVersion, dependencyKey)
    # Get the package dependencies
    dependencies = arrayNew()
    warnings = arrayNew()
    ndePackageDependencies(packages, semvers, dependencies, warnings, packageName, packageVersion, dependencyKey, objectNew())

    # Compute the dependency statistics
    dependenciesDirect = dataFilter(dependencies, 'Direct')
    dependenciesTotal = dataAggregate(dependencies, objectNew( \
        'categories', arrayNew('Package', 'Version'), \
        'measures', arrayNew( \
            objectNew('field', 'Count', 'function', 'count') \
        ) \
    ))

    # Multiple-dependency-version warning?
    dependenciesMultiple = dataFilter( \
        dataAggregate(dependenciesTotal, objectNew( \
            'categories', arrayNew('Package'), \
            'measures', arrayNew( \
                objectNew('field', 'Count', 'function', 'count') \
            ) \
        )), \
        'Count > 1' \
    )
    jumpif (arrayLength(dependenciesMultiple) == 0) multipleOK
        dataSort(dependenciesTotal, arrayNew(arrayNew('Package'), arrayNew('Version')))
        dataSort(dependenciesMultiple, arrayNew(arrayNew('Package'), arrayNew('Version')))
        ixDependency = 0
        multipleLoop:
            dependency = objectGet(arrayGet(dependenciesMultiple, ixDependency), 'Package')
            dependencyVersions = dataFilter(dependenciesTotal, 'Package == dependency', objectNew('dependency', dependency))
            versions = arrayNew()
            ixVersion = 0
            versionLoop:
                arrayPush(versions, '"' + objectGet(arrayGet(dependencyVersions, ixVersion), 'Version') + '"')
                ixVersion = ixVersion + 1
            jumpif (ixVersion < arrayLength(dependencyVersions)) versionLoop
            arrayPush(warnings, 'Multiple versions of package "' + dependency + '" (' + arrayJoin(versions, ', ') + ')')
            ixDependency = ixDependency + 1
        jumpif (ixDependency < arrayLength(dependenciesMultiple)) multipleLoop
    multipleOK:

    # Return the dependency statistics
    return objectNew( \
        'count', arrayLength(dependenciesTotal), \
        'countDirect', arrayLength(dependenciesDirect), \
        'dependencies', dependencies, \
        'dependenciesDirect', dependenciesDirect, \
        'warnings', warnings \
    )
endfunction


# Helper to compute an npm package's dependency data table
function ndePackageDependencies(packages, semvers, dependencies, warnings, packageName, packageVersion, dependencyKey, completed)
    isDirect = arrayLength(objectKeys(completed)) == 0

    # Package and version already loaded?
    if(!objectHas(completed, packageName), objectSet(completed, packageName, objectNew()))
    completedVersions = objectGet(completed, packageName)
    jumpif (!objectHas(completedVersions, packageVersion)) completedDone
        return
    completedDone:
    objectSet(completedVersions, packageVersion, true)

    # Get the package dependencies object
    packageData = objectGet(packages, packageName)
    packageJSON = ndePackageJSON(packageData, packageVersion)
    packageDependencies = objectGet(packageJSON, dependencyKey)
    dependencyNames = if(packageDependencies != null, objectKeys(packageDependencies))
    jumpif (packageDependencies != null && arrayLength(dependencyNames) > 0) dependenciesOK
        return
    dependenciesOK:

    # Add the package dependency rows
    ixDependencyName = 0
    nameLoop:
        # Determine the dependency version
        dependencyName = arrayGet(dependencyNames, ixDependencyName)
        dependencyRange = objectGet(packageDependencies, dependencyName)
        dependencyData = objectGet(packages, dependencyName)
        dependencySemvers = objectGet(semvers, dependencyName)
        if(dependencyData == null, \
            arrayPush(warnings, 'Failed to load package data for "' + dependencyName + '"'))
        dependencyVersion = if(dependencyData != null, ndePackageVersion(dependencyData, dependencySemvers, dependencyRange))
        dependencyLatest = ndePackageVersionLatest(dependencyData)
        if(dependencyData != null && dependencyVersion == null, \
            arrayPush(warnings, 'Unknown version "' + dependencyVersion + '" of package "' + dependencyName + '"'))
        jumpif (dependencyVersion == null) versionDone
            # Add the dependency row
            arrayPush(dependencies, objectNew( \
                'Package', dependencyName, \
                'Version', dependencyVersion, \
                'Latest', if(dependencyVersion == dependencyLatest, '', dependencyLatest), \
                'Range', dependencyRange, \
                'Dependent', packageName, \
                'Dependent Version', packageVersion, \
                'Direct', isDirect \
            ))

            # Add the dependency's dependencies
            ndePackageDependencies(packages, semvers, dependencies, warnings, dependencyName, dependencyVersion, 'dependencies', completed)
        versionDone:

        ixDependencyName = ixDependencyName + 1
    jumpif (ixDependencyName < arrayLength(dependencyNames)) nameLoop
endfunction


# Helper to create an npm package page URL
function ndePackagePageURL(packageName)
    return 'https://www.npmjs.com/package/' + packageName
endfunction


# Helper to create an npm package data URL
function ndePackageDataURL(packageName)
    return 'https://registry.npmjs.org/' + encodeURIComponent(packageName)
endfunction


# Helper to get a package version's JSON
function ndePackageJSON(packageData, packageVersion)
    return objectGet(objectGet(packageData, 'versions'), packageVersion)
endfunction


# Helper to get a package's latest version
function ndePackageVersionLatest(packageData)
    return objectGet(objectGet(packageData, 'dist-tags'), 'latest')
endfunction


# Helper to compute a package's version from a SemVer range
function ndePackageVersion(packageData, packageSemvers, range)
    semver = semverMatch(packageSemvers, range)
    if (semver == null, debugLog('nde: Unrecognized SemVer range "' + range + '"'))
    return if(semver != null, semverStringify(semver), ndePackageVersionLatest(packageData))
endfunction


# Call the main entry point
ndeMain()
~~~
