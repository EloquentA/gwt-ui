*** Settings ***
Documentation     Ameyo Supervisor test cases to verify auto on call functionalities.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-8895

# Suite Setup and Teardown
Suite Setup       Suite Initialization For Two Executives And Requested User
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/AutoOnCall.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify auto on call for supervisor user
    [Tags]  sanity    testid=AP-8895    regression
    I verify auto on call stats    ${instance1}    supervisor
