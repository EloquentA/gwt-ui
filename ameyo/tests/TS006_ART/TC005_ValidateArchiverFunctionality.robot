*** Settings ***
Documentation     Validate ART Reports archiver funtionlaity .
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16214
Library    String

# Suite Setup and Teardown
Suite Setup       Suite Initialization For One Executive And Requested User    admin
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot
Resource          ../../keywords/MonitoringKeywords.robot
Resource          ../../keywords/ART.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=admin    WITH NAME    Client1
Library    DateTime

*** Test Cases ***
TC - Validate reports archiever functionality
    [Tags]  smoke    testid=AP-16214    regression
    &{admin_replace_dict}=    Create Dictionary    replace_value=${CREDENTIALS['admin']['username']}
    Admin assigns all default reports to user     ${instance1}    ${admin_replace_dict}
    Validates reports assigned to user     ${instance1}    CALL History
    @{format_list}=    Create List    CSV
    I switch to requested tab   ${instance1}    0
    Manual Dial Only    ${instance1}    ${CALLING_NUMBER}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}
    Save and Dispose via Select Disposition    ${instance1}    ${DISPOSITION['disposition']}    ${DISPOSITION['sub_disposition']}
    I switch to requested tab   ${instance1}    1
    Sleep    120
    Run specific report and validate download in required formats     ${instance1}    CALL History    Day    ${format_list}
    ${current_Date}=    Get Current Date    result_format=%d/%m/%Y
    Log To Console    ${current_Date}
    Validate call data from CSV report    ${instance1}    ${CALLING_NUMBER}    ${current_Date}
