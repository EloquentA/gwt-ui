*** Settings ***
Documentation     Keywords supported for Ameyo Home page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
Manual Dial Only
    [Documentation]   This keyword does a manual dial only call to given number
    [Arguments]  ${instance}    ${CALLING_NUMBER}
    ${result}=   call method    ${instance}    manual_dial_only    ${CALLING_NUMBER}
    I verify result    ${result}

Validate logout disabled during call
    [Documentation]   This keyword validates logout functionality is disabled during call
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    validate_logout_disabled_when_call_in_progress
    I verify result    ${result}

End call and auto dispose
    [Documentation]   This keyword ends call and auto disposes in 30 seconds
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    end_call_and_auto_dispose
    I verify result    ${result}