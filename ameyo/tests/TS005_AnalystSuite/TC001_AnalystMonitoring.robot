*** Settings ***
Documentation     Ameyo Analyst test cases to verify snoop, whisper, and disconnect functionalities.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16016

# Suite Setup and Teardown
Suite Setup       Suite Initialization For One Executive And Requested User    analyst
Suite Teardown    Suite Cleanup    executive

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/MonitoringKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify snoop for analyst user
    [Tags]  smoke    testid=AP-16016-3    regression
    I verify snoop    ${instance1}    analyst

TC - Verify whisper for analyst user
    [Tags]  smoke    testid=AP-16016-3    regression
    I verify whisper    ${instance1}    analyst

TC - Verify disconnect for analyst user
    [Tags]  smoke    testid=AP-16016-3    regression
    I verify disconnect    ${instance1}    analyst

