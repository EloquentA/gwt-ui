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

End call and save and dispose
    [Documentation]   This keyword ends call and auto disposes in 30 seconds
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    end_call_and_save_and_dispose
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

I change extension
    [Documentation]   This keyword will change extension as per input given from script
    [Arguments]  ${instance}    ${CALLING_NUMBER}
    ${result}=   call method    ${instance}    change_extension    ${CREDENTIALS}    ${CALLING_NUMBER}
    I verify result    ${result}

Inbound Call Validation
    [Documentation]   This keyword will accept inbound call and perform validations
    [Arguments]  ${instance}    ${inbound_url}    ${random_did_prefix}    ${random_calling_number_prefix}    ${campaign_name}    ${queue}
    ${result}=   call method    ${instance}    validate_inbound_call    ${inbound_url}    ${random_did_prefix}    ${random_calling_number_prefix}    ${campaign_name}    ${queue}
    I verify result    ${result}

Save and validate customer info during inbound call
    [Documentation]   This keyword will save customer info during inbound call and validate stored info
    [Arguments]  ${instance}    ${inbound_url}    ${customer_name}
    ${result}=   call method    ${instance}    save_and_validate_customer_info_during_inbound_call    ${inbound_url}    ${customer_name}
    I verify result    ${result}

Save and Dispose via Select Disposition
    [Documentation]   This keyword saves and disposes call via dropdown selection
    [Arguments]  ${instance}    ${disposition_type}    ${sub_disposition_type}
    ${result}=   call method    ${instance}    select_disposition_save_and_dispose    ${disposition_type}    ${sub_disposition_type}
    I verify result    ${result}

On hold unhold
    [Documentation]   This keyword is used to show the fucntionality of holds/unhold feature on an ongoing call
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    hold_resume_call
    I verify result    ${result}

Transfer call not allowed during hold
    [Documentation]   This keyword validates that transfer call is not allowed during call hold
    [Arguments]  ${instance}    ${CALLING_NUMBER}
    ${result}=   call method    ${instance}    transfer_call_not_allowed_during_hold    ${CALLING_NUMBER}
    I verify result    ${result}

schedule callback
    [Documentation]   This keyword will cover call schedule flow
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    schedule_callback    ${CALLBACK}
    I verify result    ${result}
