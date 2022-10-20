"""
Module: This is the monitor module which contains methods for functionality related to monitoring.
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


class Monitor:
    """Monitoring functionality class"""

    def __init__(self, web_browser, common, agent_homepage):
        self.action = Action(web_browser)
        self.common = common
        self.agent_homepage = agent_homepage

    def set_up_campaign(self, campaign_details):
        """Sets up campaign to monitor for in monitoring page."""
        campign = campaign_details.get(campaign_details.get('monitor_with'))
        if campign is None:
            assert False, f'Please provide campiagn to monitor with as a key (like "voice_outbound") in campaign details: {campaign_details}'
        self.action.click_element('supervisor_monitor_tab')
        self.action.click_element('supervisor_menu_icon')
        self.action.explicit_wait('supervisor_search_campaign_input', 30)
        self.action.input_text('supervisor_search_campaign_input', campign)
        self.action.explicit_wait('supervisor_campaign_search_list', ec='element_to_be_clickable')
        self.action.select_from_ul_dropdown_using_text('supervisor_campaign_search_list', campign)
        return campign

    def open_or_close_actions(self, executive_username, retries=0):
        """Opens or closes available actions pop for requested logged in executive."""
        # This sleep is need for the user status to refresh in monitoring tab
        agent_list = []
        try:
            time.sleep(5)
            self.action.explicit_wait('agent_list_table', 20)
            row  = 0
            total_rows = self.action.get_row_count('agent_list_table')
            while row < total_rows:
                table_username_cell = self.action.get_table_cell_data('agent_list_table', row=row, col=1, raw_cell=True)
                table_agent = table_username_cell.text
                agent_list.append(table_agent)
                if table_agent == executive_username:
                    table_username_cell.click()
                    return True
                row += 1
        except Exception as err:
            retries += 1
            if retries <= 3:
                return self.open_or_close_actions(executive_username, retries)
            assert False, f'Logged in user:{executive_username} not found in agent list: {agent_list}'

    def _wrap_up(self, executive_username, action_type='snoop'):
        """Wraps up after testing fucntionalities."""
        self.action.click_element('disconnect_btn')
        if action_type == 'barge':
            self.action.click_element('end_call_confer_btn')
        self.action.click_element('supervisor_monitor_tab')
        self.open_or_close_actions(executive_username)
        # sleep to dispose call
        time.sleep(50)
        self.action.switch_to_window(0)
        self.action.explicit_wait('phone_icon', ec='element_to_be_clickable')
        self.action.click_element('phone_icon')
        self.action.switch_to_window(1)

    def verify_snoop_action(self, campaign_details, executive_username):
        """Method to verify update of requested user."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_or_close_actions(executive_username)
        self.action.explicit_wait('snoop_btn',ec='element_to_be_clickable')
        self.action.click_element('snoop_btn')
        assert self.action.verify_element_visible_and_enabled('snoop_btn'), "Snoop button not enabled even after snoop action."
        assert self.action.verify_element_visible_and_enabled('disconnect_btn'), "Disconnect/Hangup button should be enabled after snoop action."
        self._wrap_up(executive_username)
        return True

    def verify_barge_action(self, campaign_details, executive_username):
        """Method to verify update of requested user."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_or_close_actions(executive_username)
        self.action.explicit_wait('barge_btn',ec='element_to_be_clickable')
        self.action.click_element('barge_btn')
        assert self.action.verify_element_visible_and_enabled('barge_btn'), "Snoop button not enabled even after snoop action."
        assert self.action.verify_element_visible_and_enabled('disconnect_btn'), "Disconnect/Hangup button should be enabled after snoop action."
        expected_call_type = self.action.get_text('call_type')
        assert expected_call_type == 'Barge', f'Call type should be Barge. Found: {expected_call_type}'
        self.action.explicit_wait('end_call_confer_btn', ec='element_to_be_clickable')
        assert self.action.verify_element_visible_and_enabled('hold_resume_call_btn'), "Hold/Resume button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('mute_call_btn'), "Mute call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('confer_call_btn'), "Connfer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('transfer_call_btn'), "Transfer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('end_confer_btn'), "End confer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('end_call_confer_btn'), "End call confer call button should be visible and enabled."
        self._wrap_up(executive_username, 'barge')
        return True
