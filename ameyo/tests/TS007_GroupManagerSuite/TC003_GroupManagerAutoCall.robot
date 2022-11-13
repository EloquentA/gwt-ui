*** Settings ***
Documentation     Ameyo group manager test cases to verify auto call stats.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-8895
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-8913

# Suite Setup and Teardown
Suite Setup       Suite Initialization For Two Executives And Requested User    group_manager
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/AutoCall.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=group_manager    WITH NAME    Client1

*** Test Cases ***
TC - Verify auto call on stats for group manager user
    [Tags]  sanity    testid=AP-8895    regression
    I verify auto call stats    ${instance1}    group_manager    ${TRUE}

TC - Verify auto call off not on call filters for group manager user
    [Tags]  sanity    testid=AP-8913    regression
    I verify auto call and not on call filter    ${instance1}    group_manager    ${FALSE}
