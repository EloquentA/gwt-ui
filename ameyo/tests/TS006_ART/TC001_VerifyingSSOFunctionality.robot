*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot
Resource          ../../keywords/ART.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=admin    WITH NAME    Client1

*** Test Cases ***
TC - verify sso functionalty is working or not
    [Tags]  smoke    testid=AP-16205-1    regression
    I validate reports tab     ${instance1}
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    supervisor
    I validate reports tab    ${instance1}
