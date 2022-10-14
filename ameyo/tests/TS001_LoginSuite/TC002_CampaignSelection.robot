*** Settings ***
Documentation     Ameyo Login and campaign selection test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Login Initialization
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - Campaign selection test cases
    [Tags]  smoke    testid=AP-16000    regression
    IF  ${is_parent_setup}
        I logout from ameyo homepage    ${instance1}
    END
    I open ameyo home page    ${instance1}
    I login into Ameyo    ${instance1}    ${RUN_AS}
    select campaign    ${instance1}    ${RUN_AS}
