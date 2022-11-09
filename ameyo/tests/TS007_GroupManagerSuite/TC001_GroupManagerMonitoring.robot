*** Settings ***
Documentation     Ameyo group manager test cases to verify snoop, barge, whisper, conference, disconnect, and force-logout functionalities.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16025

# Suite Setup and Teardown
Suite Setup       Suite Initialization For One Executive And Requested User    group_manager
Suite Teardown    Suite Cleanup    executive

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/MonitoringKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify snoop for group manager user
    [Tags]  smoke    testid=AP-16025    regression
    I verify snoop    ${instance1}    group_manager

TC - Verify barge for group manager user
    [Tags]  smoke    testid=AP-16025    regression
    I verify barge    ${instance1}    group_manager

TC - Verify whisper for group manager user
    [Tags]  smoke    testid=AP-16025    regression
    I verify whisper    ${instance1}    group_manager

TC - Verify conference for group manager user
    [Tags]  smoke    testid=AP-16025    regression
    I verify conference    ${instance1}    group_manager

TC - Verify disconnect for group manager user
    [Tags]  smoke    testid=AP-16025    regression
    I verify disconnect    ${instance1}    group_manager

TC - Verify force logout for group manager user
    [Tags]  smoke    testid=AP-16025    regression
    I verify force logout    ${instance1}    group_manager
    I switch to requested tab   ${instance1}    0
    # Re-instante original state
    Ameyo setup   ${instance1}    ${RUN_AS}
