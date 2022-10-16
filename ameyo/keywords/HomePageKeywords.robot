*** Settings ***
Documentation     Keywords supported for Ameyo Home page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
Manual Dial Only
    [Documentation]   This keyword does a manual dial only call to given number
    [Arguments]  ${instance}    ${CALLING_NUMBER}    ${campaign_name}
    ${result}=   call method    ${instance}    manual_dial_only    ${CALLING_NUMBER}    ${campaign_name}
    I verify result    ${result}

Create and Dial Call
    [Documentation]   This keyword will store the number to ameyo and then dial call
    [Arguments]  ${instance}    ${calling_number}    ${customer_name}    ${campaign_name}
    ${result}=   call method    ${instance}    create_and_dial_call    ${calling_number}    ${customer_name}    ${campaign_name}
    I verify result    ${result}

Manual Preview Dial
    [Documentation]   This keyword will preview saved ameyo number and dial call
    [Arguments]  ${instance}    ${saved_calling_number}    ${customer_name}    ${campaign_name}
    ${result}=   call method    ${instance}    manual_preview_dial    ${saved_calling_number}    ${customer_name}    ${campaign_name}
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

dispose and dial
    [Documentation]   This keyword covers dispose and dial flow
    [Arguments]  ${instance}  ${dispose_type}  ${dial_position}
    ${result}=   call method    ${instance}    dispose_and_dial    ${DISPOSITION}
    ...          ${dispose_type}    ${dial_position}
    I verify result    ${result}

I set status
    [Documentation]   This keyword will set agent status
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    set_status
    I verify result    ${result}

I change campaign
    [Documentation]   This keyword will change campaign
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    change_campaign    ${CREDENTIALS['change_executive']['campaign_details']}
    I verify result    ${result}

I change password
    [Documentation]   This keyword changes password for logged in user
    [Arguments]  ${instance}    ${old_password}    ${new_password}
    ${result}=   call method    ${instance}    change_password    ${old_password}    ${new_password}
    I verify result    ${result}
