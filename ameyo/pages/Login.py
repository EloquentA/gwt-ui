"""
Module: This is the login module which contains methods for functionality related to Login and Logout.
"""
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Login:
    """Login functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def login(self, **kwargs) -> bool:
        """Login to Ameyo system"""
        return True

    def logout(self, **kwargs) -> bool:
        """Logout from Ameyo system"""
        return True
