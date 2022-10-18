*** Settings ***
Documentation     Keywords supported for monitoring tab
...               Developed By - Developer by EA
...               Comments:


*** Keywords **
I verify snoop
    [Documentation]   This keyword verifies snoop functionality
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    verify_snoop_action    ${CREDENTIALS['${req_run_as}']['campaign_details']}
    I verify result    ${result}
