"""
Module: This is the agent chat module which contains methods for functionality related to chat.
"""
import os
import sys
import time
import random

from selenium.webdriver.common.by import By
from uuid import uuid4

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Chat:
    """Agent Chat functionality class"""

    def __init__(self, web_browser, common, monitor):
        self.web_browser = web_browser
        self.action = Action(web_browser)
        self.common = common
        self.monitor = monitor

    def initiate_chat(self, customer_inputs):
        """To initiate chat from customer URL"""
        self.action.switch_to_window(0)
        self.common.change_status('Available', 'available_status')
        self.action.switch_to_window(1)
        try:
            self.action.switch_to_frame('chat_initiation_iframe')
            self.action.explicit_wait('chat_initiation_tab')
            if self.action.get_text('chat_initiation_tab') == "Let's Chat!":
                self.action.click_element('chat_initiation_tab')
                self.action.input_text('chat_initiation_name_input', customer_inputs['customer_name'])
                self.action.click_element('chat_initiation_submit_btn')
                self.action.input_text('chat_text_message', customer_inputs['customer_message'])
                self.action.click_element('chat_text_message_send')
        finally:
            self.action.switch_to_default_frame()
            self.action.switch_to_window(0)
        return True

    def verify_chat_routing(self, customer_inputs):
        """To verify chat routing from customer URL to agent"""
        self.action.explicit_wait('chat_received_on_agent')
        assert self.action.get_text('chat_received_on_agent') == customer_inputs['customer_message'], \
            'Chat Routing to Agent failed'
        assert self.action.get_text('customer_name_received_on_agent').split()[0] == customer_inputs['customer_name'], \
            'Customer Name Mismatch'
        return True

    def create_customer_from_routed_chat(self):
        """To create new customer from routed chat"""
        self.action.click_element('create_customer_via_chat')
        self.action.click_element('create_customer_chat_link')
        self.action.explicit_wait('create_cust_page_loader', ec='invisibility_of_element_located', waittime=60)
        self.action.input_text('create_customer_phone_input', random.randint(10**9, 10**10-1))
        self.action.click_element('create_customer_btn')
        assert self.common.validate_message_in_toast_popups(
            'Customer Added successfully'), "Toast Message not as expected - Couldn't Create Customer"
        return True

    def validate_real_time_chat_data(self, campaign_details):
        """Method to verify live monitoring for chat campaign on supervisor"""
        self.monitor.set_up_campaign(campaign_details)
        self.action.explicit_wait('live_monitoring_queue_dropdown', waittime=30)
        self.action.click_element('live_monitoring_queue_dropdown')
        self.action.select_from_ul_dropdown_using_text('ul_queue_selector', campaign_details['select_queue'])
        user_data = {
            'user_assigned': '18',
            'user_loggedin': '1'
        }
        chat_data = {
            'auto_chat_on': '1',
            'auto_chat_off': '0',
            'total_available_instances': '4',
            'total_occupied_instances': '1'
        }
        self.verify_data_on_dashboard(user_data, chat_data)
        self.sort_by_ordering_list()
        return True

    def verify_data_on_dashboard(self, user_data, chat_data):
        """Method to verify dashboard monitoring for chat on supervisor"""
        assert user_data['user_assigned'] == self.action.get_text('users_assigned'), 'Users Assigned value error'
        assert user_data['user_loggedin'] == self.action.get_text('users_loggedin'), 'Users Assigned value error'
        assert chat_data['auto_chat_on'] == self.action.get_text('auto_chat_on'), 'Auto Chat on value error'
        assert chat_data['auto_chat_off'] == self.action.get_text('auto_chat_off'), 'Auto Chat off value error'
        assert chat_data['total_available_instances'] == self.action.get_text('total_available_instances'), \
            'Available Instance value error'
        assert chat_data['total_occupied_instances'] == self.action.get_text('total_occupied_instances'), \
            'Occupied Instances value error'
        return True

    def sort_by_ordering_list(self):
        sorting_options_based_on_chat_type = {
            'active_chats': ['Order Chats by Elapsed Time (Descending)',
                             'Order Chats by User Name (Ascending)'],
            'active_chats_per_user': ['Order Users By User Name (Ascending)',
                                      'Order Users By No. Of Ongoing Chats (Ascending)',
                                      'Show Only Users With Ongoing Chats'],
            #TODO queued chats not visible ask ameyo
            # 'queued_chats': ['Order Chats by Requesting Time (Ascending)',
            #                  'Order Chats by Requesting Time (Descending)']
            'queued_chats': []
        }

        for i in sorting_options_based_on_chat_type:
            self.action.click_element(i)
            self.apply_sorting_and_verify_data(sorting_options_based_on_chat_type[i])
        return True

    def apply_sorting_and_verify_data(self, sorting_options):
        """Method to select table sorting for data on chat stats monitoring"""
        for i in sorting_options:
            self.action.click_element('sort_dropdown')
            self.action.select_from_ul_dropdown_using_text('ul_sort_selector', i)
            self.verify_chat_stats_in_table()
        return True

    def verify_chat_stats_in_table(self):
        """Method to verify table data for chat on supervisor"""
        row_values = self.action.get_table_row_values('agent_list_table')
        col_names = self.action.get_table_header_columns_text_list('agent_list_table_thead')
        for row in row_values:
            user_data = dict(zip(col_names, row_values[row]))
            assert user_data['User ID'] == 'ron'
        return True
