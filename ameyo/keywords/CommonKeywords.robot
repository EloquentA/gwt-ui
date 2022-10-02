*** Settings ***
Documentation     Keywords supported common functionalities
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot
Resource          ./LoginKeywords.robot

*** Keywords **
I open Ameyo home page ${instance}
    [Documentation]   This keyword opens Ameyo home page and maximazes wrowser window
    &{url}=    Create Dictionary      url=${AMEYO_URL}
    ${result}=   call method    ${instance}    open_home_page    ${url}
    I verify result ${result}

I close browser window ${instance}
    [Documentation]   This keyword closes the browser
    ${result}=   call method    ${instance}    close_browser_window
    I verify result ${result}

I refresh browser page ${instance}
    [Documentation]   This keyword refreshes the browser page
    ${result}=   call method    ${instance}    refresh_page
    I verify result ${result}

Ameyo setup ${instance}
    [Documentation]   This keyword sets up setup for every suite
    I open Ameyo home page ${instance}
    I login into Ameyo ${instance}

Ameyo teardown ${instance}
    [Documentation]   This keyword does teardown setup for every suite
    I logout from Ameyo ${instance1}
    I close browser window ${instance1}