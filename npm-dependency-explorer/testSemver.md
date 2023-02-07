# semver Tests

~~~ markdown-script
include 'semver.mds'


# Test statistics
testsRun = 0
testsSuccess = 0


# Test runner
function testValue(name, actual, expected)
    setGlobal('testsRun', testsRun + 1)
    setGlobal('testsSuccess', if(actual == expected, testsSuccess + 1, testsSuccess))
    markdownPrint( \
        '', \
        'Test "' + name + '" - ' + \
        if(actual == expected, 'OK', 'FAIL - ' + jsonStringify(actual) + ' != ' + jsonStringify(expected)) \
    )
endfunction


function testSemverNew()
    return jsonStringify(semverNew('1.2.3-beta.1+1234'))
endfunction
testValue('semverNew', testSemverNew(), '{"build":"1234","major":1,"minor":2,"patch":3,"release":["beta",1]}')


function testSemverStringify()
    semver = semverNew('1.2.3-beta.1+1234')
    return semverStringify(semver)
endfunction
testValue('semverStringify', testSemverStringify(), '1.2.3-beta.1+1234')


function testSemverCompare()
    semver = semverNew('1.2.3-beta.1+1234')
    other = semverNew('1.2.2-rc.2+1235')
    return jsonStringify(arrayNew( \
        semverCompare(semver, other), \
        semverCompare(other, semver), \
        semverCompare(semver, semver), \
        semverCompare(other, other) \
    ))
endfunction
testValue('semverCompare', testSemverCompare(), '[1,-1,0,0]')


function testSemverVersions()
    return jsonStringify(semverVersions(arrayNew('1.2.2', '1.2.2-rc.2+1235')))
endfunction
testValue('semverVersions', testSemverVersions(), \
    '[{"build":"1235","major":1,"minor":2,"patch":2,"release":["rc",2]},' + \
    '{"build":null,"major":1,"minor":2,"patch":2,"release":null}]' \
)


function testSemverMatch()
    versions = semverVersions(arrayNew('1.2.2', '1.2.2-rc.2+1235'))
    return jsonStringify(arrayNew( \
        semverMatch(versions, '~1.2'), \
        semverMatch(versions, '~1.3') \
    ))
endfunction
testValue('semverMatch', testSemverMatch(), '["1.2.2",null]')


# Test report
markdownPrint( \
    '', \
    '---', \
    '', \
    'Ran ' + testsRun + ' tests, ' + testsSuccess + ' succeeded, ' + (testsRun - testsSuccess) + ' failed' \
)
~~~
