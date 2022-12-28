*** Settings ***
Documentation     Keywords supported for Ameyo Home page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
I change campaign in toolbar
    [Documentation]   This keyword changes the campaign to desired campaign on toolbar
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    change_toolbar_campaign    ${CREDENTIALS['${req_run_as}']['campaign_details']}
    I verify result    ${result}