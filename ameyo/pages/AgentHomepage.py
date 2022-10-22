"""
Module: This is the login module which contains methods for functionality related to Homepage.
"""
import os
import sys
import time

sys.path.append(os.path.join(
    os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), "libs", "web_action")
                )
from action import Action

class AgentHomepage:
    """Homepage functionality class"""

    def __init__(self, web_browser, common):
        self.action = Action(web_browser)
        self.common = common

    def manual_dial_only(self, calling_number, campaign_name):
        """Method to manual dial only call to calling number."""
        self.common.change_status('Available', 'available_status')
        self.action.explicit_wait('active_phone_icon', waittime=120)
        if self.action.is_presence_of_element_located('telephony_panel_hidden'):
            self.action.explicit_wait('phone_icon', ec='element_to_be_clickable')
            self.action.click_element('phone_icon')
        self.action.explicit_wait('search_for_customer_input', ec='element_to_be_clickable')
        self.action.input_text('search_for_customer_input', calling_number)
        self.action.click_element('call_btn')
        self.action.alert_action()
        self.action.explicit_wait('dial_only_btn')
        self.action.click_element('dial_only_btn')
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        self.action.element_should_contain_text('calling_number_dialer', str(calling_number))
        self.action.element_should_contain_text('campaign_on_telephony_screen', campaign_name)
        self.action.element_should_contain_text('call_type_on_telephony_screen', 'Manual Dial')
        self.action.explicit_wait('end_call_btn')
        self.action.is_presence_of_element_located('end_call_btn')
        return True

    def create_and_dial_call(self, calling_number, customer_name, campaign_name):
        """Method to save number in ameyo and then call on that number."""

        self.common.change_status('Available', 'available_status')
        self.action.explicit_wait('active_phone_icon', waittime=120)
        if self.action.is_presence_of_element_located('telephony_panel_hidden'):
            self.action.explicit_wait('phone_icon', ec='element_to_be_clickable')
            self.action.click_element('phone_icon')
        self.action.explicit_wait('search_for_customer_input', ec='element_to_be_clickable')
        self.action.input_text('search_for_customer_input', calling_number)
        self.action.click_element('call_btn')
        self.action.alert_action()
        self.action.explicit_wait('create_and_dial_btn')
        self.action.click_element('create_and_dial_btn')
        self.action.click_element('phone_icon')
        self.create_customer_info_on_ameyo(customer_name, calling_number)
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        self.action.element_should_contain_text('calling_number_dialer', str(calling_number))
        self.action.element_should_contain_text('campaign_on_telephony_screen', campaign_name)
        self.action.element_should_contain_text('call_type_on_telephony_screen', 'Manual Dial')
        self.action.explicit_wait('end_call_btn')
        self.action.is_presence_of_element_located('end_call_btn')
        return True

    def create_customer_info_on_ameyo(self, customer_name, calling_number):
        self.action.input_text('cust_info_name_input', customer_name)
        self.action.input_text('cust_info_phone1_input', calling_number)
        self.action.explicit_wait('create_contact_btn')
        self.action.click_element('create_contact_btn')
        assert self.common.validate_message_in_toast_popups("Customer Added successfully"), "Toast Message not as expected"

    def manual_preview_dial(self, saved_phone_number, saved_customer_name, campaign_name):
        """Validate manual preview dialing for saved number"""
        self.common.change_status('Available', 'available_status')
        self.action.explicit_wait('active_phone_icon', waittime=120)
        if self.action.is_presence_of_element_located('telephony_panel_hidden'):
            self.action.explicit_wait('phone_icon', ec='element_to_be_clickable')
            self.action.click_element('phone_icon')
        self.action.explicit_wait('search_for_customer_input', ec='element_to_be_clickable')
        self.action.input_text('search_for_customer_input', saved_phone_number)
        self.action.click_element('view_btn')
        self.action.element_should_contain_text('call_type_on_telephony_screen', 'Preview')
        self.action.is_presence_of_element_located('remaining_time_autodial')
        self.action.is_presence_of_element_located('cancel_btn')
        self.action.is_presence_of_element_located('preview_alternate_phone_input')
        self.action.explicit_wait('preview_dial_call_btn')
        self.action.click_element('preview_dial_call_btn')
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        self.action.element_should_contain_text('calling_number_dialer', str(saved_phone_number))
        self.action.element_should_contain_text('customer_name_dialer', saved_customer_name)
        self.action.element_should_contain_text('campaign_on_telephony_screen', campaign_name)
        self.action.element_should_contain_text('call_type_on_telephony_screen', 'Manual Dial')
        self.action.explicit_wait('end_call_btn')
        self.action.is_presence_of_element_located('end_call_btn')
        return True

    def validate_inbound_call(self, url, did_prefix, calling_number_prefix, campaign_name, queue_name):
        """Accept and validate inbound call"""
        self.common.change_status('Available', 'available_status')
        self.action.explicit_wait('active_phone_icon', waittime=120)
        self.common.hit_get_api_with_no_authentication(url, 3)
        self.action.explicit_wait('inbound_accept_call_modal')
        self.action.element_should_contain_text('inbound_call_message', 'There is an incoming call from')
        self.action.element_should_contain_text('inbound_call_message', calling_number_prefix)
        self.action.element_should_contain_text('inbound_call_dnis', did_prefix)
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Ringing')
        self.action.is_presence_of_element_located('inbound_call_accept_btn')
        self.action.click_element('inbound_call_accept_btn')
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        self.action.element_should_contain_text('calling_number_dialer', str(calling_number_prefix))
        self.action.element_should_contain_text('campaign_on_telephony_screen', campaign_name)
        self.action.element_should_contain_text('queue_on_telephony_screen', queue_name)
        self.action.element_should_contain_text('call_type_on_telephony_screen', 'Inbound')
        self.action.element_should_contain_text('did_on_telephony_screen', did_prefix)
        self.action.explicit_wait('end_call_btn')
        self.action.is_presence_of_element_located('end_call_btn')

    def save_and_validate_customer_info_during_inbound_call(self, url, customer_name):
        """Accept and validate inbound call"""
        self.common.change_status('Available', 'available_status')
        self.action.explicit_wait('active_phone_icon', waittime=120)
        self.common.hit_get_api_with_no_authentication(url, 3)
        self.action.explicit_wait('inbound_accept_call_modal')
        self.action.is_presence_of_element_located('inbound_call_accept_btn')
        self.action.click_element('inbound_call_accept_btn')
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected', waittime=120)
        inbound_customer_number = self.action.get_text('calling_number_dialer')
        self.action.click_element('phone_icon_in_talk')
        self.create_customer_info_on_ameyo(customer_name, inbound_customer_number)
        self.action.click_element('phone_icon_in_talk')
        self.action.element_should_contain_text('customer_name_dialer', customer_name)
        self.action.element_should_contain_text('cust_info_name_label', customer_name)
        self.action.element_should_contain_text('cust_info_phone1_label', inbound_customer_number)
        self.action.explicit_wait('end_call_btn')
        self.action.is_presence_of_element_located('end_call_btn')

    def validate_logout_disabled_when_call_in_progress(self):
        """Validate logout functionality disabled when call is in progress"""
        self.action.is_presence_of_element_located('preferences_drop_down_btn')
        self.action.click_element('preferences_drop_down_btn')
        self.action.explicit_wait('disabled_logout_btn')
        return True

    def end_call_and_auto_dispose(self):
        """End the call and validate call auto disposed in 30 seconds"""
        self.action.explicit_wait('end_call_btn')
        self.action.click_element('end_call_btn')
        assert self.common.validate_message_in_toast_popups("End Call Successful"), "Toast Message not as expected"
        # Waiting for 30seconds- call auto dispose time
        time.sleep(30)
        self.action.is_presence_of_element_located('call_btn')
        self.action.click_element('phone_icon')
        return True

    def select_quick_disposition(self, dispose_value):
        """This function will select the given quick disposition value"""
        if 'Already hungup' == dispose_value:
            self.action.click_element('btn_already_hungup')
        elif 'Sale' == dispose_value:
            self.action.click_element('btn_sale')
        elif 'Foreign Language' == dispose_value:
            self.action.click_element('btn_foreign_language')
        elif 'Abrupt disconnection' == dispose_value:
            self.action.click_element('btn_abrupt_disconnection')
        elif 'Agent volume too low' == dispose_value:
            self.action.click_element('btn_agent_volume_too_low')
        else:
            print('Given value for quick_disposition did not match')
            return False

    def select_disposition(self, dispose_value, sub_disposition_value):
        """This function will select the disposition and sub disposition"""
        self.action.click_element('dropdown_disposition')
        self.action.input_text("textbox_search", dispose_value)
        self.action.press_key("textbox_search", "ARROW_DOWN")
        self.action.press_key("textbox_search", "ENTER")
        self.action.click_element('dropdown_sub_disposition')
        self.action.input_text("textbox_search", sub_disposition_value)
        self.action.press_key("textbox_search", "ARROW_DOWN")
        self.action.press_key("textbox_search", "ENTER")

    def save_and_dispose(self):
        """This function will select the disposition and sub disposition"""
        self.action.click_element('end_call_btn')
        assert self.common.validate_message_in_toast_popups("End Call Successful"), "Toast Message not as expected"
        time.sleep(2)
        self.action.click_element('btn_already_hungup')
        self.action.click_element('btn_save_and_dispose')
        assert self.common.validate_message_in_toast_popups("Disposed successfully"), "Toast Message not as expected"

    def open_close_dialer(self):
        """This function will open and close dialer"""
        self.action.explicit_wait('phone_icon', ec='element_to_be_clickable')
        self.action.click_element('phone_icon')

    def dispose_and_dial(self, dispose_dial_dict, dispose_type, dial_position):
        """This function will cover dispose and dial call flow"""
        if dial_position.lower() == 'dial_after_call_cut':
            self.action.click_element('end_call_btn')
            assert self.common.validate_message_in_toast_popups("End Call Successful"), "Toast Message not as expected"
            time.sleep(2)
        if dial_position.lower() == 'dial_before_call_cut':
            self.action.click_element('btn_disposition_down_arrow')
        if dispose_type.lower() == 'quick':
            self.select_quick_disposition(dispose_dial_dict['quick_disposition'])
        elif dispose_type.lower() == 'selection':
            self.select_disposition(dispose_dial_dict['disposition'], dispose_dial_dict['sub_disposition'])
        self.action.input_text("text_disposition_note", dispose_dial_dict['disposition_note'])
        self.action.click_element('btn_dispose_and_dial')
        self.action.input_text("text_enter_number", dispose_dial_dict['dial_number'])
        self.action.click_element('btn_call')
        self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        time.sleep(2)
        self.save_and_dispose()
        self.open_close_dialer()
        return True

    def select_disposition_save_and_dispose(self, disposition_type, sub_disposition):
        """This action will select the dispositions and sub disposition from dropdown and click on Save and Dispose"""
        self.action.explicit_wait('end_call_btn')
        self.action.click_element('end_call_btn')
        assert self.common.validate_message_in_toast_popups("End Call Successful"), "Toast Message not as expected"
        self.action.explicit_wait('dropdown_disposition')
        self.action.click_element('dropdown_disposition')
        self.action.select_from_ul_dropdown_using_text('select_dropdown_list', disposition_type)
        self.action.click_element('dropdown_sub_disposition')
        self.action.select_from_ul_dropdown_using_text('select_dropdown_list', sub_disposition)
        self.action.input_text('text_disposition_note', 'Disposition Note')
        self.action.click_element('btn_save_and_dispose')
        assert self.common.validate_message_in_toast_popups("Disposed successfully"), "Toast Message not as expected"

    def hold_resume_call(self):
        """Hold/Un-hold the call and validate the alert"""
        self.action.explicit_wait('hold_button')
        if self.action.is_presence_of_element_located('button_status_normal'):
            self.action.click_element('hold_button')
            assert self.common.validate_message_in_toast_popups("Call On Hold"), "Toast Message not as expected"
            self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='On Hold')
        else:
            self.action.click_element('hold_button')
            assert self.common.validate_message_in_toast_popups("Call Resumed"), "Toast Message not as expected"
            self.action.explicit_wait('call_status', ec='text_to_be_present_in_element', msg_to_verify='Connected')
        return True

    def transfer_call_not_allowed_during_hold(self, calling_number):
        """To validate transfer call during call hold is not allowed"""
        self.action.explicit_wait('transfer_call_btn')
        self.action.click_element('transfer_call_btn')
        self.action.explicit_wait('transfer_phone_tab')
        self.action.click_element('transfer_phone_tab')
        self.action.input_text('transfer_phone_input_text', calling_number)
        self.action.explicit_wait('transfer_phone_btn', ec='element_to_be_clickable')
        self.action.click_element('transfer_phone_btn')
        assert self.common.validate_message_in_toast_popups("Call transfer to Phone failed"), "Toast Message not as expected"
        self.action.click_element('transfer_call_btn')
        return True

    def change_campaign(self, kwargs) -> bool:
        """This function will select campaign"""
        self.action.click_element("preferences_drop_down_btn")
        self.action.click_element("change_campaign_link")
        if kwargs['new_interaction']:
            self.action.click_element("dropdown_interaction")
            self.action.select_from_ul_dropdown_using_text("ul_campaign_selector", kwargs['new_interaction'])
            self.action.click_element("button_next")
            elements = self.action.get_element('selected_campaign_verification')
            campaign_list = [element.text for element in elements]
            assert kwargs['new_video'] in campaign_list, "Campaign is not as expected"
        if kwargs['new_chat']:
            self.action.click_element("dropdown_chat")
            self.action.select_from_ul_dropdown_using_text("ul_campaign_selector", kwargs['new_chat'])
            self.action.click_element("button_next")
            elements = self.action.get_element('selected_campaign_verification')
            campaign_list = [element.text for element in elements]
            assert kwargs['new_video'] in campaign_list, "Campaign is not as expected"
        if kwargs['new_voice']:
            self.action.explicit_wait("cross_selected_campaign")
            self.action.click_element("cross_selected_campaign")
            self.action.explicit_wait("ul_campaign_selector")
            self.action.select_from_ul_dropdown_using_text("ul_campaign_selector", kwargs['new_voice'])
            self.action.click_element("button_next")
            elements = self.action.get_element('selected_campaign_verification')
            campaign_list = [element.text for element in elements]
            assert kwargs['new_video'] in campaign_list, "Campaign is not as expected"
        if kwargs['new_video']:
            self.action.click_element("dropdown_video")
            self.action.select_from_ul_dropdown_using_text("ul_campaign_selector", kwargs['new_video'])
            self.action.click_element("button_next")
            elements = self.action.get_element('selected_campaign_verification')
            campaign_list = [element.text for element in elements]
            assert kwargs['new_video'] in campaign_list, "Campaign is not as expected"
        return True

    def change_password(self, oldpass, newpass) -> bool:
        """Change Password of a logged in Agent"""
        self.action.explicit_wait('active_phone_icon', waittime=120)
        self.action.click_element("preferences_drop_down_btn")
        self.action.click_element("change_pass_link")
        self.action.input_text('current_password', oldpass)
        self.action.explicit_wait('current_password', waittime=120)
        self.action.input_text('new_password', newpass)
        self.action.explicit_wait('new_password', waittime=120)
        self.action.input_text('confirm_password', newpass)
        self.action.click_element("update_button")
        assert self.common.validate_message_in_toast_popups("Password updated successfully"), "Toast Message not as expected"
        return True

    def set_status(self) -> bool:
        """Change Agent Status from Just logged to available and to any break reason"""
        self.action.explicit_wait('active_phone_icon', waittime=120)
        self.common.change_status('Available', 'available_status')
        self.common.change_status('Break', 'break_status')
        self.common.change_status('Available', 'available_status')
        self.common.change_status('Snack', 'snack_status')
        self.common.change_status('Available', 'available_status')
        return True
