*** Settings ***
Documentation     Ameyo User test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/UserKeywords.robot
Resource          ../../keywords/CommonKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - Create executive user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create executive user    ${instance1}
