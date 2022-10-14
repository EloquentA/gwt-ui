*** Settings ***
Documentation     Keywords supported for user creation, updation and deletion operations
...               Developed By - Developer by EA
...               Comments:


*** Keywords **
I create executive user
    [Documentation]   This keyword creates executive user
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    create_user    executive
    I verify result    ${result}

