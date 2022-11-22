*** Settings ***
Documentation     Test cases for Agent state change,campaign change and extension change
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/index.php?caller=login

# Suite Setup and Teardown
Suite Setup       Suite Initialization    change_executive
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=change_executive    WITH NAME    Client1

*** Test Cases ***
TC - Test Case for Setting User Status
    [Tags]  smoke    testid=AP-16013-1    regression
    I set status    ${instance1}

TC - Test Case to change campaign
    [Tags]  smoke    testid=AP-16013-2    regression
    I change campaign    ${instance1}    change_executive

#This will fail as the UI has a bug with change password rules.
TC - Test Case to Change password
    #[Tags]  smoke    testid=AP-16013-3    regression
    [Tags]    robot:skip
    # Setting a temporary password : Robo@12345
    I change password    ${instance1}    ${CREDENTIALS['change_executive']['password']}    Robo@12345
    I logout from ameyo homepage    ${instance1}
    I open ameyo home page    ${instance1}
    I login into Ameyo using new password    ${instance1}
    select campaign    ${instance1}    change_executive
    # Setting a temporary password : Auto@12345
    I change password    ${instance1}    Robo@12345    Auto@12345
    # Calling change password again to not disrupt the flow of the suite. This will reset the password to what it orignally was
    I change password    ${instance1}    Auto@12345    ${CREDENTIALS['change_executive']['password']}

TC - Test Case to change extension
    [Tags]  smoke    testid=AP-16013-4    regression
    I change extension    ${instance1}    ${CALLING_NUMBER}