"""
This module contains methods to perform action on web elements
"""

__author__ = "Developed by EA"

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import os
import re
import time
import inspect
import datetime




class Action:
    """
    Methods to perform web operations are implemented in this class
    """

    def __init__(self, browser):
        self._browser = browser

    def click_element(self, locator, replace_dict=None, value=None, index=None):
        """Click element identified by `locator`.
        replace_dict: For dynamically changing the xpath
        value: If you have multiple elements identified by locator and you want to click on a
               particular element where some text is written, then pass value=text_on_element,
               it will match value with text written on the element and click on that.
        index : the index of the element to click. If you have multiple elements with same locator and an element at a particular
                index must be accessed, then this index parameter must be used. e.g. a web page having 5 save buttons with same locator
                (id, xpath etc.). In this case either 5 separate entries in map file should be made(using the last # e.g. #2,#3 etc) but this
                approach will make map file huge so, using this index param in this type of cases will be helpful.

        """
        # if a locator returns more than 1 element and no value to match is supplied
        if index is not None and not value:
            self.elements = self._element_finder(locator, replace_dict)
            if self.elements:
                self.elements[index].click()
                # returning as the element has already been clicked
                return
        # if a locator returns more than 1 element and some value to match is supplied
        if value:
            self.elements = self._element_finder(locator, replace_dict)
            elements = []  # to store elements which has value(passed from param)
            if self.elements:
                for i in self.elements:
                    match_text = i.text.strip()
                    if "\n" in match_text:
                        match_text = map(str.strip, match_text.split("\n"))
                    if value in match_text:
                        elements.append(i)
                # if a locator returns more than 1 element and some value to match is supplied along with some index
                if index is not None:
                    elements[index].click()
                else:
                    elements[0].click()
        else:
            self.element = self._element_finder(locator, replace_dict)
            if self.element:
                self.element.click()

    def is_presence_of_element_located(self, locator):
        """If element is found then returns True otherwise False"""
        element = self._browser.is_element_visible(locator)
        if element:
            return True
        return False

    def input_text(self, locator, Text):
        """Types the given `text` into text field identified by `locator`.

        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.clear()
            self.element.send_keys(Text)

    def submit_form(self, locator):
        """Submits a form identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.submit()

    def clear_input_text(self, locator):
        """
        clear the given text field identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.clear()

    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`.
        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            self.element.click()

    def unselect_checkbox(self, locator):
        """Un-selects checkbox identified by `locator`.

        Does nothing if checkbox is already un-selected. Key attributes for
        checkboxes are `id` and `name`.
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            self.element.click()

    def select_radio_button(self, locator):
        """Sets selection of radio button .

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            self.element.click()

    def execute_javascript(self, script_name):
        """
          execute java script
        """
        self._browser.get_current_browser().execute_script(script_name)

    def choose_file(self, locator, file_path):
        """Inputs the 'file_path' into file input field found by 'locator'.

        This keyword is most often used to input files into upload forms.
        The file specified with 'file_path' must be available on the same host
        where the Selenium is running.

        """
        if not os.path.isfile(file_path):
            print("WebUIOperation", "debug", "choose_file - File '%s' does not exist on the \
                                    local file system" % file_path)
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(file_path)

    def get_current_url(self):
        return self._browser.get_current_url()

    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).double_click(self.element).perform()

    def drag_and_drop(self, source, target):
        """Drags element identified with `source` which is a locator.

        Element can be moved on top of another element with `target`
        argument.

        `target` is a locator of the element where the dragged object is
        dropped.
        """
        self.source_ele = self._element_finder(source)
        self.target_ele = self._element_finder(target)

        if self.source_ele and self.target_ele:
            ActionChains(self._browser.get_current_browser()).drag_and_drop(self.source_ele, self.target_ele).perform()

    def drag_and_move(self, source, target):
        """Drags element identified with `source` which is a locator.
        Element can be moved on top of another element with `target`
        argument.
        `target` is a locator of the element where the dragged object is
        dropped.
        """
        self.source_ele = self._element_finder(source)
        self.target_ele = self._element_finder(target)

        if self.source_ele and self.target_ele:
            ActionChains(self._browser.get_current_browser()).click_and_hold(self.source_ele).move_to_element(
                self.target_ele).perform()

    def right_click(self, locator):
        """Right Click on element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).context_click(self.element).perform()

    def explicit_wait(self, locator, waittime=20, replace_dict=None,
                      ec='visibility_of_element_located', msg=None,
                      msg_to_verify=None, condition_category="until"):
        """
        explicit_wait() is used to wait until element is displayed & enabled
        locator: the web element to find as per resources file
        waittime: max time to wait
        replace_dict: to replace variables in the value in map file. Refer _map_converter function in browser.py for more info
        ec: expected condition to wait on
        msg: msg to be validated irrespective of the element e.g. title_is or title_contains
        msg_to_verify: msg to be validated on a web element e.g. text_to_be_present_in_element
        condition_category = category of conditions to verify with until being default. To make the condition checking to until_not pass this
        parameter as until_not while calling this function. Example below

        e.g.
        For a resource file entry as below
        "comp_name":{"by": "xpath", "value": "//*[@id='companyName']", "index": "0"}

        some example calls to this function could be
        r = self.action.explicit_wait("comp_name")
        r = self.action.explicit_wait("comp_name", ec="title_contains", msg="Account") # "comp_name" i.e. element is not required
        in this call but it is required as it is a mandatory argument. It is this way to make this function backward compatible
        r = self.action.explicit_wait("comp_name", ec="text_to_be_present_in_element", msg_to_verify="ABC Company")

        There are some custom expected conditions as well. They are implemented in the custom_expected_conditions.py file.
        Some of the custom wats are length_of_drop_down_is,drop_down_has_option etc.

        Example usage is given below:
        # to wait till the length of drop down grows more than 5
        mydrop_down = self.action.explicit_wait('Peopleselect_dropbox', ec="length_of_drop_down_is", msg_to_verify=5)
        # to wait till the given drop down has an option "ff ll"
        mydrop_down = self.action.explicit_wait('Peopleselect_dropbox', ec="drop_down_has_option", msg_to_verify="ff ll")
        self.action.explicit_wait('SwitchAcc_ok', ec="visibility_of_element_located",condition_category="until_not")
        """
        element_to_find = self._browser.resources[locator]

        if 'not' in condition_category:
            wait = WebDriverWait(self._browser.get_current_browser(), waittime).until_not
            error_msg = "The element <%s> can not be located after explicit wait." % locator
        else:
            wait = WebDriverWait(self._browser.get_current_browser(), waittime).until
            error_msg = "Could not locate element <%s> during explicit wait." % locator
        result = None
        try:
            condition = getattr(EC, ec)
        except AttributeError as e:
            # condition = getattr(CEC, ec)
            pass

        try:
            if msg:
                result = wait(condition(msg))
            elif msg is None and msg_to_verify is None:
                result = wait(condition((self._browser.get_locator(element_to_find["by"]), element_to_find["value"])))
            elif msg_to_verify:
                result = wait(condition((self._browser.get_locator(element_to_find["by"]), element_to_find["value"]), msg_to_verify))
        except Exception as e:
            raise Exception(error_msg + str(e))

        return result

    def focus(self, locator):
        """Sets focus to element identified by `locator`."""

        self.element = self._element_finder(locator)
        self._current_browser().execute_script("arguments[0].focus();", self.element)

    def wait_for_alert_and_act(self, cancel=False, waittime=20):
        """Waits for alert to appear and performs requested action.

        By default, this keyword chooses 'OK' option from the dialog. If
            'Cancel' needs to be chosen, set keyword ` Cancel = True'"""
        WebDriverWait(self._browser.get_current_browser(), waittime).until(EC.alert_is_present(),
                                        'Timed out waiting for ' +
                                        'confirmation popup to appear.')
        self.alert_action(cancel)

    def alert_action(self, Cancel=False):
        """Dismisses currently shown alert dialog and returns it's message.

        By default, this keyword chooses 'OK' option from the dialog. If
        'Cancel' needs to be chosen, set keyword ` Cancel = True'
        """
        self.text = self._alert(Cancel)
        return self.text

    def press_key(self, locator, key):
        """Simulates user pressing key on element identified by `locator`.

        `key` is a single character.

        Examples:
        press_key ("GoogleSearch", "BACKSPACE")
        """
        if len(key) < 1:
            print("WebUIOperation", "error", "press_key - Key value \
                                    not present  - %s" % (key))
            return None
        keydict = self._map_ascii_key_code_to_key(key)
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(keydict)

    def mouse_hover(self, locator):
        """Mouse hover on element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).move_to_element(self.element).perform()

    def switch_to_frame(self, locator):
        """
          switch to frame("myframe")
        """
        self.frame = self._element_finder(locator)
        self.browserdriver = self._browser.get_current_browser()
        self.browserdriver.switch_to.frame(self.frame)

    def switch_to_default_frame(self):
        """
        switches to main frame
        :return:
        """
        self.browserdriver = self._browser.get_current_browser()
        self.browserdriver.switch_to.default_content()

    def switch_to_parent_frame(self):
        """
        switches to parent frame for the context
        :return:
        """
        self.browserdriver = self._browser.get_current_browser()
        self.browserdriver.switch_to.parent_frame()

    def select_from_ul_dropdown_using_text(self, locator, itemtext):
        """ Selecting item from unordered dropdown list by using the li item text
        """
        selection_list = self.get_element(locator).find_elements(By.TAG_NAME, "li")
        for li_item in selection_list:
            if itemtext == li_item.text:
                li_item.click()
                break

    def select_from_dropdown_using_text(self, locator, itemtext):
        """ Selecting item from dropdownlist by using the option itemtext
        
        """
        selectionlist = self._element_finder(locator)
        for option in selectionlist.find_elements(By.TAG_NAME,'option'):
            if option.text.strip() == itemtext:
                option.click()
                break

    def select_from_dropdown_using_index(self, locator, itemindex):
        """ Selecting item from drop down list by using the option itemindex
        
        """
        selectionlist = self._element_finder(locator)
        sel = Select(selectionlist)
        sel.select_by_index(itemindex)

    def select_list_item_using_text(self, locator, itemtext):
        """
           select item from list by using item text
        """
        # below change is to take care of new dropdown implementation
        selectlist = self._element_finder(locator)
        for item in selectlist:
            if item.text == itemtext:
                item.click()
                break

    def select_list_item_using_index(self, locator, itemindex):
        """
         select item from list by using itemindex
        """
        selectlist = self._element_finder(locator)
        for item in selectlist:
            if item["index"] == itemindex:
                item["index"].click()
                break

    def close_window(self):
        """
          closes the current window
        """
        self.browserdriver = self._browser.get_current_browser()
        self.browserdriver.close()
        self.window_list = self.browserdriver.window_handles

    def switch_to_window(self, window):
        """
          switch to window('window')  or
          can be used to switch to a tab
          switch_to_window(1)
          switch_to_window(2)

          the index number is the index of tab based on the order of tab opening

        """
        self.browserdriver = self._browser.get_current_browser()
        self.window_list = self.browserdriver.window_handles
        self.browserdriver.switch_to.window(self.window_list[window])

    def scroll(self, locator, position=1000):
        """Scrolls from top to desired position at bottom
           locator is the id or class of scroll bar not exactly xpath
           position is the value of the place till where you want to scroll
           pass position=0 for scrolling from bottom to top
        """
        self.xpath = self._browser._map_converter(locator)["BY_VALUE"]
        self.type = self._browser._map_converter(locator)["ELEMENT_TYPE"]
        if self.type == "id":
            scriptName = "$(document).ready(function(){$('#" + self.xpath + "').scrollTop(" + str(position) + ");});"
            self._browser.get_current_browser().execute_script(scriptName)
        else:
            scriptName = "$(document).ready(function(){$('." + self.xpath + "').scrollTop(" + str(position) + ");});"
            self._browser.get_current_browser().execute_script(scriptName)

    def input_text_basic(self, locator, text):
        """sets the given 'text' into the field identified by 'locator'
           extra info: This method performs operation on HTML element called time
           Eg: if you want to set time then pass the time parameter in form of 'hhmm'
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(text)

    def window_handles_count(self):
        """
          Get window handles count 
        """
        self.browserdriver = self._browser.get_current_browser()
        self.window_list = self.browserdriver.window_handles
        return len(self.window_list)

    def check_checkbox(self, locator):
        """Checks if checkbox identified by `locator` is selected or unselected
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            return True
        else:
            return False

    def clear_input_text_new(self, locator):
        """
        clear the given text field identified by `locator`.
        clear_input_text() does not work if text is right aligned,this new api works.

        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(Keys.CONTROL + "a")
            self.element.send_keys(Keys.DELETE)

    def maximize_browser_window(self):
        """Maximizes the currently opened browser window
        """
        self._current_browser().maximize_window()

    def minimize_browser_window(self):
        """minimizes the currently opened browser window
        """
        self._current_browser().set_window_position(-2000, 0)

    def takeScreenshot(self, funcName, location=None):
        """
        Method to save screen shot to a given path with the function name
        :param funcName: Function name
        :param location: is an optional parameter.If present, the provided location will be used for saving the screen shot
        :return: None
        """
        # trying to figure out the report location
        if location is None:
            for frame in inspect.stack():
                if "page" in frame[1] and "Component" in frame[1]:
                    feature_file = frame[1]
                    location = feature_file.split("page")[0]
                    break
                elif "lib" in frame[1] and "Component" in frame[1]:
                    feature_file = frame[1]
                    location = feature_file.split("lib")[0]
                    break
            else:
                # falling back to framework location
                location = os.path.dirname(os.path.dirname(__file__))
        path = location + "\\reports\\report_" + str(datetime.datetime.now().date()) + os.sep
        try:
            if not os.path.exists(path):
                print("Report path not found.Creating...")
                os.makedirs(path)
            name = path + funcName + str(datetime.datetime.now().time()).replace(":", "_") + ".png"
            print(name)
            self._browser.get_screenshot_as_file(name)
        except Exception as e:
            print(e)

    def sg_get_rows(self, locator):
        """
        returns all the visible rows in a slick grid.

        """
        slick_grid = self._element_finder(locator)
        grid_data = []
        row_data = []
        if self.element:
            rows = slick_grid.find_elements(By.CLASS_NAME,"slick-row")
            for row in rows:
                cells = row.find_elements(By.CLASS_NAME,"slick-cell")
                for cell in cells:
                    row_data.append(cell.text)
                grid_data.append(row_data)
                row_data = []
            return grid_data

    def sg_select_row_containing_text(self, locator, text, all=False):
        """
        text : select a row by clicking on its check box if it has a given text in any of its cells
        all : if true, all rows containing the given text will be selected

        """
        slick_grid = self._element_finder(locator)
        selected = False
        if self.element:
            rows = slick_grid.find_elements(By.CLASS_NAME,"slick-row")
            for row in rows:
                cells = row.find_elements(By.CLASS_NAME,"slick-cell")
                for cell in cells:
                    if cell.text == text:
                        cells[0].click()
                        selected = True
                        break
                if selected and not all:
                    break
            if not selected:
                print("WebUIOperation", "error", "sg_select_row_containing_text operation \
                                                         unsuccessful- %s" % (locator))

    def sg_select_rows_by_index(self, locator, indexes):
        """
        indexes : list of row index to be selected

        """
        slick_grid = self._element_finder(locator)
        if self.element:
            rows = slick_grid.find_elements(By.CLASS_NAME,"slick-row")
            for index in indexes:
                rows[index].find_elements(By.CLASS_NAME,"slick-cell")[0].click()

    def sg_get_grid_columns_header(self, locator):
        """
        locator : locator for the slick grid

        """
        slick_grid = self._element_finder(locator)
        if self.element:
            headers = slick_grid.find_elements(By.CLASS_NAME,"slick-column-name")
            names = [x.get_attribute('title') for x in headers]
            if len(names):
                return names
            return False

    def element_should_contain_text(self, locator, expected):
        """Verifies element identified by `locator` contains text `expected`.

        It matches substring on the text of the element

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.actual = self._get_text(locator)
        if not expected in self.actual:
            return False
        return True

    def element_should_not_contain_text(self, locator, expected):
        """Verifies element identified by `locator` does not contains text `expected`.

        It matches substring on the text of the element
        """
        self.actual = self._get_text(locator)
        if expected in self.actual:
            return False
        return True

    def values_should_be_equal(self, actualValue, expectedValue):
        """Verifies that actualValue is equal to expectedValue
        """
        if actualValue != expectedValue:
            return False
        return True

    def frame_should_contain_text(self, locator, text):
        """Verifies frame identified by `locator` contains `text`.
        """
        if not self._frame_contains(locator, text):
            return False
        return True

    def page_should_contain_text(self, text):
        """Verifies that current page contains `text`.
        """
        if not self._page_contains(text):
            return False
        return True

    def page_should_contain_element(self, locator):
        """Verifies element identified by `locator` is found on the current page.
        """
        if not self._page_should_contain_element(locator):
            return False
        return True

    def page_should_not_contain_text(self, text):
        """Verifies the current page does not contain `text`.

        """
        if self._page_contains(text):
            return False
        return True

    def page_should_not_contain_element(self, locator):
        """Verifies element identified by `locator` is not found on the current page.

        """
        if self._page_should_contain_element(locator):
            return False
        return True

    def element_should_be_disabled(self, locator):
        """Verifies that element identified with `locator` is disabled.

        """
        if self._is_enabled(locator):
            return False
        return True

    def element_should_be_disabled_1(self, locator):
        """Verifies that element identified with `locator` is disabled by searching disabled in the class attribute of the element.

        """
        if not self._is_disabled(locator):
            return False
        return True

    def element_should_be_enabled(self, locator):
        """Verifies that element identified with `locator` is enabled.

        """
        if not self._is_enabled(locator):
            return False
        return True

    def element_should_be_displayed(self, locator):
        """Verifies that the element identified by `locator` is displayed.

        Herein, displayed means that the element is logically visible, not optically
        visible in the current browser viewport. For example, an element that carries
        display:none is not logically visible, so using this keyword on that element
        would fail.

        """
        self.visible = self._is_visible(locator)
        if not self.visible:
            return False
        return True

    def element_should_not_be_displayed(self, locator):
        """Verifies that the element identified by `locator` is NOT displayed.

        This is the opposite of `element_should_be_displayed`.

        """
        self.visible = self._browser.elements_finder(locator)
        if len(self.visible) > 0:
            return False
        return True

    def element_should_be_selected(self, locator):
        """Verifies element identified by `locator` is selected/checked.

        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            return False
        return True

    def element_should_not_be_selected(self, locator):
        """Verifies element identified by `locator` is not selected/checked.
        """

        self.element = self._element_finder(locator)
        if self.element.is_selected():
            return False
        return True

    def element_text_should_be_exact(self, locator, expected):
        """Verifies element identified by `locator` exactly contains text `expected`.

        In contrast to `element_should_contain_text`, this keyword does not try
        a substring match but an exact match on the element identified by `locator`.

        """
        self.element = self._element_finder(locator)
        actual = self.element.text
        if expected != actual:
            return False
        return True

    def current_frame_contains_text(self, text):
        """Verifies that current frame contains `text`.

        """
        if not self._is_text_present(text):
            return False
        return True

    def current_frame_should_not_contain_text(self, text):
        """Verifies that current frame contains `text`.
        """
        if self._is_text_present(text):
            return False
        return True

    def verify_element_color(self, locator, expectedColor):
        """
        Verifies element color
        """
        pass

    def verify_text_in_dropdown(self, textList, valueToVerify):
        """ Verifies the value identified by valueToVerify is present in list identified by textList
        """
        count = 0
        for text in textList:
            if text == valueToVerify:
                count = count + 1
                return True
        if count == 0:
            return False

    def values_should_not_be_equal(self, actualValue, expectedValue):
        """Verifies that actualValue is not equal to expectedValue
        """
        if actualValue == expectedValue:
            return False
        return True

    def page_should_not_contain_javascript_errors(self):
        """
        `Description;`  Verifies the current page does not contain JavaScript errors.

        `Param:`  None

        `Returns:`  status - True/False

        `Created by:` Jim Wendt

        """
        error_recap = []
        keep_phrases = [
            '"description": "EvalError',
            '"description": "InternalError',
            '"description": "RangeError',
            '"description": "ReferenceError',
            '"description": "SyntaxError',
            '"description": "TypeError',
            '"description": "URIError',
            '"description": "ReferenceError',
            '"description": "DOMException'
        ]
        status = False
        if self._browser.console_log:
            for line in self._browser.console_log:
                for phrase in keep_phrases:
                    if phrase in line:
                        line = line.replace("\"description\": ", "")
                        line = line.replace("\\n", "").strip()
                        line = re.sub("\s+", " ", line)
                        line = line[1:-2]
                        if not line in error_recap:
                            error_recap.append(line)
            if len(error_recap):
                for line in error_recap:
                    print("AssertElement", "error", line)
                print("AssertElement", "error", "Page Contains JavaScript Errors")
                self._browser.console_log.truncate()
                raise AssertionError()
            else:
                status = True
                return status
        else:
            raise AssertionError("Unable to Validate Javascript Errors")

    def get_table_row_elements(self, locator):
        """Returns row elements from table."""
        try:
            self.table = self._element_finder(locator)
            if self.table:
                self.rowlist = self.table.find_elements(By.TAG_NAME,'tr')
                return self.rowlist
        except Exception as err:
            raise AssertionError(f"Error in get_table_row_elements - Check table locator: {err}")

    def get_table_cell_data(self, locator, row, col):
        """Returns cell data of a table using row & col number.
        your xpath for table should be something like : //form[2]/table/tbody

        """
        try:
            self.table = self._element_finder(locator)
            if self.table:
                self.rowlist = self.table.find_elements(By.TAG_NAME,'tr')
                if (len(self.rowlist) < row):
                    raise AssertionError("Expected row no is not present in table")

                # get coloumn list
                self.expectedrow = self.rowlist[row]
                self.colList = self.expectedrow.find_elements(By.TAG_NAME,'td')

                # check col count
                if (len(self.colList) < col):
                    raise AssertionError("Expected row no is not present in table")

                print("Query", "info", "get_table_cell_data - expected cell " \
                                       "data -  %s " % (str(self.colList[col].text)))
                return self.colList[col].text
        except:
            raise AssertionError("Error in get_table_cell_data - Check table xpath" \
                                 "or row count or col count")

    def get_table_cell_data_using_primaryId_modified(self, locator, primaryCol, primaryId, elementCol,
                                                     looseSearch=False):
        """Returns cell data of a table using primary Id  & element col number.
        PrimaryID is the text that we are using to search the row 
        primaryCol is the coloumn where PrimaryId is located
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_cell_data_using_primaryId("TenantTable",1,"PaxshoreTxt1",6)

        """
        try:
            self.flag = 0
            self.table = self._element_finder(locator)
            if self.table:
                for row in self.table.find_elements(By.TAG_NAME,'tr'):
                    self.colList = row.find_elements(By.TAG_NAME,'td')
                    if (len(self.colList) > primaryCol):
                        if looseSearch == False:
                            if self.colList[primaryCol].text == primaryId:
                                self.flag = 1
                                break
                        else:
                            if primaryId in self.colList[primaryCol].text:
                                self.flag = 1
                                break
                if self.flag:
                    if (len(self.colList) >= elementCol):
                        print("Query", "info", "get_table_cell_data_using_primaryId -" \
                                               "expected cell data -  %s " % (str(self.colList[elementCol].text)))

                        return self.colList[elementCol].text
                    else:
                        print("Query", "error", "get_table_cell_data_using_primaryId" \
                                                "- Expected element col  %s is not found in the table" % (
                                  str(elementCol)))
                        raise AssertionError("Expected primary Id is not present in table")
                else:
                    print("Query", "error", "get_table_cell_data_using_primaryId" \
                                            "- Expected primaryID %s is not found in the table" % (primaryId))
                    raise AssertionError("Expected primary Id is not present in table")

        except Exception as inst:
            if str(inst) == 'The element is found but is not enabled/visible.':
                print("Query", "info", "get_table_cell_data_using_primaryId -" \
                                       "expected cell data")
                return False
            else:
                raise AssertionError("Error in get_table_cell_data_using_primaryId" \
                                     "- Check table xpath or primaryID or element col no")

    def get_table_cell_data_using_primaryId(self, locator, primaryCol, primaryId, elementCol, looseSearch=False):
        """Returns cell data of a table using primary Id  & element col number.
        PrimaryID is the text that we are using to search the row 
        primaryCol is the coloumn where PrimaryId is located
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_cell_data_using_primaryId("TenantTable",1,"PaxshoreTxt1",6)

        """
        try:
            self.flag = 0
            self.table = self._element_finder(locator)
            if self.table:
                for row in self.table.find_elements(By.TAG_NAME,'tr'):
                    self.colList = row.find_elements(By.TAG_NAME,'td')
                    if (len(self.colList) > primaryCol):
                        if looseSearch == False:
                            if self.colList[primaryCol].text == primaryId:
                                self.flag = 1
                                break
                        else:
                            if primaryId in self.colList[primaryCol].text:
                                self.flag = 1
                                break
                if self.flag:
                    if (len(self.colList) >= elementCol):
                        print("Query", "info", "get_table_cell_data_using_primaryId -" \
                                               "expected cell data -  %s " % (str(self.colList[elementCol].text)))

                        return self.colList[elementCol].text
                    else:
                        print("Query", "error", "get_table_cell_data_using_primaryId" \
                                                "- Expected element col  %s is not found in the table" % (
                                  str(elementCol)))
                        raise AssertionError("Expected primary Id is not present in table")
                else:
                    print("Query", "error", "get_table_cell_data_using_primaryId" \
                                            "- Expected primaryID %s is not found in the table" % (primaryId))
                    raise AssertionError("Expected primary Id is not present in table")

        except:
            raise AssertionError("Error in get_table_cell_data_using_primaryId" \
                                 "- Check table xpath or primaryID or element col no")

    def get_table_cell_obj_using_primaryId(self, locator, primaryCol, primaryId, elementCol):
        """Returns cell obj of a table using primary Id  & element col number.
        your xpath for table should be something like : //form[2]/table/tbody

        """
        try:
            self.flag = 0
            self.table = self._element_finder(locator)
            if self.table:
                for row in self.table.find_elements(By.TAG_NAME,'tr'):
                    self.colList = row.find_elements(By.TAG_NAME,'td')
                    if (len(self.colList) > primaryCol):
                        if self.colList[primaryCol].text == primaryId:
                            self.flag = 1
                            break
                if self.flag:
                    if (len(self.colList) >= elementCol):
                        print("Query", "info", "get_table_cell_obj_using_primaryId -" \
                                               "returning expected cell obj ")
                        return self.colList[elementCol]
                    else:
                        print("Query", "error", "get_table_cell_obj_using_primaryId" \
                                                "- Expected element col  %s is not found in the table" % (
                                  str(elementCol)))
                        raise AssertionError("Expected primary Id is not present in table")
                else:
                    print("Query", "error", "get_table_cell_obj_using_primaryId" \
                                            "- Expected primaryID %s is not found in the table" % (primaryId))
                    raise AssertionError("Expected primary Id is not present in table")

        except:
            raise AssertionError("Error in get_table_cell_obj_using_primaryId" \
                                 "- Check table xpath or primaryID or element col no")

    # number of rows in the given table.
    def get_row_count(self, locator):
        """
        return number of rows in the given table
        """
        self.table = self._element_finder(locator)
        if self.table:
            return (len(self.table.find_elements(By.TAG_NAME,'tr')))
        else:
            return False

    # number of columns in the given table. Hope your table has TH row in it.
    def get_col_count(self, locator):
        """
        return number of columns in the given table. Hope your table has TH row in it.
        """
        self.table = self._element_finder(locator)
        if self.table:
            self.tr = self.table.find_elements(By.TAG_NAME,'tr')
            return (len(self.tr[0].find_elements(By.TAG_NAME,'th')))
        else:
            return False

    def element_displayed(self, locator):
        """Verifies that element identified by 'locator' is not displayed."""
        length_of_elements = len(self._browser.search_element(locator, None))
        if length_of_elements > 0:
            return True
        else:
            return False

    def element_enabled(self, locator):
        """
        Verifies that element identified by `locator` is enabled or not.
        """
        self.elemlist = self._browser.elements_finder(locator)
        if (len(self.elemlist) == 1):
            if not self.elemlist[0].is_enabled():
                return False
            else:
                return True
        else:
            return True

    def text_present(self, text):
        """
        Verifies that text is present on the page or not
        """
        if self._page_contains(text):
            return text
        else:
            return False

    def get_text_list_from_dropdown(self, locator):
        """ Selecting item from dropdownlist by using the option itemindex
        
        """
        selectionlist = self._element_finder(locator)
        text_list = list()
        for option in selectionlist.find_elements(By.TAG_NAME,'option'):
            text_list.append(option.get_attribute("text"))
        return text_list

    def get_text_of_selected_dropdown_option(self, locator):
        """
        return text of selected option from drop down list
        """
        selected_option = self._get_selected_option_from_dropdown(locator)
        if selected_option is not None:
            return selected_option.get_attribute("text")
        else:
            return False

    def get_table_header_columns_text_list(self, locator):
        """Returns list of text in table header 
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_header_columns_text_list("TenantTable")

        """
        self.table = self._element_finder(locator)
        if self.table:
            row = self.table.find_elements(By.TAG_NAME,'tr')
            self.colList = row[0].find_elements(By.TAG_NAME,'th')
            textList = list()
            for header in self.colList:
                textList.append(header.text)
            print("Query", "info", "get_table_header_columns_text_list -" \
                                   "executed successfully,table header text list returned")
            return textList
        else:
            return False

    def get_table_column_value(self, locator, col):
        """Returns list of text in table header 
        your xpath for table should be something like : //form[2]/table/tbody
        
        e.g. get_table_header_columns_text_list("TenantTable")
        """
        self.table = self._element_finder(locator)
        if self.table:
            rowList = self.table.find_elements(By.TAG_NAME,'tr')
            textList = list()
            for row in rowList:
                self.colList = row.find_elements(By.TAG_NAME,'td')
                textList.append(self.colList[col].text)
            return textList

    def verify_element_visible_and_enabled(self, locator):
        """Checks that the element is visible and enabled
         identified by `locator`.
        """
        if self._is_visible(locator) and self._is_enabled(locator):
            return True

    def verify_element_visible_and_disabled(self, locator):
        """Checks that the element is visible but disabled 
         identified by `locator`.
        """
        if self._is_visible(locator) and not self._is_enabled(locator):
            return True
        return False

    def verify_checkbox(self, locator):
        """Checks the status of checkbox identified by `locator`
         whether it is selected or not.
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            return True
        else:
            return False

    def get_element_attribute(self, locator, attribute):
        """Return value of element attribute.
        """
        return self._get_attribute(locator, attribute)

    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element is None:
            return False
        return self.element.location['x']

    def get_value(self, locator):
        """Returns the value attribute of element identified by `locator`.
        """
        return self._get_attribute(locator, "value")

    def get_text(self, locator):
        """Returns the text value of element identified by `locator`.
        """
        return self._get_text(locator)

    def get_value_execute_javascript(self, script_name):
        """
          execute java script and get return value
        """
        return self._browser.get_current_browser().execute_script("return " + script_name)

    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by `locator`.

        The position is returned in pixels offset the top of the page,
        as an integer. Fails if a matching element is not found.

        See also `get_horizontal_position`.
        """
        element = self._element_finder(locator)
        if element is None:
            return False
        return element.location['y']

    def get_element(self, locator):
        """Returns element """
        return self._element_finder(locator)

    def get_color(self, locator):
        """
            returns color of the object
        """
        self.element = self._element_finder(locator)
        rgb = self.element.value_of_css_property("background-color")
        r, g, b = map(int, re.search(r'rgba*\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
        hex_color = '#%02x%02x%02x' % (r, g, b)

        if "#09cf94" in hex_color:
            return "green"
        elif "#ffd500" in hex_color:
            return "yellow"
        elif "#ff5550" in hex_color:
            return "red"
        elif "#d9d9d9" in hex_color:
            return "gray"
        elif "#F49300" in hex_color:
            return "orange"
        else:
            return hex_color

    '''
    def file_upload(self, file_path):
        autoit.win_exists("[TITLE:Open]")
        autoit.control_send("[TITLE:Open]", "Edit1", file_path)
        autoit.control_click("[TITLE:Open]", "Button1")
    '''

    def _element_finder(self, locator, replace_dict=None):
        """
        _element_finder() - Method to invoke element_finder from browser class
        """
        for i in range(5):
            try:
                element = self._browser.search_element(locator, replace_dict)
                if element:
                    return element
            except:
                time.sleep(2)
        else:
            raise Exception(f"Could not locate element on webpage {locator}")
            # return None

    def _map_ascii_key_code_to_key(self, key_code):
        map = {
            "NULL": Keys.NULL,
            "BACKSPACE": Keys.BACK_SPACE,
            "TAB": Keys.TAB,
            "RETURN": Keys.RETURN,
            "ENTER": Keys.ENTER,
            "CANCEL": Keys.CANCEL,
            "ESCAPE": Keys.ESCAPE,
            "SPACE": Keys.SPACE,
            "MULTIPLY": Keys.MULTIPLY,
            "ADD": Keys.ADD,
            "SUBTRACT": Keys.SUBTRACT,
            "DECIMAL": Keys.DECIMAL,
            "DIVIDE": Keys.DIVIDE,
            "SEMICOLON": Keys.SEMICOLON,
            "EQUALS": Keys.EQUALS,
            "SHIFT": Keys.SHIFT,
            "ARROW_UP": Keys.ARROW_UP,
            "ARROW_DOWN": Keys.ARROW_DOWN,
            "ARROW_LEFT": Keys.ARROW_LEFT,
            "ARROW_RIGHT": Keys.ARROW_RIGHT,
            "INSERT": Keys.INSERT,
            "DELETE": Keys.DELETE,
            "END": Keys.END,
            "HOME": Keys.HOME,
            "F12": Keys.F12,
            "ALT": Keys.ALT

        }
        key = map.get(key_code)
        if key is None:
            key = chr(key_code)
        return key

    def _alert(self, cancel=False):
        alert = None
        try:

            alert = self._browser.get_current_browser().switch_to.alert
            text = ' '.join(alert.text.splitlines())  # collapse new lines chars
            if cancel:
                alert.dismiss()
            else:
                alert.accept()
            return text
        except WebDriverException:
            return None

    def _current_browser(self):
        return self._browser.get_current_browser()

    def _get_list_item_using_text(self, locator, itemtext):
        selectlist = self._element_finder(locator)
        for item in selectlist:
            if item.text == itemtext:
                return item

    def _get_parent_obj(self, obj):
        return obj.find_element_by_xpath('..')

    def _frame_contains(self, locator, text):
        self._driver = self._current_browser()
        element = self._element_finder(locator)

        self._driver.switch_to.frame(element)
        found = self._is_text_present(text)
        self._driver.switch_to.default_content()
        return found

    def _get_text(self, locator):
        element = self._element_finder(locator)
        if element is not None:
            return element.text
        return None

    def _is_text_present(self, text):
        locator = "//*[contains(., '%s')]" % (text)
        return self._is_element_contains(locator)

    def _is_element_present(self, locator):
        return self._element_finder(locator)

    def _is_element_contains(self, locator):
        self._driver = self._browser.get_current_browser()
        return self._driver.find_elements(By.XPATH,locator)

    def _page_contains(self, text):
        self._driver = self._current_browser()
        self._driver.switch_to.default_content()

        if self._is_text_present(text):
            return True

        subframes = self._element_finder("xpath=//frame|//iframe")
        if subframes:
            for frame in subframes:
                self._driver.switch_to.frame(frame)
                found_text = self._is_text_present(text)
                self._driver.switch_to.default_content()
                if found_text:
                    return True

        return False

    def _page_should_contain_element(self, locator):
        return self._is_element_present(locator)

    def _get_value(self, locator, tag=None):
        element = self._element_finder(locator, True, False, tag=tag)
        return element.get_attribute('value') if element is not None else None

    def _is_enabled(self, locator):
        element = self._element_finder(locator)
        if not element.is_enabled():
            return False
        read_only = element.get_attribute('readonly')
        if read_only == 'readonly' or read_only == 'true':
            return False
        return True

    def _is_disabled(self, locator):
        element = self._element_finder(locator)
        if "disabled" in element.get_attribute('class').lower():
            return True
        return False

    def _is_visible(self, locator):
        element = self._element_finder(locator)
        if element is not None:
            return element.is_displayed()
        return None

    def _get_attribute(self, locator, attribute):
        self.element = self._element_finder(locator)
        if self.element:
            actualattrib = self.element.get_attribute(attribute)
            return actualattrib

    def _get_selected_option_from_dropdown(self, locator):
        dropDown = self._element_finder(locator)
        if dropDown is not None:
            optionList = dropDown.find_elements(By.TAG_NAME,'option')
            for option in optionList:
                if option.is_selected():
                    return option

    def refresh_page(self):
        self._browser.refresh_page()
