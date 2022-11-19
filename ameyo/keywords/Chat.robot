*** Settings ***
Documentation     Keywords supported for Ameyo Home page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
I verify chat routing to agent
    [Documentation]   This keyword will verify if chat is routed to available agent
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_chat_routing    ${CREDENTIALS['${req_run_as}']}
    I verify result    ${result}
