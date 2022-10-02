*** Settings ***
Documentation     Keywords supported common functionalities
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot
Resource          ./LoginKeywords.robot

*** Keywords **
I open Ameyo home page
    [Documentation]   This keyword opens Ameyo home page and maximazes wrowser window
    [Arguments]  ${instance}
    &{url}=    Create Dictionary      url=${AMEYO_URL}
    ${result}=   call method    ${instance}    open_home_page    ${url}
    I verify result ${result}

I close browser window
    [Documentation]   This keyword closes the browser
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    close_browser_window
    I verify result ${result}

I refresh browser page
    [Documentation]   This keyword refreshes the browser page
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    refresh_page
    I verify result ${result}

Ameyo setup
    [Documentation]   This keyword sets up setup for every suite
    [Arguments]  ${instance}
    I open Ameyo home page ${instance}
    I login into Ameyo ${instance}

Ameyo teardown
    [Documentation]   This keyword does teardown setup for every suite
    [Arguments]  ${instance}
    I logout from Ameyo ${instance1}
    I close browser window ${instance1}