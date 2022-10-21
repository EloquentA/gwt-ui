*** Settings ***
Documentation     Keywords supported for user creation, updation and deletion operations
...               Developed By - Developer by EA
...               Comments:


*** Keywords **
Change Mapper Policy
    [Documentation]   This keyword changes Admin user mapping policy type
    [Arguments]  ${instance}    ${mapper_policy_type}
    ${result}=   call method    ${instance}    change_user_mapper_policy_via_admin    ${mapper_policy_type}
    I verify result    ${result}
