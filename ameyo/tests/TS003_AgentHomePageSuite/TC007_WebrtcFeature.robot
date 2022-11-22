*** Settings ***
Documentation     Calling Test Cases for webrtc agent
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16012
Library    String

# Suite Setup and Teardown
Suite Setup       Suite Initialization    webrtc_executive
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=webrtc_executive    WITH NAME    Client1

*** Test Cases ***
TC - verify manual outbound calling is working
    [Tags]  smoke    testid=AP-16012-1    regression
    Manual Dial Only    ${instance1}    ${CALLING_NUMBER}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_outbound']}

TC - verify mute unmute feature is working
    [Tags]  smoke    testid=AP-16012-2    regression
    Verify mute umute on call    ${instance1}

TC - verify DTMF feature is working
    [Tags]  smoke    testid=AP-16012-3    regression
    Verify DTMF feature    ${instance1}
    End call and auto dispose    ${instance1}
#
TC - Inbound Call States Validation
    [Tags]  smoke    testid=AP-16012-4    regression
    I change campaign    ${instance1}    webrtc_executive
    ${random_did_prefix}=  Generate Random String  4  [NUMBERS]
    ${random_calling_number_prefix}=  Generate Random String  9  [NUMBERS]
    ${inbound_api_url_append_calls}=  Replace String    ${INBOUND_API_URL}    no_of_calls    1
    ${inbound_api_url_append_did}=  Replace String    ${inbound_api_url_append_calls}    did_prefix    ${random_did_prefix}
    ${inbound_api_url_append_number}=  Replace String    ${inbound_api_url_append_did}    calling_number    ${random_calling_number_prefix}
    Log To Console    ${inbound_api_url_append_number}
    Inbound Call Validation    ${instance1}    ${inbound_api_url_append_number}    ${random_did_prefix}    ${random_calling_number_prefix}    ${CREDENTIALS['${RUN_AS}']['campaign_details']['voice_inbound']}    ${CREDENTIALS['${RUN_AS}']['inbound_queue']}
    Save and Dispose via Select Disposition    ${instance1}    ${DISPOSITION['disposition']}    ${DISPOSITION['sub_disposition']}
