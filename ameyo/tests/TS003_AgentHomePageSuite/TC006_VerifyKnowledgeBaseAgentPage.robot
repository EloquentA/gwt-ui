*** Settings ***
Documentation     Ameyo Knowledgebase page validation test case
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16002

# Suite Setup and Teardown
Suite Setup       Suite Initialization    change_executive
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot
Resource          ../../keywords/KnowledgeBase.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=change_executive    WITH NAME    Client1

*** Test Cases ***
TC - To verify knowledge base page is opening in extension agent
    [Tags]  smoke    testid=AP-16002-1    regression
    I validate knowledge base page    ${instance1}    change_executive
    I logout from ameyo homepage    ${instance1}

TC - To verify knowledge base page is opening in webrtc agent
    [Tags]  smoke    testid=AP-16002-2    regression
    Ameyo setup    ${instance1}    executive
    I validate knowledge base page    ${instance1}    executive
