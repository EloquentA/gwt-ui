*** Settings ***
Documentation     Ameyo User test cases
...               Developed By - Developer by EA
...               https://touchstone.ameyo.com/linkto.php?tprojectPrefix=AP&item=testcase&id=AP-16047

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup    admin

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/AdminUserKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=admin    WITH NAME    Client1

*** Test Cases ***
TC - Create executive user
    [Tags]  smoke    testid=AP-16047-1    regression
    ${created_user}=   I create executive user    ${instance1}
    Set Suite Variable    ${created_executive_user}    ${created_user}

TC - Create supervisor user
    [Tags]  smoke    testid=AP-16047-1    regression
    ${created_user}=   I create supervisor user    ${instance1}
    Set Suite Variable    ${created_supervisor_user}    ${created_user}


TC - Create professional agent user
    [Tags]  smoke    testid=AP-16047-1    regression
    ${created_user}=   I create professional agent user    ${instance1}
    Set Suite Variable    ${created_pa_user}    ${created_user}


TC - Create group manager user
    [Tags]  smoke    testid=AP-16047-1    regression
    ${created_user}=   I create group manager user    ${instance1}
    Set Suite Variable    ${created_gm_user}    ${created_user}


TC - Create analyst user
    [Tags]  smoke    testid=AP-16047-1    regression
    ${created_user}=   I create analyst user    ${instance1}
    Set Suite Variable    ${created_analyst_user}    ${created_user}


TC - Create user access manager user
    [Tags]  smoke    testid=AP-16047-1    regression
    ${created_user}=   I create user access manager user    ${instance1}
    Set Suite Variable    ${created_uam_user}    ${created_user}

TC - Update executive user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update executive user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_executive_user}

TC - Update supervisor user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update supervisor user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_supervisor_user}

TC - Update professional agent user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update professional agent user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_pa_user}

TC - Update group manager user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update group manager user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_gm_user}

TC - Update analyst user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update analyst user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_analyst_user}

TC - Update user access manager user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update user access manager user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_uam_user}

TC - Delete executive user
    [Tags]  smoke    testid=AP-16047-3    regression
    I delete executive user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_executive_user}

TC - Delete supervisor user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I close alert if present    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete supervisor user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_supervisor_user}

TC - Delete professional agent user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I close alert if present    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete professional agent user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_pa_user}

TC - Delete group manager user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete group manager user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_gm_user}

TC - Delete analyst user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete analyst user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_analyst_user}

TC - Delete user access manager user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete user access manager user    ${instance1}    ${CREDENTIALS['admin']['password']}    ${created_uam_user}
