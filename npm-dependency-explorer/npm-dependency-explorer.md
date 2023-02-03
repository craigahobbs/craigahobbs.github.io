~~~ markdown-script
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
    packageVersion = if(packageVersion != null, packageVersion, if(packageData != null, ndePackageVersionLatest(packageData)))
    packageJSON = if(packageData != null, ndePackageJSON(packageData, packageVersion))
    if(packageJSON != null, ndeFetchPackageData(packages, arrayNew(packageJSON), dependencyKey, objectNew()))

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
                    'size', '36' \
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

    # Get the package dependencies
    dependencies = arrayNew()
    warnings = arrayNew()
    ndePackageDependencies(packages, dependencies, warnings, packageName, packageVersion, dependencyKey, objectNew())

    # Compute the dependency statistics
    dependenciesDirect = dataFilter(dependencies, 'Direct')
    dependenciesTotal = dataAggregate(dependencies, objectNew( \
        'categories', arrayNew('PackageName', 'PackageVersion'), \
        'measures', arrayNew( \
            objectNew('field', 'DependentName', 'function', 'count', 'name', 'Count') \
        ) \
    ))

    # Compute the showing links
    linkAll = if(!vDirect, 'All', '[All](' + ndeLink(objectNew('direct', 0)) + ')')
    linkDirect = if(vDirect, 'Direct', '[Direct](' + ndeLink(objectNew('direct', 1)) + ')')

    # Compute the dependency type links
    linkPackage = if(dependencyType == 'Package', 'Package', '[Package](' + ndeLink(objectNew('type', '')) + ')')
    linkDevelopment = if(dependencyType == 'Development', 'Development', '[Development](' + ndeLink(objectNew('type', 'Development')) + ')')
    linkOptional = if(dependencyType == 'Optional', 'Optional', '[Optional](' + ndeLink(objectNew('type', 'Optional')) + ')')
    linkPeer = if(dependencyType == 'Peer', 'Peer', '[Peer](' + ndeLink(objectNew('type', 'Peer')) + ')')

    # Report the package name and dependency stats
    dependenciesDescriptor = if(dependencyType != 'Package', '*' + stringLower(dependencyType) + '* ', '')
    markdownPrint( \
        '', \
        '## [' + markdownEscape(packageName) + '](' + ndePackagePageURL(packageName) + ')', \
        '', \
        '**Description:** ' + markdownEscape(objectGet(packageJSON, 'description')) + ' \\', \
        '**Version:** ' + markdownEscape(packageVersion), \
        '', \
        '**Direct ' + dependenciesDescriptor + 'dependencies:** ' + arrayLength(dependenciesDirect) + ' \\', \
        '**Total ' + dependenciesDescriptor + 'dependencies:** ' + arrayLength(dependenciesTotal), \
        '', \
        '**Showing:** ' + linkAll + ' | ' + linkDirect + ' \\',  \
        '**Dependency type:** ' + linkPackage + ' | ' + linkDevelopment + ' | ' + linkOptional + ' | ' + linkPeer \
    )

    # Render warnings
    jumpif (arrayLength(warnings) == 0) warningsDone
        markdownPrint('', '### Warnings')
        ixWarning = 0
        warningLoop:
            warning = arrayGet(warnings, ixWarning)
            markdownPrint('', '- ' + warning)
            ixWarning = ixWarning + 1
        jumpif (ixWarning < arrayLength(warnings)) warningLoop
    warningsDone:

    # Render the dependency table
    dependenciesTable = if(!vDirect, dependencies, dependenciesDirect)
    jumpif (arrayLength(dependenciesTable) == 0) tableDone
        # Sort the table data
        dataSort(dependenciesTable, arrayNew( \
            arrayNew('PackageName'), \
            arrayNew('PackageVersion'), \
            arrayNew('DependentName'), \
            arrayNew('DependentVersion') \
        ))

        # Make the name field links
        ixRow = 0
        rowLoop:
            row = arrayGet(dependenciesTable, ixRow)
            rowPackageName = objectGet(row, 'PackageName')
            rowPackageVersion = objectGet(row, 'PackageVersion')
            rowPackageLink = ndeLink(objectNew('name', rowPackageName, 'version', rowPackageVersion, 'type', ''))
            rowDependentName = objectGet(row, 'DependentName')
            rowDependentVersion = objectGet(row, 'DependentVersion')
            rowDependentLink = ndeLink(objectNew('name', rowDependentName, 'version', rowDependentVersion, 'type', ''))
            objectSet(row, 'PackageName', '[' + markdownEscape(rowPackageName) + '](' + rowPackageLink + ')')
            objectSet(row, 'DependentName', '[' + markdownEscape(rowDependentName) + '](' + rowDependentLink + ')')
            ixRow = ixRow + 1
        jumpif (ixRow < arrayLength(dependenciesTable)) rowLoop

        # Render the dependencies table
        markdownPrint('### ' + if(dependencyType != 'Package', dependencyType, '') + ' Dependencies')
        dataTable(dependenciesTable, objectNew( \
            'categories', arrayNew('PackageName', 'PackageVersion'), \
            'fields', arrayNew('DependentName', 'DependentVersion'), \
            'markdown', arrayNew('PackageName', 'DependentName') \
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
    type = objectGet(args, 'type')
    direct = objectGet(args, 'direct')

    # Variable arguments
    name = if(name != null, name, vName)
    version = if(version != null, version, vVersion)
    type = if(type != null, type, vType)
    direct = if(direct != null, direct, vDirect)

    # Cleared arguments
    name = if(name != null && stringLength(name) > 0, name)
    version = if(version != null && stringLength(version) > 0, version)
    type = if(type != null && stringLength(type) > 0, type)

    # Create the link
    parts = arrayNew()
    if(name != null, arrayPush(parts, "var.vName='" + encodeURIComponent(name) + "'"))
    if(version != null, arrayPush(parts, "var.vVersion='" + encodeURIComponent(version) + "'"))
    if(type != null, arrayPush(parts, "var.vType='" + encodeURIComponent(type) + "'"))
    if(direct != null && direct, arrayPush(parts, 'var.vDirect=1'))
    return if(arrayLength(parts) != 0, '#' + arrayJoin(parts, '&'), '#var=')
endfunction


# Package name button on-click handler
function ndePackageNameOnClick()
    packageName = getDocumentInputValue('package-name-text')
    setWindowLocation(ndeLink(objectNew('name', packageName, 'version', '', 'type', '', 'direct', 0)))
endfunction


# Package name text input on-keyup handler
function ndePackageNameOnKeyup(keyCode)
    if(keyCode == 13, ndePackageNameOnClick())
endfunction


# Helper to recursively load package data
async function ndeFetchPackageData(packages, packageJSONs, dependencyKey, completed)
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
            dependencySemver = objectGet(packageDependencies, dependencyName)

            # Has this dependency/semver been processed?
            if(!objectHas(completed, dependencyName), objectSet(completed, dependencyName, objectNew()))
            completedSemvers = objectGet(completed, dependencyName)
            jumpif (objectHas(completedSemvers, dependencySemver)) dependencyContinue
            objectSet(completedSemvers, dependencySemver, true)

            # Add the unloaded dependency semver
            if(!objectHas(unloaded, dependencyName), objectSet(unloaded, dependencyName, objectNew()))
            dependencySemvers = objectGet(unloaded, dependencyName)
            objectSet(dependencySemvers, dependencySemver, true)

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

            # Iterate each unloaded semver
            unloadedSemvers = objectKeys(objectGet(unloaded, unloadedName))
            ixSemver = 0
            semverLoop:
                unloadedSemver = arrayGet(unloadedSemvers, ixSemver)
                unloadedVersion = ndePackageVersion(unloadedData, unloadedSemver)
                unloadedJSON = if(unloadedVersion != null, ndePackageJSON(unloadedData, unloadedVersion))
                if(unloadedJSON != null, arrayPush(unloadedJSONs, unloadedJSON))
                ixSemver = ixSemver + 1
            jumpif (ixSemver < arrayLength(unloadedSemvers)) semverLoop

            dependsContinue:
            ixUnloaded = ixUnloaded + 1
        jumpif (ixUnloaded < arrayLength(unloadedNames)) dependsLoop

        # Compute the dependencies' dependencies
        ndeFetchPackageData(packages, unloadedJSONs, 'dependencies', completed)
    dependsDone:
endfunction


# Helper to compute an npm package's dependency data table
async function ndePackageDependencies(packages, dependencies, warnings, packageName, packageVersion, dependencyKey, completed)
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
        dependencySemver = objectGet(packageDependencies, dependencyName)
        dependencyData = objectGet(packages, dependencyName)
        if(dependencyData == null, \
            arrayPush(warnings, 'Failed to load package data for "' + dependencyName + '"'))
        dependencyVersion = if(dependencyData != null, ndePackageVersion(dependencyData, dependencySemver))
        if(dependencyData != null && dependencyVersion == null, \
            arrayPush(warnings, 'Unknown version "' + dependencyVersion + '" of package "' + dependencyName + '"'))
        jumpif (dependencyVersion == null) versionDone
            # Add the dependency row
            arrayPush(dependencies, objectNew( \
                'PackageName', dependencyName, \
                'PackageVersion', dependencyVersion, \
                'DependentName', packageName, \
                'DependentVersion', packageVersion, \
                'Direct', isDirect \
            ))

            # Add the dependency's dependencies
            ndePackageDependencies(packages, dependencies, warnings, dependencyName, dependencyVersion, 'dependencies', completed)
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


# Helper to compute a package's version from an npm semver
function ndePackageVersion(packageData, semver)
    return if(semver, ndePackageVersionLatest(packageData), ndePackageVersionLatest(packageData))
endfunction


# Call the main entry point
ndeMain()
~~~
