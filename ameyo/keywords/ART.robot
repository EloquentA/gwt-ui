*** Settings ***
Documentation     Keywords supported common functionalities
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords **
I validate reports tab
    [Documentation]   This keyword validates whether the report tab is working in admin and supervisor
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    validate_reports_tab
    I verify result    ${result}
