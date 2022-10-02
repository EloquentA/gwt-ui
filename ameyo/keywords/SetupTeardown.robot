# Keywords Definition file
Resource          ../CommonKeywords.robot


# This section is specific to this testcase - for setup and teardown
*** Keywords ***
Root Initialization
    ${obj_instance1}=  Get library instance    Client1
    Set Global Variable	${instance1}  ${obj_instance1}
    Ameyo setup ${instance1}

Root Cleanup
    Ameyo teardown ${instance1}

Login Initialization
    ${current_instance1} =    Get Variable Value    ${instance1}
    Set Global Variable	${is_parent_setup}  """${current_instance1}""" != 'None'
    IF  not ${is_parent_setup}
        ${obj_instance1}=  Get library instance    Client1
        Set Global Variable	${instance1}  ${obj_instance1}
    END
    I refresh browser page ${instance1}

Login Cleanup
    IF  ${is_parent_setup}
        Ameyo setup ${instance1}
    ELSE
        I close browser window ${instance1}
    END

Suite Initialization
    ${current_instance1} =    Get Variable Value    ${instance1}
    Set Global Variable	${is_parent_setup}  """${current_instance1}""" != 'None'
    IF  not ${is_parent_setup}
        ${obj_instance1}=  Get library instance    Client1
        Set Global Variable	${instance1}  ${obj_instance1}
        Ameyo setup ${instance1}
    END
    I refresh browser page ${instance1}

Suite Cleanup
    IF  not ${is_parent_setup}
        Ameyo teardown ${instance1}
    END