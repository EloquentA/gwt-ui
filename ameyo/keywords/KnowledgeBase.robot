*** Settings ***
Documentation     Keywords supported for Ameyo knowledge base page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
I validate knowledge base page
    [Documentation]   This keyword will validate the knowledge base page for requested user
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    validate_knowledge_base_page    ${req_run_as}    ${CREDENTIALS['${req_run_as}']['campaign_details']}
    I verify result    ${result}