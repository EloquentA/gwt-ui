*** Settings ***
Documentation     Ameyo test cases to verify chat features.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16169
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16171

# Suite Setup and Teardown
Suite Setup       Suite Initialization For Single Requested User And Customer Chat Window    chat_executive
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/Chat.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=chat_executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify chat routed to agent
    [Tags]  smoke    testid=AP-16169    regression
    I verify chat routing to agent    ${instance1}    chat_executive

TC - Create customer from routed chat
    [Tags]  smoke    testid=AP-16171    regression
    I create customer from routed chat    ${instance1}
