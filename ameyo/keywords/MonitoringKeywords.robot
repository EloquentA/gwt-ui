*** Settings ***
Documentation     Keywords supported for monitoring tab
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./SetupTeardown.robot
Resource          ./CommonKeywords.robot

*** Keywords **
Suite Initialization For Monitoring
    [Documentation]   This keyword does suite initialization for monitoring test cases
    Suite Initialization    executive
    I open ameyo home page in separate tab    ${instance1}
    I switch to requested tab   ${instance1}    1
    Ameyo setup    ${instance1}    supervisor

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
