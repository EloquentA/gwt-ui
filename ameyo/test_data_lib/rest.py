__author__ = "Developed by EA"

import os
import time
import json
import re
import yaml
import allure

from urllib.parse import urljoin
from ameyo.test_data_lib.create_data import DataCreationAPIs


class AmeyoRest(DataCreationAPIs):
    """
    Main Class for Ameyo Rest Library
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.sessionIds = dict()
        if self.noop is False:
            if not hasattr(self.creds, 'username'):
                raise Exception(f"username is Required Parameter !!")

            # We will wait till Token for CC Manager Expires, and then make a new one
            # no force logging for multi cc user
            force = True if os.environ.get('AMEYO_FORCE_LOGIN', None) else False
            while True:
                try:
                    self.ccManagerToken = self.generate_user_token(
                        user=self.creds.username, password=self.creds.password, force=force
                    )
                    break
                except (Exception, ValueError):
                    self.logger.info(f"User: {self.creds.username} Failed to Login, Retry after 15 seconds ...")
                    time.sleep(15)

        self.userCRTObjectId, self.customerCRTObjectId = None, None
        self._iter = 1

    def generate_user_token(self, user, password='Test300!@#', force=True):
        """
        Generate a new user Token (Login)
        :param user:
        :param password:
        :param force:
        :return:
        """
        response = self.user_login(userId=user, token=password, forceLogin=force)
        if self.noop is True:
            return response
        self.rest.raise_for_status(response)
        Json = response.json()
        if 'status' in Json and Json['status'] == 512 and 'info' in Json:
            raise Exception(f"Cannot Generate Token !! System-Message: {Json['info']}")
        return Json['userSessionInfo']['sessionId']

    def keep_alive(self, **kwargs):
        """
        Keep Alive with Ping Push
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', None)

        # Get all Recent Push Notifications
        # self.ws_data(sessionId=sessionId, process=False)

        if sessionId is None:
            raise Exception(f"sessionId is None")

        if sessionId and sessionId not in self.sessionIds.keys():
            self.sessionIds[sessionId] = {
                'listener-name': f'webcore_{round(time.time() * 1000)}',
                'lastProcessedPush': -1,
            }

        listenerName = self.sessionIds[sessionId]['listener-name']
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, 'ameyorestapi/session/keepAliveWithPingPush'),
            'headers': {'sessionId': sessionId},
            'json': {
                'sessionId': sessionId, 'listenerName': listenerName, 'pushesFollowPing': True,
                'lastProcessedPushId': self.sessionIds[sessionId]['lastProcessedPush'],
            },
        })
        if self.noop is True:
            return response
        # response.raise_for_status()
        return response

    def ws_data(self, sessionId, process=True, lastProcessedPush=None):
        """
        Get Push Messages
        :param sessionId:
        :param process:
        :param lastProcessedPush:
        :return:
        """
        if sessionId and sessionId not in self.sessionIds.keys():
            # when sessionId is missing from dict (1st Run)
            self.sessionIds[sessionId] = {
                'listener-name': f'webcore_{round(time.time() * 1000)}',
                'lastProcessedPush': -1,
            }

        if lastProcessedPush == -1:
            # new listener who want all push notifications
            listener = f'webcore_{round(time.time() * 1000)}'
        else:
            # for only new pushes
            listener = self.sessionIds[sessionId]['listener-name']

        if lastProcessedPush is None:
            # case when user does not want all pushes, we send latest to him
            lastProcessedPush = self.sessionIds[sessionId]['lastProcessedPush']

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f'ameyorestapi/pushes'),
            'headers': {"sessionId": sessionId, },
            'params': {
                'listener-name': listener, 'lastProcessedPush': lastProcessedPush,
            },
            'stream': True, 'timeout': 1,
        })

        data = ''
        try:
            for chunk in response.iter_content(1024):
                data += chunk.decode()
        except (Exception, ValueError) as Exp:
            pass

        response = list(map(lambda a: json.loads(a), [x for x in re.findall(r'({.*})', data, re.I | re.M)]))
        if listener == self.sessionIds[sessionId]['listener-name'] and len(response) > 0:
            # store seqNo only when listener name matches with stored listener name
            self.sessionIds[sessionId]['lastProcessedPush'] = response[-1]['seqNo']

        if len(response) > 0:
            return self.__sort_pushes(response=response, process=process, lastProcessed=response[-1]['seqNo'])
        else:
            if "--DON'T_PANIC!_more_will_follow" != data.strip():
                print(f"Are pushes empty? for {sessionId} data received is <{data}>")
        return []

    @staticmethod
    def __sort_pushes(response, lastProcessed, process=True):
        """
        Save Pushes
        :param response:
        :param process:
        :return:
        """
        if process is True:
            data = []
            for _ref in ['UserCallModel', 'CustomerCallMember', 'JobProgressNotifyPush']:
                data.extend(list(filter(lambda a: a['pushType'].startswith(_ref), response)))
            data = sorted(data, key=lambda a: a['seqNo'])
        else:
            data = sorted(response, key=lambda a: a['seqNo'])

        # attach Push Notifications to allure report
        allure.attach(
            yaml.dump_all(data, sort_keys=False), name=f'Push-Notifications-{lastProcessed:03}.yaml',
            attachment_type=allure.attachment_type.YAML
        )
        return data

    def get_user_crt(self, pushes=None, sessionId=None):
        """
        Get User CRT
        :param pushes:
        :return:
        """
        sessionId = self.executiveToken if sessionId is None else sessionId
        if pushes is None or len(pushes) == 0:
            pushes = self.ws_data(sessionId=sessionId, lastProcessedPush=-1)
        if not len(pushes):
            raise Exception(f"user CRT Object not found as no push received for {sessionId}")

        for push in pushes[::-1]:
            if push['pushType'] == 'UserCallModelUpdatedPush':
                user_crt = push['data']['crtObjectId']
                return user_crt
        else:
            raise Exception(f"user CRT Object not found in UserCallModelUpdatedPush !!")

    def get_customer_crt(self, pushes=None, sessionId=None):
        """
        Get Customer CRT
        :return:
        """
        sessionId = self.executiveToken if sessionId is None else sessionId
        if pushes is None or len(pushes) == 0:
            pushes = self.ws_data(sessionId=sessionId, lastProcessedPush=-1)

        if not len(pushes):
            self.logger.info(f"Customer CRT Object not found as no push received for {sessionId}")
            return

        for push in pushes[::-1]:
            if push['pushType'] == 'CustomerCallMemberCreatedPush':
                customer_crt = push['data']['crtObjectId']
                self.logger.debug(f"Customer CRT Object found in CustomerCallMemberCreatedPush")
                return customer_crt
            elif push['pushType'] == 'CustomerCallMemberUpdatedPush':
                self.logger.debug(f"Customer CRT Object found in CustomerCallMemberUpdatedPush")
                customer_crt = push['data']['crtObjectId']
                return customer_crt
        else:
            self.logger.info(f"Customer CRT Object not found in pushes. Retrying...")

    def get_value_from_push(self, pushes=None, push_type=None, attribute_to_return=None, preview_dial=False):
        """
        Get value of an attribute from a specific push after confirming presence of some value(optional)
        :return:
        """
        if not len(pushes):
            self.logger.info(f"No push received for processing")
            time.sleep(1)
            return

        for push in pushes[::-1]:
            if push['pushType'] == push_type:
                if preview_dial:
                    if push["data"].get("associationAttributes", {}).get("customer.object.type",
                                                                         None) == "auto.preview.dial.customer":
                        return push['data'][attribute_to_return]
                else:
                    return push["data"][attribute_to_return]
        else:
            self.logger.info(f"{push_type} not found in {len(pushes)} pushes Retrying...")

    def verify_manual_dial_pushes(self, callContextName, pushes):
        """
        Verify Manual Dial Pushes
        :param callContextName:
        :param pushes:
        :return:
        """

        references = self.CustomerCx[callContextName]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.info(f"#{self._iter:02} {callContextName}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self.customerCRTObjectId = self.get_customer_crt(pushes=pushes)
        if self.customerCRTObjectId is None:
            self.logger.error(f"customerCRTObjectId is None/Not-Set !!")
            return False

        self._iter = 1
        return True

    def verify_auto_dial_pushes(self, reference_push, pushes):
        """
        Verify Auto Dial Pushes
        These pushes to agent will activate its telephony on UI
        :param reference_push:
        :param pushes:
        :return:
        """

        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self._iter = 1
        return True

    def verify_transfer_to_campaign_pushes(self, reference_push, pushes):
        """
        Verify transfer to campaign Pushes
        :param reference_push:
        :param pushes:
        :return:
        """
        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self._iter = 1
        return True

    def verify_transfer_to_phone_pushes(self, reference_push, pushes):
        """
        Verify transfer to phone Pushes
        :param reference_push:
        :param pushes:
        :return:
        """
        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self._iter = 1
        return True

    def verify_confer_to_phone_pushes(self, reference_push, pushes):
        """
        Verify confer to phone Pushes
        :param reference_push:
        :param pushes:
        :return:
        """
        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self._iter = 1
        return True

    def verify_confer_to_user_pushes(self, reference_push, pushes):
        """
        Verify transfer to user Pushes
        :param reference_push:
        :param pushes:
        :return:
        """
        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self._iter = 1
        return True

    def verify_transfer_to_user_pushes(self, reference_push, pushes):
        """
        Verify transfer to user Pushes
        :param reference_push:
        :param pushes:
        :return:
        """
        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False  # if there is a mismatch between expected and received status
            else:
                return False  # if the type of push is not at all present in the received pushes

        self._iter = 1
        return True

    def verify_transfer_to_queue_pushes(self, reference_push, pushes):
        """
        Verify transfer to queue Pushes
        :param reference_push:
        :param pushes:
        :return:
        """
        references = self.CustomerCx[reference_push]['pushes']
        received = dict()
        for push in list(filter(lambda a: a['pushType'] in list(references.keys()), pushes)):
            _type, _status = push['pushType'], push['data']['status']
            if _type not in received.keys():
                received[_type] = [_status]
            else:
                if _status not in received[_type]:
                    received[_type].append(_status)

        for _type, _ref in references.items():
            if _type in received.keys():
                left = set(_ref) - set(received[_type])
                if len(left) > 0:
                    self.logger.error(f"#{self._iter:02} {reference_push}: {_type} → Not-Received: {left} !!")
                    self._iter += 1
                    return False
            else:
                return False

        self._iter = 1
        return True

    def verify_login_pushes(self, pushes):
        """
        Verify Pushes after Login
        :param pushes:
        :return:
        """
        names = {
            # 'UserCallModelUpdatedPush',  # UserCallModelCreatePush is missing :(
            'UserCCRuntimeCreatedPush', 'UserCCRuntimeUpdatedPush',
            'UserCCPresenceCreatedPush', 'UserCCPresenceUpdatedPush',
            # 'UserCampaignRuntimeCreatedPush', 'UserCampaignRuntimeUpdatedPush',
            # 'UserAQRuntimeCreatedPush', 'UserAQRuntimeUpdatedPush',
        }
        for push in pushes:
            if push['pushType'] in names:
                names.remove(push['pushType'])

        if len(names) == 0:
            self._iter = 1
            return True

        self._iter += 1
        self.logger.error(f"Waiting for {names} Pushes !!")
        return False

    def make_customer(self, acd, phone1, priority=1):
        """
        Make Customer from agent column definition
        :param acd:
        :param phone1:
        :return:
        """
        f_name = self.faker.first_name()
        l_name = self.faker.last_name()
        timezone = 'Asia Pacific'

        customerData = {}
        for col in acd:
            if 'phone' in col['columnName']:
                customerData[col['columnName']] = phone1
            elif 'name' in col['columnName']:
                customerData[col['columnName']] = f"{f_name} {l_name} {phone1}"
            elif 'timezone' in col['columnName']:
                customerData[col['columnName']] = timezone
            elif 'email' in col['columnName']:
                customerData[col['columnName']] = f"{f_name}.{l_name}_{phone1}@yopmail.com"
            elif 'priority' in col['columnName']:
                customerData[col['columnName']] = priority
            else:
                customerData[col['columnName']] = f"{f_name}{l_name}{phone1}"

        return customerData


if __name__ == '__main__':
    _x = AmeyoRest(url="https://fluidcxdemo.ameyo.com:8443", username="ANSHUMAN_MULTI_CC", password="ANSHUMAN_MULTI_CC")
    print(_x)
