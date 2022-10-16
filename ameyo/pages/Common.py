"""
Module: This is the common module which contains methods for common flows in AMEYO UI."""
import datetime
import os
import random
import sys
import string
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Common:
    """Common functionality class"""

    def __init__(self, web_browser):
        self.action = Action(web_browser)

    def close_alert_if_exists(self, cancel=False, waittime=20):
        """Method to close force login pop up."""
        try:
            self.action.wait_for_alert_and_act(cancel, waittime)
            return True
        except Exception as e:
            print("Error closing alert after logout: ", e)
            return True

    def change_status(self, desired_state, new_state_element):
        """Method to change user status to desired state"""
        if not self.action.get_element_attribute('status_dropdown_link', 'title') == desired_state:
            self.action.explicit_wait('status_dropdown_link')
            self.action.click_element('status_dropdown_link')
            self.action.explicit_wait(new_state_element)
            self.action.click_element(new_state_element)
        return True

    @staticmethod
    def generate_random_password():
        """Generated random password."""
        # select 1 lowercase
        password = random.choice(string.ascii_lowercase)
        # select 1 uppercase
        password += random.choice(string.ascii_uppercase)
        # select 1 digit
        password += random.choice(string.digits)
        # select 1 special symbol
        password += random.choice(string.punctuation)
        # generate other characters
        password +=''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(5))
        print("Generated password is: ", password)
        return password

    def wait_for_toast_to_appear_and_disappear(self):
        """waits for toast to appear and disappear."""
        try:
            self.action.explicit_wait('toast_message_div', waittime=60)
            self.action.explicit_wait('toast_message_div', ec='invisibility_of_element_located', waittime=10)
        except Exception as err:
            print('Error while waiting for toast message to appear: ',err)
