*** Settings ***
Documentation     Verify default reports is working and downloaded in all formats
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16207

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
TC - verify default reports is working
    [Tags]  smoke    testid=AP-16207-1    regression
    &{admin_replace_dict}=    Create Dictionary    replace_value=${CREDENTIALS['admin']['username']}
    Admin assigns all default reports to user     ${instance1}    ${admin_replace_dict}
    Validates reports assigned to user     ${instance1}    ACD Call Details
    @{format_list}=    Create List    CSV    PDF    HTML
    Run specific report and validate download in required formats     ${instance1}    ACD Call Details    Day    ${format_list}
    &{supervisor_replace_dict}=    Create Dictionary    replace_value=${CREDENTIALS['supervisor']['username']}
    Admin assigns all default reports to user     ${instance1}    ${supervisor_replace_dict}
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    supervisor
    Validates reports assigned to user     ${instance1}    ACD Abandon Call Summary Report
    Run specific report and validate download in required formats     ${instance1}    ACD Abandon Call Summary Report