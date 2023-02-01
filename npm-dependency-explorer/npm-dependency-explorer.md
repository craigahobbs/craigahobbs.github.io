# npm Dependency Explorer

~~~ markdown-script
# The npm Dependency Explorer main entry point
async function ndeMain()
    # Variable arguments
    packageName = if(vName != null, vName, 'markdown-up')
    packageVersion = vVersion
    dependencyKey = objectGet(ndeDependencyTypeKeys, vType)
    dependencyType = if(dependencyKey != null, vType, 'Package')
    dependencyKey = if(dependencyKey != null, dependencyKey, objectGet(ndeDependencyTypeKeys, dependencyType))
    dependenciesDescriptor = if(dependencyType != 'Package', '**' + dependencyType + '** ', '')

    # Get the package dependencies
    dependencies = arrayNew()
    packages = objectNew()
    errors = arrayNew()
    ndePackageDependencies(packageName, packageVersion, dependencyKey, dependencies, packages, errors, objectNew())
    schemaValidate(ndeTypes, 'PackageDependencies', dependencies)

    # Report errors, if necessary
    jumpif (arrayLength(errors) == 0) packageOK
        markdownPrint( \
            'Failed to get dependency information for package "' + markdownEscape(packageName) + '"', \
            '', \
            '~~~', \
            arrayJoin(errors, stringFromCharCode(13)), \
            '~~~' \
        )
        return
    packageOK:

    # Dependency statistics
    dependenciesDirect = dataFilter(dependencies, 'Direct')
    dependenciesTotal = dataAggregate(dependencies, objectNew( \
        'categories', arrayNew('PackageName', 'PackageVersion'), \
        'measures', arrayNew( \
            objectNew('field', 'DependentName', 'function', 'count', 'name', 'Count') \
        ) \
    ))

    # Report the package name and dependency stats
    markdownPrint( \
        '## ' + markdownEscape(packageName), \
        '', \
        'Direct ' + stringLower(dependenciesDescriptor) + 'dependencies: ' + arrayLength(dependenciesDirect) + ' \\', \
        'Total ' + stringLower(dependenciesDescriptor) + 'dependencies: ' + arrayLength(dependenciesTotal) \
    )

    # Render the dependency table
    dependenciesTable = if(!vDirect, dependencies, dependenciesDirect)
    jumpif (arrayLength(dependenciesTable) == 0) tableDone
        markdownPrint('### ' + dependenciesDescriptor + ' Dependencies')
        dataSort(dependenciesTable, arrayNew( \
            arrayNew('PackageName'), \
            arrayNew('PackageVersion'), \
            arrayNew('DependentName'), \
            arrayNew('DependentVersion') \
        ))
        dataTable(dependenciesTable, objectNew( \
            'categories', arrayNew('PackageName', 'PackageVersion'), \
            'fields', arrayNew('DependentName', 'DependentVersion') \
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


# Dependency data schema
ndeTypes = schemaParse( \
    '# A package dependency table', \
    'typedef PackageDependency[] PackageDependencies', \
    '', \
    '', \
    '# A package dependency row', \
    'struct PackageDependency', \
    '', \
    '    # The dependency package name', \
    '    string PackageName', \
    '', \
    '    # The dependency package version', \
    '    string PackageVersion', \
    '', \
    '    # The dependent package name', \
    '    string DependentName', \
    '', \
    '    # The dependent package version', \
    '    string DependentVersion', \
    '', \
    '    # Is this is a direct dependency?', \
    '    bool Direct' \
)


# Helper to compute an npm package's dependency data table
async function ndePackageDependencies(packageName, packageVersion, dependencyKey, dependencies, packages, errors, completed)
    isDirect = arrayLength(objectKeys(completed)) == 0

    # Fetch the package data, if necessary
    packageData = objectGet(packages, packageName)
    jumpif (packageData != null) packageDone
        packageData = fetch(ndePackageURL(packageName))
        jumpif (packageData != null) packageOK
            arrayPush(errors, 'Failed to load package data for "' + packageName + '"')
            return
        packageOK:
        objectSet(packages, packageName, packageData)
    packageDone:

    # Package and version already loaded?
    packageVersion = if(packageVersion != null, packageVersion, ndePackageVersionLatest(packages, packageName))
    packageVersionKey = packageName + ',' + packageVersion
    jumpif (!objectGet(completed, packageVersionKey)) versionNotLoaded
        return
    versionNotLoaded:
    objectSet(completed, packageVersionKey, true)

    # Get the package JSON
    packageJSON = objectGet(objectGet(packageData, 'versions'), packageVersion)
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
    ixDependencyName = 0
    urlNameLoop:
        dependencyName = arrayGet(dependencyNames, ixDependencyName)
        dependencyData = objectGet(packages, dependencyName)
        if(dependencyData == null, arrayPush(dependencyURLs, ndePackageURL(dependencyName)))
        if(dependencyData == null, arrayPush(dependencyURLNames, dependencyName))
        ixDependencyName = ixDependencyName + 1
    jumpif (ixDependencyName < arrayLength(dependencyNames)) urlNameLoop

    # Fetch the dependency package data in parallel
    jumpif (arrayLength(dependencyURLs) == 0) urlsDone
        dependencyDatum = fetch(dependencyURLs)
        ixDependencyURL = 0
        urlLoop:
            dependencyName = arrayGet(dependencyURLNames, ixDependencyURL)
            dependencyData = arrayGet(dependencyDatum, ixDependencyURL)
            if(dependencyData != null, objectSet(packages, dependencyName, dependencyData))
            if(dependencyData == null, arrayPush(errors, 'Failed to load package data for "' + dependencyName + '"'))
            ixDependencyURL = ixDependencyURL + 1
        jumpif (ixDependencyURL < arrayLength(dependencyURLs)) urlLoop
    urlsDone:

    # Add each package dependency name
    ixDependencyName = 0
    nameLoop:
        # Determine the dependency version
        dependencyName = arrayGet(dependencyNames, ixDependencyName)
        dependencyVersion = ndePackageVersion(packages, dependencyName, objectGet(packageDependencies, dependencyName))
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
endfunction


# Helper to compute a package's version from an npm semver
function ndePackageVersion(packages, packageName)
    return ndePackageVersionLatest(packages, packageName)
endfunction


# Helper to compute a package's latest version
function ndePackageVersionLatest(packages, packageName)
    packageData = objectGet(packages, packageName)
    return objectGet(objectGet(packageData, 'dist-tags'), 'latest')
endfunction


# Helper to create an npm package data URL
function ndePackageURL(packageName)
    return 'https://registry.npmjs.org/' + encodeURIComponent(packageName)
endfunction


# Call the main entry point
ndeMain()
~~~
