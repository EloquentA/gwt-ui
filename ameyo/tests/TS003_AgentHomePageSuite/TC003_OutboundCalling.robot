*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA
Library    String

# Suite Setup and Teardown
Suite Setup       Suite Initialization    ${RUN_AS}
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/HomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - verify manual outbound calling is working
    [Tags]  smoke    testid=AP-16003-1    regression
    Manual Dial Only    ${instance1}    ${CALLING_NUMBER}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}
    End call and auto dispose    ${instance1}

TC - verify create and dial feature is working
    [Tags]  smoke    testid=AP-16003-2    regression
    ${random_calling_number}=  Generate Random String  10  [NUMBERS]
    ${random_customer_name}=  Generate Random String  10  [LETTERS][NUMBERS]
    Create and Dial Call    ${instance1}    ${random_calling_number}    ${random_customer_name}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}
    Set Suite Variable    ${saved_calling_number}    ${random_calling_number}
    Set Suite Variable    ${saved_customer_name}    ${random_customer_name}
    Save and Dispose via Select Disposition    ${instance1}    ${DISPOSITION['disposition']}    ${DISPOSITION['sub_disposition']}

TC - verify manual preview dialing is working fine
    [Tags]  smoke    testid=AP-16003-3    regression
    Manual Preview Dial    ${instance1}    ${saved_calling_number}    ${saved_customer_name}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}
    Save and Dispose via Select Disposition    ${instance1}    ${DISPOSITION['disposition']}    ${DISPOSITION['sub_disposition']}