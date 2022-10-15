*** Settings ***
Documentation     Ameyo dispose and dial workflow
...               Developed By - Developer by EA
Library    String
# Suite Setup and Teardown
Suite Setup       Suite Initialization    ${RUN_AS}
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/LoginKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/HomePageKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - dispose and dial before call cut
    IF  ${is_parent_setup}
        I logout from ameyo homepage    ${instance1}
    END
    [Tags]  smoke    testid=AP-16014-1    regression
    I login into Ameyo    ${instance1}    ${RUN_AS}
    select campaign    ${instance1}    ${RUN_AS}
    ${customer_number1}=  Generate Random String  10  123456789
    Manual Dial Only    ${instance1}    ${customer_number1}
    dispose and dial    ${instance1}    dispose_type=selection    dial_position=dial_before_call_cut

TC - dispose and dial after call cut
    [Tags]  smoke    testid=AP-16014-2    regression
    ${customer_number2}=  Generate Random String  10  123456789
    Manual Dial Only    ${instance1}    ${customer_number2}
    dispose and dial    ${instance1}    dispose_type=quick    dial_position=dial_after_call_cut
