"""
Module: This is the auto call module which contains methods for functionality related to auto call.
"""
import os
import sys
import time

from uuid import uuid4

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class AutoCall:
    """Auto call functionality class"""

    def __init__(self, web_browser, common, agent_homepage, monitor):
        self.web_browser = web_browser
        self.action = Action(web_browser)
        self.common = common
        self.agent_homepage = agent_homepage
        self.monitor = monitor

    def set_auto_call(self, auto_call):
        """Sets user's auto call status to requested status."""
        auto_call_phone_icon_div_class = self.action.get_element_attribute('auto_call_phone_icon_div', 'class')
        trigger = False
        if 'active' in auto_call_phone_icon_div_class:
            if auto_call:
                print('Auto call status is already set to ON')
            else:
                trigger = True
        else:
            if not auto_call:
                print('Auto call status is already set to OFF')
            else:
                trigger = True
        if trigger:
            self.action.click_element('auto_call_phone_icon')
            self.action.explicit_wait('auto_call_lever', ec='element_to_be_clickable')
            self.action.click_element('auto_call_lever')
            self.action.click_element('auto_call_phone_icon')
        auto_call_phone_icon_div_class = self.action.get_element_attribute('auto_call_phone_icon_div', 'class')
        current_auto_call_verified = 'active' in auto_call_phone_icon_div_class if auto_call \
            else 'inactive' in auto_call_phone_icon_div_class
        assert current_auto_call_verified,  f'Failed to set auto call to: {auto_call}'

    def get_auto_call_count(self, auto_call_selector):
        """Gets auto call count selector for on/off as per requested selector."""
        auto_call_text = self.action.get_text(auto_call_selector)
        return int(auto_call_text.split(':')[-1].strip())

    def setup_executives_with_auto_call(self, auto_call):
        """Sets up users to auto call on or off."""
        for i in range(2):
            self.action.switch_to_window(i)
            self.common.change_status('Available', 'available_status')
            self.set_auto_call(auto_call)
        self.action.switch_to_window(2)

    def _verify_auto_call_stats(self, auto_call, is_connected):
        """Verifies stats for auto call."""
        # Wait for data to auto refresh
        time.sleep(10)
        if auto_call:
            auto_call_selector = 'auto_call_on'
            auto_call_connected_selector = 'auto_call_on_connected'
            auto_call_not_on_call_selector = 'auto_call_on_not_on_call'
        else:
            auto_call_selector = 'auto_call_off'
            auto_call_connected_selector = 'auto_call_off_connected'
            auto_call_not_on_call_selector = 'auto_call_off_not_on_call'

        if is_connected:
            auto_call_expected = 2
            auto_call_connected_expected = 1
            auto_call_not_on_call_expected = 1
        else:
            auto_call_expected = 2
            auto_call_connected_expected = 0
            auto_call_not_on_call_expected = 2

        auto_call_count = self.get_auto_call_count(auto_call_selector)
        assert auto_call_count == auto_call_expected,\
            f"Auto call {'on' if auto_call else 'off'} count should be {auto_call_expected}, " \
            f"found: {auto_call_count} when call is connected."

        auto_call_connected = int(self.action.get_text(auto_call_connected_selector).strip())
        assert auto_call_connected == auto_call_connected_expected, \
            f"Auto call {'on' if auto_call else 'off'}, connected count should be " \
            f"{auto_call_connected_expected}, found: {auto_call_connected} when call is connected."

        auto_call_not_on_call = int(self.action.get_text(auto_call_not_on_call_selector).strip())
        assert auto_call_not_on_call == auto_call_not_on_call_expected, \
            f"Auto call {'on' if auto_call else 'off'}, not connected count should be " \
            f"{auto_call_not_on_call_expected}, found: {auto_call_not_on_call} when call is connected."

    def verify_auto_call_stats(self, campaign_details, auto_call):
        """Verifies auto call on/off stats."""
        self.setup_executives_with_auto_call(auto_call)
        campaign = self.monitor.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign, auto_call)
        self.action.switch_to_window(2)
        self._verify_auto_call_stats(auto_call, is_connected=True)
        self.action.switch_to_window(0)
        self.agent_homepage.end_call_and_auto_dispose()
        self.action.switch_to_window(2)
        self._verify_auto_call_stats(auto_call, is_connected=False)
        return True

    def verify_auto_call_not_on_call_filter(self, campaign_details, auto_call):
        """Verifies auto call on/off, not on call filter."""
        self.setup_executives_with_auto_call(auto_call)
        campaign = self.monitor.set_up_campaign(campaign_details)
        # TODO(praveen): WIP
        return True