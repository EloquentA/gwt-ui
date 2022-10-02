*** Settings ***
Documentation     Keywords supported for handling result verification from single file
...               Developed By - Developer by EA
...               Comments:


*** Keywords **
I verify result ${result}
    [Documentation]   This keyword verifies result for consistency and single point to manage
    IF  ${TESTRAIL_REPORTING}
        Should Be Equal As Strings      "${result[1]}"     "${EMPTY}"
    ELSE
        Log To Console    ${result[1]}
    END
    Should be true      ${result[0]}