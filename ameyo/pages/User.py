"""
Module: This is the user module which contains methods for functionality related to creatio, updation or deletion of users.
"""
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class User:
    """User functionality class"""
    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def _wait_for_dropdown_to_load(self):
        """Waits for user dropdown to load with data.
            Maximum wait time is 1 minute.
        """
        current_time = time.time()
        while self.action.get_text('user_type_dropdown') != 'Administrator' and time.time() - current_time <= 60:
            time.sleep(1)

    def _wait_for_searched_user_record_to_load(self):
        """Waits for searched user to be loaded in table.
            Maximum wait time is 1 minute.
        """
        current_time = time.time()
        while self.get_total_user_records() != 1 and time.time() - current_time <= 60:
            time.sleep(1)

    def get_total_user_records(self):
        """Gets total user records."""
        records_str = self.action.get_text('total_user_records')
        return int(records_str.split('of')[-1].strip())

    def create_user(self, ref_data, user_type):
        """Creates requested user."""
        self.action.click_element('user_tab')
        user_name_text = f"aaa_{ref_data.get('username_prefix')}_{'_'.join(user_type.split(' '))}"
        user_id_text = f"aaa_{ref_data.get('userid_prefix')}_{'_'.join(user_type.split(' '))}"
        self.action.click_element('create_user_btn')
        self.action.input_text('create_user_id_input', user_id_text)
        self.action.input_text('user_name_input', user_name_text)
        self.action.input_text('create_password_input', ref_data.get('password'))
        self.action.input_text('confirm_password_input', ref_data.get('password'))
        self.action.input_text('phone_number_input', ref_data.get('phone_number'))
        self._wait_for_dropdown_to_load()
        self.action.click_element('user_type_dropdown')
        self.action.input_text('user_type_dropdown_search', user_type)
        self.action.select_from_ul_dropdown_using_text('user_type_dropdown_list', user_type)
        self.action.click_element('save_user_btn')
        return user_name_text

    def verify_create_user(self,ref_data, user_type):
        """Verifies creating user persona."""
        user_name_text = self.create_user(ref_data, user_type)
        self.action.input_text('user_table_search_input', user_name_text)
        self.action.press_key('user_table_search_input', 'ENTER')
        self._wait_for_searched_user_record_to_load()
        user_table_rows = self.action.get_table_row_elements('user_table')
        user_table_data = ''
        for row in user_table_rows:
            row_text = ( row.text or '')
            user_table_data += row_text
            if user_name_text in row_text and user_type in row_text:
                break
        else:
            assert False, f'Expected: {user_name_text} user not found in the user table rows: {user_table_data}'
        return True
