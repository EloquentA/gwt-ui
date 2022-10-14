"""
Module: This is the user module which contains methods for functionality related to creatio, updation or deletion of users.
"""
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class User:
    """User functionality class"""
    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def create_user(self, user_type):
        """Creates requested user."""
        return True