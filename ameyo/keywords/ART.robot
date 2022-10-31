*** Settings ***
Documentation     Keywords supported ART functionalities
...               Developed By - Developer by EA
...               Comments:

# Keywords Definition file
Resource          ./VerifyResult.robot
*** Variables ***
@{format_list}=    CSV    XLS    PDF    HTML

*** Keywords **
I validate reports tab
    [Documentation]   This keyword validates whether the report tab is working in admin and supervisor
    [Arguments]  ${instance}
    ${result}=   call method    ${instance}    validate_reports_tab
    I verify result    ${result}

Admin assigns all default reports to user
    [Documentation]   This keyword assigns all default reports to specific user via admin management tab
    [Arguments]  ${instance}    ${replace_dict}
    ${result}=   call method    ${instance}    assign_all_default_reports_to_user    ${replace_dict}
    I verify result    ${result}

Validates reports assigned to user
    [Documentation]   This keyword validates the reports are assigned to given user
    [Arguments]  ${instance}    ${report_name}=${None}
    ${result}=   call method    ${instance}    validate_reports_assigned_to_user    ${report_name}
    I verify result    ${result}

Run specific report and validate download in required formats
    [Documentation]   This keyword runs specific report and validate successful download in all formats
    [Arguments]  ${instance}    ${report_name}    ${current_time_duration}=Year    ${format_list}=${format_list}
    ${result}=   call method    ${instance}    run_report_and_validate_download_in_required_formats    ${report_name}    ${current_time_duration}    ${format_list}
    I verify result    ${result}