"""
Module: This is the agent chat module which contains methods for functionality related to chat.
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


class Chat:
    """Agent Chat functionality class"""

    def __init__(self, web_browser, common):
        self.web_browser = web_browser
        self.action = Action(web_browser)
        self.common = common

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
