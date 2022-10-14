"""
Module: This is the login module which contains methods for functionality related to Homepage.
"""
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Homepage:
    """Homepage functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def manual_dial_only(self, calling_number):
        """Method to manual dial only call to calling number."""
        self.common.change_status('Available', 'available_status')
        self.action.explicit_wait('active_phone_icon', waittime=120)
        self.action.explicit_wait('phone_icon', ec='element_to_be_clickable')
        self.action.click_element('phone_icon')
        self.action.explicit_wait('search_for_customer_input', ec='element_to_be_clickable')
        self.action.input_text('search_for_customer_input', calling_number)
        self.action.click_element('call_btn')
        self.action.alert_action()
        self.action.explicit_wait('dial_only_btn')
        self.action.click_element('dial_only_btn')
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        self.action.explicit_wait('end_call_btn')
        self.action.is_presence_of_element_located('end_call_btn')
        return True

    def validate_logout_disabled_when_call_in_progress(self):
        """Validate logout functionality disabled when call is in progress"""
        self.action.is_presence_of_element_located('preferences_drop_down_btn')
        self.action.click_element('preferences_drop_down_btn')
        self.action.explicit_wait('disabled_logout_btn')
        return True

    def end_call_and_auto_dispose(self):
        """End the call and validate call auto disposed in 30 seconds"""
        self.action.explicit_wait('end_call_btn')
        self.action.click_element('end_call_btn')
        # Waiting for 30seconds- call auto dispose time
        time.sleep(30)
        self.action.is_presence_of_element_located('call_btn')
        return True
