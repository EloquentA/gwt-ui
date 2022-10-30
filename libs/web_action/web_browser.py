"""
Module: Web Browser
File name: Browser.py
Description: Browser module contains methods to control & retrieve information from web Browsers
"""
__author__ = "Developed by EA"

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
import tempfile
import logging
from pathlib import Path

sys.path.append(os.path.join((os.path.dirname(os.path.dirname(__file__))), "utils"))
from resource_parser import ResourceParser


class WebBrowser:
    """
        Base class for Web Automation uses python selenium Web Driver for this module
    """
    _DEFAULT_TIMEOUT = 15
    BROWSERS = ["chrome", "firefox", "ie", "edge"]

    def __init__(self, **kwargs):
        """
            Web Automation base class initiator which sets Default browser as Chrome
        """
        obj = ResourceParser(project=kwargs["project"])
        self.resources = obj.get_resources()

        # Part of JavaScript console.log modification
        selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
        selenium_logger.setLevel(logging.WARNING)
        self.console_log = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
        # Initialize remote browser
        if kwargs["browser_config"].get("is_remote_driver", False):
            self.server = kwargs["browser_config"].get('server', 'localhost')
            self.browserName = kwargs["browser_config"]["name"]
            self._browser = self.get_remote_driver_object(self.browserName, self.server, kwargs)
        else:
            # initializing local browser based on platform
            self.browsertype = kwargs["browser_config"]["name"]
            if sys.platform == "win32":
                self._FIREFOX_DEFAULT_PATH = os.path.join(os.environ["ProgramFiles"], "Mozilla Firefox\\firefox.exe")
                if not os.path.exists(self._FIREFOX_DEFAULT_PATH):
                    self._FIREFOX_DEFAULT_PATH = os.path.join(os.environ["ProgramW6432"],
                                                              "Mozilla Firefox\\firefox.exe")
                self.user_data_dir = "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data"
            elif sys.platform == "darwin":
                self._FIREFOX_DEFAULT_PATH = "//Applications//Firefox.app//Contents//MacOS//firefox-bin"
                self.user_data_dir = "//Users//administrator//Library//Application Support//Google//Chrome"
            elif sys.platform == "linux2":
                self._FIREFOX_DEFAULT_PATH = "//Applications//Firefox.app//Contents//MacOS//firefox-bin"
                self.user_data_dir = "//Users//administrator//Library//Application Support//Google//Chrome"

            if self.browsertype in self.BROWSERS:
                self._browser = self.create_webdriver(**kwargs)
            else:
                raise Exception("\nBrowser not supported. Supported browsers: %s\n" %
                                self.BROWSERS)
        self._browser.implicitly_wait(10)

    def create_webdriver(self, **kwargs):
        """
        Create the local webdriver object
        """
        import sys
        browser = kwargs["browser_config"]["name"]
        if kwargs is None:
            kwargs = {}
        if browser == 'firefox':
            from selenium.webdriver.firefox.service import Service
            from webdriver_manager.firefox import GeckoDriverManager
            # we need to explicitly specify to use Marionette
            # firefoxCap['marionette'] = True
            testdriver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

        elif browser in ['ie', 'ie64']:
            from selenium.webdriver.ie.service import Service
            from webdriver_manager.microsoft import IEDriverManager
            from selenium.webdriver.ie.options import Options
            opt = Options()
            opt.initial_browser_url = kwargs.get("initial_browser_url", "about:blank")
            testdriver = webdriver.Ie(service=Service(IEDriverManager().install()), options=opt)

        elif browser == 'edge_html':
            # for edge HTML version 18 and 19
            exe_path = r'C:\Windows\System32\MicrosoftWebDriver.exe'
            if not os.path.exists(exe_path):
                raise Exception(
                    "Microsoftwebdriver.exe not found in c:\\windows\\system32. Please, enable developer tools.")
            verbose = kwargs.get("verbose", False)
            logfile = kwargs.get("log_path", None)
            testdriver = webdriver.Edge(verbose=verbose)

        elif browser == 'edge':
            # for edge version 75 or so to 80+
            from selenium.webdriver.edge.service import Service
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            testdriver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

        elif browser == 'ghost':
            testdriver = webdriver.PhantomJS(self._BROWSER_INFO[browser]['webdriver_path'])

        elif browser == 'chrome' and sys.platform == "linux":
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument(r"--no-sandbox")
            testdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        else:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            options = Options()
            prefs = {}
            if "crx" in kwargs.keys():
                options.add_extension(kwargs["crx"])

            if "notifications" in kwargs.keys():
                if kwargs["notifications"] == "allow":
                    notif_index = 1
                else:
                    notif_index = 2
                prefs = {"profile.default_content_setting_values.notifications": notif_index}
            else:
                prefs = {"profile.default_content_setting_values.notifications": 2}

            if "download_directory" in kwargs.keys():
                prefs["download.default_directory"] = kwargs["download_directory"]

            # to disable file download protection i.e. Keep and Discard
            prefs["safebrowsing.enabled"] = "false"
            options.add_experimental_option("prefs", prefs)

            if "proxy_server" in kwargs.keys():
                options.add_argument('--proxy-server={}'.format(kwargs["proxy_server"]))

            # Ignore certificate errors
            options.add_argument('--ignore-certificate-errors')

            #Allow microphone access
            options.add_argument("--use-fake-ui-for-media-stream")

            # Part of JavaScript console.log modification
            service_args = []
            if self.console_log:
                service_args.append("--verbose")
                service_args.append("--log-path=" + self.console_log.name)

            testdriver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), service_args=service_args, options=options
            )

        testdriver.implicitly_wait(self._DEFAULT_TIMEOUT)
        return testdriver

    def get_remote_driver_object(self, browserName, server, kwargs):
        """
        This method returns remote driver object
        """
        desired_capabilities = {
            'browserName': browserName,
            'javascriptEnabled': True,
            'se:recordVideo': True,
        }

        if kwargs["browser_config"]["name"] == 'chrome':
            desired_capabilities.update({'goog:loggingPrefs': {"performance": "ALL"}})
        driver = webdriver.Remote(
            command_executor='http://' + server + ':' + kwargs["browser_config"]["port"] + '/wd/hub',
            desired_capabilities=desired_capabilities)

        _session = dict()
        _session[driver.session_id] = driver.capabilities

        sessionYml = Path(__file__).parent.parent.parent / "sessions.yml"
        if os.path.isfile(sessionYml):
            with open(sessionYml, 'r') as fp:
                _session.update(yaml.safe_load(fp.read()))
        with open(sessionYml, 'w') as fp:
            fp.write(yaml.safe_dump(_session))

        return driver

    def get_current_browser(self):
        return self._browser

    def get_current_url(self):
        return self._browser.current_url

    def get_locator(self, by):
        """
        generic method to return found elements
        """
        locators = {
            "id": By.ID, "name": By.NAME, "tag_name": By.TAG_NAME, "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT, "xpath": By.XPATH, "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }

        return locators.get(by, None)

    def go_to(self, url):
        """
            go_to() method goes to the specific URL after the browser instance launches
        """
        self._browser.get(url)

    def get_screenshot_as_file(self, screenshot_file):
        """
            get_screenshot_as_file() - Gets the screenshot of the current window.
            Returns False if there is any IOError, else returns True.
             Use full paths in your filename.
        """
        self._browser.get_screenshot_as_file(screenshot_file)

    def is_element_visible(self, locator):
        """It returns element if element is located within a max timeout of 10 seconds
            It will be called only in action.py
        """
        element_to_find = self.resources[locator]
        by = element_to_find["by"]
        try:
            element = WebDriverWait(self._browser, 10).until(
                EC.presence_of_element_located((self.get_locator(by), element_to_find["value"]))
            )
            return element
        except (Exception, ValueError) as error:
            print(f"Element can not be located on web page {locator}")
            return None

    def search_element(self, locator, replace_dict=None):
        """
        search_element() - locates the element in the web application
        return element object
        """
        element_to_find = self.resources[locator]
        # handling to update value and index during execution
        value = element_to_find["value"]
        if replace_dict:
            if 'value' in replace_dict:
                value = replace_dict['value']
            elif 'replace_value' in replace_dict:
                value = value.replace("replace_me", replace_dict['replace_value'])
            elif 'index' in replace_dict:
                element_to_find['index'] = replace_dict['index']
        print(f"Searching element - {element_to_find}")
        element = self.get_element(
            by=element_to_find["by"], value=value, index=element_to_find["index"]
        )
        return element

    def get_element(self, by=None, value=None, index=0):
        """
            Returns all the elements identified by the locator unless an index is passed
            index = -1 - Returns all the elements
            index = index - the element present at index defaults to 0
        """
        index = int(index)
        if by is None or value is None:
            raise Exception(f"Either by <{by}> or value <{value}> is None.")

        # Getting element identifier object
        locator = self.get_locator(by)
        if not locator:
            raise Exception(f"Given locator <{by}> is invalid.\nPossible locators are <id, name, tag_name, link_text, "
                            f"partial_link_text, xpath, css, class>")
        # Returning identified element
        web_elements = self._browser.find_elements(locator, value)
        if index == -1:
            return web_elements
        else:
            if index >= len(web_elements):
                raise Exception(f"Element index {index} is outside of number of elements found <{len(web_elements)}>.")
            else:
                if (not web_elements[index].is_displayed()) or (not web_elements[index].is_enabled()):
                    return None

                return web_elements[index]

    def quit(self):
        """
            Close the Browser
        """
        try:
            self._browser.quit()
        except (Exception, ValueError):
            import time
            time.sleep(2)
            try:
                self._browser.quit()
            except (Exception, ValueError):
                pass

    def close_browser(self):
        """
        Close the current browser window
        """
        self._browser.close()

    def waitfor_ajax_complete(self):
        """
        Executes a jQuery JavaScript snippet that checks for active Ajax Requests
        return boolean of active requests
        jim wendt
        """
        for x in range(100):
            if self._browser.execute_script("return window.jQuery != undefined && jQuery.active == 0"):
                return True
            time.sleep(.25)
            print("Waiting for AJAX to complete")
        return False

    def select_item_from_table(self, locator, Search_Item):
        self.varlist = self.get_element(locator)
        for item in self.varlist:
            name_list = item.text
            if Search_Item == name_list:
                time.sleep(1)
                item.click()
            break

    def get_shadow_dom(self, element):
        """
        This function will return the shadow root of a web element
        :param element: a web element e.g. return of methods like find_elements_by_id() or find_elements_by_css_selector()
        :return: the shadow root which can then be use to find other web elements inside it

        e.g.
        root1 = driver.find_element_by_css_selector('some css')
        shadow_root1 = get_shadow_dom(root1)
        el = shadow_root1.find_element_by_css_selector('some other css')
        el.click()
        """
        shadow_root = self._browser.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    def navigate_back(self):
        self._browser.back()

    def refresh_page(self):
        self._browser.refresh()

    def navigate_forward(self):
        self._browser.forward()

    def get_current_page_source(self):
        var = self._browser.page_source
        return var
