"""
Module: This is the Report module which contains methods for functionality related to ART - Reports.
"""
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
)
from action import Action

class Reports:
    """Report functionality class"""

    def __init__(self, web_browser):
        self.action = Action(web_browser)

    def navigate_to_reports(self):
        """This will navigate to Reports Tab and switches the frame"""
        current_url = self.action.get_current_url()
        if 'Reports' not in current_url:
            self.action.is_presence_of_element_located('reports_tab')
            self.action.click_element('reports_tab')
        self.action.switch_to_frame('reports_frame')
        return True

    def handle_no_reports_found_alert(self):
        """Handles alert when no reports are assigned"""
        try:
            self.action.explicit_wait('ok_btn_report_tab_alert')
            self.action.click_element('ok_btn_report_tab_alert')
            return True
        except Exception as e:
            print("Error closing No Report Found Alert: ", e)
            return True

    def validate_reports_tab(self):
        """Validate reports tab for admin and supervisor UI"""
        self.navigate_to_reports()
        self.handle_no_reports_found_alert()
        self.action.click_element('home_tab')
        self.action.click_element('report_list_tab')
        self.action.switch_to_default_frame()
        return True

    def assign_all_default_reports_to_user(self, replace_dict):
        """Assigns all default reports to given user via Management-> User Privilege"""
        try:
            self.navigate_to_reports()
            self.handle_no_reports_found_alert()
            self.action.click_element('management_tab')
            self.action.click_element('user_privilege_tab')
            self.action.click_element('user_name', replace_dict=replace_dict)
            self.action.click_element('privileges_type_select')
            self.action.select_from_dropdown_using_text('privileges_type_select', 'Available')
            self.action.explicit_wait('select_all_btn')
            self.action.click_element('select_all_btn')
            self.action.click_element('save_btn')
            self.action.explicit_wait('report_assign_modal')
            self.action.click_element('report_assign_modal')
            self.action.click_element('ok_btn_report_tab_alert')
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_reports_assigned_to_user(self, report_name=None):
        """Validates reports are assigned to the given user"""
        try:
            self.navigate_to_reports()
            self.action.click_element('home_tab')
            self.action.is_presence_of_element_located('report_list_table')
            print(report_name)
            if report_name is not None:
                self.action.input_text('reports_search_box', report_name)
                self.action.click_element('search_button')
                reports_name_elements = self.action.get_element('report_name_column')
                reports_name_list = [element.text for element in reports_name_elements]
                print(reports_name_list)
                assert report_name in reports_name_list, "Expected Report not found in assigned reports list"
        finally:
            self.action.switch_to_default_frame()
        return True

    def run_report_and_validate_download_in_required_formats(self, report_name, current_time_duration='Year', report_formats_list=['CSV','XLS','PDF','HTML']):
        """Search and Run specific report for given time window in all formats"""
        try:
            self.navigate_to_reports()
            self.action.click_element('home_tab')
            self.action.click_element('report_list_tab')
            self.action.is_presence_of_element_located('report_list_table')
            self.action.input_text('reports_search_box', report_name)
            self.action.click_element('search_button')
            self.action.element_should_contain_text('first_report_name', report_name)
            self.action.click_element('first_report_run_button')
            self.action.explicit_wait('for_current_radio')
            self.action.click_element('for_current_radio')
            self.action.click_element('nothing_selected_btn')
            self.action.click_element('time_duration_selection', replace_dict={'replace_value': current_time_duration})
            self.action.explicit_wait('select_all_campaigns')
            self.action.click_element('select_all_campaigns')
            self.action.explicit_wait('select_all_queues')
            self.action.click_element('select_all_queues')
            print(report_formats_list)
            for report_format in report_formats_list:
                self.action.click_element('report_format_checkbox', replace_dict={'replace_value': report_format})
            self.action.explicit_wait('run_report_btn', ec='element_to_be_clickable')
            self.action.click_element('run_report_btn')
            self.action.switch_to_default_frame()
            self.validate_report_in_queue_and_download(report_name, report_formats_list)
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_report_in_queue_and_download(self, report_name, report_formats_list=['CSV','XLS','PDF','HTML']):
        """Validate successful report run from queue and download it in all desired formats"""
        try:
            self.navigate_to_reports()
            self.action.click_element('queue_tab')
            self.action.click_element('report_queue_tab')
            self.action.element_should_contain_text('first_report_name', report_name)
            self.action.explicit_wait('first_report_queue_status', waittime=240, ec='text_to_be_present_in_element', msg_to_verify='SUCCESS')
            print(report_formats_list)
            if 'CSV' in report_formats_list:
                print("Downloading CSV")
                #Navigating to Template Queue tab just to reload the DOM as WA for table elements disappearing from DOM issue
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('first_report_queue_csv', ec='element_to_be_clickable')
                self.action.click_element('first_report_queue_csv')
            if 'XLS' in report_formats_list:
                print("Downloading XLS")
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('first_report_queue_xls', ec='element_to_be_clickable')
                self.action.click_element('first_report_queue_xls')
            if 'PDF' in report_formats_list:
                print("Downloading PDF")
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('first_report_queue_pdf', ec='element_to_be_clickable')
                self.action.click_element('first_report_queue_pdf')
            if 'HTML' in report_formats_list:
                print("Opening HTML")
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('first_report_queue_html', ec='element_to_be_clickable')
                self.action.click_element('first_report_queue_html')
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_rerun_report_from_queue(self, report_name, report_formats_list=['CSV', 'XLS', 'PDF', 'HTML']):
        """Validate the re-run of reports from the Queue>>Report Queue"""
        try:
            self.navigate_to_reports()
            self.action.click_element('queue_tab')
            self.action.click_element('report_queue_tab')
            self.action.element_should_contain_text('first_report_name', report_name)
            self.action.click_element('first_report_queue_rerun')
            print(report_formats_list)
            for report_format in report_formats_list:
                self.action.click_element('report_format_checkbox', replace_dict={'replace_value': report_format})
            self.action.explicit_wait('run_report_btn', ec='element_to_be_clickable')
            self.action.click_element('run_report_btn')
            self.action.switch_to_default_frame()
            self.validate_report_in_queue_and_download(report_name, report_formats_list)
        finally:
            self.action.switch_to_default_frame()
        return True