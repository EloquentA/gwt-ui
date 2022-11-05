"""
Module: This is the group module which contains methods for functionality related to group creation, updation, deletion
    and user assignment to group.
"""
import os
import sys
import time
from uuid import uuid4

from selenium.webdriver.common.by import By


sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action

class AdminGroup:
    """Group functionality class"""
    def __init__(self, web_browser, common, admin_user):
        self.action = Action(web_browser)
        self.common = common
        self.admin_user = admin_user

    def open_group_tab(self):
        """Opens group tab."""
        self.admin_user.open_user_tab()
        self.action.click_element('group_sub_tab')

    def is_group_present(self, group):
        """Checks if group present in groups table."""
        for i in range(self.common.get_total_records('total_groups_records', 'groups_table_tbody')):
            col_group = self.action.get_table_cell_data('groups_table_tbody', row=i, col=0)
            print(col_group, group)
            if col_group == group:
                return True
        else:
            return False

    def _wait_for_group_name_input_to_load(self):
        """Waits for group name input to be loaded in edit window.
            Maximum wait time is 10 seconds.
        """
        current_time = time.time()
        while not self.action.get_value('group_name_input') and time.time() - current_time <= 10:
            time.sleep(3)

    def assign_user_to_group(self, search_user='executive'):
        """Assigns user to group."""
        search_user, _ = self.common.get_col_text_from_ameyo_table(
            search_query_str=search_user,
            page_limit_selector='available_page_limit',
            total_records_selector='total_available_users_and_groups_records',
            table_selector='available_users_and_groups_table_tbody',
            table_search_input='available_users_and_group_search_input',
            click_on_row=True
        )
        self.action.explicit_wait('assign_user_btn', ec='element_to_be_clickable')
        self.action.click_element('assign_user_btn')
        return search_user

    def open_edit_group(self,group, placement='before'):
        """Opens edit group form."""
        for i in range(self.common.get_total_records('total_groups_records', 'groups_table_tbody')):
            col_group = self.action.get_table_cell_data('groups_table_tbody', row=i, col=0)
            if col_group == group:
                record_col = self.action.get_table_cell_data('groups_table_tbody', row=i, col=5, raw_cell=True)
                actions = record_col.find_elements(By.TAG_NAME, "i")
                for action in actions:
                    if 'pencil' in action.get_attribute('class'):
                        action.click()
                        break
                else:
                    assert False, "Edit button not found in actions."
                break
        else:
            assert False, f"Group not found {placement} assignment. {group}"

    def verify_create_group(self, group_manager):
        """Method to verify creation of group."""
        self.open_group_tab()
        group_name_text = f"aaa_group_name_{str(uuid4())[:4]}"
        group_desc = f'This is test description  for {group_name_text}'
        current_records = self.common.get_total_records('total_groups_records', 'groups_table_tbody')
        if self.action.is_presence_of_element_located('create_new_group_btn_with_data') and \
                self.action.is_presence_of_element_located('groups_table_header'):
            self.action.click_element('create_new_group_btn_with_data')
        else:
            self.action.click_element('create_new_group_btn')
        self.action.input_text('group_name_input', group_name_text)
        self.action.input_text('group_desc_input', group_desc)
        self.assign_user_to_group(group_manager)
        self.action.click_element('submit_create_group_btn')
        self.action.explicit_wait('groups_table_header', 20)
        self.common.wait_for_searched_record_to_load('total_groups_records', 'groups_table_tbody', current_records+1)
        assert self.is_group_present(group_name_text), f"Group not found after creation. {group_name_text}"
        return True, group_name_text

    def verify_assign_group_users(self, group):
        """Method to verify assignment of users to group."""
        self.open_group_tab()
        current_records = self.common.get_total_records('total_groups_records', 'groups_table_tbody')
        self.open_edit_group(group)

        assigned_user = self.assign_user_to_group()
        self.action.explicit_wait('edit_group_btn', ec='element_to_be_clickable')
        self.action.click_element('edit_group_btn')
        self.action.explicit_wait('groups_table_header', 20)
        self.common.wait_for_searched_record_to_load('total_groups_records', 'groups_table_tbody', current_records)

        self.open_edit_group(group, 'after')

        # Check to verify user was added to assigned
        self.common.wait_for_data_to_load('assigned_users_and_groups_table_tbody')
        user, _ = self.common.get_col_text_from_ameyo_table(
            search_query_str=assigned_user,
            page_limit_selector='assigned_page_limit',
            total_records_selector='total_assigned_users_and_groups_records',
            table_selector='assigned_users_and_groups_table_tbody',
            table_search_input='assigned_users_and_group_search_input',
        )
        assert user == assigned_user, 'Assigned user not found in table.'
        self.action.click_element('users_sub_tab')
        return True

    def verify_update_group(self, group):
        """Method to verify updation of group."""
        self.open_group_tab()
        current_records = self.common.get_total_records('total_groups_records', 'groups_table_tbody')
        for i in range(current_records):
            col_group = self.action.get_table_cell_data('groups_table_tbody', row=i, col=0)
            if col_group == group:
                record_col = self.action.get_table_cell_data('groups_table_tbody', row=i, col=5, raw_cell=True)
                actions = record_col.find_elements(By.TAG_NAME, "i")
                for action in actions:
                    if 'pencil' in action.get_attribute('class'):
                        action.click()
                        break
                else:
                    assert False, "Edit button not found in actions."
                break
        else:
            assert False, f"Group not found before updation. {group}"
        self.action.explicit_wait('group_name_input', ec='element_to_be_clickable')
        self._wait_for_group_name_input_to_load()
        updated_group_name = f"{self.action.get_value('group_name_input')}_updated"
        self.action.input_text('group_name_input', updated_group_name)
        self.action.explicit_wait('edit_group_btn', ec='element_to_be_clickable')
        self.action.click_element('edit_group_btn')
        self.common.wait_for_searched_record_to_load('total_groups_records', 'groups_table_tbody', current_records)
        assert self.is_group_present(updated_group_name), "Updated group name not found in table data."
        return True

    def verify_delete_group(self, group):
        """Method to verify deletion of group."""
        self.open_group_tab()
        current_records = self.common.get_total_records('total_groups_records', 'groups_table_tbody')
        for i in range(current_records):
            col_group = self.action.get_table_cell_data('groups_table_tbody', row=i, col=0)
            if col_group == f'{group}_updated':
                record_col = self.action.get_table_cell_data('groups_table_tbody', row=i, col=5,raw_cell=True)
                actions = record_col.find_elements(By.TAG_NAME,"i")
                for action in actions:
                    if 'delete' in action.get_attribute('class'):
                        action.click()
                        break
                else:
                    assert False, "Delete button not found in actions."
                break
        else:
            assert False, f"Group not found before deletion. {group}"
        self.action.explicit_wait('confirm_delete_group_btn', ec='element_to_be_clickable')
        self.action.click_element('confirm_delete_group_btn')
        self.common.wait_for_searched_record_to_load('total_groups_records', 'groups_table_tbody', current_records-1)
        assert not self.is_group_present(group), f"Group found even after deletion. {group}"
        return True
