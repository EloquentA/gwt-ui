*** Settings ***
Documentation     Ameyo supervisor callback schedule
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16021
Library    String
Library    DateTime

# Suite Setup and Teardown
Suite Setup       Suite Initialization    supervisor
Suite Teardown    Suite Cleanup    supervisor

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot
Resource          ../../keywords/manage.robot
Resource    ../../keywords/manage.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - Supervisor- Callback schedule
    [Tags]  smoke    testid=AP-16021-1    regression
    ${current_time}=    Get Current Date    result_format=%I_%M
    @{hh_mm}=    Split String    ${current_time}    _
    Log To Console    ${hh_mm}
    supervisor schedules a callback    ${instance1}    ${hh_mm}

TC - Supervisor- verify call details
    [Tags]  smoke    testid=AP-16021-2    regression
    verify call details    ${instance1}