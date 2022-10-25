"""
Module: This is the login module which contains methods for functionality related to call details page.
"""
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class CallDetails:
    """Call Details functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def delete_callback(self):
        """this function will delete callback"""
        self.action.click_element('delete_callback')
        self.action.input_text("text_delete_message", 'delete')
        self.action.click_element("btn_delete_popup")

    def verify_callback(self, kwargs):
        """This function will verify callback details and delete"""
        self.action.click_element('call_details_tab')
        self.action.click_element('callback_tab')
        time.sleep(1)
        self.action.click_element('btn_filter')
        self.action.click_element('btn_filter_select_all')
        self.action.click_element('btn_apply_filter')
        time.sleep(2)
        data = self.action.get_table_row_values('table_data')
        assert kwargs['actions'] in data[0], "Failed: There is no callback entry found"
        self.delete_callback()
        return True

    def verify_call_history(self, kwargs):
        """This function will verify call history details"""
        self.action.click_element('call_details_tab')
        self.action.click_element('call_history_tab')
        time.sleep(1)
        self.action.click_element('btn_filter')
        if kwargs['campaign'].lower() == 'finance_outbound':
            self.action.click_element('btn_filter_finance_outbound')
        elif kwargs['campaign'].lower() == 'finance_inbound':
            self.action.click_element('btn_filter_finance_inbound')
        for disposition_filter in kwargs['disposition'].split(','):
            if disposition_filter.lower() == 'select_all':
                self.action.click_element('btn_filter_select_all')
        self.action.click_element('btn_apply_filter')
        time.sleep(2)
        data = self.action.get_table_row_values('table_data')
        print(data)
        self.action.click_element('btn_listen')
        assert self.action.is_presence_of_element_located('audio_panel') is True
        self.action.click_element('close_audio')
        return True
