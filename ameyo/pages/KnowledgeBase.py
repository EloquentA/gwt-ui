"""
Module: This is the knowledgebase module which contains methods for knowledgebase flows in AMEYO UI."""
import os
import sys
import time


sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class KnowledgeBase:
    """KnowledgeBase functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def validate_knowledge_base_page(self, user_type, campaign_details):
        """This function will validate knowledge base page"""
        if user_type in ['supervisor', 'group_manager']:
            self.common.setup_workbench_for_campaign(campaign_details)
        self.action.explicit_wait('knowledge_base_btn')
        self.action.click_element('knowledge_base_btn')
        try:
            self.action.switch_to_frame('kb_iframe')
            self.action.explicit_wait('kb_about_us_tab', ec='element_to_be_clickable')
            if self.action.is_presence_of_element_located('kb_cookies_ok_btn'):
                self.action.click_element('kb_cookies_ok_btn')
            self.action.execute_javascript("window.scrollTo(0, document.body.scrollHeight);")
            # Cannot scroll without sleep
            time.sleep(2)
            self.action.explicit_wait('copyright_am', ec='presence_of_element_located')
            self.action.click_element('copyright_am')
        finally:
            self.action.switch_to_default_frame()
        return True
