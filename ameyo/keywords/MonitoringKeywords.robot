*** Settings ***
Documentation     Keywords supported for monitoring tab
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./SetupTeardown.robot
Resource          ./CommonKeywords.robot

*** Keywords **
I verify snoop
    [Documentation]   This keyword verifies snoop functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_snoop_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['executive']['username']}
    I verify result    ${result}

I verify barge
    [Documentation]   This keyword verifies barge functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_barge_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['executive']['username']}
    I verify result    ${result}

I verify whisper
    [Documentation]   This keyword verifies whisper functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_whisper_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['executive']['username']}
    I verify result    ${result}

I verify conference
    [Documentation]   This keyword verifies conference functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_conference_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['executive']['username']}
    I verify result    ${result}

I verify disconnect
    [Documentation]   This keyword verifies disconnect functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_disconnect_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['executive']['username']}
    I verify result    ${result}

I verify force logout
    [Documentation]   This keyword verifies force logout functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_force_logout_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['executive']['username']}    ${AMEYO_URL}
    I verify result    ${result}

# Live Monitoring keywords
I verify live monitoring
    [Documentation]   This keyword verifies live monitoring functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${random_did_prefix}=  Generate Random String  4  [NUMBERS]
    ${random_calling_number_prefix}=  Generate Random String  9  [NUMBERS]
    ${inbound_api_url_append_calls}=  Replace String    ${INBOUND_API_URL}    no_of_calls    1
    ${inbound_api_url_append_did}=  Replace String    ${inbound_api_url_append_calls}    did_prefix    ${random_did_prefix}
    ${inbound_api_url_append_number}=  Replace String    ${inbound_api_url_append_did}    calling_number    ${random_calling_number_prefix}
    Log To Console    ${inbound_api_url_append_number}
    &{inbound_call_details}=    Create Dictionary    inbound_url=${inbound_api_url_append_calls}    did_prefix=${random_did_prefix}    calling_number=${random_calling_number_prefix}
    ${result}=   call method    ${instance}    verify_live_monitoring    ${CREDENTIALS}    ${req_run_as}    ${inbound_call_details}
    I verify result    ${result}

# Agent Monitoring keywords
I verify agent monitoring
    [Documentation]   This keyword verifies agent monitoring functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_agent_monitoring    ${CREDENTIALS}    ${req_run_as}
    I verify result    ${result}

# Dashboard Monitoring keywords
I verify dashboard monitoring
    [Documentation]   This keyword verifies dashboard monitoring functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${random_did_prefix}=  Generate Random String  4  [NUMBERS]
    ${random_calling_number_prefix}=  Generate Random String  9  [NUMBERS]
    ${inbound_api_url_append_calls}=  Replace String    ${INBOUND_API_URL}    no_of_calls    1
    ${inbound_api_url_append_did}=  Replace String    ${inbound_api_url_append_calls}    did_prefix    ${random_did_prefix}
    ${inbound_api_url_append_number}=  Replace String    ${inbound_api_url_append_did}    calling_number    ${random_calling_number_prefix}
    Log To Console    ${inbound_api_url_append_number}
    &{inbound_call_details}=    Create Dictionary    inbound_url=${inbound_api_url_append_calls}    did_prefix=${random_did_prefix}    calling_number=${random_calling_number_prefix}
    ${result}=   call method    ${instance}    verify_dashboard_monitoring    ${CREDENTIALS}    ${req_run_as}    ${inbound_call_details}
    I verify result    ${result}