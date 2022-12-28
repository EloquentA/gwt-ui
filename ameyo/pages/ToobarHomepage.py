"""
Module: This is the login module which contains methods for functionality related to Homepage.
"""
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action

class ToolbarHomepage:
    """Toolbar Homepage functionality class"""
    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def change_toolbar_campaign(self, campaign_details):
        self.action.explicit_wait('more_btn_toolbar')
        self.action.click_element('more_btn_toolbar')
        self.action.explicit_wait('setting_button')
        self.action.click_element('setting_button')
        self.action.click_element('change_campaign_btn')
        self.action.explicit_wait('toolbar_campaign_change_checkbox')
        self.action.click_element('toolbar_campaign_change_checkbox')
        self.action.explicit_wait('campaign_change_search')
        self.action.click_element('campaign_change_search')
        self.action.input_text('change_toolbar_campaign_search', campaign_details['voice_inbound'])
        self.action.explicit_wait('toolbar_campaign_change_new_checkbox')
        self.action.click_element('toolbar_campaign_change_new_checkbox')
        self.action.click_element('toolbar_campaign_change_next')
        assert self.action.get_text('toolbar_selected_campaign_verification') == campaign_details['voice_inbound'], \
            'Campaign Change failed for Toolbar'
        return True

