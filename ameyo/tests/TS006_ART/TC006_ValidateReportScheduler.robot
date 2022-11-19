*** Settings ***
Documentation     Validate ART Reports archiver funtionlaity .
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16206
Library    String

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/ART.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=admin    WITH NAME    Client1

*** Test Cases ***
TC - Validate report scheduler functionality
    [Tags]  smoke    testid=AP-16206    regression
    &{admin_replace_dict}=    Create Dictionary    replace_value=${CREDENTIALS['admin']['username']}
    Admin assigns all default reports to user     ${instance1}    ${admin_replace_dict}
    Validates reports assigned to user     ${instance1}    ACD Call Details
    @{format_list}=    Create List    CSV    PDF    HTML
    ${random_schedule_name}=  Generate Random String  15  Schedule[NUMBERS]
    Schedule report from Scheduler Tab     ${instance1}    ${random_schedule_name}    ACD Call Details    Day    ${format_list}
    Delete scheduled report from Scheduler Tab     ${instance1}    ${random_schedule_name}
#    &{supervisor_replace_dict}=    Create Dictionary    replace_value=${CREDENTIALS['supervisor']['username']}
#    Admin assigns all default reports to user     ${instance1}    ${supervisor_replace_dict}
#    I logout from ameyo homepage    ${instance1}
#    I login into Ameyo  ${instance1}    supervisor
#    Validates reports assigned to user     ${instance1}    ACD Abandon Call Summary Report
#    Schedule report from Scheduler Tab     ${instance1}    ${random_schedule_name}    ACD Abandon Call Summary Report    Quarter
#    Delete scheduled report from Scheduler Tab     ${instance1}    ${random_schedule_name}
