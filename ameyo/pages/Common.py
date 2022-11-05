"""
Module: This is the common module which contains methods for common flows in AMEYO UI."""
import datetime
import os
import random
import sys
import string
import time
import requests

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
            self.action.explicit_wait('selected_agent_status', ec='text_to_be_present_in_element', msg_to_verify=desired_state)
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

    def hit_get_api_with_no_authentication(self, url, no_of_retries):
        """Hits GET API and validates success response"""
        for attempt in range(no_of_retries):
            resp = requests.get(url)
            if resp.status_code == 200:
                break

    def validate_message_in_toast_popups(self, expected_message):
        """Gets the text for all the popups present and validates the expected message present or not"""
        time.sleep(1)
        elements = self.action.get_element('toast_message_popup')
        toast_text_list = [element.text for element in elements]
        self.action.explicit_wait('toast_message_popup', ec='invisibility_of_element_located', waittime=60)
        print(toast_text_list)
        if expected_message in toast_text_list:
            return True
        return False

    def get_non_empty_files_count_in_directory(self, directory=os.path.join(os.getcwd(), "ameyo", "temp_downloads")):
        """Used to get count of non-empty files in given directory"""
        count = 0
        for path in os.listdir(directory):
            # check if current path is a file and file is not empty(zero bytes)
            if os.path.isfile(os.path.join(directory, path)) and os.path.getsize(os.path.join(directory, path)) > 0:
                count += 1
        return count
