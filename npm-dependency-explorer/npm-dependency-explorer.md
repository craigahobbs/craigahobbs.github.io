[Home](#var=) | [About](#url=README.md)

# npm Dependency Explorer

~~~ markdown-script
# The npm Dependency Explorer main entry point
async function ndeMain()
    # Variable arguments
    packageName = if(vName != null && stringLength(vName) > 0, vName)
    packageVersion = if(vVersion != null && stringLength(vVersion) > 0, vVersion)
    dependencyKey = objectGet(ndeDependencyTypeKeys, vType)
    dependencyType = if(dependencyKey != null, vType, 'Package')
    dependencyKey = if(dependencyKey != null, dependencyKey, objectGet(ndeDependencyTypeKeys, dependencyType))

    # Get the package dependencies
    dependencies = arrayNew()
    packages = objectNew()
    errors = arrayNew()
    if(packageName != null, \
        ndePackageDependencies(packageName, packageVersion, dependencyKey, dependencies, packages, errors, objectNew()))

    # If no package is loaded, render the package selection form
    jumpif (packageName != null) packageOK
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
        return
    packageOK:

    # Render the package name sub-heading
    markdownPrint('', '## [' + markdownEscape(packageName) + '](' + ndePackagePageURL(packageName) + ')')

    # Render error messages, if any
    errorCount = arrayLength(errors)
    jumpif (errorCount == 0) errorsDone
        ixError = 0
        errorLoop:
            markdownPrint('', 'Error: ' + markdownEscape(arrayGet(errors, ixError)))
            ixError = ixError + 1
        jumpif (ixError < errorCount) errorLoop
        return
    errorsDone:

    # Get the package JSON
    packageData = objectGet(packages, packageName)
    packageVersion = if(packageVersion != null, packageVersion, ndePackageVersionLatest(packageData))
    packageJSON = ndePackageJSON(packageData, packageVersion)

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
    dependenciesDescriptor = if(dependencyType != 'Package', '*' + dependencyType + '* ', '')
    markdownPrint( \
        '', \
        '**Description:** ' + markdownEscape(objectGet(packageJSON, 'description')) + ' \\', \
        '**Version:** ' + markdownEscape(packageVersion), \
        '', \
        '**Direct ' + stringLower(dependenciesDescriptor) + 'dependencies:** ' + arrayLength(dependenciesDirect) + ' \\', \
        '**Total ' + stringLower(dependenciesDescriptor) + 'dependencies:** ' + arrayLength(dependenciesTotal), \
        '', \
        '**Showing:** ' + linkAll + ' | ' + linkDirect + ' \\',  \
        '**Dependency type:** ' + linkPackage + ' | ' + linkDevelopment + ' | ' + linkOptional + ' | ' + linkPeer \
    )

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

        # Make the name fields links
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
        markdownPrint('### ' + dependenciesDescriptor + ' Dependencies')
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


# Helper to compute an npm package's dependency data table
async function ndePackageDependencies(packageName, packageVersion, dependencyKey, dependencies, packages, errors, completed)
    isDirect = arrayLength(objectKeys(completed)) == 0

    # Fetch the package data, if necessary
    packageData = objectGet(packages, packageName)
    jumpif (packageData != null) packageDone
        packageData = fetch(ndePackageDataURL(packageName))
        jumpif (packageData != null) packageOK
            arrayPush(errors, 'Failed to load package data for "' + packageName + '"')
            return
        packageOK:
        objectSet(packages, packageName, packageData)
    packageDone:

    # Package and version already loaded?
    packageVersion = if(packageVersion != null, packageVersion, ndePackageVersionLatest(packageData))
    packageVersionKey = packageName + ',' + packageVersion
    jumpif (!objectGet(completed, packageVersionKey)) versionNotLoaded
        return
    versionNotLoaded:
    objectSet(completed, packageVersionKey, true)

    # Get the package JSON
    packageJSON = ndePackageJSON(packageData, packageVersion)
    jumpif (packageJSON != null) versionOK
        arrayPush(errors, 'Unknown version "' + packageVersion + '" of package "' + packageName + '"')
        return
    versionOK:

    # Get the package dependencies map
    packageDependencies = objectGet(packageJSON, dependencyKey)
    jumpif (packageDependencies != null) dependenciesOK
        return
    dependenciesOK:

    # Compute list of dependency URLs that need to be fetched
    dependencyURLs = arrayNew()
    dependencyURLNames = arrayNew()
    dependencyNames = objectKeys(packageDependencies)
    jumpif (arrayLength(dependencyNames) == 0) urlsDone
        ixDependencyName = 0
        urlNameLoop:
            dependencyName = arrayGet(dependencyNames, ixDependencyName)
            dependencyData = objectGet(packages, dependencyName)
            if(dependencyData == null, arrayPush(dependencyURLs, ndePackageDataURL(dependencyName)))
            if(dependencyData == null, arrayPush(dependencyURLNames, dependencyName))
            ixDependencyName = ixDependencyName + 1
        jumpif (ixDependencyName < arrayLength(dependencyNames)) urlNameLoop
    urlsDone:

    # Fetch the dependency package data in parallel
    jumpif (arrayLength(dependencyURLs) == 0) dataDone
        dependencyDatum = fetch(dependencyURLs)
        ixDependencyURL = 0
        urlLoop:
            dependencyName = arrayGet(dependencyURLNames, ixDependencyURL)
            dependencyData = arrayGet(dependencyDatum, ixDependencyURL)
            if(dependencyData != null, objectSet(packages, dependencyName, dependencyData))
            if(dependencyData == null, arrayPush(errors, 'Failed to load package data for "' + dependencyName + '"'))
            ixDependencyURL = ixDependencyURL + 1
        jumpif (ixDependencyURL < arrayLength(dependencyURLs)) urlLoop
    dataDone:

    # Add the package dependency rows
    jumpif (arrayLength(dependencyNames) == 0) rowsDone
        ixDependencyName = 0
        nameLoop:
            # Determine the dependency version
            dependencyName = arrayGet(dependencyNames, ixDependencyName)
            dependencyData = objectGet(packages, dependencyName)
            dependencySemver = objectGet(packageDependencies, dependencyName)
            dependencyVersion = if(dependencyData != null, ndePackageVersion(dependencyData, dependencySemver))
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
                ndePackageDependencies(dependencyName, dependencyVersion, 'dependencies', dependencies, packages, errors, completed)
            versionDone:

            ixDependencyName = ixDependencyName + 1
        jumpif (ixDependencyName < arrayLength(dependencyNames)) nameLoop
    rowsDone:
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
function ndePackageVersion(packageData)
    return ndePackageVersionLatest(packageData)
endfunction


# Call the main entry point
ndeMain()
~~~
