*** Settings ***
Documentation     Ameyo Knowledgebase page validation test case
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16002

# Suite Setup and Teardown
Suite Setup       Suite Initialization    supervisor
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/AgentHomePageKeywords.robot
Resource          ../../keywords/KnowledgeBase.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=supervisor    WITH NAME    Client1

*** Test Cases ***
TC - To verify knowledge base page is opening in supervisor
    [Tags]  smoke    testid=AP-16002-1    regression
    I validate knowledge base page    ${instance1}    supervisor
