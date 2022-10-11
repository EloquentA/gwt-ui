*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA

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
TC - Login into Ameyo as ${RUN_AS} user
    [Tags]  smoke    testrailid=AP-15997
    IF  ${is_parent_setup}
        I logout from ameyo    ${instance1}
    END
    I open ameyo home page    ${instance1}
    I login into Ameyo    ${instance1}    ${RUN_AS}

TC - Logout from Ameyo
    [Tags]  smoke    testrailid=AP-15997
    I logout from ameyo    ${instance1}

TC - Login into Ameyo with incorrect username and incorrect password
    [Tags]  smoke    testrailid=AP-15997
    I open ameyo home page    ${instance1}
    I login into ameyo with incorrect username and incorrect password    ${instance1}

TC - Login into Ameyo with correct username and incorrect password
    [Tags]  smoke    testrailid=AP-15997
    I open ameyo home page    ${instance1}
    I login into ameyo with correct username and incorrect password    ${instance1}

TC - Login into Ameyo with incorrect username and correct password
    [Tags]  smoke    testrailid=AP-15997
    I open ameyo home page    ${instance1}
    I login into ameyo with incorrect username and correct password    ${instance1}

TC - Login into Ameyo with blank username and blank password
    [Tags]  smoke    testrailid=AP-15997
    I open ameyo home page    ${instance1}
    I login into ameyo with blank username and blank password    ${instance1}