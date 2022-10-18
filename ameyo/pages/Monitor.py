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

    def __init__(self, web_browser, common, homepage):
        self.action = Action(web_browser)
        self.common = common
        self.homepage = homepage

    def verify_snoop_action(self, campaign_details):
        """Method to verify update of requested user."""
        return True