*** Settings ***
Documentation     Ameyo test cases to verify superivor monitoring chat data.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16201

# Suite Setup and Teardown
Suite Setup       Suite Initialization For Two Requested Users And Customer Chat Window    chat_executive
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/Chat.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=chat_executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify live monitoring data on supervisor for chat
    [Tags]  smoke    testid=AP-16201    regression
    I verify live monitoring data for chat    ${instance1}    chat_supervisor
