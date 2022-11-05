*** Settings ***
Documentation     Keywords supported for group creation, updation, deletion and assign users to group operations
...               Developed By - Developer by EA


*** Keywords **
I create group
    [Documentation]   This keyword creates group
    [Arguments]  ${instance}    ${admin_password}
    ${result}=   call method    ${instance}    verify_create_group    ${CREDENTIALS['group_manager']['username']}
    I verify result    ${result}
    Return From Keyword    ${result[2]}

I assign user to group
    [Documentation]   This keyword assigns user to group
    [Arguments]  ${instance}    ${created_group}
    ${result}=   call method    ${instance}    verify_assign_group_users    ${created_group}
    I verify result    ${result}

I update group
    [Documentation]   This keyword updates group
    [Arguments]  ${instance}    ${admin_password}    ${created_group}
    ${result}=   call method    ${instance}    verify_update_group    ${created_group}
    I verify result    ${result}

I delete group
    [Documentation]   This keyword deletes group
    [Arguments]  ${instance}    ${admin_password}    ${created_group}
    ${result}=   call method    ${instance}    verify_delete_group    ${created_group}
    I verify result    ${result}
