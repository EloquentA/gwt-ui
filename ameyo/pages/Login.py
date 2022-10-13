"""
Module: This is the login module which contains methods for functionality related to Login and Logout.
"""
import os
import sys

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
        self.action.is_presence_of_element_located('logout_btn')
        return True

    def logout_from_campaign_selection_page(self, **kwargs) -> bool:
        """Logout from Ameyo system"""
        self.action.is_presence_of_element_located('logout_btn')
        self.action.click_element('logout_btn')
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

    def select_campaign(self, kwargs) -> bool:
        """This function will select campaign"""
        current_url = self.action.get_current_url()
        if 'agentConfiguration' in current_url:
            if kwargs['interaction']:
                self.action.click_element("dropdown_interaction")
                self.action.input_text("textbox_search", kwargs['interaction'])
                self.action.press_key("textbox_search", "ARROW_DOWN")
                self.action.press_key("textbox_search", "ENTER")
            if kwargs['chat']:
                self.action.click_element("dropdown_chat")
                self.action.input_text("textbox_search", kwargs['chat'])
                self.action.press_key("textbox_search", "ARROW_DOWN")
                self.action.press_key("textbox_search", "ENTER")
            if kwargs['voice']:
                self.action.click_element("dropdown_voice")
                self.action.input_text("textbox_search", kwargs['voice'])
                self.action.press_key("textbox_search", "ARROW_DOWN")
                self.action.press_key("textbox_search", "ENTER")
            if kwargs['video']:
                self.action.click_element("dropdown_video")
                self.action.input_text("textbox_search", kwargs['video'])
                self.action.press_key("textbox_search", "ARROW_DOWN")
                self.action.press_key("textbox_search", "ENTER")
            self.action.click_element("button_next")
        else:
            print("Already on home page.", current_url)
        return True
