*** Settings ***
Documentation     Keywords supported for Ameyo Chat Functionalities
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

I create customer from routed chat
    [Documentation]   This keyword will create new customer when chat is new
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    create_customer_from_routed_chat
    I verify result    ${result}

I verify live monitoring data for chat
    [Documentation]   This keyword will verify and validate real-time data on live monitoring screen on supervisor
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    validate_real_time_chat_data    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${CREDENTIALS['chat_executive']['username']}
    I verify result    ${result}

I verify queue monitoring data for chat
    [Documentation]   This keyword will verify and validate real-time data on queue monitoring screen on supervisor
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_and_validate_queue_monitoring    ${CREDENTIALS['${req_run_as}']['campaign_details']}
    I verify result    ${result}