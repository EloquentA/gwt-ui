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
from User import User
from Monitor import Monitor


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
        self.user = User(self.web_browser, self.common)
        self.monitor = Monitor(self.web_browser, self.common, self.homepage)

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

    def open_home_page_in_separate_tab(self, url):
        """Opens home page in separate tab."""
        try:
            self.action.execute_javascript(f'''window.open("{url}","_blank");''')
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("open_home_page_in_separate_tab", error))

    def switch_to_tab(self, req_tab=-1):
        """Switches to requested tab. By default switches to last tab."""
        try:
            self.action.switch_to_window(int(req_tab))
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("switch_to_tab", error))

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

    def ameyo_login_new_password(self, user, pwd):
        """Method to login"""
        try:
            return self._return_result(self.login.login_new_password(user, pwd))
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("ameyo_login_new_password", error))

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

    def select_campaign(self, kwargs, run_as, voice_campaign_type="voice_outbound"):
        """This function will select campaign"""
        try:
            kwargs = kwargs.get(run_as).get('campaign_details')
            if kwargs is not None:
                self.login.select_campaign(kwargs, voice_campaign_type)
            else:
                print(f'Select campaign is not applicable for user type: {run_as}')
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("select_campaign", error))

    def manual_dial_only(self, calling_number, campaign_name):
        """Method to manual dial only"""
        try:
            self.homepage.manual_dial_only(calling_number, campaign_name)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("manual_dial_only", error))

    def create_and_dial_call(self, calling_number, customer_name, campaign_name):
        """Method to create contact in ameyo and dial call"""
        try:
            self.homepage.create_and_dial_call(calling_number, customer_name, campaign_name)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("create_and_dial_call", error))

    def manual_preview_dial(self, saved_calling_number, saved_customer_name, campaign_name):
        """Method to preview saved contact in ameyo and dial call"""
        try:
            self.homepage.manual_preview_dial(saved_calling_number, saved_customer_name, campaign_name)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("manual_preview_dial", error))

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

    def end_call_and_save_and_dispose(self):
        """Method to end the call and save and dispose"""
        try:
            self.homepage.save_and_dispose()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("end_call_and_save_and_dispose", error))

    def verify_create_user(self,user_type):
        """Method to verify creation of requested user."""
        try:
            is_passed, user_id_text = self.user.verify_create_user(user_type)
            return self._return_result(is_passed, '', '', user_id_text)
        except Exception as error:
            return self._return_result(False, error, self.__capture_error(f"verify_create_user_{user_type}", error))

    def dispose_and_dial(self, dispose_dial_config, dispose_type, dial_position):
        """This function will cover dispose and dial"""
        try:
            self.homepage.dispose_and_dial(dispose_dial_config, dispose_type, dial_position)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error(f"dispose_and_dial", error))

    def verify_delete_user(self,user_type, admin_password, userid_text):
        """Method to verify deletion of requested user."""
        try:
            return self._return_result(self.user.verify_delete_user(user_type, admin_password, userid_text))
        except Exception as error:
            return self._return_result(False, error, self.__capture_error(f"verify_delete_user_{user_type}", error))

    def set_status(self):
        """This function will change agent status"""
        try:
            self.homepage.set_status()
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("set_status", error))

    def change_campaign(self, kwargs):
        """This function will change campaign"""
        try:
            self.homepage.change_campaign(kwargs)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("change_campaign", error))

    def change_password(self, oldpass, newpass):
        """Method to change the password of logged in user"""
        try:
            self.homepage.change_password(oldpass, newpass)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("change_password", error))

    def verify_update_user(self,user_type, admin_password, userid_text):
        """Method to verify update of requested user."""
        try:
            return self._return_result(self.user.verify_update_user(user_type, admin_password, userid_text))
        except Exception as error:
            return self._return_result(False, error, self.__capture_error(f"verify_update_user_{user_type}", error))

    def validate_inbound_call(self, url, did_prefix, calling_number_prefix, campaign_name, queue_name):
        """Method to preview saved contact in ameyo and dial call"""
        try:
            self.homepage.validate_inbound_call(url, did_prefix, calling_number_prefix, campaign_name, queue_name)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("validate_inbound_call", error))

    def save_and_validate_customer_info_during_inbound_call(self, url, customer_name):
        """Method to save customer info during inbound call and validate stored info"""
        try:
            self.homepage.save_and_validate_customer_info_during_inbound_call(url, customer_name)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("save_and_validate_customer_info_during_inbound_call", error))

    def select_disposition_save_and_dispose(self, disposition_type, sub_disposition_type):
        """Method to select the dispositions and sub disposition from dropdown and click on Save and Dispose"""
        try:
            self.homepage.select_disposition_save_and_dispose(disposition_type, sub_disposition_type)
            return self._return_result()
        except Exception as error:
            return self._return_result(False, error, self.__capture_error("select_disposition_save_and_dispose", error))

    def verify_snoop_action(self, campaign_details):
        """Method to verify update of requested user."""
        try:
            return self._return_result(self.monitor.verify_snoop_action(campaign_details))
        except Exception as error:
            return self._return_result(False, error, self.__capture_error(f"verify_snoop{user_type}", error))
