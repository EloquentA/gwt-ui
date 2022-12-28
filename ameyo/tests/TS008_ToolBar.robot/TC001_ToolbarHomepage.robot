*** Settings ***
Documentation     Outbound Calling Test Cases
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16258

Library    String

# Suite Setup and Teardown
Suite Setup       Suite Initialization For ToolBar    webrtc_executive
Suite Teardown    Suite Cleanup Toolbar

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/ToolbarHomepage.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=webrtc_executive    WITH NAME    Client1

*** Test Cases ***
TC - change campagin and validate
    [Tags]  smoke    testid=AP-16258    regression
    I change campaign in toolbar   ${instance1}    webrtc_executive
