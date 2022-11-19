"""
Module: This is the login module which contains methods for functionality related to Login and Logout.
"""
import os
import random
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Login:
    """Login functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common
    def close_force_login_pop_up(self):
        """Method to close force login pop up."""
        try:
            self.action.explicit_wait('force_login_ok_btn')
            self.action.click_element('force_login_ok_btn')
            return True
        except Exception as e:
            print("Error closing force login pop up: ", e)
            return True

    def login(self, **kwargs) -> bool:
        """Login to Ameyo system"""
        self.action.explicit_wait('user_id_input')
        self.action.explicit_wait('password_input')
        self.action.input_text('user_id_input', kwargs['username'])
        self.action.input_text('password_input', kwargs['password'])
        self.action.click_element('login_btn')
        self.close_force_login_pop_up()
        assert self.action.is_presence_of_element_located('logout_btn'), "Logout button not located after login."
        return True

    def login_new_password(self, user, pwd) -> bool:
        """Login to Ameyo system"""
        self.action.explicit_wait('user_id_input')
        self.action.explicit_wait('password_input')
        self.action.input_text('user_id_input', user)
        self.action.input_text('password_input', pwd)
        self.action.click_element('login_btn')
        self.close_force_login_pop_up()
        assert self.action.is_presence_of_element_located('logout_btn'), "Logout button not located after login."
        return True

    def logout_from_campaign_selection_page(self, **kwargs) -> bool:
        """Logout from Ameyo system"""
        assert self.action.is_presence_of_element_located('logout_btn'), "Logout button not located."
        self.action.click_element('logout_btn')
        self.common.close_alert_if_exists()
        return True

    def logout_from_ameyo_homepage(self):
        """Logout from Ameyo Homepage"""
        self.action.is_presence_of_element_located('preferences_drop_down_btn')
        self.action.click_element('preferences_drop_down_btn')
        self.action.explicit_wait('preferences_logout_btn', ec='element_to_be_clickable')
        self.action.click_element('preferences_logout_btn')
        self.common.close_alert_if_exists()
        return True

    def verify_login_error_msg(self):
        """Gets login error message."""
        self.action.explicit_wait('login_error_msg_span', 60)
        expected = 'UserId or Password is either incorrect or left blank'
        msg = self.action.get_text('login_error_msg_span')
        assert msg == expected, f'Login error miss matched. expected: {expected}, found:{msg}'

    def login_failure(self, kwargs, username_type, password_type):
        """Method to test failure cases for login."""
        if username_type == 'incorrect_username' and password_type == 'incorrect_password':
            self.action.input_text('user_id_input', username_type)
            self.action.input_text('password_input', password_type)
            self.action.click_element('login_btn')
            self.verify_login_error_msg()
        elif username_type == 'correct_username' and password_type == 'incorrect_password':
            self.action.input_text('user_id_input', kwargs['username'])
            self.action.input_text('password_input', password_type)
            self.action.click_element('login_btn')
            self.verify_login_error_msg()
        elif username_type == 'incorrect_username' and password_type == 'correct_password':
            self.action.input_text('user_id_input', username_type)
            self.action.input_text('password_input', kwargs['password'])
            self.action.click_element('login_btn')
            self.verify_login_error_msg()
        elif username_type == 'blank_username' and password_type == 'blank_password':
            self.action.input_text('user_id_input', '')
            self.action.input_text('password_input', '')
            self.action.click_element('login_btn')
            self.verify_login_error_msg()
        else:
            assert False, f'Invalid failure case requested for login: {username_type} and {password_type}'
        return True

    def make_campaign_selection(self, dropdown_locator, search_box_locator, value):
        """This function will select campaign as per given inputs"""
        self.action.click_element(dropdown_locator)
        self.action.input_text(search_box_locator, value)
        self.action.press_key(search_box_locator, "ARROW_DOWN")
        self.action.press_key(search_box_locator, "ENTER")

    def select_campaign(self, kwargs, user_type, voice_campaign_type="voice_outbound", workbench=False) -> bool:
        """This function will select campaign"""
        current_url = self.action.get_current_url()
        if 'executive' in user_type.lower():
            if 'agentConfiguration' in current_url:
                if kwargs['interaction']:
                    self.action.click_element("dropdown_interaction")
                    self.action.select_from_ul_dropdown_using_text('ul_campaign_selector', kwargs['interaction'])
                if kwargs['chat']:
                    self.action.click_element("dropdown_chat")
                    self.action.select_from_ul_dropdown_using_text('ul_campaign_selector', kwargs['chat'])
                if voice_campaign_type:
                    self.action.click_element("dropdown_voice")
                    for voice_campaign in voice_campaign_type.split(','):
                        if kwargs.get(voice_campaign):
                            self.action.select_from_ul_dropdown_using_text('ul_campaign_selector', kwargs.get(voice_campaign))
                if kwargs['video']:
                    self.action.click_element("dropdown_video")
                    self.action.select_from_ul_dropdown_using_text('ul_campaign_selector', kwargs['video'])
                self.action.click_element("button_next")
            else:
                print("Already on home page.", current_url)
        elif workbench and user_type.lower() == 'supervisor':
            self.action.click_element('workbench_tab')
            if kwargs['interaction']:
                self.make_campaign_selection('dropdown_interaction', 'textbox_search', kwargs['interaction'])
            if kwargs['chat']:
                self.make_campaign_selection('dropdown_chat', 'textbox_search', kwargs['chat'])
            if kwargs['voice']:
                self.action.click_element('dropdown_voice_supervisor')
                for voice_campaign in kwargs['voice'].split(','):
                    self.action.select_list_item_using_text('dropdown_items', voice_campaign)
            if kwargs['video']:
                self.make_campaign_selection('dropdown_video_supervisor', 'textbox_search', kwargs['video'])
            self.action.click_element("button_next")
        return True

    def select_extension(self, kwargs) -> bool:
        """This function will select extension."""
        current_url = self.action.get_current_url()
        if any([i in current_url for i in ['agentConfiguration', 'LiveMonitoring', 'MonitoringNavBar']]) and \
                self.action.is_presence_of_element_located('extension_selection_modal_header'):
            self.action.explicit_wait("extension_dropdown")
            self.action.click_element("extension_dropdown")
            self.action.select_from_ul_dropdown_using_text("ul_campaign_selector", kwargs['extension'])
            self.action.explicit_wait("phone_number_input_for_extension")
            self.action.input_text("phone_number_input_for_extension", f'{random.randrange(1, 10**3):3}')
            self.action.explicit_wait("extension_save_btn")
            self.action.click_element("extension_save_btn")
        return True
