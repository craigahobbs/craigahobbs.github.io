# semver Tests

~~~ markdown-script
include 'semver.mds'


# Test statistics
testsRun = objectNew()
testsSuccess = 0


# Test runner
function testValue(name, expected)
    # Single test?
    if vTest != null && vTest != name then
        return
    endif

    # Multiple runs of the same test?
    if objectHas(testsRun, name) then
        markdownPrint('', 'Test "' + markdownEscape(name) + '" run multiple times')
        return
    endif
    objectSet(testsRun, name)

    # Get the test func
    testFn = getGlobal(name)
    if testFn == null then
        markdownPrint('', 'Test "' + markdownEscape(name) + '" not found')
        return
    endif

    # Run the test
    actual = testFn()
    isSuccess = (actual == expected)
    if isSuccess then
        setGlobal('testsSuccess', testsSuccess + 1)
    endif

    # Report
    markdownPrint( \
        '', \
        'Test "' + markdownEscape(name) + '" - ', \
        if(isSuccess, 'OK', 'FAIL - ' + markdownEscape(jsonStringify(actual)) + ' != ' + markdownEscape(jsonStringify(expected))) \
    )
endfunction


#
# Tests
#


function testSemverParse()
    semver = semverParse('1.2.3-beta.1+1234')
    return jsonStringify(semver)
endfunction
testValue('testSemverParse', '{"build":"1234","major":1,"minor":2,"patch":3,"release":["beta",1]}')


function testSemverStringify()
    semver = semverParse('1.2.3-beta.1+1234')
    return semverStringify(semver)
endfunction
testValue('testSemverStringify', '1.2.3-beta.1+1234')


function testSemverCompare_release()
    semver = semverParse('1.2.3-beta.1+1234')
    other = semverParse('1.2.2-rc.2+1235')
    return jsonStringify(arrayNew( \
        semverCompare(semver, other), \
        semverCompare(other, semver), \
        semverCompare(semver, semver), \
        semverCompare(other, other) \
    ))
endfunction
testValue('testSemverCompare_release', '[1,-1,0,0]')


function testSemverCompare_releaseSame()
    semver = semverParse('1.2.3-beta.1+1234')
    other = semverParse('1.2.3-beta.2+1235')
    return jsonStringify(arrayNew( \
        semverCompare(semver, other), \
        semverCompare(other, semver), \
        semverCompare(semver, semver), \
        semverCompare(other, other) \
    ))
endfunction
testValue('testSemverCompare_releaseSame', '[-1,1,0,0]')


function testSemverVersions()
    versions = semverVersions(arrayNew('1.2.2', '1.2.2-rc.2+1235'))
    dataCalculatedField(versions, 'semver', 'semver != null')
    return jsonStringify(versions)
endfunction
testValue('testSemverVersions', \
    '[{"build":null,"major":1,"minor":2,"patch":2,"release":null,"semver":true},' + \
    '{"build":"1235","major":1,"minor":2,"patch":2,"release":["rc",2],"semver":true}]' \
)


function testSemverMatch_tilde()
    versions = semverVersions(arrayNew('1.2.2', '1.2.2-rc.2+1235'))
    return jsonStringify(arrayNew( \
        semverMatch(versions, '~1.2'), \
        semverMatch(versions, '~1.3') \
    ))
endfunction
testValue('testSemverMatch_tilde', '["1.2.2",null]')


function testSemverMatch_carrot()
    versions = semverVersions(arrayNew(\
        '0.0.1', '0.0.2', '0.0.3', \
        '0.1.1', '0.1.2', '0.1.3', \
        '1.0.1', '1.0.2', '1.0.3', \
        '1.1.1', '1.1.2', '1.1.3', \
        '1.2.1-beta.1', '1.2.1-beta.2', \
        '2.0.0' \
    ))
    return jsonStringify(arrayNew( \
        semverMatch(versions, '^0.0.1'), \
        semverMatch(versions, '^0.0.3'), \
        semverMatch(versions, '^0.0.4'), \
        semverMatch(versions, '^0.1.1'), \
        semverMatch(versions, '^0.1.3'), \
        semverMatch(versions, '^0.1.4'), \
        semverMatch(versions, '^1.0.1'), \
        semverMatch(versions, '^1.0.3'), \
        semverMatch(versions, '^1.0.4'), \
        semverMatch(versions, '^1.1.1'), \
        semverMatch(versions, '^1.1.3'), \
        semverMatch(versions, '^1.1.4'), \
        semverMatch(versions, '^1.2.1-beta.1'), \
        semverMatch(versions, '^1.2.1'), \
        semverMatch(versions, '^2.0.0') \
    ))
endfunction
testValue('testSemverMatch_carrot', \
    '["0.0.1","0.0.3",null,"0.1.3","0.1.3",null,"1.1.3","1.1.3","1.1.3","1.1.3","1.1.3",null,"1.2.1-beta.2",null,"2.0.0"]')


#
# End tests
#


# Test report
runCount = arrayLength(objectKeys(testsRun))
markdownPrint( \
    '', \
    '---', \
    '', \
    'Ran ' + runCount + ' tests, ' + testsSuccess + ' succeeded, ' + (runCount - testsSuccess) + ' failed' \
)
~~~
