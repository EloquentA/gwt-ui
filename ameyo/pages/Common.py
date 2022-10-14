"""
Module: This is the common module which contains methods for common flows in AMEYO UI."""
import datetime
import os
import sys
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
        if not self.action._get_attribute('status_dropdown_link', 'title') == desired_state:
            self.action.explicit_wait('status_dropdown_link')
            self.action.click_element('status_dropdown_link')
            self.action.explicit_wait(new_state_element)
            self.action.click_element(new_state_element)
        return True
