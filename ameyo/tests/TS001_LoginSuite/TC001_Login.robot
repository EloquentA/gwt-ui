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
    [Tags]  sanity
    IF  ${is_parent_setup}
        I logout from Ameyo ${instance1}
    END
#    I open Ameyo home page ${instance1}
    I login into Ameyo ${instance1}

TC - Logout from Ameyo
    [Tags]  sanity
    I logout from Ameyo ${instance1}
