*** Settings ***
Documentation     Keywords supported for Login page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
I login into Ameyo
    [Documentation]   This keyword logs-in to Ameyo portal
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    ameyo_login    ${CREDENTIALS}    ${req_run_as}
    I verify result    ${result}

I logout from campaign selection page
    [Documentation]   This keyword logouts from campaign selection page
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    logout_from_campaign_selection_page
    I verify result    ${result}

I login into ameyo with incorrect username and incorrect password
    [Documentation]   This keyword logs-in to Ameyo portal with incorrect username and password
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    login_failure    ${CREDENTIALS}    incorrect_username    incorrect_password
    I verify result    ${result}

I login into ameyo with correct username and incorrect password
    [Documentation]   This keyword logs-in to Ameyo portal with correct username and incorrect password
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    login_failure    ${CREDENTIALS}    correct_username    incorrect_password
    I verify result    ${result}

I login into ameyo with incorrect username and correct password
    [Documentation]   This keyword logs-in to Ameyo portal with incorrect username and correct password
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    login_failure    ${CREDENTIALS}    incorrect_username    correct_password
    I verify result    ${result}

I login into ameyo with blank username and blank password
    [Documentation]   This keyword logs-in to Ameyo portal with blank username and blank password
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    login_failure    ${CREDENTIALS}    blank_username    blank_password
    I verify result    ${result}

select campaign
    [Documentation]   This keyword will select campaigns as per input given from script
    [Arguments]  ${instance}    ${req_run_as}
    ${result}=   call method    ${instance}    select_campaign    ${CREDENTIALS}    ${req_run_as}
    I verify result    ${result}

I logout from ameyo homepage
    [Documentation]   This keyword logouts from the Ameyo home page by clicking on the preferences dropdown
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    logout_from_ameyo_homepage
    I verify result    ${result}

