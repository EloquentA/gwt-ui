*** Settings ***
Documentation     Keywords supported for Ameyo call details
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
verify callback
    [Documentation]   This keyword will verify the call back details
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_callback    ${CALLBACK_DETAILS}
    I verify result    ${result}

verify call history
    [Documentation]   This keyword will verify the call hisotry details
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_call_history    ${CALL_HISTORY}
    I verify result    ${result}