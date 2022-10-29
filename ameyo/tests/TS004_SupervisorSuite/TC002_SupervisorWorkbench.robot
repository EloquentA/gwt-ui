*** Settings ***
Documentation     Ameyo supervisor workbench screen
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16020
Library    String
# Suite Setup and Teardown
Suite Setup       Suite Initialization    supervisor
Suite Teardown    Suite Cleanup    supervisor

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot
Resource          ../../keywords/CallDetailsKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - supervisor login after campaign selection
    [Tags]  smoke    testid=AP-16020-1    regression
    select campaign    ${instance1}    supervisor    workbench=${TRUE}

TC - call from supervisor login
    [Tags]  smoke    testid=AP-16020-2    regression
    ${customer_number1}=  Generate Random String  10  123456789
    Manual Dial Only    ${instance1}    ${customer_number1}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice']}

TC - workbench - verify callback
    [Tags]  smoke    testid=AP-16020-3    regression
    schedule callback    ${instance1}
    verify callback    ${instance1}

TC - workbench - verify call hisotry
    [Tags]  smoke    testid=AP-16020-4    regression
    verify call history    ${instance1}