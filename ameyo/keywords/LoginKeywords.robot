*** Settings ***
Documentation     Keywords supported for Login page
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot

*** Keywords ***
I login into Ameyo ${instance}
    [Documentation]   This keyword logs-in to Ameyo portal
    ${result}=   call method    ${instance}    ameyo_login    ${CREDENTIALS}
    I verify result ${result}

I logout from Ameyo ${instance}
    [Documentation]   This keyword logouts from the Ameyo portal
    ${result}=   call method    ${instance}    logout
    I verify result ${result}