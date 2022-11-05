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

Validate rerun report from queue
    [Documentation]   This keyword validates the re-run of reports from the Queue>>Report Queue
    [Arguments]  ${instance}    ${report_name}    ${format_list}=${format_list}
    ${result}=   call method    ${instance}    validate_rerun_report_from_queue    ${report_name}    ${format_list}
    I verify result    ${result}

Create template and run report from template
    [Documentation]   This keyword creates template and run report via template"""
    [Arguments]  ${instance}    ${report_name}    ${template_name}=TestTemplate    ${current_time_duration}=Year    ${format_list}=${format_list}
    ${result}=   call method    ${instance}    create_template_and_run_report_from_template    ${report_name}    ${template_name}    ${current_time_duration}    ${format_list}
    I verify result    ${result}
