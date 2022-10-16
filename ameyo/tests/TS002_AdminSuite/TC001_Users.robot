*** Settings ***
Documentation     Ameyo User test cases
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Suite Initialization    admin
Suite Teardown    Suite Cleanup

# Keywords Definition file
Resource          ../../keywords/SetupTeardown.robot
Resource          ../../keywords/UserKeywords.robot
Resource          ../../keywords/CommonKeywords.robot
Resource          ../../keywords/LoginKeywords.robot


# Main library file which contains methods to perform some functionality
Library           ../../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1

*** Test Cases ***
TC - Create executive user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create executive user    ${instance1}

TC - Create supervisor user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create supervisor user    ${instance1}

TC - Create professional agent user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create professional agent user    ${instance1}

TC - Create group manager user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create group manager user    ${instance1}

TC - Create analyst user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create analyst user    ${instance1}

TC - Create user access manager user
    [Tags]  smoke    testid=AP-16047-1    regression
    I create user access manager user    ${instance1}

TC - Update executive user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update executive user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Update supervisor user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update supervisor user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Update professional agent user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update professional agent user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Update group manager user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update group manager user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Update analyst user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update analyst user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Update user access manager user
    [Tags]  smoke    testid=AP-16047-2    regression
    I update user access manager user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Delete executive user
    [Tags]  smoke    testid=AP-16047-3    regression
    I delete executive user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Delete supervisor user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I close alert if present    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete supervisor user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Delete professional agent user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I close alert if present    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete professional agent user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Delete group manager user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete group manager user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Delete analyst user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete analyst user    ${instance1}    ${CREDENTIALS['admin']['password']}

TC - Delete user access manager user
    [Tags]  smoke    testid=AP-16047-3    regression
    # TODO: Remove this once UI stops generating multiple modal doms each time you open delete modal
    I logout from ameyo homepage    ${instance1}
    I login into Ameyo  ${instance1}    admin
    I delete user access manager user    ${instance1}    ${CREDENTIALS['admin']['password']}
