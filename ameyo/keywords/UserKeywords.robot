*** Settings ***
Documentation     Keywords supported for user creation, updation and deletion operations
...               Developed By - Developer by EA
...               Comments:


*** Keywords **
I create executive user
    [Documentation]   This keyword creates executive user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_create_user    ${CREATE_USER_DATA}    Executive
    I verify result    ${result}

I create supervisor user
    [Documentation]   This keyword creates supervisor user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_create_user    ${CREATE_USER_DATA}    Supervisor
    I verify result    ${result}

I create professional agent user
    [Documentation]   This keyword creates professional-agent user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_create_user    ${CREATE_USER_DATA}    Professional-Agent
    I verify result    ${result}

I create group manager user
    [Documentation]   This keyword creates group manager user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_create_user    ${CREATE_USER_DATA}    Group Manager
    I verify result    ${result}

I create analyst user
    [Documentation]   This keyword creates analyst user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_create_user    ${CREATE_USER_DATA}    Analyst
    I verify result    ${result}

I create user access manager user
    [Documentation]   This keyword creates user access manager user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    verify_create_user    ${CREATE_USER_DATA}    UserAccessManager
    I verify result    ${result}
