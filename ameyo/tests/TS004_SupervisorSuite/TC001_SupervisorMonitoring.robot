*** Settings ***
Documentation     Ameyo Supervisor test cases to verify snoop, barge, whisper, conference, disconnect, and force-logout functionalities.
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization For Monitoring
Suite Teardown    Suite Cleanup    executive

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/MonitoringKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify snoop for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I verify snoop    ${instance1}    supervisor

TC - Verify barge for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I verify barge    ${instance1}    supervisor

TC - Verify whisper for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I verify whisper    ${instance1}    supervisor

TC - Verify conference for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I verify conference    ${instance1}    supervisor

TC - Verify disconnect for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I verify disconnect    ${instance1}    supervisor

TC - Verify force logout for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I verify force logout    ${instance1}    supervisor
    I switch to requested tab   ${instance1}    0
    # Re-instante original state
    Ameyo setup   ${instance1}    ${RUN_AS}
