# Keywords Definition file
Resource          ../CommonKeywords.robot
Resource          ../LoginKeywords.robot


# This section is specific to this testcase - for setup and teardown
*** Keywords ***
Root Initialization
    ${obj_instance1}=  Get library instance    Client1
    Set Global Variable	${instance1}  ${obj_instance1}
    Ameyo setup    ${instance1}    ${RUN_AS}

Root Cleanup
    Ameyo teardown    ${instance1}

Login Initialization
    ${current_instance1} =    Get Variable Value    ${instance1}
    Set Global Variable	${is_parent_setup}  """${current_instance1}""" != 'None'
    IF  not ${is_parent_setup}
        ${obj_instance1}=  Get library instance    Client1
        Set Global Variable	${instance1}  ${obj_instance1}
    END

Login Cleanup
    IF  ${is_parent_setup}
        Ameyo setup    ${instance1}    ${RUN_AS}
    ELSE
        I close browser window    ${instance1}
    END

Suite Initialization
    [Arguments]    ${req_run_as}
    ${current_instance1} =    Get Variable Value    ${instance1}
    Set Global Variable	${is_parent_setup}  """${current_instance1}""" != 'None'
    IF  not ${is_parent_setup}
        ${obj_instance1}=  Get library instance    Client1
        Set Global Variable	${instance1}  ${obj_instance1}
        Ameyo setup  ${instance1}    ${req_run_as}
    ELSE
        # If some other persona has been requested in common suite setup, login with requested persona
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    I logout from ameyo homepage    ${instance1}
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    Ameyo setup    ${instance1}    ${req_run_as}
    END

Suite Cleanup
    IF  not ${is_parent_setup}
        Ameyo teardown  ${instance1}
    END