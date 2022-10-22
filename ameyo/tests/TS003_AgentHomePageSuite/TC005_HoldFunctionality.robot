*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    ${RUN_AS}
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - verify hold/unhold is working fine
    [Tags]  smoke    testid=AP-16010-1    regression
    Manual Dial Only    ${instance1}    ${CALLING_NUMBER}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}
    On hold unhold    ${instance1}
    Transfer call not allowed during hold    ${instance1}    ${CALLING_NUMBER}
    On hold unhold    ${instance1}
    End call and auto dispose    ${instance1}
