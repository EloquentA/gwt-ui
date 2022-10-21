*** Settings ***
Documentation     Ameyo User test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AdminSystemKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - verify admin should be able to change the mapper policy type
    [Tags]  smoke    testid=AP-16053    regression
    Change Mapper Policy    ${instance1}    ${ADMIN_MAPPING_POLICY_TYPE}