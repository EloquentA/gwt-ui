*** Settings ***
Documentation     Ameyo Supervisor test cases to verify live monitoring functionalities.
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16038

# Suite Setup and Teardown
Suite Setup       Suite Initialization For One Executive And Requested User    supervisor    voice_outbound,voice_inbound
Suite Teardown    Suite Cleanup    executive

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/MonitoringKeywords.robot


Library    String
# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=executive    WITH NAME    Client1

*** Test Cases ***
TC - Verify dashboard monitoring for supervisor user
    [Tags]  smoke    testid=AP-16038    regression
    I verify dashboard monitoring    ${instance1}    supervisor
