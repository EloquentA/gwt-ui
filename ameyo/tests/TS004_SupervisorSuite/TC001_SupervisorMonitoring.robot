*** Settings ***
Documentation     Ameyo Supercisor test cases to verify snoop, barge, whisper, conference, and force-logout functionalities.
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    supervisor
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/MonitoringKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=supervisor    WITH NAME    Client1

*** Test Cases ***
TC - Verify barge for supervisor user
    [Tags]  smoke    testid=AP-16016-1    regression
    I open ameyo home page in separate tab    ${instance1}
    I switch to requested tab   ${instance1}
#    Ameyo setup    ${instance1}    executive
    I verify snoop    ${instance1}    supervisor
