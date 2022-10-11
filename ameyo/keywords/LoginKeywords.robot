*** Settings ***
Documentation     Keywords supported for Login page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
I login into Ameyo
    [Documentation]   This keyword logs-in to Ameyo portal
    [Arguments]  ${instance}    ${run_as}
    ${result}=   call method    ${instance}    ameyo_login    ${CREDENTIALS}    ${run_as}
    I verify result    ${result}

I logout from ameyo
    [Documentation]   This keyword logouts from the Ameyo portal
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    logout
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