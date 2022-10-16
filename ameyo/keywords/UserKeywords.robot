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

I delete executive user
    [Documentation]   This keyword deletes executive user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_delete_user    Executive    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I delete supervisor user
    [Documentation]   This keyword deletes supervisor user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_delete_user    Supervisor    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I delete professional agent user
    [Documentation]   This keyword deletes professional agent user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_delete_user    Professional-Agent    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I delete group manager user
    [Documentation]   This keyword deletes group manager user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_delete_user    Group Manager    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I delete analyst user
    [Documentation]   This keyword deletes analyst user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_delete_user    Analyst    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I delete user access manager user
    [Documentation]   This keyword deletes user access manager user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_delete_user    UserAccessManager    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I update executive user
    [Documentation]   This keyword updates executive user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_update_user    Executive    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I update supervisor user
    [Documentation]   This keyword updates supervisor user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_update_user    Supervisor    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I update professional agent user
    [Documentation]   This keyword updates professional agent user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_update_user    Professional-Agent    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I update group manager user
    [Documentation]   This keyword updates group manager user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_update_user    Group Manager    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I update analyst user
    [Documentation]   This keyword updates analyst user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_update_user    Analyst    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}

I update user access manager user
    [Documentation]   This keyword updates user access manager user
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_update_user    UserAccessManager    ${admin_password}    ${CREATE_USER_DATA}
    I verify result    ${result}
