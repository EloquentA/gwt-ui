*** Settings ***
Documentation     Keywords supported common functionalities
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot
Resource          ./LoginKeywords.robot

*** Keywords **
I open ameyo home page
    [Documentation]   This keyword opens Ameyo home page and maximazes wrowser window
    [Arguments]  ${instance}
    &{url}=    Create Dictionary      url=${AMEYO_URL}
    ${result}=   call method    ${instance}    open_home_page    ${url}
    I verify result    ${result}

I close browser window
    [Documentation]   This keyword closes the browser
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    close_browser_window
    I verify result    ${result}

I close alert if present
    [Documentation]   This keyword closes alert if present
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    close_alert_if_present
    I verify result    ${result}

Ameyo setup
    [Documentation]   This keyword sets up setup for every suite
    [Arguments]  ${instance}
    I open ameyo home page    ${instance}
    I close alert if present   ${instance}
    I login into Ameyo    ${instance}    ${RUN_AS}
    select campaign    ${instance}    ${RUN_AS}

Ameyo teardown
    [Documentation]   This keyword does teardown setup for every suite
    [Arguments]  ${instance}
    I logout from ameyo home page    ${instance1}
    I close browser window    ${instance1}