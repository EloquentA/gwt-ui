*** Settings ***
Documentation     Ameyo Login test cases
...               Developed By - Developer by EA
Library    String

# Suite Setup and Teardown
Suite Setup       Suite Initialization    ${RUN_AS}    voice_inbound    ${TRUE}
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - verify Inbound calling is working, save customer info during call and validate
    [Tags]  smoke    testid=AP-16004-1    regression
    ${random_customer_name}=  Generate Random String  10  [LETTERS][NUMBERS]
    ${random_did_prefix}=  Generate Random String  4  [NUMBERS]
    ${random_calling_number_prefix}=  Generate Random String  9  [NUMBERS]
    ${inbound_api_url_append_calls}=  Replace String    ${INBOUND_API_URL}    no_of_calls    1
    ${inbound_api_url_append_did}=  Replace String    ${inbound_api_url_append_calls}    did_prefix    ${random_did_prefix}
    ${inbound_api_url_append_number}=  Replace String    ${inbound_api_url_append_did}    calling_number    ${random_calling_number_prefix}
    Log To Console    ${inbound_api_url_append_number}
    Save and validate customer info during inbound call    ${instance1}    ${inbound_api_url_append_number}    ${random_customer_name}
    End call and auto dispose    ${instance1}

TC - Inbound Call States Validation
    [Tags]  smoke    testid=AP-16004-2    regression
    ${random_did_prefix}=  Generate Random String  4  [NUMBERS]
    ${random_calling_number_prefix}=  Generate Random String  9  [NUMBERS]
    ${inbound_api_url_append_calls}=  Replace String    ${INBOUND_API_URL}    no_of_calls    1
    ${inbound_api_url_append_did}=  Replace String    ${inbound_api_url_append_calls}    did_prefix    ${random_did_prefix}
    ${inbound_api_url_append_number}=  Replace String    ${inbound_api_url_append_did}    calling_number    ${random_calling_number_prefix}
    Log To Console    ${inbound_api_url_append_number}
    Inbound Call Validation    ${instance1}    ${inbound_api_url_append_number}    ${random_did_prefix}    ${random_calling_number_prefix}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_inbound']}    ${CREDENTIALS['${RUN_AS}']['inbound_queue']}
    Save and Dispose via Select Disposition    ${instance1}    ${DISPOSITION['disposition']}    ${DISPOSITION['sub_disposition']}


TC - verify 20 inbound call with single acd and customer query nodeflow.
    [Tags]  smoke    testid=AP-16004-3    regression
    FOR    ${call_attempt}    IN RANGE    20
        Log To Console    Call Attempt: ${call_attempt}
        ${random_did_prefix}=  Generate Random String  4  [NUMBERS]
        ${random_calling_number_prefix}=  Generate Random String  9  [NUMBERS]
        ${inbound_api_url_append_calls}=  Replace String    ${INBOUND_API_URL}    no_of_calls    1
        ${inbound_api_url_append_did}=  Replace String    ${inbound_api_url_append_calls}    did_prefix    ${random_did_prefix}
        ${inbound_api_url_append_number}=  Replace String    ${inbound_api_url_append_did}    calling_number    ${random_calling_number_prefix}
        Log To Console    ${inbound_api_url_append_number}
        Inbound Call Validation    ${instance1}    ${inbound_api_url_append_number}    ${random_did_prefix}    ${random_calling_number_prefix}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_inbound']}    ${CREDENTIALS['${RUN_AS}']['inbound_queue']}
        Save and Dispose via Select Disposition    ${instance1}    ${DISPOSITION['disposition']}    ${DISPOSITION['sub_disposition']}
    END
