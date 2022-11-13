"""
Module: This is the auto call module which contains methods for functionality related to auto call.
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
        if ' active' in auto_call_phone_icon_div_class:
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

    def select_all_topline_filters(self):
        """Selects all top line filters like: break, connected, on acw, ready and customers on hold."""
        for selector in ['break_div', 'ready_div', 'connected_div', 'on_acw_div', 'customers_on_hold_div']:
            self.action.click_element(selector)
            if selector == 'break_div':
                # TODO(praveen): Break filter not working in UI, remove this once filter is fixed
                continue
            assert 'active' in self.action.get_element_attribute(selector, 'class'), \
                f"Requested filter: {selector}, was not selected."

    def verify_all_top_line_filters(self, selected):
        """Verifies all top line filters are selected or not."""
        for selector in ['break_div', 'ready_div', 'connected_div', 'on_acw_div', 'customers_on_hold_div']:
            if selector == 'break_div':
                # TODO(praveen): Break filter not attaching active class in UI, remove this once filter is fixed
                continue
            if selected:
                assert 'active' in self.action.get_element_attribute(selector, 'class'), \
                    f"Requested filter: {selector}, was not selected."
            else:
                assert 'active' not in self.action.get_element_attribute(selector, 'class'), \
                    f"Requested filter: {selector}, was selected."
        try:
            self.action.click_element('open_filter_btn')
            for selector in [
                'break_filter_span', 'ready_filter_span', 'connected_filter_span',
                'on_acw_filter_span', 'on_hold_filter_span'
            ]:
                checkbox = self.action.get_element(selector).find_element(By.TAG_NAME,'input').get_attribute('checked')
                assert checkbox == 'true' if selected else not checkbox, f"Checkbox selected state should be: {selected}."
        finally:
            self.action.click_element('open_filter_btn')

    def verify_auto_call_not_on_call_filter(self, campaign_details, auto_call):
        """Verifies auto call on/off, not on call filter."""
        self.setup_executives_with_auto_call(auto_call)
        campaign = self.monitor.set_up_campaign(campaign_details)
        # Wait for data to refresh
        time.sleep(10)
        assert len(self.action.get_table_row_elements('agent_list_table')) == 2, \
            "Only two users should be in the agent table."
        self.select_all_topline_filters()
        self.verify_all_top_line_filters(selected=True)
        self.action.click_element('auto_call_on_not_on_call_div')
        assert 'selected-div' in self.action.get_element_attribute('auto_call_on_not_on_call_div', 'class'),\
            "Not on call filter is not active after enabling not on call filter."
        self.verify_all_top_line_filters(selected=False)
        self.select_all_topline_filters()
        assert 'selected-div' not in self.action.get_element_attribute('auto_call_on_not_on_call_div', 'class'), \
            'Not on call is active after enabling break, connected etc.'
        # Select and de-select filter to re-instate the state
        self.action.click_element('auto_call_on_not_on_call_div')
        self.action.click_element('auto_call_on_not_on_call_div')
        return True

    def wait_for_user_inactivity(self, wakeup_times):
        """Check auto-call on stats values on supervisor monitor with yield"""
        for wakeup_time in wakeup_times:
            time.sleep(wakeup_time)
            yield wakeup_time

    def verify_auto_call_not_on_call_activity(self, campaign_details, auto_call):
        """Verifies auto call on and agent inactive"""
        self.monitor.set_up_campaign(campaign_details)
        self.setup_executives_with_auto_call(auto_call)
        # A dictionary for wake up times i.e 32 and 42 having expected count as values
        inactivity_time_expected_values = {
            32: {
                'not_on_call': '2',
                'less_than_20': '0',
                '20_to_60': '2',
                'more_than_60': '0'
            },

            42: {
                'not_on_call': '2',
                'less_than_20': '0',
                '20_to_60': '0',
                'more_than_60': '2',
            }
        }
        for wakeup_time in self.wait_for_user_inactivity(inactivity_time_expected_values.keys()):
            assert inactivity_time_expected_values[wakeup_time]['not_on_call'] == \
                   self.action.get_text('auto_call_on_and_agent_inactive').split(':')[-1].strip(), \
                'Auto call on and not on call count Error'
            assert inactivity_time_expected_values[wakeup_time]['less_than_20'] == \
                   self.action.get_text('inactive_twenty_secs'), 'Auto call on less than 20 secs value Error'
            assert inactivity_time_expected_values[wakeup_time]['20_to_60'] == \
                   self.action.get_text('inactive_twenty_sixty_secs'), 'Auto call on 20_to_60 secs value Error'
            assert inactivity_time_expected_values[wakeup_time]['more_than_60'] == \
                   self.action.get_text('inactive_more_than_sixty_secs'), 'Auto call on more than 60 secs value Error'
        return True
