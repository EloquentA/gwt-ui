"""
Module: This is the common module which contains methods for common flows in AMEYO UI."""
import datetime
import os
import random
import sys
import string
import time
import requests
import csv

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action


class Common:
    """Common functionality class"""

    def __init__(self, web_browser):
        self.action = Action(web_browser)

    def close_alert_if_exists(self, cancel=False, waittime=20):
        """Method to close force login pop up."""
        try:
            self.action.wait_for_alert_and_act(cancel, waittime)
            return True
        except Exception as e:
            print("Error closing alert after logout: ", e)
            return True

    def change_status(self, desired_state, new_state_element):
        """Method to change user status to desired state"""
        if not self.action.get_element_attribute('status_dropdown_link', 'title') == desired_state:
            self.action.explicit_wait('status_dropdown_link')
            self.action.click_element('status_dropdown_link')
            self.action.explicit_wait(new_state_element)
            self.action.click_element(new_state_element)
            self.action.explicit_wait('selected_agent_status', ec='text_to_be_present_in_element', msg_to_verify=desired_state)
        return True

    @staticmethod
    def generate_random_password():
        """Generated random password."""
        # select 1 lowercase
        password = random.choice(string.ascii_lowercase)
        # select 1 uppercase
        password += random.choice(string.ascii_uppercase)
        # select 1 digit
        password += random.choice(string.digits)
        # select 1 special symbol
        password += random.choice(string.punctuation)
        # generate other characters
        password +=''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(5))
        print("Generated password is: ", password)
        return password

    def wait_for_toast_to_appear_and_disappear(self):
        """waits for toast to appear and disappear."""
        try:
            self.action.explicit_wait('toast_message_div', waittime=60)
            self.action.explicit_wait('toast_message_div', ec='invisibility_of_element_located', waittime=10)
        except Exception as err:
            print('Error while waiting for toast message to appear: ',err)

    def hit_get_api_with_no_authentication(self, url, no_of_retries):
        """Hits GET API and validates success response"""
        for attempt in range(no_of_retries):
            resp = requests.get(url)
            if resp.status_code == 200:
                break

    def validate_message_in_toast_popups(self, expected_message):
        """Gets the text for all the popups present and validates the expected message present or not"""
        time.sleep(1)
        elements = self.action.get_element('toast_message_popup')
        toast_text_list = [element.text for element in elements]
        self.action.explicit_wait('toast_message_popup', ec='invisibility_of_element_located', waittime=60)
        print(toast_text_list)
        if expected_message in toast_text_list:
            return True
        return False

    def setup_workbench_for_campaign(self, campaign_details):
        """Sets up workbench for conference."""
        self.action.explicit_wait('workbench_tab', ec='element_to_be_clickable')
        self.action.click_element('workbench_tab')
        monitor_with = campaign_details.get('monitor_with')
        dropdown_selector = {
            'interaction': 'dropdown_interaction',
            'chat': 'dropdown_chat',
            'video': 'dropdown_video'
        }
        selector = dropdown_selector.get(monitor_with, 'dropdown_voice')
        self.action.explicit_wait(selector, ec='element_to_be_clickable')
        self.action.click_element(selector)
        self.action.select_from_ul_dropdown_using_text('ul_campaign_selector', campaign_details.get(monitor_with))
        self.action.click_element("button_next")
        return True

    def get_non_empty_files_count_in_directory(self, directory=os.path.join(os.getcwd(), "ameyo", "temp_downloads")):
        """Used to get count of non-empty files in given directory"""
        count = 0
        for path in os.listdir(directory):
            # check if current path is a file and file is not empty(zero bytes)
            if os.path.isfile(os.path.join(directory, path)) and os.path.getsize(os.path.join(directory, path)) > 0:
                count += 1
        return count

    def get_total_records(self, total_records_selector,table_selector,retries=0):
        """Gets total records."""
        try:
            self.wait_for_data_to_load(table_selector)
            records_str = self.action.get_text(total_records_selector)
            total_records = int(records_str.split('of')[-1].strip())
            print('Total records present for selector: ', total_records_selector, ' : ', total_records)
            return total_records
        except Exception as err:
            retries += 1
            if retries <= 3:
                time.sleep(3)
                return self.get_total_records(total_records_selector, table_selector, retries)
            print(f"Error getting total records for {total_records_selector}: {err} after {retries} retries.")
            return 0

    def wait_for_data_to_load(self, table_selector):
        """Waits for data to be loaded in table.
            Maximum wait time is 10 seconds.
        """
        current_time = time.time()
        while self.action.get_row_count(table_selector) < 1 and time.time() - current_time <= 10:
            time.sleep(3)

    def wait_for_searched_record_to_load(self, total_records_selector,table_selector,expected_records=1):
        """Waits for searched record to be loaded in table.
            Maximum wait time is 10 seconds.
        """
        current_time = time.time()
        while self.get_total_records(
                total_records_selector,table_selector) != expected_records and time.time() - current_time <= 10:
            time.sleep(3)

    def search_record(self, search_str, input_selector,total_records_selector ,table_selector,expected_records=1):
        """Searches for requested record in table and waits for records to load."""
        self.action.input_text(input_selector, search_str)
        self.action.press_key(input_selector, 'ENTER')
        self.wait_for_searched_record_to_load(total_records_selector, table_selector,expected_records)
        return True

    def get_col_text_from_ameyo_table(
            self,
            search_query_str,
            page_limit_selector,
            total_records_selector,
            table_selector,
            table_search_input,
            col=1,
            click_on_row=False
    ):
        """Gets record from ameyo tables used commonly."""
        current_total_records = self.get_total_records(total_records_selector, table_selector)
        if current_total_records > int(self.action.get_value(page_limit_selector)):
            self.search_record(search_query_str, table_search_input, total_records_selector, table_selector)
            if click_on_row:
                first_col = self.action.get_table_cell_data(table_selector, row=0, col=0, raw_cell=True)
                first_col.click()
            search_query_str = self.action.get_table_cell_data(table_selector, row=0, col=col)
        else:
            table_data = []
            for i in range(current_total_records):
                user = self.action.get_table_cell_data(table_selector, row=i, col=col)
                table_data.append(user)
                if search_query_str.lower() in user.lower():
                    if click_on_row:
                        first_col = self.action.get_table_cell_data(table_selector, row=i, col=0, raw_cell=True)
                        first_col.click()
                    search_query_str =  user
                    break
            else:
                assert False, f"No such search record found in table: {search_query_str}. in table data: {table_data}"
        return search_query_str, current_total_records

    def rename_file(self, directory=os.path.join(os.getcwd(), "ameyo", "temp_downloads"), extension=".csv"):
        """Used to rename files from given directory"""
        for path in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, path)) \
                    and os.path.getsize(os.path.join(directory, path)) > 0 and path.endswith(extension):
                new_filename = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
                new_filename += extension
                os.rename(os.path.join(directory, path), os.path.join(directory, new_filename))
            else:
                pass
        return new_filename

    def get_texts_from_csv_file(self, filename, directory=os.path.join(os.getcwd(), "ameyo", "temp_downloads")):
        """Get contents of CSV file as a list of dictionary"""
        filepath = directory+"\\\\"+filename
        with open(filepath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            row_count = 0
            file_content_list = []
            for row in csv_reader:
                row_count += 1
                file_content_list.append(row)
            print(row_count)
        return file_content_list

    @staticmethod
    def sleep(sleep_for, step=30):
        """Sleeps with indicator."""
        for i in range(sleep_for, 0, -step):
            print(f"Sleeping for...{i}", end="\r", flush=True)
            time.sleep(step)
