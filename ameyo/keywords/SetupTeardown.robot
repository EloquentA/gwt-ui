# Keywords Definition file
Resource          ../CommonKeywords.robot
Resource          ../LoginKeywords.robot


# This section is specific to this testcase - for setup and teardown
*** Keywords ***
Root Initialization
    [Arguments]    ${voice_campaign_type}=voice_outbound
    ${obj_instance1}=  Get library instance    Client1
    Set Global Variable	${instance1}  ${obj_instance1}
    Ameyo setup    ${instance1}    ${RUN_AS}    ${voice_campaign_type}

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
    [Arguments]    ${req_run_as}    ${voice_campaign_type}=voice_outbound    ${override}=${FALSE}
    ${current_instance1} =    Get Variable Value    ${instance1}
    Set Global Variable	${is_parent_setup}  """${current_instance1}""" != 'None'
    IF  not ${is_parent_setup}
        ${obj_instance1}=  Get library instance    Client1
        Set Global Variable	${instance1}  ${obj_instance1}
        Ameyo setup  ${instance1}    ${req_run_as}    ${voice_campaign_type}
    ELSE IF    ${override}
        I logout from ameyo homepage    ${instance1}
        Ameyo setup    ${instance1}    ${req_run_as}    ${voice_campaign_type}
    ELSE
        # If some other persona has been requested in common suite setup, login with requested persona
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    I logout from ameyo homepage    ${instance1}
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    Ameyo setup    ${instance1}    ${req_run_as}    ${voice_campaign_type}
    END

Suite Cleanup
    [Arguments]    ${req_run_as}=${RUN_AS}
    IF  not ${is_parent_setup}
        Ameyo teardown  ${instance1}
    ELSE
        # Close second tab if present
        I close requested tab    ${instance1}    1    ${FALSE}
        # Close second tab if present
        I close requested tab    ${instance1}    2    ${FALSE}
        # If some other persona has been requested in common suite setup, login with original persona on suite cleanup
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    I logout from ameyo homepage    ${instance1}
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    Ameyo setup    ${instance1}    ${RUN_AS}
    END

Suite Initialization For Two Executives And Requested User
    [Documentation]   This keyword does suite initialization for two executives and one requested user
    [Arguments]  ${req_run_as}=supervisor
    Suite Initialization    executive
    I open ameyo home page in separate tab    ${instance1}
    I switch to requested tab   ${instance1}    1
    Ameyo setup    ${instance1}    spare_executive
    I open ameyo home page in separate tab    ${instance1}
    I switch to requested tab   ${instance1}    2
    Ameyo setup    ${instance1}    ${req_run_as}

Suite Initialization For One Executive And Requested User
    [Documentation]   This keyword does suite initialization for one executive and one requested user
    [Arguments]  ${req_run_as}=supervisor    ${voice_campaign_type}=voice_outbound
    Suite Initialization    executive    ${voice_campaign_type}
    I open ameyo home page in separate tab    ${instance1}
    I switch to requested tab   ${instance1}    1
    Ameyo setup    ${instance1}    ${req_run_as}

Suite Initialization For Single Requested User And Customer Chat Window
    [Documentation]   This keyword does suite initialization for one executive and one customer chat window
    [Arguments]  ${req_run_as}
    Suite Initialization    chat_executive
    I open ameyo customer chat page in separate tab    ${instance1}    ${req_run_as}

Suite Initialization For Two Requested Users And Customer Chat Window
    [Documentation]   This keyword does suite initialization for one executive and one customer chat window
    [Arguments]  ${req_run_as}
    Suite Initialization    ${req_run_as}
    I open ameyo customer chat page in separate tab    ${instance1}    ${req_run_as}
    I open ameyo home page in separate tab    ${instance1}
    I switch to requested tab   ${instance1}    2
    Ameyo setup    ${instance1}    chat_supervisor

Suite Initialization For ToolBar
    [Arguments]    ${req_run_as}    ${voice_campaign_type}=voice_outbound    ${override}=${FALSE}
    ${current_instance1} =    Get Variable Value    ${instance1}
    Set Global Variable	${is_parent_setup}  """${current_instance1}""" != 'None'
    IF  not ${is_parent_setup}
        ${obj_instance1}=  Get library instance    Client1
        Set Global Variable	${instance1}  ${obj_instance1}
        Ameyo Toolbar setup  ${instance1}    ${req_run_as}
    ELSE IF    ${override}
        I logout from ameyo toolbar    ${instance1}
        Ameyo Toolbar setup    ${instance1}    ${req_run_as}
    ELSE
        # If some other persona has been requested in common suite setup, login with requested persona
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    I logout from ameyo toolbar    ${instance1}
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    Ameyo Toolbar setup    ${instance1}    ${req_run_as}
    END

Suite Cleanup Toolbar
    [Arguments]    ${req_run_as}=${RUN_AS}
    IF  not ${is_parent_setup}
        Ameyo Toolbar teardown  ${instance1}
    ELSE
        # Close second tab if present
        I close requested tab    ${instance1}    1    ${FALSE}
        # Close second tab if present
        I close requested tab    ${instance1}    2    ${FALSE}
        # If some other persona has been requested in common suite setup, login with original persona on suite cleanup
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    I logout from ameyo toolbar    ${instance1}
        Run Keyword If    '${req_run_as}' != '${RUN_AS}'    Ameyo Toolbar setup    ${instance1}    ${RUN_AS}
    END