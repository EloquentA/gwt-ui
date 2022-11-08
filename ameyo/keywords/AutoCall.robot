*** Settings ***
Documentation     Keywords supported for auto call features
...               Developed By - Developer by EA


*** Keywords **
I verify auto call stats
    [Documentation]   This keyword verifies auto call on/off stats for requested user
    [Arguments]  ${instance}    ${req_run_as}    ${auto_call}
    ${result}=   call method    ${instance}    verify_auto_call_stats    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${req_run_as}    ${auto_call}
    I verify result    ${result}

I verify auto call and not on call filter
    [Documentation]   This keyword verifies auto call on/off, not on call filter for requested user
    [Arguments]  ${instance}    ${req_run_as}    ${auto_call}
    ${result}=   call method    ${instance}    verify_auto_call_not_on_call_filter    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${req_run_as}    ${auto_call}
    I verify result    ${result}