"""
Module: This is the user module which contains methods for functionality related to creatio, updation or deletion of users.
"""
import os
import sys
import time

from selenium.webdriver.common.by import By
from uuid import uuid4

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class User:
    """User functionality class"""
    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def _wait_for_dropdown_to_load(self, user_type):
        """Waits for user dropdown to load with data.
            Maximum wait time is 1 minute.
        """
        current_time = time.time()
        while user_type not in self.action.get_text('user_type_dropdown') and time.time() - current_time <= 60:
            time.sleep(2)

    def _wait_for_searched_user_record_to_load(self, expected_records=1):
        """Waits for searched user to be loaded in table.
            Maximum wait time is 1 minute.
        """
        current_time = time.time()
        while self.get_total_user_records() != expected_records and time.time() - current_time <= 60:
            time.sleep(3)

    def get_total_user_records(self):
        """Gets total user records."""
        records_str = self.action.get_text('total_user_records')
        return int(records_str.split('of')[-1].strip())

    def open_user_tab(self):
        """Opens user tab."""
        current_url = self.action.get_current_url()
        print(current_url)
        if 'agentMonitoring' in current_url:
            print("Already selected user's tab.")
            return
        self.action.explicit_wait('user_tab', ec='element_to_be_clickable')
        self.action.click_element('user_tab')
        self.action.explicit_wait('user_table_search_input')

    def search_user(self, userid_text, expected_records=1):
        """Searches for requested user in user table and waits for records to load."""
        self.action.input_text('user_table_search_input', userid_text)
        self.action.press_key('user_table_search_input', 'ENTER')
        self._wait_for_searched_user_record_to_load(expected_records)
        return True

    def create_user(self,user_type):
        """Creates requested user."""
        self.open_user_tab()
        user_name_text = f"aaa_{'_'.join(user_type.split(' '))}_name"
        userid_text = f"aaa_{'_'.join(user_type.split(' '))}_{str(uuid4())[:4]}_id"
        password = self.common.generate_random_password()
        self.action.click_element('create_user_btn')
        self.action.explicit_wait('create_user_id_input')
        self.action.input_text('create_user_id_input', userid_text)
        self.action.input_text('user_name_input', user_name_text)
        self.action.input_text('create_password_input', password)
        self.action.input_text('confirm_password_input', password)
        self.action.input_text('phone_number_input', 9999999999)
        self._wait_for_dropdown_to_load(user_type)
        self.action.click_element('user_type_dropdown')
        self.action.input_text('user_type_dropdown_search', user_type)
        self.action.select_from_ul_dropdown_using_text('user_type_dropdown_list', user_type)
        self.action.click_element('save_user_btn')
        self.common.wait_for_toast_to_appear_and_disappear()
        return userid_text

    def verify_create_user(self,user_type):
        """Verifies creating user persona."""
        user_id_text = self.create_user(user_type)
        self.action.input_text('user_table_search_input', user_id_text)
        self.action.press_key('user_table_search_input', 'ENTER')
        self._wait_for_searched_user_record_to_load()
        user_table_user_id = self.action.get_table_cell_data('user_table_tbody', row=0, col=1)
        user_table_user_type = self.action.get_table_cell_data('user_table_tbody', row=0, col=3)
        assert user_table_user_id == user_id_text, f'Expected: {user_id_text} user not found in the user table rows, found: {user_table_data}'
        assert user_table_user_type == user_type, f'Expected: {user_type} user type not found in the user table rows, found: {user_table_user_type}'
        return True, user_id_text

    def delete_user(self, userid_text, admin_password, user_type):
        """Deletes requested user."""
        self.open_user_tab()
        self.search_user(userid_text, expected_records=1)
        user_table_user_id_col = self.action.get_table_cell_data('user_table_tbody', row=0, col=1, raw_cell=True)
        user_table_user_id_col.click()
        self.action.click_element('delete_user_btn')
        self.action.explicit_wait('confirm_delete_user_btn', 60)
        self.action.click_element('confirm_delete_user_btn')
        self.action.explicit_wait('authorize_delete_user_password_input')
        self.action.input_text('authorize_delete_user_password_input', admin_password)
        self.action.click_element('submit_delete_user_btn')
        self.common.wait_for_toast_to_appear_and_disappear()
        return True

    def verify_delete_user(self, user_type, admin_password, userid_text):
        """Method to verify deletion of requested user."""
        self.delete_user(userid_text, admin_password, user_type)
        # Re-verify if user was deleted
        self.search_user(userid_text, expected_records=0)
        user_table_user_id = self.action.get_table_cell_data('user_table_tbody', row=0, col=1, raise_error=False)
        user_table_user_type = self.action.get_table_cell_data('user_table_tbody', row=0, col=3, raise_error=False)
        assert user_table_user_id != userid_text, f'Deleted user: {userid_text}  found in the user table rows: {user_table_user_id} after deletion!'
        assert user_table_user_type != user_type, f'Deleted user type: {user_type}  found in the user table rows: {user_table_user_type} after deletion!'
        return True

    def open_update_user_form(self, userid_text):
        """Opens update user form."""
        self.open_user_tab()
        self.search_user(userid_text, expected_records=1)
        self.action.click_element('edit_user_link')
        self.action.explicit_wait('edit_user_password_input')
        return self.action.get_element_attribute('edit_user_username_input', 'value') + '_updated'

    def update_user(self, userid_text, admin_password):
        """Updates requested user."""
        edited_username = self.open_update_user_form(userid_text)
        password = self.common.generate_random_password()
        self.action.input_text('edit_user_username_input', edited_username)
        self.action.input_text('edit_user_password_input', password)
        self.action.input_text('edit_user_confirm_password_input', password)
        self.action.click_element('apply_edit_user_btn')
        self.action.explicit_wait('authorize_edit_user_password_input')
        self.action.input_text('authorize_edit_user_password_input', admin_password)
        self.action.click_element('submit_edit_user_btn')
        self.common.wait_for_toast_to_appear_and_disappear()
        return edited_username

    def verify_update_user(self, user_type, admin_password, userid_text):
        """Method to verify update of requested user."""
        edited_username_expected = self.update_user(userid_text, admin_password)
        edited_username = self.open_update_user_form(userid_text)
        self.action.click_element('cancel_edit_user_btn')
        assert edited_username != edited_username_expected, f"Username should be updated to {edited_username_expected}, found:{edited_username}"
        return True
