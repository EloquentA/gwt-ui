*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    ${RUN_AS}
Suite Teardown    Login Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - Logout from Ameyo Homepage
    [Tags]  smoke    testid=AP-15999-1    regression
    I logout from ameyo homepage    ${instance1}

TC - Unable to logout while user is on call
    [Tags]  smoke    testid=AP-15999-2    regression
    I login into Ameyo    ${instance1}    ${RUN_AS}
    select campaign    ${instance1}    ${RUN_AS}
    Manual Dial Only    ${instance1}    ${CALLING_NUMBER}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}
    Validate logout disabled during call    ${instance1}

TC - Dispose the call and logout from Ameyo
    [Tags]  smoke    testid=AP-15999-3    regression
    End call and auto dispose    ${instance1}
    I logout from ameyo homepage    ${instance1}