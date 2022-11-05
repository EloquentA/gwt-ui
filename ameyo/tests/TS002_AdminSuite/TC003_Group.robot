*** Settings ***
Documentation     Ameyo group test cases
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16023

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup    admin

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/AdminGroup.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=admin    WITH NAME    Client1

*** Test Cases ***
TC - Create group
    [Tags]  smoke    testid=AP-16023    regression
    ${created_group}=   I create group    ${instance1}    ${CREDENTIALS['admin']['password']}
    Set Suite Variable    ${created_group}    ${created_group}

TC - Assign user to group
    [Tags]  smoke    testid=AP-16023    regression
    I assign user to group    ${instance1}    ${created_group}

TC - Update group
    [Tags]  smoke    testid=AP-16023    regression
    I update group    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_group}

TC - Delete group
    [Tags]  smoke    testid=AP-16023    regression
    I delete group    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_group}
