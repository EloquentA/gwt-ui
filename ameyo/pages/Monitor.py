"""
Module: This is the monitor module which contains methods for functionality related to monitoring.
"""
import os
import sys
import time

from uuid import uuid4

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Monitor:
    """Monitoring functionality class"""

    def __init__(self, web_browser, common, agent_homepage):
        self.web_browser = web_browser
        self.action = Action(web_browser)
        self.common = common
        self.agent_homepage = agent_homepage

    def set_up_campaign(self, campaign_details):
        """Sets up campaign to monitor for in monitoring page."""
        current_campaign = self.action.get_text('current_selected_campaign_tab')
        campign = campaign_details.get(campaign_details.get('monitor_with'))
        if campign is None:
            assert False, f'Please provide campaign to monitor with as a key (like "voice_outbound") in campaign details: {campaign_details}'
        if campign == current_campaign:
            print("Requested campaign already selected: ", current_campaign)
            return campign
        self.action.explicit_wait('menu_icon')
        self.action.explicit_wait('monitor_tab', ec='element_to_be_clickable')
        self.action.click_element('monitor_tab')
        self.action.explicit_wait('menu_icon', ec='element_to_be_clickable')
        self.action.click_element('menu_icon')
        self.action.explicit_wait('search_campaign_input', 30)
        self.action.input_text('search_campaign_input', campign)
        self.action.explicit_wait('campaign_search_list', ec='element_to_be_clickable')
        self.action.select_from_ul_dropdown_using_text('campaign_search_list', campign)
        return campign

    def open_actions(self, executive_username, retries=0):
        """Opens  available actions pop for requested logged in executive."""
        agent_list = []
        try:
            # This sleep is need for the user status to refresh in monitoring tab
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
                return self.open_actions(executive_username, retries)
            assert False, f'Logged in user:{executive_username} not found in agent list: {agent_list}'

    def _wrap_up(self, executive_username, action_type='snoop'):
        """Wraps up after testing fucntionalities."""
        if action_type == 'barge':
            self.action.click_element('end_call_confer_btn')
        if action_type == 'conference':
            self.action.click_element('quit_confer_btn')
        if action_type != 'disconnect':
            self.action.click_element('disconnect_btn')
        self.action.click_element('monitor_tab')
        self.action.click_element('close_actions')
        # sleep to dispose call
        time.sleep(50)
        self.action.switch_to_window(0)
        self.agent_homepage.open_close_dialer()
        self.action.switch_to_window(1)

    def verify_snoop_action(self, campaign_details, executive_username):
        """Method to verify snoop functionality."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_actions(executive_username)
        self.action.explicit_wait('snoop_btn',ec='element_to_be_clickable')
        self.action.click_element('snoop_btn')
        assert self.action.verify_element_visible_and_enabled('snoop_btn'), "Snoop button not enabled even after snoop action."
        assert self.action.verify_element_visible_and_enabled('disconnect_btn'), "Disconnect/Hangup button should be enabled after snoop action."
        self._wrap_up(executive_username)
        return True

    def verify_barge_action(self, campaign_details, executive_username):
        """Method to verify barge functionality."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_actions(executive_username)
        self.action.explicit_wait('barge_btn',ec='element_to_be_clickable')
        self.action.click_element('barge_btn')
        assert self.action.verify_element_visible_and_enabled('disconnect_btn'), "Disconnect/Hangup button should be enabled after snoop action."
        self.action.explicit_wait('end_call_confer_btn', ec='element_to_be_clickable')
        expected_call_type = self.action.get_text('call_type')
        assert expected_call_type == 'Barge', f'Call type should be Barge. Found: {expected_call_type}'
        assert self.action.verify_element_visible_and_enabled('hold_resume_call_btn'), "Hold/Resume button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('mute_call_btn'), "Mute call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('confer_call_btn'), "Connfer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('transfer_call_btn'), "Transfer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('end_confer_btn'), "End confer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('end_call_confer_btn'), "End call confer call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('dtmf_btn'), "DTMF button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('disposition_btn'), "Disposition button call button should be visible and enabled."
        self._wrap_up(executive_username, 'barge')
        return True

    def verify_whisper_action(self, campaign_details, executive_username):
        """Method to verify whisper functionality."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_actions(executive_username)
        self.action.explicit_wait('whisper_btn',ec='element_to_be_clickable')
        self.action.click_element('whisper_btn')
        assert self.action.verify_element_visible_and_enabled('whisper_btn'), "Whisper button not enabled even after snoop action."
        assert self.action.verify_element_visible_and_enabled('disconnect_btn'), "Disconnect/Hangup button should be enabled after snoop action."
        self._wrap_up(executive_username, 'whisper')
        return True

    def verify_conference_action(self, campaign_details, executive_username):
        """Method to verify conference functionality."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_actions(executive_username)
        self.common.setup_workbench_for_campaign(campaign_details)
        self.action.explicit_wait('conference_btn',ec='element_to_be_clickable')
        self.action.click_element('conference_btn')
        self.action.explicit_wait('accept_conference_call', ec='element_to_be_clickable', waittime=60)
        self.action.click_element('accept_conference_call')
        assert self.action.verify_element_visible_and_enabled('conference_btn'), "Conference button should be enabled after snoop action."
        assert self.action.verify_element_visible_and_enabled('disconnect_btn'), "Disconnect/Hangup button should be enabled after snoop action."
        self.action.explicit_wait('quit_confer_btn', ec='element_to_be_clickable')
        expected_call_type = self.action.get_text('call_type')
        assert expected_call_type == 'Confer', f'Call type should be Confer. Found: {expected_call_type}'
        assert expected_call_type == 'Confer', f'Call type should be Barge. Found: {expected_call_type}'
        assert self.action.verify_element_visible_and_enabled('confer_call_btn'), "Connference call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('quit_confer_btn'), "Quite conference call button should be visible and enabled."
        assert self.action.verify_element_visible_and_enabled('mute_call_btn'), "Mute call button should be visible and enabled."
        self._wrap_up(executive_username, 'conference')
        return True

    def verify_disconnect_action(self, campaign_details, executive_username):
        """Method to verify disconnect functionality."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign)
        self.action.switch_to_window(1)
        self.open_actions(executive_username)
        self.action.explicit_wait('disconnect_btn',ec='element_to_be_clickable')
        self.action.click_element('disconnect_btn')
        self.action.switch_to_window(0)
        assert self.action.page_should_contain_text('Disposition'), "Disposition pop up should be open."
        self.action.switch_to_window(1)
        self._wrap_up(executive_username, 'disconnect')
        return True

    def verify_force_logout_action(self, campaign_details, executive_username, home_url):
        """Method to verify force logout functionality."""
        self.action.switch_to_window(0)
        self.common.change_status('Available', 'available_status')
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(campaign_details)
        self.open_actions(executive_username)
        self.action.explicit_wait('force_logout_btn',ec='element_to_be_clickable')
        self.action.click_element('force_logout_btn')
        self.action.explicit_wait('reason_for_logout_textarea')
        force_logout_reason = 'Test force logout reason from automation.'
        self.action.input_text('reason_for_logout_textarea', force_logout_reason)
        self.action.click_element('save_reason_for_logout_btn')
        self.action.switch_to_window(0)
        self.action.explicit_wait('logout_confirmation_btn', ec='element_to_be_clickable')
        assert self.action.page_should_contain_text(force_logout_reason), f"Pop up should contain logout reason:{force_logout_reason}"
        # Three pop ups are there so this will not work
        # TODO: Uncomment when modal issue is fixed
        # self.action.click_element('logout_confirmation_btn')
        # TODO: Remove below line when modal issue is fixed
        self.web_browser.go_to(home_url)
        expected_home_url = self.action.get_current_url()
        assert expected_home_url == home_url, f"Home url mismatched after force logout. Expected:{home_url}, Found:{expected_home_url}"
        return True

    def get_user_data(self, executive_username, retries=0):
        """Gets available data for requested logged in executive."""
        agent_list = []
        try:
            # This sleep is need for the user status to refresh in monitoring tab
            if retries == 0:
                time.sleep(10)
            self.action.explicit_wait('agent_list_table', 20)
            row_values = self.action.get_table_row_values('agent_list_table')
            col_names = self.action.get_table_header_columns_text_list('agent_list_table_thead')
            for row in row_values:
                if executive_username in row_values[row]:
                    return dict(zip(col_names, row_values[row]))
            else:
                assert False, f"Expected user not found in user table data: {row_values}"
        except Exception as err:
            retries += 1
            if retries <= 3:
                return self.get_user_data(executive_username, retries)
            assert False, f'Logged in user:{executive_username} not found in agent list: {agent_list}'

    def _verify_user_stats(self, expected_user_data, executive_username):
        """Verifies user stats from table."""
        user_data = self.get_user_data(executive_username)
        for col in expected_user_data.keys():
            assert expected_user_data[col] in user_data[col], \
                f"{col} missmatch in table data expected:{expected_user_data[col]},  found:{user_data[col]}"

    def _wrap_up_call(self):
        """Wraps up call."""
        self.action.switch_to_window(0)
        self.agent_homepage.save_and_dispose()
        self.agent_homepage.open_close_dialer()
        self.action.switch_to_window(1)

    def verify_live_monitoring(self, credentials, user_type, inbound_call_details):
        """Method to verify live monitoring functionality."""
        self.action.switch_to_window(1)
        campaign = self.set_up_campaign(credentials[user_type]['campaign_details'])
        self.action.switch_to_window(0)
        self.agent_homepage.manual_dial_only(999999999, campaign, select_campaign=True)
        self.action.switch_to_window(1)
        executive_username = credentials['executive']['username']
        expected_user_data = {
            'Agent Name': executive_username,
            'Agent ID': executive_username,
            'AutoCall Status': 'On',
            'Agent Status': 'Available',
            'Extension': credentials['executive']['extension'],
            'Agent Call Status': 'Connected',
            'Call Type': 'outbound manual dial',
            'Phone': '999999999',
            'Customer Call Status': 'Connected'
        }
        # Verify stats for connected outbound call
        self._verify_user_stats(expected_user_data, executive_username)
        self._wrap_up_call()
        expected_user_data.update({
            'Call Type': '',
            'Agent Call Status': 'inactive',
            'Customer Call Status': '',
            'Phone': ''
        })
        # Verify stats for not on call
        self._verify_user_stats(expected_user_data, executive_username)
        self.action.switch_to_window(0)
        self.agent_homepage.validate_inbound_call(
            inbound_call_details['inbound_url'],
            inbound_call_details['did_prefix'],
            inbound_call_details['calling_number'],
            credentials['executive']['campaign_details']['voice_inbound'],
            credentials['executive']['inbound_queue']
        )
        self.action.switch_to_window(1)
        expected_user_data.update({
            'Agent Call Status': 'Connected',
        })
        # Verify stats for inbound call
        self._verify_user_stats(expected_user_data, executive_username)
        self._wrap_up_call()
        return True