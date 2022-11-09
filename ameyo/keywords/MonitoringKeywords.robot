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
