*** Settings ***
Documentation     Ameyo Login and campaign selection test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    change_executive
Suite Teardown    Login Cleanup

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
    I change campaign    ${instance1}

TC - Test Case to Change password
    [Tags]  smoke    testid=AP-16013-3    regression
    I change password    ${instance1}    ${CREDENTIALS['change_executive']['password']}    Robo@12345
    I logout from ameyo homepage    ${instance1}
    I open ameyo home page    ${instance1}
    I login into Ameyo using new password    ${instance1}
    select campaign    ${instance1}    change_executive
    # Setting a temporary password : Roof@12345
    I change password    ${instance1}    Robo@12345    Auto@12345
    # Calling change password again to not disrupt the flow of the suite. This will reset the password to what it orignally was
    I change password    ${instance1}    Auto@12345    ${CREDENTIALS['change_executive']['password']}