"""
Module: This is the Report module which contains methods for functionality related to ART - Reports.
"""
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
)
from action import Action
from Common import Common

class Reports:
    """Report functionality class"""

    def __init__(self, web_browser):
        self.action = Action(web_browser)
        self.common = Common(web_browser)

    def navigate_to_reports(self):
        """This will navigate to Reports Tab and switches the frame"""
        current_url = self.action.get_current_url()
        if 'Reports' not in current_url:
            self.action.is_presence_of_element_located('reports_tab')
            self.action.click_element('reports_tab')
        self.action.switch_to_frame('reports_frame')
        return True

    def handle_no_reports_found_alert(self):
        """Handles alert when no reports are assigned"""
        try:
            self.action.explicit_wait('ok_btn_report_tab_alert')
            self.action.click_element('ok_btn_report_tab_alert')
            return True
        except Exception as e:
            print("Error closing No Report Found Alert: ", e)
            return True

    def validate_reports_tab(self):
        """Validate reports tab for admin and supervisor UI"""
        self.navigate_to_reports()
        self.handle_no_reports_found_alert()
        self.action.click_element('home_tab')
        self.action.click_element('report_list_tab')
        self.action.switch_to_default_frame()
        return True

    def assign_all_default_reports_to_user(self, replace_dict):
        """Assigns all default reports to given user via Management-> User Privilege"""
        try:
            self.navigate_to_reports()
            self.handle_no_reports_found_alert()
            self.action.click_element('management_tab')
            self.action.click_element('user_privilege_tab')
            self.action.click_element('user_name', replace_dict=replace_dict)
            self.action.click_element('privileges_type_select')
            self.action.select_from_dropdown_using_text('privileges_type_select', 'Available')
            self.action.explicit_wait('select_all_btn')
            self.action.click_element('select_all_btn')
            self.action.click_element('save_btn')
            self.action.explicit_wait('report_assign_modal')
            self.action.click_element('report_assign_modal')
            self.action.click_element('ok_btn_report_tab_alert')
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_reports_assigned_to_user(self, report_name=None):
        """Validates reports are assigned to the given user"""
        try:
            self.navigate_to_reports()
            self.action.click_element('home_tab')
            self.action.is_presence_of_element_located('report_list_table')
            print(report_name)
            if report_name is not None:
                self.action.input_text('reports_search_box', report_name)
                self.action.click_element('search_button')
                reports_name_elements = self.action.get_element('report_name_column')
                reports_name_list = [element.text for element in reports_name_elements]
                print(reports_name_list)
                assert report_name in reports_name_list, "Expected Report not found in assigned reports list"
        finally:
            self.action.switch_to_default_frame()
        return True

    def run_report_and_validate_download_in_required_formats(self, report_name, current_time_duration='Year', report_formats_list=['CSV','XLS','PDF','HTML']):
        """Search and Run specific report for given time window in all formats"""
        try:
            self.navigate_to_reports()
            self.action.click_element('home_tab')
            self.action.click_element('report_list_tab')
            self.action.is_presence_of_element_located('report_list_table')
            self.action.input_text('reports_search_box', report_name)
            self.action.click_element('search_button')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=0, raw_cell=True).text == report_name,"Incorrect report name"
            self.action.get_table_cell_data('report_queue_table', row=0, col=2, raw_cell=True).click()
            self.action.explicit_wait('for_current_radio')
            self.action.click_element('for_current_radio')
            self.action.click_element('nothing_selected_btn')
            self.action.click_element('time_duration_selection', replace_dict={'replace_value': current_time_duration})
            self.action.explicit_wait('select_all_campaigns')
            self.action.click_element('select_all_campaigns')
            if self.action.is_presence_of_element_located('select_all_queues'):
                self.action.click_element('select_all_queues')
            print(report_formats_list)
            for report_format in report_formats_list:
                self.action.click_element('report_format_checkbox', replace_dict={'replace_value': report_format})
            self.action.explicit_wait('run_report_btn', ec='element_to_be_clickable')
            self.action.click_element('run_report_btn')
            self.action.switch_to_default_frame()
            self.validate_report_in_queue_and_download(report_name, report_formats_list)
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_report_in_queue_and_download(self, report_name, report_formats_list=['CSV','XLS','PDF','HTML']):
        """Validate successful report run from queue and download it in all desired formats"""
        try:
            self.navigate_to_reports()
            self.action.click_element('queue_tab')
            self.action.click_element('report_queue_tab')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=0, raw_cell=True).text == report_name, "Incorrect report name"
            self.action.explicit_wait('first_report_queue_status', waittime=240, ec='text_to_be_present_in_element', msg_to_verify='SUCCESS')
            print(report_formats_list)
            file_count = self.common.get_non_empty_files_count_in_directory()
            print(file_count)
            if 'CSV' in report_formats_list:
                print("Downloading CSV")
                #Navigating to Template Queue tab just to reload the DOM as WA for table elements disappearing from DOM issue
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=9, raw_cell=True).click()
                time.sleep(1)
                file_count = file_count + 1
                assert self.common.get_non_empty_files_count_in_directory() == file_count, "Files count mismatch, not downloaded"
            if 'XLS' in report_formats_list:
                print("Downloading XLS")
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=10, raw_cell=True).click()
                time.sleep(1)
                file_count = file_count + 1
                assert self.common.get_non_empty_files_count_in_directory() == file_count, "Files count mismatch, not downloaded"
            if 'PDF' in report_formats_list:
                print("Downloading PDF")
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=11, raw_cell=True).click()
                time.sleep(1)
                file_count = file_count + 1
                assert self.common.get_non_empty_files_count_in_directory() == file_count, "Files count mismatch, not downloaded"
            if 'HTML' in report_formats_list:
                print("Opening HTML")
                self.action.click_element('template_queue_tab')
                self.action.is_presence_of_element_located('template_name_header')
                self.action.click_element('report_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=12, raw_cell=True).click()
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_rerun_report_from_queue(self, report_name, report_formats_list=['CSV', 'XLS', 'PDF', 'HTML']):
        """Validate the re-run of reports from the Queue>>Report Queue"""
        try:
            self.navigate_to_reports()
            self.action.click_element('queue_tab')
            self.action.click_element('report_queue_tab')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=0, raw_cell=True).text == report_name, "Incorrect report name"
            self.action.get_table_cell_data('report_queue_table', row=0, col=8, raw_cell=True).click()
            print(report_formats_list)
            for report_format in report_formats_list:
                self.action.click_element('report_format_checkbox', replace_dict={'replace_value': report_format})
            self.action.explicit_wait('run_report_btn', ec='element_to_be_clickable')
            self.action.click_element('run_report_btn')
            self.action.switch_to_default_frame()
            self.validate_report_in_queue_and_download(report_name, report_formats_list)
        finally:
            self.action.switch_to_default_frame()
        return True

    def create_template_and_run_report_from_template(self, report_name, template_name, current_time_duration='Year', report_formats_list=['CSV','XLS','PDF','HTML']):
        """Save template of the report and run template and download"""
        try:
            self.navigate_to_reports()
            self.action.click_element('home_tab')
            self.action.click_element('report_list_tab')
            self.action.is_presence_of_element_located('report_list_table')
            self.action.input_text('reports_search_box', report_name)
            self.action.click_element('search_button')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=0, raw_cell=True).text == report_name, "Incorrect report name"
            self.action.get_table_cell_data('report_queue_table', row=0, col=2, raw_cell=True).click()
            self.action.explicit_wait('for_current_radio')
            self.action.click_element('for_current_radio')
            self.action.click_element('nothing_selected_btn')
            self.action.click_element('time_duration_selection', replace_dict={'replace_value': current_time_duration})
            self.action.explicit_wait('select_all_campaigns')
            self.action.click_element('select_all_campaigns')
            if self.action.is_presence_of_element_located('select_all_queues'):
                self.action.click_element('select_all_queues')
            print(report_formats_list)
            for report_format in report_formats_list:
                self.action.click_element('report_format_checkbox', replace_dict={'replace_value': report_format})
            self.action.explicit_wait('save_template_btn', ec='element_to_be_clickable')
            self.action.click_element('save_template_btn')
            self.action.explicit_wait('save_template_as_modal')
            self.action.input_text('template_name_input', template_name)
            self.action.explicit_wait('ok_btn_report_tab_alert')
            self.action.click_element('ok_btn_report_tab_alert')
            self.action.switch_to_default_frame()
            self.validate_template_in_queue_and_download(template_name, report_name, report_formats_list)
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_template_in_queue_and_download(self, template_name, report_name, report_formats_list=['CSV', 'XLS', 'PDF', 'HTML']):
        """Validate successful template run from queue and download it in all desired formats"""
        try:
            self.navigate_to_reports()
            self.action.click_element('queue_tab')
            self.action.click_element('template_queue_tab')
            self.action.explicit_wait('template_name_header')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=0,
                                                   raw_cell=True).text == template_name, "Incorrect template name"
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=2,
                                                   raw_cell=True).text == report_name, "Incorrect report name"
            self.action.explicit_wait('first_template_queue_status', waittime=240, ec='text_to_be_present_in_element',
                                      msg_to_verify='SUCCESS')
            print(report_formats_list)
            file_count = self.common.get_non_empty_files_count_in_directory()
            if 'CSV' in report_formats_list:
                print("Downloading CSV")
                # Navigating to Template Queue tab just to reload the DOM as WA for table elements disappearing from DOM issue
                self.action.explicit_wait('report_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('template_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('template_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=10, raw_cell=True).click()
                time.sleep(1)
                file_count = file_count + 1
                assert self.common.get_non_empty_files_count_in_directory() == file_count, "Files count mismatch, not downloaded"
            if 'XLS' in report_formats_list:
                print("Downloading XLS")
                self.action.explicit_wait('report_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('template_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('template_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=11, raw_cell=True).click()
                time.sleep(1)
                file_count = file_count + 1
                assert self.common.get_non_empty_files_count_in_directory() == file_count, "Files count mismatch, not downloaded"
            if 'PDF' in report_formats_list:
                print("Downloading PDF")
                self.action.explicit_wait('report_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('template_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('template_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=12, raw_cell=True).click()
                time.sleep(1)
                file_count = file_count + 1
                assert self.common.get_non_empty_files_count_in_directory() == file_count, "Files count mismatch, not downloaded"
            if 'HTML' in report_formats_list:
                print("Opening HTML")
                self.action.explicit_wait('report_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('report_queue_tab')
                self.action.explicit_wait('template_queue_tab', ec='element_to_be_clickable')
                self.action.click_element('template_queue_tab')
                self.action.get_table_cell_data('report_queue_table', row=0, col=13, raw_cell=True).click()
        finally:
            self.action.switch_to_default_frame()
        return True

    def validate_call_data_from_csv_report(self, calling_number, call_date):
        """Validates calling data from csv report"""
        new_filename = self.common.rename_file(extension=".csv")
        csv_content_list = self.common.get_texts_from_csv_file(new_filename)
        print(csv_content_list[-1])
        assert csv_content_list[-1]['Phone'] == str(calling_number), "Calling Number doesnt match"
        assert csv_content_list[-1]['Call Time'].split(" ")[0] == call_date, "Calling Date doesnt match"
        return True

    def schedule_report(self, schedule_name, report_name, current_time_duration='Year', report_formats_list=['CSV','XLS','PDF','HTML']):
        """Schedules report from Scheduler Tab at particular time of given duration and given formats"""
        try:
            self.navigate_to_reports()
            self.action.click_element('scheduler_tab')
            self.action.explicit_wait('add_schedule_btn', ec='element_to_be_clickable')
            self.action.click_element('add_schedule_btn')
            self.action.input_text('schedule_name_input', schedule_name)
            for report_format in report_formats_list:
                self.action.click_element('schedule_output_format', replace_dict={'replace_value': report_format})
            self.action.click_element('schedule_start_time')
            self.action.explicit_wait('schedule_never_ends_radio', ec='element_to_be_clickable')
            self.action.click_element('schedule_never_ends_radio')
            self.action.click_element('frequency_duration', replace_dict={'replace_value': 'Yearly'})
            self.action.click_element('frequency_duration', replace_dict={'replace_value': 'Hourly'})
            self.action.explicit_wait('hours_input', ec='element_to_be_clickable')
            self.action.input_text('hours_input', '2')
            self.action.click_element('schedule_reports_dropdown')
            self.action.click_element('schedule_report_name', replace_dict={'replace_value': report_name})
            self.action.explicit_wait('for_current_radio', ec='element_to_be_clickable')
            self.action.click_element('for_current_radio')
            self.action.explicit_wait('nothing_selected_btn', ec='element_to_be_clickable')
            self.action.click_element('nothing_selected_btn')
            self.action.click_element('time_duration_selection', replace_dict={'replace_value': current_time_duration})
            self.action.explicit_wait('select_all_campaigns', ec='element_to_be_clickable', waittime=60)
            self.action.click_element('select_all_campaigns')
            if self.action.is_presence_of_element_located('select_all_queues'):
                self.action.click_element('select_all_queues')
            self.action.click_element('schedule_start_time')
            self.action.explicit_wait('current_time', ec='element_to_be_clickable')
            self.action.click_element('current_time')
            self.action.explicit_wait('save_btn', ec='element_to_be_clickable')
            self.action.click_element('save_btn')
            self.action.explicit_wait('scheduled_saved_modal')
            self.action.click_element('scheduled_saved_modal')
            self.action.explicit_wait('schedule_saved_message')
            self.action.click_element('ok_btn_report_tab_alert')
            self.action.explicit_wait('report_queue_table')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=1,
                                                   raw_cell=True).text == schedule_name, "Incorrect schedule name"
        finally:
            self.action.switch_to_default_frame()
        return True

    def delete_scheduled_report(self, schedule_name):
        """Deletes scheduled report from Scheduler Tab"""
        try:
            self.navigate_to_reports()
            self.action.click_element('scheduler_tab')
            assert self.action.get_table_cell_data('report_queue_table', row=0, col=1,
                                                   raw_cell=True).text == schedule_name, "Incorrect schedule name"
            self.action.get_table_cell_data('report_queue_table', row=0, col=0, raw_cell=True).click()
            self.action.explicit_wait('delete_schedule_btn', ec='element_to_be_clickable')
            self.action.click_element('delete_schedule_btn')
            self.action.explicit_wait('delete_schedule_modal')
            self.action.click_element('ok_btn_report_tab_alert')
        finally:
            self.action.switch_to_default_frame()
        return True
