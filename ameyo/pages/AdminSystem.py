"""
Module: This is the user module which contains methods for functionality related to settings needs to performed in Ameyo's admin system tab
"""
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action

class AdminSystem:
    """Admin System functionality class"""
    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def open_system_config_settings(self):
        """Opens settings tab under System-> System Configuration."""
        self.action.explicit_wait('system_tab', ec='element_to_be_clickable')
        self.action.click_element('system_tab')
        self.action.select_from_ul_dropdown_using_text('system_options_ul', 'System Configuration')
        self.action.explicit_wait('settings_tab', ec='element_to_be_clickable')
        self.action.click_element('settings_tab')

    def change_user_mapper_policy(self, mapper_policy):
        """Method to change user mapper policy under System Settings"""
        self.open_system_config_settings()
        self.action.explicit_wait('mapping_policy_dropdown', ec='element_to_be_clickable')
        self.action.click_element('mapping_policy_dropdown')
        self.action.select_from_ul_dropdown_using_text('mapping_policy_ul', mapper_policy)
        self.action.explicit_wait('mapping_policy_dropdown', ec='text_to_be_present_in_element', msg_to_verify=mapper_policy)
        self.action.explicit_wait('apply_btn', ec='element_to_be_clickable')
        self.action.click_element('apply_btn')
        assert self.common.validate_message_in_toast_popups("System setting successfully updated."), "Toast Message not as expected"