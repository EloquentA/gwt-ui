*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-15997

# Suite Setup and Teardown
Suite Setup       Login Initialization
Suite Teardown    Login Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - Login into Ameyo as executive user
    [Tags]  smoke    testid=AP-15997-1    regression
    IF  ${is_parent_setup}
        I logout from ameyo homepage    ${instance1}
    END
    I open ameyo home page    ${instance1}
    I login into Ameyo    ${instance1}    executive

TC - Logout from Ameyo Campaign Selection Page
    [Tags]  smoke    testid=AP-15997-1    regression
    I logout from campaign selection page    ${instance1}

TC - Login into Ameyo with incorrect username and incorrect password
    [Tags]  smoke    testid=AP-15997-2    regression
    I open ameyo home page    ${instance1}
    I login into ameyo with incorrect username and incorrect password    ${instance1}

TC - Login into Ameyo with correct username and incorrect password
    [Tags]  smoke    testid=AP-15997-3    regression
    I open ameyo home page    ${instance1}
    I login into ameyo with correct username and incorrect password    ${instance1}

TC - Login into Ameyo with incorrect username and correct password
    [Tags]  smoke    testid=AP-15997-4    regression
    I open ameyo home page    ${instance1}
    I login into ameyo with incorrect username and correct password    ${instance1}

TC - Login into Ameyo with blank username and blank password
    [Tags]  smoke    testid=AP-15997-5    regression
    I open ameyo home page    ${instance1}
    I login into ameyo with blank username and blank password    ${instance1}