"""
Module: This is the common module which contains methods for common flows in EXOTEL UI."""
import datetime
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Common:
    """Common functionality class"""

    def __init__(self, web_browser):
        self.action = Action(web_browser)