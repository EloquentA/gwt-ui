*** Settings ***
Documentation     Keywords supported for Ameyo call details
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
supervisor schedules a callback
    [Documentation]   This keyword will schedule a callback from supervisor manage tab
    [Arguments]  ${instance}    ${current_time}
    ${result}=   call method    ${instance}    supervisor_schedule_callback    ${CREDENTIALS['supervisor']['call_back']}    ${current_time}
    I verify result    ${result}

verify call details
    [Documentation]   This keyword will verify call details from supervisor manage tab
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_call_details    ${CREDENTIALS['supervisor']['call_details']['user']}
    I verify result    ${result}