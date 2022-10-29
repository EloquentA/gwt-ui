"""
Module: This module contains functionality related to supervisor manage tab.
"""
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Manage:
    """Call Details functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def delete_callback(self):
        """this function will delete callback"""
        self.action.click_element('checkbox_callback')
        self.action.click_element('delete_user_btn')
        self.action.input_text("textbox_delete_confirmation", 'delete callback')
        self.action.click_element("btn_yes")

    def schedule_callback(self, kwargs, current_time):
        """This function will verify schedule callback under manage tab from
        supervisor"""
        self.action.click_element('manage_tab')
        self.action.click_element('callback')
        time.sleep(1)
        self.action.click_element('btn_add_callback')
        if kwargs['callback_type'].lower() == 'user':
            self.action.click_element('radio_btn_user')
            self.action.click_element('dropdown_select_user')
            self.action.input_text('textbox_search', kwargs['user'])
            self.action.press_key("textbox_search", "ENTER")
        if kwargs['callback_type'].lower() == 'campaign':
            self.action.click_element('radio_btn_campaign')
        self.action.click_element('callback_date')
        self.action.click_element('select_current_date')
        self.action.click_element('callback_time')
        time.sleep(1)
        replace_dict_hour = {'index': str(int(current_time[0]) - 1)}
        self.action.click_element('clock_hours', replace_dict=replace_dict_hour)
        replace_dict_minute = {'index': str(int(current_time[1])//5 + 1)}
        time.sleep(1)
        self.action.click_element('clock_minutes', replace_dict=replace_dict_minute)
        time.sleep(1)
        self.action.click_element('btn_ok')
        self.action.input_text('textbox_phone', kwargs['phone_number'])
        self.action.click_element('btn_save')
        time.sleep(1)
        self.delete_callback()
        return True

    def verify_call_details(self, username):
        """This function will verify call details under manage tab using supervisor"""
        self.action.click_element('link_call_details_tab')
        time.sleep(2)
        self.action.input_text('textbox_search_call_details', username)
        self.action.press_key("textbox_search_call_details", 'ENTER')
        time.sleep(1)
        self.action.click_element('btn_listen')
        assert self.action.is_presence_of_element_located('audio_panel') is True
        time.sleep(1)
        self.action.click_element("download_voice_log")
        time.sleep(2)
        self.action.click_element('close_audio')
        return True
