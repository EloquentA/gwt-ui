*** Settings ***
Documentation     Keywords supported for auto call stats
...               Developed By - Developer by EA


*** Keywords **
I verify auto call on stats
    [Documentation]   This keyword verifies auto call on stats for requested user
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_auto_call_on_stats    ${CREDENTIALS['${req_run_as}']['campaign_details']}    ${req_run_as}
    I verify result    ${result}
