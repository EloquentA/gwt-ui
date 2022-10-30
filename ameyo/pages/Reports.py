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
        self.action.is_presence_of_element_located('reports_tab')
        self.action.click_element('reports_tab')
        self.action.switch_to_frame('reports_frame')
        self.handle_no_reports_found_alert()
        self.action.click_element('home_tab')
        self.action.click_element('report_list_tab')
        self.action.switch_to_default_frame()
        return True

    def assign_all_default_reports_to_user(self, replace_dict):
        """Assigns all default reports to given user via Management-> User Privilege"""
        try:
            self.action.is_presence_of_element_located('reports_tab')
            self.action.click_element('reports_tab')
            self.action.switch_to_frame('reports_frame')
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
            self.action.click_element('reports_tab')
            self.action.switch_to_frame('reports_frame')
            self.action.click_element('home_tab')
            self.action.is_presence_of_element_located('report_list_table')
            print(report_name)
            if report_name is not None:
                reports_name_elements = self.action.get_element('report_name_column')
                reports_name_list = [element.text for element in reports_name_elements]
                print(reports_name_list)
                assert report_name in reports_name_list, "Expected Report not found in assigned reports list"
        finally:
            self.action.switch_to_default_frame()
        return True
