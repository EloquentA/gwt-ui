"""
Module: This is the main module which contains methods for functionality related to Ameyo
        Any sub-functionality must be kept in other page files, ex: Actions related to login
        functionality must be kept in Login.py
"""
import datetime
import os
import sys

from robot.libraries.BuiltIn import BuiltIn

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action
from web_browser import WebBrowser
from Common import Common
from Login import Login
from Homepage import Homepage


class Ameyo:
    """Ameyo functionality class"""
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, **kwargs):
        self.web_browser = WebBrowser(**kwargs)
        self._run_as = kwargs.get('run_as')
        self.common = Common(self.web_browser)
        self._error_screenshot_path = BuiltIn().get_variables()['${OUTPUT DIR}']

        self.action = Action(self.web_browser)
        self.login = Login(self.web_browser, self.common)
        self.homepage = Homepage(self.web_browser, self.common)

    def __capture_error(self, method_name, error_msg):
        """Utility method to capture and report errors"""
        screenshot_file_name = self.get_file_name(method_name)
        self.web_browser.get_screenshot_as_file(screenshot_file_name)
        print(f"Error in '{method_name}' is: {error_msg}")
        print(f"Check error screenshot here: {screenshot_file_name}")
        return screenshot_file_name

    def open_home_page(self, kwargs):
        """Opens Ameyo home page and maximizes browser window"""
        try:
            self.web_browser.go_to(kwargs["url"])
            self.action.maximize_browser_window()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("open_home_page", error))

    def close_alert_if_present(self):
        """Closes alert if present"""
        try:
            self.common.close_alert_if_exists()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("close_alert_if_present", error))

    def ameyo_login(self, kwargs, run_as=None):
        """Method to login"""
        try:
            print(f'Logging in as {self._run_as}')
            return self._return_result(self.login.login(**kwargs.get(run_as or self._run_as)))
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("ameyo_login", error))

    def logout_from_campaign_selection_page(self):
        """Method to logout from campaign selection page."""
        try:
            self.login.logout_from_campaign_selection_page()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("logout_from_campaign_selection_page", error))

    def logout_from_ameyo_homepage(self):
        """Method to logout from Ameyo Home Page"""
        try:
            self.login.logout_from_ameyo_homepage()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("logout_from_ameyo_homepage", error))

    def login_failure(self, kwargs, username_type, password_type):
        """Method to test login failures."""
        try:
            self.login.login_failure(kwargs.get(self._run_as), username_type, password_type)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error(f"login_failure_{username_type}_{password_type}", error))

    @staticmethod
    def _return_result(status=True, error='', ss_path='', *args):
        """Single point to return result for every test case."""
        if ss_path:
            ss_path = f'{error}. Check screenshot at: <{ss_path}>'
        return status, ss_path, *args

    def close_browser_window(self):
        """Close all the browser windows"""
        try:
            self.web_browser.quit()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("close_browser_window", error))

    def get_file_name(self, method_name):
        """returns the screenshot file name"""
        # get the path where screenshots will be stored
        file_storage_path = os.path.normpath(
            os.path.join(
                self._error_screenshot_path or os.path.dirname(os.path.dirname(__file__)),
                'reports',
                f'reports_{str(datetime.datetime.now().date())}'
            )
        )
        # Create the path if it does not exist
        if not os.path.exists(file_storage_path):
            os.makedirs(file_storage_path)
        # get the screenshot file name
        file_name = method_name + f'{str(datetime.datetime.now().time()).replace(":", "_")}.png'
        # get the final screenshot file path
        return file_storage_path + os.sep + file_name

    def select_campaign(self, kwargs):
        """This function will select campaign"""
        try:
            self.login.select_campaign(kwargs)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("select_campaign", error))

    def manual_dial_only(self, calling_number):
        """Method to manual dial only"""
        try:
            self.homepage.manual_dial_only(calling_number)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("manual_dial_only", error))

    def validate_logout_disabled_when_call_in_progress(self):
        """Method to validate logout functionality disabled when call in progress"""
        try:
            self.homepage.validate_logout_disabled_when_call_in_progress()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("validate_logout_disabled_when_call_in_progress", error))

    def end_call_and_auto_dispose(self):
        """Method to end the call and validate its auto disposed in 30 seconds"""
        try:
            self.homepage.end_call_and_auto_dispose()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("end_call_and_auto_dispose", error))
