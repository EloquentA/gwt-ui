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
