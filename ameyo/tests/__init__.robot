*** Settings ***
Documentation     Common setup and teardown at root level
...               Developed By - Developer by EA

# Suite Setup and Teardown
Suite Setup       Root Initialization
Suite Teardown    Root Cleanup

# Keywords Definition file
Resource          ../keywords/SetupTeardown.robot
Resource          ../keywords/CommonKeywords.robot

# Main library file which contains methods to perform some functionality
Library           ../pages/Ameyo.py    browser_config=${BROWSER_CONFIG}    project=${PROJECT}    run_as=${RUN_AS}    WITH NAME    Client1
