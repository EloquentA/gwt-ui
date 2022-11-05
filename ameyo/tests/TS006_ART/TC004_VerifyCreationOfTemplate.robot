*** Settings ***
Documentation     Verify creation of template and run report via template
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16208
Library    String

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
TC - verify creation of template and run report from template
    [Tags]  smoke    testid=AP-16208    regression
    &{admin_replace_dict}=    Create Dictionary    replace_value=${CREDENTIALS['admin']['username']}
    Admin assigns all default reports to user     ${instance1}    ${admin_replace_dict}
    Validates reports assigned to user     ${instance1}    ACD Call Details
    @{format_list}=    Create List    CSV    XLS    PDF    HTML
    ${random_template_name}=  Generate Random String  15  Template[LETTERS][NUMBERS]
    Create template and run report from template     ${instance1}    ACD Call Details    ${random_template_name}    Day    ${format_list}