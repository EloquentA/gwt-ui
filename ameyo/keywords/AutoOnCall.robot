*** Settings ***
Documentation     Keywords supported for auto on call stats
...               Developed By - Developer by EA


*** Keywords **
I verify auto on call stats
    [Documentation]   This keyword verifies auto on call stats for requested user
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_auto_on_call_stats    ${CREDENTIALS['${req_run_as}']['campaign_details']}
    I verify result    ${result}
