__author__ = "Developed by EA"

from datetime import datetime
import time
import csv
import json
import urllib
from urllib.parse import urljoin
from pathlib import Path

from ameyo.test_data_lib.wrapper import Wrapper


class DataCreationAPIs(Wrapper):
    """
    Ameyo Contact Center CRUD (Create, Read, Update and Delete) Operations
    """

    def __init__(self, **kwargs):
        """
        Init Class for Crud Operations
        :param instance: instance name
        :param noop: no operation to be performed
        """
        super().__init__(**kwargs)

    def create_cc(self, **kwargs):
        """
        Create a Contact Center
        :param kwargs:
        :return:
        """
        contactCenterName = kwargs.get('contactCenterName', None)
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([contactCenterName, sessionId])

        accessTemplateId = kwargs.get('accessTemplateId', 1)
        description = kwargs.get('description', f"{contactCenterName} Description :)")
        userIds = kwargs.get('userIds', None)
        if userIds and not isinstance(userIds, list):
            userIds = [userIds]
        isRoot = kwargs.get('isRoot', None)
        userTypes = kwargs.get('userTypes', None)
        if userTypes and not isinstance(userTypes, list):
            userTypes = [userTypes]

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/contactCenters"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {x: y for x, y in {
                "contactCenterName": contactCenterName,
                "accessTemplateId": accessTemplateId,
                "description": description,
                "userIds": userIds,
                "isRoot": isRoot,
                "userTypes": userTypes
            }.items() if y is not None}
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'contactCenterId', 'processIds', 'contactCenterName', 'userTemplateIds', 'blendGroupIds',
            'contactCenterPrivilegePlanIds', 'knowledgeBaseURL', 'accessTemplateId', 'breakReasons',
            'privilegeUniverse', 'skillIds', 'contactCenterUserIds', 'contactCenterTeamIds', 'authenticationType',
            'dateAdded', 'dateModified'
        ], response.json())
        return response

    def get_all_cc(self, **kwargs):
        """
        Get all Contact Centers
        :param kwargs:
        :return:
        """
        url = urljoin(self.creds.url, "ameyorestapi/cc/contactCenters/getAllContactCenters")
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': url,
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'accessTemplateId', 'skillIds', 'contactCenterPrivilegePlanIds', 'contactCenterUserIds',
                'knowledgeBaseURL', 'userTemplateIds', 'blendGroupIds', 'contactCenterTeamIds', 'authenticationType',
                'breakReasons', 'privilegeUniverse', 'contactCenterName', 'contactCenterId', 'processIds', 'dateAdded',
                'dateModified', 'description'
            ], _item)
        return response

    def get_all_users(self, **kwargs):
        """
        Get all users in system (both mapped and not-mapped to cc)
        :param kwargs:
        RPC: getAllContactCenterUsers
        :return:
        """
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/contactCenterHierarchy/getAllUsers"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'contactCenterId', 'systemRole', 'userID', 'ccUserId',
                'userName'
            ], _item)
        return response

    def get_all_users_assigned_to_cc(self, **kwargs):
        """
        Get all Contact Center users
        :param kwargs:
        :return:
        """
        ccId = kwargs.get('ccId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([ccId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'ccId': ccId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/contactCenterUsers/getAllContactCenterUsers"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'ccUserId', 'userId', 'userType', 'skillLevelIds', 'skillIds', 'userName', 'systemUserType',
                'privilegePlanId', 'defaultReady', 'maskedPrivileges', 'maxAllowedLogins', 'loginPolicy',
                'mappingUserId'
            ], _item)
        return response

    def delete_cc(self, **kwargs):
        """
        Delete a Contact Center
        :param kwargs:
        :return:
        """
        contactCenterId = kwargs.get('contactCenterId', None)
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([contactCenterId, sessionId])

        response = self.rest.send_request(**{
            'method': 'DELETE',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/contactCenters/{contactCenterId}"),
            'params': {'reason': kwargs.get('reason', "Reason not given")},
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def create_cc_user(self, **kwargs):
        """
        Create a Contact Center Admin User
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        userName = kwargs.get('userName', userId)
        userType = kwargs.get('userType', 'Administrator')
        isDeleted = kwargs.get('isDeleted', False)
        isRoot = kwargs.get('isRoot', True)  # Supervisor and Executive = False
        userData = kwargs.get('userData', 'Test300!@#')
        maxAllowedLogins = kwargs.get('maxAllowedLogins', 1)
        loginPolicy = kwargs.get('loginPolicy', 'verify.before.force.login')
        sessionId = kwargs.get('sessionId', self.ccManagerToken)

        self.check_required_args([
            userId, userType, userName, isDeleted, isRoot, userData, maxAllowedLogins, loginPolicy, sessionId
        ])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/user/users"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "userId": userId, "userType": userType, "username": userName, "isDeleted": isDeleted,
                "isRoot": isRoot, "userData": userData, "maxAllowedLogins": maxAllowedLogins, "loginPolicy": loginPolicy
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'userId', 'username', 'userType', 'systemPrivilegePlanId', 'isRoot', 'isDeleted', 'maxAllowedLogins',
            'loginPolicy'
        ], response.json())
        return response

    def assign_user_to_cc(self, **kwargs):
        """
        Assign User to CC
        :param kwargs:
        :return:
        """
        allocateContactCenterId = kwargs.get('allocateContactCenterId', None)

        userIds = kwargs.get('userIds', None)
        if not isinstance(userIds, list):
            userIds = [userIds]

        userTypes = kwargs.get('userTypes', 'Administrator')
        if not isinstance(userTypes, list):
            userTypes = [userTypes]

        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([userIds, userTypes, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/allocateMultipleUsersToContactCenter"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'allocateContactCenterId': allocateContactCenterId,
                'userIds': userIds, 'userTypes': userTypes
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'contactCenterTeamIds', 'userBusinessMetadata', 'contactCenterUserId', 'userType', 'sysetmUserType',
                'defaultReady', 'skillLevelIds', 'processUserIds', 'contactCenterId', 'privilegePlanId',
                'maskedPrivileges', 'root', 'userId', 'assigned', 'extensions'
            ], _item)
        return response

    def delete_cc_user(self, **kwargs):
        """
        Delete a User from CC
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([userId, sessionId])
        response = self.rest.send_request(**{
            'method': 'DELETE',
            'params': {'userId': userId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/removeUser"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def update_break_reasons(self, **kwargs):
        """
        Update the break reasons
        Note: This will overwrite the existing break reasons
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        breakReasons = kwargs.get('breakReasons', None)
        if not isinstance(breakReasons, list):
            breakReasons = [breakReasons]
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/contactCenterSettings/updateBreakReasons"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'breakReasons': breakReasons,
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'knowledgeBaseURL', 'breakReasons', 'contactCenterName', 'contactCenterId'
        ], response.json())
        return response

    def update_knowledge_base_url(self, **kwargs):
        """
        update_knowledge_base_url
        Note: This will overwrite the existing knowledge base url
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        knowledge_base_url = kwargs.get('knowledge_base_url', None)
        # if not isinstance(breakReasons, list):
        #     breakReasons = [breakReasons]
        self.check_required_args([sessionId, knowledge_base_url])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/contactCenterSettings/updateKnowledgeBaseURL"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'knowledgeBaseURL': knowledge_base_url,
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'knowledgeBaseURL', 'breakReasons', 'contactCenterName', 'contactCenterId'
        ], response.json())
        return response

    def get_voice_resource_status(self, **kwargs):
        """
        Get the voice resource status
        CCManager-> Admin->DefaultCC->More->Call Manager->VoiceResource
        :param kwargs:
        :return: status of reachable and recordingStatus as Boolean
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url,
                           f"ameyorestapi/cm/voiceResourceStatuses/getVoiceResourceStateByVoiceResourceId"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {
                'info': False,
                'voiceResourceId': 1,
                f'ts{round(datetime.now().timestamp()) * 1000}': None
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'reachable', 'recordingStatus', 'voiceResourceId'
        ], response.json())
        return response

    def delete_process(self, **kwargs):
        """
        Delete Given Process
        :param kwargs:
        :return:
        """
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processId, sessionId])
        response = self.rest.send_request(**{
            'method': 'DELETE',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/processes/{processId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        return response

    def terminate_all_sessions_for_user(self, **kwargs):
        """
        Terminate all user Sessions
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        reason = kwargs.get('reason', 'Terminating all user Sessions !!')
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([userId, reason, sessionId])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/session/terminateAllSessionsForUser"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'userId': userId,
                'reason': reason
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def delete_user(self, **kwargs):
        """
        Delete an agent
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([userId, sessionId])

        response = self.rest.send_request(**{
            'method': 'DELETE',
            'url': urljoin(self.creds.url, f"ameyorestapi/user/users/{userId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def user_login(self, **kwargs):
        """
        Login a user
        RPC Call: userLogin
        :param kwargs:
        :return:
        """
        if self.system_version == "4.x":
            userId = kwargs.get('userId', None)
            token = kwargs.get('token', 'Test300!@#')
            self.check_required_args([userId, token])

            forceLogin = kwargs.get('forceLogin', True)
            domain = kwargs.get('domain', self.creds.domain)
            response = self.rest.send_request(**{
                'method': 'POST',
                'url': urljoin(self.creds.url, 'ameyorestapi/userLogin/login'),
                'json': {"domain": domain, "userId": userId, "token": token, "forceLogin": forceLogin},
                'headers': {"correlation": self.uuid}
            })
            if response.status_code == 512:
                msg = "SessionService.login.failed.not.able.to.fetch.user.info"
                if msg in response.json()["message"]:
                    self.logger.info("Login failed, retrying...")
                    while True:
                        response = self.rest.send_request(**{
                            'method': 'POST',
                            'url': urljoin(self.creds.url, 'ameyorestapi/userLogin/login'),
                            'json': {"domain": domain, "userId": userId, "token": token, "forceLogin": forceLogin},
                            'headers': {"correlation": self.uuid}
                        })
                        if response.status_code == 200:
                            self.is_logged_in = True
                            break
                        else:
                            time.sleep(2)
            if self.noop is True or kwargs.get('toFail', True) is False:
                return response
            self.rest.raise_for_status(response)
            self.is_key_there_in_dict([
                'requestId', 'contactCenterId', 'userSessionInfo', 'authenticationState', 'configurations'
            ], response.json())
            return response
        elif self.system_version == "5.x":
            userId = "agent"  # kwargs.get('userId', None)
            token = "agent"  # kwargs.get('token', 'Test300!@#')
            self.check_required_args([userId, token])

            forceLogin = kwargs.get('forceLogin', True)
            domain = kwargs.get('domain', self.creds.domain)
            continueUrl = kwargs.get('continueUrl', f"https://{domain}/newapp")
            response = self.rest.send_request(**{
                'method': 'POST',
                'url': urljoin(self.creds.url, 'session/login'),
                'json': {"domain": domain, "userId": userId, "token": token, "forceLogin": forceLogin},
                'params': {"continueUrl": continueUrl},
                'headers': {"correlation": self.uuid}
            })
            if self.noop is True or kwargs.get('toFail', True) is False:
                return response
            self.rest.raise_for_status(response)
            self.is_key_there_in_dict([
                'requestId', 'contactCenterId', 'userSessionInfo', 'authenticationState', 'loginProperties'
            ], response.json())
            return response

    def create_user(self, **kwargs):
        """
        Create a user
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        userType = kwargs.get('userType', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([userId, userType, sessionId])

        userName = kwargs.get('userName', userId)
        emailId = kwargs.get('emailId', f"{userName}@yopmail.com")
        password = kwargs.get('password', 'Test300!@#')
        userData = kwargs.get('userData', password)
        contactCenterId = kwargs.get('contactCenterId', 1)
        phoneNumber = kwargs.get('phoneNumber', self.faker.msisdn()[3:])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/addUserWithMultimediaAttributesToCC"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "contactCenterUserMultiMediaAttributesBean": {
                    "contactCenterId": contactCenterId,
                    "userId": userId,
                    "isEmailAllowed": False,
                    "numOfChatExtensions": 5,
                    "numOfInteractionExtensions": 50,
                    "isSmsAllowed": False,
                    "isWebQueryAllowed": False,
                    "emailId": emailId,
                    "password": password,
                    "phoneNumber": phoneNumber,
                    "isScreenRecordAllowed": False
                },
                "description": "Automation Created User",
                "loginPolicy": "verify.before.force.login",
                "mappingUserId": "",
                "maxAllowedLogins": 1,
                "systemUserType": userType,
                "userData": userData,
                "userId": userId,
                "userName": userName,
                "userType": userType,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'userId', 'userType', 'assigned', 'contactCenterUserId', 'skillLevelIds', 'systemUserType',
            'privilegePlanId', 'maskedPrivileges', 'processUserIds', 'contactCenterTeamIds', 'userBusinessMetadata',
            'contactCenterId', 'defaultReady', 'extensions', 'root', 'description', 'userName'
        ], response.json())
        return response

    def get_password_policy_for_user(self, **kwargs):
        """
        Get password policy for user
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', None)
        userId = kwargs.get('userId', None)
        self.check_required_args([sessionId, userId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/session/getPasswordPolicyForUser"),
            'params': {"userId": userId},
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'allowed_special_character', 'anagramAllow', 'complexPasswordPolicyConfigured',
            'disallowPreviousPassword', 'disallowUserId', 'disallowUserName', 'enforcePasswordPolicyConfigured',
            'excludeStrings', 'maxPasswordAge', 'maxPasswordLength', 'minLowercaseLetter', 'minNumber',
            'minPasswordAge', 'minPasswordLength', 'minSpecialCharacter', 'minUppercaseLetter', 'mustContainString',
            'pwdGraceValue', 'regrexPasswordPolicyConfigurated', 'repeatingCharacterAllow', 'required_lowercase',
            'required_number', 'required_specialCharcater', 'required_uppercase', 'simplePasswordPolicyConfigured'
        ], response.json())
        return response

    def change_password(self, **kwargs):
        """
        Change login password
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', None)
        userId = kwargs.get('userId', None)
        oldPassword = kwargs.get('oldPassword', None)
        newPassword = kwargs.get('newPassword', None)
        self.check_required_args([sessionId, userId, oldPassword, newPassword])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, 'ameyorestapi/session/changePassword'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {"userId": userId, "oldPassword": oldPassword, "newPassword": newPassword}
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def get_all_call_context(self, **kwargs):
        """
        Get all System Level Call Contexts
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.ccManagerToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cm/callContexts/getAllCallContexts"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'id', 'voiceResourceId', 'entityName', 'name', 'isLocal', 'isEndpoint', 'allowIncoming',
                'allowOutgoing', 'dstphoneIncomingScript', 'dstphoneOutgoingScript', 'srcphoneIncomingScript',
                'srcphoneOutgoingScript', 'dstphoneIncomingScriptEnabled', 'dstphoneOutgoingScriptEnabled',
                'srcphoneIncomingScriptEnabled', 'srcphoneOutgoingScriptEnabled', 'autoGenerated'
            ], _item)
        return response

    def get_cc_call_contexts(self, **kwargs):
        """
        Get call context(s) assigned to a contact center
        RPC Call: getAllContactCenterCallContext
        :param kwargs:
        :return:
        """
        ccId = kwargs.get('ccId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'ccId': ccId} if ccId else {},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/contactCenterCallContexts/getAllContactCenterCallContext"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'contactCenterCallContextId', 'maxOutboundCalls', 'maxInboundCalls', 'maxTotalActiveCalls',
                'callContextId', 'callContextName', 'isEndPoint', 'isLocal', 'contactCenterId'
            ], _item)
        return response

    def assign_call_contexts_to_cc(self, **kwargs):
        """
        Assign call context(s) to a contact center
        :param kwargs:
        :return:
        """
        contactCenterId = kwargs.get('contactCenterId', None)
        callContexts = kwargs.get('callContexts', None)
        if not isinstance(callContexts, list):
            raise Exception(f"callContexts has to be a list")
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([contactCenterId, callContexts, sessionId])

        contactCenterCallContextBeans = []
        for callContext in callContexts:
            callContextId = callContext.get('callContextId', None)
            assert callContextId, "ERROR: callContextId cannot be None !!"
            contactCenterCallContextBeans.append({
                "contactCenterId": contactCenterId,
                "callContextId": callContextId,
                "maxOutboundCalls": callContext.get('maxOutboundCalls', 1000),
                "maxInboundCalls": callContext.get('maxInboundCalls', 1000),
                "maxTotalActiveCalls": callContext.get('maxTotalActiveCalls', 1000),
            })

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/assignCallContextsToContactCenter"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "ccId": contactCenterId,
                "contactCenterCallContextBeans": contactCenterCallContextBeans
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['contactCenterCallContextBeans', 'ccId'], response.json())
        for _item in response.json()['contactCenterCallContextBeans']:
            self.is_key_there_in_dict([
                'id', 'contactCenterId', 'callContextId', 'maxOutboundCalls', 'maxInboundCalls', 'maxTotalActiveCalls'
            ], _item)
        return response


    def get_table_definitions(self, **kwargs):
        """
        Get Table Definitions
        if tableDefinitionId is passed, table definitions for that ID are sent back, else for all tables in system
        RPC Call: getAllTableDefinitionsInContactCenter
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])

        tableDefinitionId = kwargs.get('tableDefinitionId', None)
        if tableDefinitionId is None:
            url = urljoin(self.creds.url, f'ameyorestapi/cc/tableDefinitions/getAllTableDefinition')
        else:
            url = urljoin(self.creds.url, f'ameyorestapi/cc/tableDefinitions/{tableDefinitionId}')

        response = self.rest.send_request(**{
            'method': 'GET', 'url': url,
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'tableDefinitionId', 'tableDefinitionName', 'columnDefinitionsMap', 'description', 'dateModified'
            ], _item)

        return response

    def create_table_definitions(self, **kwargs):
        """
        Create Table Definitions
        RPC Call: createTable
        :param kwargs:
        :return:
        """
        tableDefinitionName = kwargs.get('tableDefinitionName', None)
        columns = kwargs.get('columns', None)
        if not isinstance(columns, list):
            raise Exception(f"Parameter columns has to be list !!")
        description = kwargs.get('description', f"{tableDefinitionName} Description")
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([tableDefinitionName, columns, sessionId])

        columnDefinitionList = []
        for column in columns:
            columnDefinition = {
                "columnName": None, "columnType": 3, "defaultValue": "", "isMaskable": False, "encrypted": False,
                "nullable": False, "unique": False, "isMasked": False, "sequenceId": 0, "primaryKey": False,
                "isComposite": False, "maskingPolicyProperties": {}, "displayName": None,
            }
            columnDefinition.update(column)
            columnDefinitionList.append(columnDefinition)

        if len(list(filter(lambda a: a['columnName'] is None, columnDefinitionList))) > 0:
            raise Exception(f"columnName is mandatory in columnDefinition list !!")

        response = self.rest.send_request(**{
            'method': 'POST', 'url': urljoin(self.creds.url, f'ameyorestapi/cc/tableDefinitions'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'description': description, 'tableDefinitionName': tableDefinitionName,
                'columnDefinitionList': columnDefinitionList
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'tableDefinitionId', 'tableDefinitionName', 'columnDefinitionsMap', 'description', 'dateModified'
        ], response.json())

        for _item, _value in response.json()['columnDefinitionsMap'].items():
            self.is_key_there_in_dict([
                'columnType', 'nullable', 'columnId', 'unique', 'encrypted', 'tableDefinitionId', 'columnName',
                'defaultValue', 'sequenceId', 'primaryKey', 'isComposite', 'isMasked', 'isMaskable',
                'maskingPolicyType', 'maskingPolicyProperties', 'displayName'
            ], _value)
        return response

    def get_agent_table_definitions(self, **kwargs):
        """
        Get Agent Table Definitions
        RPC Call: getAllAgentTableDefinationForTableDefinationId
        :param kwargs:
        :return:
        """
        tableDefinitionId = kwargs.get('tableDefinitionId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([tableDefinitionId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'tableDefinitionId': tableDefinitionId},
            'url': urljoin(self.creds.url, f'ameyorestapi/cc/agentTableDefinitions/getAllAgentTableDefinitions'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'agentTableDefinitionId', 'agentTableDefinitionName', 'description', 'tableDefinitionId',
                'columnDefinitionIds', 'dateAdded', 'dateModified', 'agentColumnDefinitions'
            ], _item)
        return response

    def create_agent_table_definitions(self, **kwargs):
        """
        Create Agent Table Definitions
        RPC Call: addAgentTableDefinition
        :param kwargs:
        :return:
        """
        name = kwargs.get('name', None)
        tableDefinitionId = kwargs.get('tableDefinitionId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        columnDefinitionIds = kwargs.get('columnDefinitionIds', None)
        self.check_required_args([name, sessionId, columnDefinitionIds, tableDefinitionId])

        description = kwargs.get('description', f"{name} Description")
        if not isinstance(columnDefinitionIds, list):
            raise Exception(f"Parameter columnDefinitionIds has to be list !!")

        response = self.rest.send_request(**{
            'method': 'POST', 'url': urljoin(self.creds.url, f'ameyorestapi/customerManager/addAgentTableDefinition'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'name': name, 'description': description,
                'tableDefinitionId': tableDefinitionId,
                'columnDefinitionIds': columnDefinitionIds
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'tableDefinitionId', 'columnDefinitionIds', 'agentTableDefinitionName', 'customerAddable', 'processIds',
            'agentColumnDefinitions', 'agentTableDefinitionId'
        ], response.json())
        return response

    def get_all_campaign_types(self, **kwargs):
        """
        Get All Campaign Types
        RPC Call: getAllCampaignTypeConstants
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f'ameyorestapi/cc/getAllCampaignTypeConstants'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignTypeName', 'defaultCampaignCallbackHandler', 'tableFilterConstants', 'columnMappingAttributes'
            ], _item)
        return response

    def get_all_column_mappings(self, **kwargs):
        """
        Get All Column Mappings
        RPC Call: getColumnMappingsByTableDefinitionId
        :param kwargs:
        :return:
        """
        tableDefinitionId = kwargs.get('tableDefinitionId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([tableDefinitionId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'getAllColumnMappingsByTableDefinitionId': tableDefinitionId},
            'url': urljoin(self.creds.url, f'ameyorestapi/cc/columnMappings/getAllColumnMappings'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'columnMappingId', 'columnMappingName', 'columnMappingDefinitions', 'campaignType', 'tableDefinitionId',
                'campaignVersion', 'campaignContextIds'
            ], _item)
        return response

    def create_table_column_mapping(self, **kwargs):
        """
        Create Table Column Mapping
        :param kwargs:
        :return:
        """
        columnMappingName = kwargs.get('columnMappingName', None)
        campaignType = kwargs.get('campaignType', None)
        tableDefinitionId = kwargs.get('tableDefinitionId', None)
        campaignMappings = kwargs.get('campaignMappings', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([
            columnMappingName, campaignType, tableDefinitionId, campaignMappings, sessionId
        ])

        columnMappingDefinitions = [
            {'columnMappingAttributeName': 'name', 'tableColumnName': 'name', 'isUniqueIdentifier': False},
            {'columnMappingAttributeName': 'timezone', 'tableColumnName': 'timezone', 'isUniqueIdentifier': False},
            {'columnMappingAttributeName': 'phone1', 'tableColumnName': 'phone1', 'isUniqueIdentifier': False},
            {'columnMappingAttributeName': 'phone2', 'tableColumnName': 'phone2', 'isUniqueIdentifier': False},
            {'columnMappingAttributeName': 'phone3', 'tableColumnName': 'phone3', 'isUniqueIdentifier': False},
        ]

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f'ameyorestapi/cc/columnMappings'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'columnMappingName': columnMappingName,
                'columnMappingDefinitions': columnMappingDefinitions,
                'campaignType': campaignType,
                'tableDefinitionId': tableDefinitionId,
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'columnMappingId', 'columnMappingName', 'columnMappingDefinitions', 'campaignType',
            'tableDefinitionId', 'campaignVersion', 'campaignContextIds'
        ], response.json())
        return response

    def get_all_processes(self, **kwargs):
        """
        Get all Processes
        RPC Call: getAllProcesses
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/processes/getAllProcesses"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['processId', 'processName', 'description', 'processType'], _item)
        return response

    def create_process(self, **kwargs):
        """
        Create a Process
        :param kwargs:
        :return:
        """
        processName = kwargs.get('processName', None)
        description = kwargs.get('description', f'{processName} Description')
        processType = kwargs.get('processType', 'Default')
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processName, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/processes"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "processName": processName,
                "processType": processType,
                "description": description,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['processId', 'processName', 'description', 'processType'], response.json())
        return response

    def get_process_crm_settings(self, **kwargs):
        """
        Get Process CRM Settings
        :param kwargs:
        :return:
        """
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/hybrid/crmAdapterSettings/{processId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['processId', 'crmPropsUrl'], response.json())
        return response

    def update_process_crm_settings(self, **kwargs):
        """
        Update Given Process
        :param kwargs:
        :return:
        """
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processId, sessionId])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/hybrid/crmAdapterSettings/{processId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'crmPropsUrl': "",
                'propagateCustomerRemoval': True,
                'propagateLeadRemoval': True
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'crmPropsUrl', 'propagateCustomerRemoval', 'propagateLeadRemoval', 'processId'
        ], response.json())
        return response

    def initialize_process_td(self, **kwargs):
        """
        Initialize the process
        :param kwargs:
        :return:
        """
        processName = kwargs.get('processName', None)
        processId = kwargs.get('processId', None)
        tableDefinitionId = kwargs.get('tableDefinitionId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processName, processId, tableDefinitionId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/hybrid/initializeProcessDefaultData"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {
                "processName": processName,
                "processId": processId,
                "tableDefinitionId": tableDefinitionId,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def get_all_campaigns(self, **kwargs):
        """
        Get all Existing Campaigns
        RPC Call: getCampaignListForCC
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/campaigns/getAllCampaigns"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignId', 'campaignName', 'campaignType', 'description', 'processId', 'contactCenterId'
            ], _item)
        return response

    def get_all_campaign_users(self, **kwargs):
        """
        Assign a user to Campaign
        RPC Call: getAllCampaignUsers
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/campaignUsers/getByCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {'campaignId': campaignId, }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignUserId', 'campaignId', 'ccUserId', 'userId', 'defaultWorkingCampaign', 'primaryCampaign',
                'privilegePlanId', 'getMaskedPrivileges', 'processId', 'assigned', 'processUserId', 'user'
            ], _item)
        return response

    def assign_agent_to_campaign(self, **kwargs):
        """
        Assign a user to Campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        contactCenterUserIds = kwargs.get('contactCenterUserIds', None)
        privilegePlanIds = kwargs.get('privilegePlanIds', None)
        userIds = kwargs.get('userIds', None)
        contactCenterUserTypes = kwargs.get('contactCenterUserTypes', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([
            campaignId, privilegePlanIds, userIds, contactCenterUserIds, contactCenterUserTypes, sessionId
        ])

        if not isinstance(privilegePlanIds, list):
            privilegePlanIds = [privilegePlanIds]
        if not isinstance(userIds, list):
            userIds = [userIds]
        if not isinstance(contactCenterUserIds, list):
            contactCenterUserIds = [contactCenterUserIds]
        if not isinstance(contactCenterUserTypes, list):
            contactCenterUserTypes = [contactCenterUserTypes]

        # Find if there are any duplicate values !!
        duplicates = {x for x in userIds if userIds.count(x) > 1}
        if len(duplicates) > 0:
            raise Exception(f"userIds have following duplicates {duplicates}")
        duplicates = {x for x in contactCenterUserIds if contactCenterUserIds.count(x) > 1}
        if len(duplicates) > 0:
            raise Exception(f"contactCenterUserIds have following duplicates {duplicates}")

        # Verify privilegePlanIds, userIds, contactCenterUserIds and contactCenterUserTypes are of same length
        _len = max(len(privilegePlanIds), len(userIds), len(contactCenterUserIds), len(contactCenterUserTypes))
        if _len != len(privilegePlanIds):
            raise Exception(f"privilegePlanIds Count = {len(privilegePlanIds)} While Total = {_len}")
        if _len != len(userIds):
            raise Exception(f"userIds Count = {len(userIds)} While Total = {_len}")
        if _len != len(contactCenterUserIds):
            raise Exception(f"contactCenterUserIds Count = {len(contactCenterUserIds)} While Total = {_len}")
        if _len != len(contactCenterUserTypes):
            raise Exception(f"contactCenterUserTypes Count = {len(contactCenterUserTypes)} While Total = {_len}")

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/campaignUsers/assignUsersToCampaignContext"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'campaignContextId': campaignId,
                'privilegePlanIds': privilegePlanIds,
                'userIds': userIds,
                'contactCenterUserIds': contactCenterUserIds,
                'contactCenterUserType': contactCenterUserTypes,
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignUserId', 'campaignId', 'ccUserId', 'userId', 'defaultWorkingCampaign', 'primaryCampaign',
                'privilegePlanId', 'getMaskedPrivileges', 'processId', 'assigned', 'processUserId', 'user'
            ], _item)
        return response

    def delete_campaign(self, **kwargs):
        """
        Delete Given Campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'DELETE',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/hybrid/campaigns/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def create_campaign(self, **kwargs):
        """
        Create a Campaign
        RPC Call: createNewCampaignForProcess
        :param kwargs:
        :return:
        """
        campaignName = kwargs.get('campaignName', None)
        campaignType = kwargs.get('campaignType', None)
        description = kwargs.get('description', None)
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignName, campaignType, description, processId, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/hybrid/campaigns"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignName": campaignName,
                "campaignType": campaignType,
                "description": description,
                "processId": processId,
                # "isIdempotent": False  # Removed @pritam 5th Jan 7:30 PM
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignId', 'campaignName', 'campaignType', 'description', 'processId'
        ], response.json())
        return response

    def get_call_contexts_in_campaign(self, **kwargs):
        """
        Get call context(s) assigned to a Campaign
        RPC Call: getAllCampaignCallContextsByCampaignId
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignId': campaignId},
            'url': urljoin(
                self.creds.url, f"ameyorestapi/cc/campaignCallContexts/getAllCampaignCallContextsByCampaignId"
            ),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignCallContextId', 'maxOutboundCalls', 'maxInboundCalls', 'maxTotalActiveCalls',
                'processCallContextId', 'campaignId', 'callContextName', 'contactCenterCallContextId',
                'isEndpoint', 'callContextId'
            ], _item)
        return response

    def assign_call_context_to_campaign(self, **kwargs):
        """
        Assign Call Context to Campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        contactCenterCallContextId = kwargs.get('contactCenterCallContextId', None)
        contactCenterId = kwargs.get('contactCenterId', None)
        callContextId = kwargs.get('callContextId', None)
        maxOutboundCalls = kwargs.get('maxOutboundCalls', None)
        maxInboundCalls = kwargs.get('maxInboundCalls', None)
        maxTotalActiveCalls = kwargs.get('maxTotalActiveCalls', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([
            campaignId, contactCenterCallContextId, contactCenterId, callContextId, maxOutboundCalls, maxInboundCalls,
            maxTotalActiveCalls, sessionId
        ])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/assignCallContextsToCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignId": campaignId,
                "contactCenterCallContextBeans": [{
                    "id": contactCenterCallContextId,
                    "contactCenterId": contactCenterId,
                    "callContextId": callContextId,
                    "maxOutboundCalls": maxOutboundCalls,
                    "maxInboundCalls": maxInboundCalls,
                    "maxTotalActiveCalls": maxTotalActiveCalls,
                }],
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignId', 'id', 'processCallContextId', 'maxOutboundCalls', 'maxInboundCalls', 'maxTotalActiveCalls'
            ], _item)
        return response

    def get_all_leads_for_process(self, **kwargs):
        """
        Get all leads for a Given ProcessId
        :param kwargs:
        :return:
        """
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {"processId": processId},
            'url': urljoin(self.creds.url, "ameyorestapi/cc/getAllLeads"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'processId', 'leadName', 'enabled', 'description', 'timezone', 'userId', 'campaignContextIds', 'leadId'
            ], _item)
        return response

    def add_lead(self, **kwargs):
        """
        Add Lead in supervisor
        """
        processId = kwargs.get('processId', None)
        leadname = kwargs.get('leadName', None)
        ownerUserId = kwargs.get('ownerUserId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processId, leadname, ownerUserId, sessionId])

        enabled = kwargs.get('enabled', True)
        description = kwargs.get('description', f"{leadname} Description")
        timeZone = kwargs.get('timeZone', "")

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/customerManager/addLeadWithUser"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "leadName": leadname,
                "processId": processId,
                "enabled": enabled,
                "description": description,
                "timeZone": timeZone,
                "ownerUserId": ownerUserId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'leadName', 'processId', 'isEnabled', 'timeZone', 'ownerUserId', 'leadId'
        ], response.json())
        return response

    def assign_lead_to_campaign(self, **kwargs):
        """
        Assign Lead to Campaign
        """
        campaignContextId = kwargs.get('campaignContextId', None)
        leadIds = kwargs.get('leadIds', None)
        if not isinstance(leadIds, list):
            leadIds = [leadIds]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignContextId, leadIds, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/assignLeadsToCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignContextId": campaignContextId,
                "leadIds": leadIds
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def get_user_run_time(self, **kwargs):
        """
        Get all users Run Time Status (admin token)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/userCCRuntimes"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'isOnBreak', 'sessionId', 'isOnAuto', 'statusDescription', 'userId', 'terminalInfo', 'startTime',
                'readyBreakTime', 'autoChangeTime', 'thresholdParameterBreached', 'workingMode', 'thresholdBreach',
            ], _item)
        return response

    def user_logout(self, **kwargs):
        """
        User Log Out (Using user's own session ID)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', None)
        self.check_required_args([sessionId])
        reason = kwargs.get('reason', 'Logout from UI')

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, 'ameyorestapi/session/userLogout'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {"sessionId": sessionId, "reason": reason}
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def un_assign_agent_from_campaign(self, **kwargs):
        """
        Remove a user from Campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        campaignContextUserIds = kwargs.get('campaignContextUserIds', None)
        self.check_required_args([campaignId, sessionId, campaignContextUserIds])

        if not isinstance(campaignContextUserIds, list):
            campaignContextUserIds = [campaignContextUserIds]

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/campaignUsers/unassignUsersFromCampaignContext"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {'campaignContextId': campaignId, 'campaignContextUserIds': campaignContextUserIds}
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def delete_lead(self, **kwargs):
        """
        Delete Lead in supervisor
        """
        leadId = kwargs.get('leadId', None)
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        self.check_required_args([leadId, sessionId])

        response = self.rest.send_request(**{
            'method': 'DELETE',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/processLeads/{leadId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def get_all_leads_for_campaign(self, **kwargs):
        """
        Get lead data for a campaign
        """
        campaignId = kwargs.get('campaignId', None)
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        self.check_required_args([campaignId, processId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, "ameyorestapi/manageConfig/getAllContactLeadListData"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {
                'campaignId': campaignId,
                'processId': processId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def create_customer_csv(self, **kwargs):
        """
        Create Customer CSV
        """
        rows = list()
        count = kwargs.get('count', 100)
        for i in range(count):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            name = f"{first_name} {last_name}"
            email = f"{first_name}.{last_name}@ameyo.com"
            phone = self.faker.msisdn()[3:]
            rows.append([name, email, phone])

        name = Path(__file__).parent.parent / 'customers.csv'
        header = ['name', 'email', 'phone1']
        if not isinstance(rows, list):
            raise Exception(f"Rows Should be list !!")

        with open(name, 'w') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(header)  # Write header
            csvWriter.writerows(rows)  # write Rows

        return name

    def upload_csv_to_lead(self, **kwargs):
        """
        Uploads a csv(containing customer data) to the lead
        """
        processId = kwargs.get('processId', None)
        leadId = kwargs.get('leadIds', None)
        csvPath = kwargs.get('csvPath', None)
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        self.check_required_args([processId, leadId, csvPath, sessionId])

        update = kwargs.get("update", True)
        migrate = kwargs.get("migrate", False)
        churn = kwargs.get("churn", False)
        headerMapping = json.dumps(kwargs.get("headerMapping", {
            "twitter": "", "timezone": "", "facebook": "", "phone2": "", "name": "", "phone3": "",
            "phone4": "", "phone5": "", "email": "", "phone1": ""
        }))
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "upload/servlet.gupld"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'files': {'file': ('customers.csv', open(csvPath, 'rb'), "application/vnd.ms-excel")},
            'params': {
                'uploadType': 'contactsLead',
                "processId": processId,
                "update.customer": update,
                "migrate.customer": migrate,
                "churn.customer": churn,
                "leadId": leadId,
                "serverHostUrl": self.creds.url,
                "headerMapping": headerMapping,
            },
            "data": {"authorizationToken": sessionId},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def get_routing_policies_for_campaign(self, **kwargs):
        """
        Create Routing for Campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(
                self.creds.url, f"ameyorestapi/voice/basicCallContextDeterminationPolicies/"
                                f"getAllBasicCallContextDeterminationPolicyByCampaignId"
            ),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {'campaignId': campaignId}
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'policyId', 'campaignId', 'policyName', 'policyType', 'campaignCallContextIds', 'dateAdded',
                'dateModified'
            ], _item)
        return response

    def create_routing_policy_for_campaign(self, **kwargs):
        """
        Create Routing for Campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        campaignCallContextIds = kwargs.get('campaignCallContextIds', None)
        if not isinstance(campaignCallContextIds, list):
            campaignCallContextIds = [campaignCallContextIds]
        policyName = kwargs.get('policyName', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        policyType = kwargs.get('policyType', 'basic.single.call.context.type')
        self.check_required_args([campaignId, campaignCallContextIds, policyName, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/basicCallContextDeterminationPolicies"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignId": campaignId, "policyType": policyType, "policyName": policyName,
                "campaignCallContextIds": campaignCallContextIds
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'policyId', 'campaignId', 'policyName', 'policyType', 'campaignCallContextIds', 'dateAdded',
            'dateModified'
        ], response.json())
        return response

    def delete_routing_policy(self, **kwargs):
        """
        Delete Routing Policy
        :param kwargs:
        :return:
        """
        policyId = kwargs.get('policyId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([policyId, sessionId])

        response = self.rest.send_request(**{
            'method': 'DELETE',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/basicCallContextDeterminationPolicies/{policyId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        return response


    def update_manual_dial_profile(self, **kwargs):
        """
        Update Manual Dial Profile
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        policyId = kwargs.get('policyId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, policyId, sessionId])

        setUpTimeout = kwargs.get('setUpTimeout', 60)
        ringTimeout = kwargs.get('ringTimeout', 45)
        useMinutesProfiler = kwargs.get('useMinutesProfiler', False)

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/manualDialProfiles/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "policyId": policyId,
                "setUpTimeout": setUpTimeout,
                "ringTimeout": ringTimeout,
                "useMinutesProfiler": useMinutesProfiler
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'policyId', 'useMinutesProfiler', 'setUpTimeout', 'ringTimeout'
        ], response.json())
        return response


    def get_conference_dial_profile(self, **kwargs):
        """
        Get Conference Dial Profile
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/conferenceDialProfiles/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'policyId', 'campaignId', 'useMinutesProfiler', 'setUpTimeout', 'ringTimeout'
        ], response.json())
        return response


    def update_conference_dial_profile(self, **kwargs):
        """
        Update Conference Dial Profile
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        policyId = kwargs.get('policyId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, policyId, sessionId])

        setUpTimeout = kwargs.get('setUpTimeout', 60)
        ringTimeout = kwargs.get('ringTimeout', 45)
        useMinutesProfiler = kwargs.get('useMinutesProfiler', False)

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/conferenceDialProfiles/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "policyId": policyId,
                "setUpTimeout": setUpTimeout,
                "ringTimeout": ringTimeout,
                "useMinutesProfiler": useMinutesProfiler
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'policyId', 'campaignId', 'useMinutesProfiler', 'setUpTimeout', 'ringTimeout'
        ], response.json())
        return response


    def get_auto_dial_profile(self, **kwargs):
        """
        Get Auto Dial Profile
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/autoDialProfiles/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'policyId', 'campaignId', 'useMinutesProfiler', 'setUpTimeout', 'ringTimeout'
        ], response.json())
        return response

    def update_auto_dial_profile(self, **kwargs):
        """
        Update Auto Dial Profile
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        policyId = kwargs.get('policyId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, policyId, sessionId])

        setUpTimeout = kwargs.get('setUpTimeout', 60)
        ringTimeout = kwargs.get('ringTimeout', 45)
        useMinutesProfiler = kwargs.get('useMinutesProfiler', False)

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/autoDialProfiles/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "policyId": policyId,
                "setUpTimeout": setUpTimeout,
                "ringTimeout": ringTimeout,
                "useMinutesProfiler": useMinutesProfiler
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'policyId', 'setUpTimeout', 'useMinutesProfiler', 'ringTimeout'
        ], response.json())
        return response

    def update_default_atd_for_campaign(self, **kwargs):
        """
        Get all data tables for a process
        RPC Call: updateDefaultATDForCampiagn
        """
        atdId = kwargs.get('atdId', None)
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([atdId, campaignId, sessionId])

        shouldAssignUserInAtd = kwargs.get('shouldAssignUserInAtd', False)
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/customerManager/updateDefaultAtdForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "atdId": atdId,
                "campaignId": campaignId,
                "shouldAssignUserInAtd": shouldAssignUserInAtd
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignId', 'default_atd_id', 'shouldAssignUsersInDefaultATD', 'id'
        ], response.json())
        return response

    def set_column_mapping_for_campaign(self, **kwargs):
        """
        Set Column Mapping for Campaign
        RPC Call: setColumnMappingForCampaign
        """
        columnMappingId = kwargs.get('columnMappingId', None)
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([columnMappingId, campaignId, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/setColumnMappingForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "columnMappingId": columnMappingId,
                "campaignId": campaignId,
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def get_disposition_classes(self, **kwargs):
        """
        Get all Disposition Classes
        RPC Call: getAllDispositionClasses (OK)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = None
        for i in range(5):
            try:
                self.logger.info(f"iteration: {i}")
                response = self.rest.send_request(**{
                    'method': 'GET',
                    'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionClasses/getAllDispositionClasses"),
                    'headers': {"sessionId": sessionId, "correlation": self.uuid},
                })
                self.logger.info(f"response code: {response.status_code}")
                if response.status_code == 200:
                    break
            except:
                self.logger.info(f"I am in except for iteration {i} of getAllDispositionClasses")
                self.logger.info(f"Potential bug in getAllDispositionClasses")
                time.sleep(5)
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionClassId', 'dispositionClassName', 'dispositionCodes'], _item)
        return response

    def get_disposition_classes_for_campaign(self, **kwargs):
        """
        Get all Disposition Classes
        RPC Call: getAllDispositionClasses (OK)
        :param kwargs:
        :return:
        """
        campaignContextId = kwargs.get('campaignContextId', None)
        sessionId = kwargs.get('sessionId', self.executiveToken)
        self.check_required_args([campaignContextId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignContextId': campaignContextId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionClasses/getDispositionClassesForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionClassId', 'dispositionClassName', 'dispositionCodes'], _item)
        return response

    def get_disposition_plans(self, **kwargs):
        """
        Get all Disposition Plans
        RPC Call: getAllDispositionPlans, getAllDispositionPlanDetails (OK)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionPlans"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionPlanName', 'dispositionCodeIds', 'dispositionPlanId'], _item)
        return response

    def get_disposition_plans_for_campaign(self, **kwargs):
        """
        Get all Disposition Plans for Campaign
        RPC Call: getAllDispositionPlans, getDispositionPlanForCampaign (OK)
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignId': campaignId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionPlans/getDispositionPlanForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['dispositionPlanName', 'dispositionCodeIds', 'dispositionPlanId'], response.json())
        return response

    def create_disposition_code(self, **kwargs):
        """
        Create Disposition Code
        RPC Call: createDispositionCode (OK)
        :param kwargs:
        :return:
        """
        dispositionCodeName = kwargs.get('dispositionCodeName', None)
        dispositionClassId = kwargs.get('dispositionClassId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionCodeName, dispositionClassId, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionCodes"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionCodeName": dispositionCodeName,
                "dispositionClassId": dispositionClassId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['dispositionCodeId', 'dispositionCodeName', 'dispositionClassId'], response.json())
        return response

    def create_disposition_class(self, **kwargs):
        """
        Create Disposition Classes
        RPC Call: createDispositionClass (OK)
        :param kwargs:
        :return:
        """
        dispositionClassName = kwargs.get('dispositionClassName', None)
        dispositionCodes = kwargs.get('dispositionCodes', None)
        if not isinstance(dispositionCodes, list):
            dispositionCodes = [dispositionCodes]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionClassName, dispositionCodes, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionClasses"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionClassName": dispositionClassName,
                "dispositionCodes": dispositionCodes
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'dispositionClassName', 'dispositionCodes'
        ], response.json())
        return response

    def update_disposition_class(self, **kwargs):
        """
        Update Disposition Classes
        RPC Call: createDispositionClass (OK)
        :param kwargs:
        :return:
        """
        dispositionClassName = kwargs.get('dispositionClassName', None)
        dispositionCodes = kwargs.get('dispositionCodes', None)
        dispositionClassId = kwargs.get('dispositionClassId', None)
        if not isinstance(dispositionCodes, list):
            dispositionCodes = [dispositionCodes]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionClassName, dispositionCodes, sessionId])

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionClasses"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionClassName": dispositionClassName,
                "dispositionCodes": dispositionCodes,
                'dispositionClassId': dispositionClassId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'dispositionClassName', 'dispositionCodes'
        ], response.json())
        return response

    def get_disposition_classes(self, **kwargs):
        """
        Get all Disposition Classes
        RPC Call: getAllDispositionClasses (OK)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = None
        for i in range(5):
            try:
                self.logger.info(f"iteration: {i}")
                response = self.rest.send_request(**{
                    'method': 'GET',
                    'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionClasses/getAllDispositionClasses"),
                    'headers': {"sessionId": sessionId, "correlation": self.uuid},
                })
                self.logger.info(f"response code: {response.status_code}")
                if response.status_code == 200:
                    break
            except:
                self.logger.info(f"I am in except for iteration {i} of getAllDispositionClasses")
                self.logger.info(f"Potential bug in getAllDispositionClasses")
                time.sleep(5)
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionClassId', 'dispositionClassName', 'dispositionCodes'], _item)
        return response

    def get_disposition_classes_for_campaign(self, **kwargs):
        """
        Get all Disposition Classes
        RPC Call: getAllDispositionClasses (OK)
        :param kwargs:
        :return:
        """
        campaignContextId = kwargs.get('campaignContextId', None)
        sessionId = kwargs.get('sessionId', self.executiveToken)
        self.check_required_args([campaignContextId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignContextId': campaignContextId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionClasses/getDispositionClassesForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionClassId', 'dispositionClassName', 'dispositionCodes'], _item)
        return response

    def get_disposition_plans(self, **kwargs):
        """
        Get all Disposition Plans
        RPC Call: getAllDispositionPlans, getAllDispositionPlanDetails (OK)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionPlans"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionPlanName', 'dispositionCodeIds', 'dispositionPlanId'], _item)
        return response

    def get_disposition_plans_for_campaign(self, **kwargs):
        """
        Get all Disposition Plans for Campaign
        RPC Call: getAllDispositionPlans, getDispositionPlanForCampaign (OK)
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignId': campaignId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionPlans/getDispositionPlanForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['dispositionPlanName', 'dispositionCodeIds', 'dispositionPlanId'], response.json())
        return response

    def create_disposition_code(self, **kwargs):
        """
        Create Disposition Code
        RPC Call: createDispositionCode (OK)
        :param kwargs:
        :return:
        """
        dispositionCodeName = kwargs.get('dispositionCodeName', None)
        dispositionClassId = kwargs.get('dispositionClassId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionCodeName, dispositionClassId, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionCodes"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionCodeName": dispositionCodeName,
                "dispositionClassId": dispositionClassId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['dispositionCodeId', 'dispositionCodeName', 'dispositionClassId'], response.json())
        return response

    def create_disposition_class(self, **kwargs):
        """
        Create Disposition Classes
        RPC Call: createDispositionClass (OK)
        :param kwargs:
        :return:
        """
        dispositionClassName = kwargs.get('dispositionClassName', None)
        dispositionCodes = kwargs.get('dispositionCodes', None)
        if not isinstance(dispositionCodes, list):
            dispositionCodes = [dispositionCodes]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionClassName, dispositionCodes, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionClasses"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionClassName": dispositionClassName,
                "dispositionCodes": dispositionCodes
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'dispositionClassName', 'dispositionCodes'
        ], response.json())
        return response

    def update_disposition_class(self, **kwargs):
        """
        Update Disposition Classes
        RPC Call: createDispositionClass (OK)
        :param kwargs:
        :return:
        """
        dispositionClassName = kwargs.get('dispositionClassName', None)
        dispositionCodes = kwargs.get('dispositionCodes', None)
        dispositionClassId = kwargs.get('dispositionClassId', None)
        if not isinstance(dispositionCodes, list):
            dispositionCodes = [dispositionCodes]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionClassName, dispositionCodes, sessionId])

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionClasses"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionClassName": dispositionClassName,
                "dispositionCodes": dispositionCodes,
                'dispositionClassId': dispositionClassId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'dispositionClassName', 'dispositionCodes'
        ], response.json())
        return response

    def get_disposition_codes_for_campaign(self, **kwargs):
        """
        Get Disposition Codes for a given Campaign
        RPC Call: TODO
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        self.check_required_args([campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {"campaignId": campaignId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionCodes/getByCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid}
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionCodeId', 'dispositionCodeName', 'dispositionClassId'], _item)
        return response

    def get_disposition_codes(self, **kwargs):
        """
        Get all Disposition Codes
        RPC Call: getAllDispositionCodes (OK)
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/dispositionCodes/getAllDispositionCodes"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['dispositionCodeId', 'dispositionCodeName', 'dispositionClassId'], _item)
        return response

    def create_disposition_plan(self, **kwargs):
        """
        Create Disposition Classes
        RPC Call: createDispositionPlan (OK)
        :param kwargs:
        :return:
        """
        dispositionPlanName = kwargs.get('dispositionPlanName', None)
        dispositionCodeIds = kwargs.get('dispositionCodeIds', None)
        if not isinstance(dispositionCodeIds, list):
            dispositionCodeIds = [dispositionCodeIds]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionPlanName, dispositionCodeIds, sessionId])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dispositionPlans"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionPlanName": dispositionPlanName,
                "dispositionCodeIds": dispositionCodeIds
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'dispositionPlanName', 'dispositionCodeIds'
        ], response.json())
        return response

    def assign_disposition_plan_to_campaign(self, **kwargs):
        """
        Assign Disposition plan to Campaign
        RPC Call: setDispositionPlanForCampaign (OK)
        :param kwargs:
        :return:
        """
        dispositionPlanId = kwargs.get('dispositionPlanId', None)
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([dispositionPlanId, campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/setDispositionPlanForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "dispositionPlanId": dispositionPlanId,
                "campaignId": campaignId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['dispositionPlanId', 'campaignId'], response.json())
        return response

    def assign_user_to_atd(self, **kwargs):
        """
        Assign User to Agent Table Definition
        RPC Call: assignUsersToAgentTableDefinition
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        atdId = kwargs.get('atdId', None)
        userIds = kwargs.get('userIds', None)
        if not isinstance(userIds, list):
            userIds = [userIds]
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, atdId, userIds, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f'ameyorestapi/customerManager/assignUserToATD'),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignId": campaignId,
                "atdId": atdId,
                "userIds": userIds
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignId', 'agentTableDefinitionId', 'campaignContextUserATDId', 'campaignContextUserId',
                'responseType', 'userId',
            ], _item)
        return response

    def get_data_table_for_process(self, **kwargs):
        """
        Get all data tables for a process
        RPC Call: getDataTableForProcess
        """
        processId = kwargs.get('processId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([processId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'processId': processId},
            'url': urljoin(self.creds.url, "ameyorestapi/cc/dataTables/getDataTableForProcess"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['dataTableName', 'dataTableId', 'tableDefinitionId', 'campaignId'], response.json())
        return response

    def update_default_atd_for_campaign(self, **kwargs):
        """
        Get all data tables for a process
        RPC Call: updateDefaultATDForCampiagn
        """
        atdId = kwargs.get('atdId', None)
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([atdId, campaignId, sessionId])

        shouldAssignUserInAtd = kwargs.get('shouldAssignUserInAtd', False)
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/customerManager/updateDefaultAtdForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "atdId": atdId,
                "campaignId": campaignId,
                "shouldAssignUserInAtd": shouldAssignUserInAtd
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignId', 'default_atd_id', 'shouldAssignUsersInDefaultATD', 'id'
        ], response.json())
        return response

    def get_all_queue(self, **kwargs):
        """
        Get all Campaign queue
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        info = kwargs.get('info', False)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, info, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/agentQueues/getByCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {
                "campaignId": campaignId,
                "info": info
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict(['queueName', 'description', 'queueType'], _item)
        return response

    def create_queue(self, **kwargs):
        """
        Create Queue for campaign
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        queueName = kwargs.get('queueName', None)
        description = kwargs.get('description', None)
        userIdList = kwargs.get('userIdList', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignId, sessionId, queueName, userIdList])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/agentQueues"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "queueName": queueName,
                "campaignId": campaignId,
                "queueType": "resource.request.queue.fifo.type",
                "resourceSchedulerType": "resource.scheduler.lru.type",
                "queuePriority": 1,
                "transferrable": True,
                "description": description,
                "userIdList": userIdList
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.is_key_there_in_dict([
            'agentQueueId', 'campaignId', 'queueName', 'queueType', 'resourceSchedulerType', 'queuePriority',
            'description', 'transferrable', 'skillIds', 'userIdList', 'dateAdded', 'dateModified', 'moreInfo'
        ], response.json())
        return response

    def get_users_in_queue(self, **kwargs):
        """
        Get Users in Queue
        :param kwargs:
        :return:
        """
        agentQueueId = kwargs.get('agentQueueId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([agentQueueId, sessionId])

        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/agentQueueUsers/getByAgentQueue"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'params': {
                "agentQueueId": agentQueueId,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        for _item in response.json():
            self.is_key_there_in_dict([
                'agentQueueUserId', 'agentQueueId', 'campaignUserId', 'campaignId', 'userId', 'assigned',
                'privilegePlanId', 'user'
            ], _item)
        return response

    def un_assign_agent_from_queue(self, **kwargs):
        """
        Un-assign agent from Queue
        :param kwargs:
        :return:
        """
        agentQueueId = kwargs.get('agentQueueId', None)
        agentQueueUserIds = kwargs.get('agentQueueUserIds', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([agentQueueId, sessionId, agentQueueUserIds])

        if not isinstance(agentQueueUserIds, list):
            agentQueueUserIds = [agentQueueUserIds]

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/agentQueueUsers/unassignUsersFromAgentQueue"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "agentQueueId": agentQueueId,
                "agentQueueUserIds": agentQueueUserIds,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        return response

    def update_queue_data(self, **kwargs):
        """
        Update the queue description
        """
        queueId = kwargs.get('queueId', None)
        queueName = kwargs.get('queueName', None)
        description = kwargs.get('description', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId, queueName, description, queueId])

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/agentQueues/{queueId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "queueName": queueName,
                "queueType": "resource.request.queue.fifo.type",
                "resourceSchedulerType": "resource.scheduler.lru.type",
                "queuePriority": 1,
                "transferrable": True,
                "description": description,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.is_key_there_in_dict([
            'agentQueueId', 'campaignId', 'queueName', 'queueType', 'resourceSchedulerType', 'queuePriority',
            'description', 'transferrable', 'skillIds', 'userIdList', 'dateAdded', 'dateModified', 'moreInfo'
        ], response.json())
        return response

    def assign_agent_to_queue(self, **kwargs):
        """
        Again assign agent to queue
        :param kwargs:
        :return:
        """
        agentQueueId = kwargs.get('agentQueueId', None)
        campaignContextUserIds = kwargs.get('campaignContextUserIds', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([agentQueueId, campaignContextUserIds, sessionId])

        if not isinstance(campaignContextUserIds, list):
            campaignContextUserIds = [campaignContextUserIds]

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/agentQueueUsers/assignUsersToAgentQueue"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "agentQueueId": agentQueueId,
                "campaignContextUserIds": campaignContextUserIds,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        for _item in response.json():
            self.is_key_there_in_dict([
                'agentQueueUserId', 'agentQueueId', 'campaignUserId', 'campaignId', 'userId', 'assigned',
                'privilegePlanId', 'user'
            ], _item)
        return response
    
    def enable_lead_for_process(self, **kwargs):
        """
        Enables/Disables Lead for a process
        """
        leadId = kwargs.get('leadId', None)
        enabled = kwargs.get('enabled', None)
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        self.check_required_args([enabled, leadId, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/enableDisableLead"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                'enabled': enabled,
                'leadId': leadId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def enable_lead_for_campaign(self, **kwargs):
        """
        Enables Lead for a Campaign
        """
        leadName = kwargs.get('leadName', None)
        campaignLeadId = kwargs.get('campaignLeadId', None)
        campaignId = kwargs.get('campaignId', None)
        leadId = kwargs.get('leadId', None)
        leadDialingConfigurationEnabled = kwargs.get('leadDialingConfigurationEnabled', None)

        sessionId = kwargs.get('sessionId', self.supervisorToken)
        self.check_required_args([leadName, campaignLeadId, campaignId, leadId, leadDialingConfigurationEnabled])
        payload = {
            "leadBeanWrapper": {
                "campaignLeadDetails": [
                    {
                        "leadName": leadName,
                        "campaignLeadId": campaignLeadId,
                        "campaignId": campaignId,
                        "timeZone": "",
                        "leadDialingConfigurationEnabled": leadDialingConfigurationEnabled,
                        "priority": 1,
                        "weightage": 1,
                        "maxAttempt": 10,
                        "tagName": None,
                        "leadDialingEnabledAtAllTime": True,
                        "enabled": False,
                        "leadId": leadId
                    }
                ]
            },
            "leadNameVsleadIdMap": {
                leadName: leadId,
            },
            "campaignLeadIdVsAssignedQueueId": {
                campaignLeadId: None,
            },
            "campaignLeadIdVsUnassignedQueueId": {
                campaignLeadId: None,
            },
            "leadIdVsUserMappingName": {
                leadId: ""
            }
        }

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/voice/setUpdatedCampaignLeadDetails"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': payload,
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def update_campaign_data(self, **kwargs):
        """
        Update Data for a Campaign
        RPC Call: updateCampaignData
        :param kwargs:
        :return:
        """
        campaignName = kwargs.get('campaignName', None)
        campaignId = kwargs.get('campaignId', None)
        description = kwargs.get('description', f'{campaignName} Description')
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([campaignName, campaignId, description, sessionId])

        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/campaigns/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignName": campaignName,
                "description": description,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignName', 'campaignId', 'description'], response.json())
        return response

    def create_tpv_info(self, **kwargs):
        """
        Create TPV info
        :param kwargs:
        :return:
        """
        thirdPartyName = kwargs.get('thirdPartyName', None)
        thirdPartyPhone = kwargs.get('thirdPartyPhone', None)
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)

        self.check_required_args([thirdPartyName, thirdPartyPhone, sessionId, campaignId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/voice/tpvInfos"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "thirdPartyName": thirdPartyName, "thirdPartyPhone": thirdPartyPhone, "campaignId": campaignId
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['tpvInfoId', 'campaignId', 'thirdPartyName', 'thirdPartyPhone'], response.json())
        return response

    def create_local_IVR(self, **kwargs):
        """
        Create local IVR
        :param kwargs:
        :return:
        """
        name = kwargs.get('name', None)
        contactCenterCallContextId = kwargs.get('contactCenterCallContextId', None)
        isOverrideDstPhone = kwargs.get('isOverrideDstPhone', False)
        dstPhone = kwargs.get('dstPhone', None)
        isOverrideSrcPhone = kwargs.get('isOverrideSrcPhone', False)
        srcPhone = kwargs.get('srcPhone', None)
        desc = kwargs.get('desc', None)
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)

        self.check_required_args([name, contactCenterCallContextId, dstPhone, srcPhone, desc, campaignId, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/cc/localIVRs"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "name": name, "contactCenterCallContextId": contactCenterCallContextId, "campaignId": campaignId,
                "isOverrideDstPhone": isOverrideDstPhone, "dstPhone": dstPhone, "isOverrideSrcPhone": isOverrideSrcPhone,
                "srcPhone": srcPhone, "desc": desc
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['id', 'campaignId', 'name', 'contactCenterCallContextId',
                                   'isOverrideDstPhone', 'dstPhone', 'isOverrideSrcPhone',
                                   'srcPhone'], response.json())
        return response

    def get_all_local_IVR_for_campaign(self, **kwargs):
        """
        get_all_local_IVR_for_campaign
        :param kwargs:
        RPC: getAllLocalIVRForCampaign
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignId': campaignId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/getAllLocalIVRForCampaign"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        for _item in response.json():
            self.is_key_there_in_dict([
                'campaignId', 'id', 'name', 'contactCenterCallContextId', 'isOverrideDstPhone',
                'dstPhone', 'isOverrideSrcPhone', 'srcPhone', 'desc'
            ], _item)
        return response

    def create_customer_data_to_upload(self, **kwargs):
        """
        Create Customer data to upload
        Uploading callback data is pending
        """
        upload_callback_record = kwargs.get("upload_callback_record", False)
        data = {}
        customer_records = list()
        count = kwargs.get('count', 10)
        for i in range(count):
            customer_record = dict()
            customer_record["customerRecord"] = dict()
            customer_record["customerRecord"]["phone1"] = self.faker.msisdn()[3:]
            customer_records.append(customer_record)

        if upload_callback_record:
            callback_data = dict()
            callback_data["userId"] = "Agent_1"
            callback_data["isSelfCallBack"] = True
            callback_data["callBackPhone"] = "9654158622"
            callback_data["callBackTime"] = "2022-01-27 18:30:00 PM"
            callback_data["callBackPhone"] = "1292468"
            callback_records = dict()
            callback_records["callbackRecord"] = callback_data
            customer_records.append(callback_records)

        data["campaignId"] = None
        data["customerAndCallbackRecords"] = customer_records
        data["leadId"] = None
        data["properties"] = {"update.customer": True, "migrate.customer": True}

        return data

    def upload_contacts(self, **kwargs):
        """
        Upload the contact to the system i.e. campaign
        :param kwargs:
        :return:
        """
        data = kwargs.get("data")
        hashkey = kwargs.get("hashkey", self.webaccess_api_token)
        self.check_required_args([data, hashkey])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyowebaccess/command"),
            'headers': {
                "requesting-host": "localhost", "policy-name": "token-based-authorization-policy",
                "hash-key": hashkey, "content-type": "application/x-www-form-urlencoded"},
            'params': {'command': "uploadContactAndAddCallback"},
            'data': f'data={urllib.parse.quote(json.dumps(data))}',
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        return response

    def set_preview_algo_setting(self, **kwargs):
        """
        Get all preview algo settings
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        leadUserDialing = kwargs.get('leadUserDialing', False)
        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/previewAlgoSettings/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "peakCallCount": 20,
                "leadUserDialing": leadUserDialing
            },
        })
        self.rest.raise_for_status(response)
        return response

    def set_predictive_algo_setting(self, **kwargs):
        """
        Get all predictive algo settings
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        agentWaitTime = kwargs.get('agentWaitTime', 5)
        callDropRatio = kwargs.get('callDropRatio', 5)
        maxPacingRatio = kwargs.get('maxPacingRatio', 2)
        peakCallCount = kwargs.get('peakCallCount', 20)
        varianceFactor = kwargs.get('varianceFactor', 100)

        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/predictiveAlgoSettings/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "agentWaitTime": agentWaitTime,
                "callDropRatio": callDropRatio,
                "maxPacingRatio": maxPacingRatio,
                "peakCallCount": peakCallCount,
                "varianceFactor": varianceFactor,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'agentWaitTime', 'callDropRatio', 'maxPacingRatio', 'peakCallCount', 'varianceFactor'
        ], response.json())
        return response

    def set_progressive_algo_setting(self, **kwargs):
        """
        Get all progressive algo settings
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        peakCallCount = kwargs.get('peakCallCount', 20)

        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/progressiveAlgoSettings/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "peakCallCount": peakCallCount,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignId', 'peakCallCount'], response.json())
        return response

    def enable_auto_dial(self, **kwargs):
        """
        Enable auto dial -> sup token
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/startDialer"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignId": campaignId,
            },

        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        if response.status_code == 512:
            if response.json()["message"].startswith('["OutboundVoiceCampaign.dial.in.progress"'):
                self.logger.info("Auto dial already enabled")
                self.is_auto_dial_enabled = True
                return True

        self.rest.raise_for_status(response)
        self.is_auto_dial_enabled = True
        return response

    def disable_auto_dial(self, **kwargs):
        """
        Disable auto dial -> sup token
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/stopDialer"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignId": campaignId,
            },

        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        if response.status_code == 512:
            if response.json()["message"].startswith('["OutboundVoiceCampaign.dialing.not.in.progress"'):
                self.logger.info("Auto dial already disabled")
                self.is_auto_dial_enabled = False
                return True

        self.rest.raise_for_status(response)
        self.logger.info("Auto dial disabled")
        self.is_auto_dial_enabled = False
        return response

    def set_outbound_voice_campaign_setting(self, **kwargs):
        """

        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        dialerAlgoType = kwargs.get('dialerAlgoType', None)
        self.check_required_args([sessionId, campaignId, dialerAlgoType])
        payload = {
            "dialerAlgoType": dialerAlgoType,
            "acwConnected": 30,
            "acwConnectedEnabled": False,
            "acwNotConnected": 30,
            "amdType": "DEFAULT",
            "autoAnswer": True,
            "beepDuration": 5,
            "beepEnabled": False,
            "callerId": "NODID",
            "crmURL": "",
            "customerProviderType": "campaign.based.customer.provider",
            "dialOnTimeOut": 30,
            "dialOnTimeOutEnabled": True,
            "dialPhoneEnabled": True,
            # "dialerAlgoType": "Predictive",
            "dispositionURL": "",
            "inheritAutoAnswerFromParent": False,
            "isAMDEnabled": False,
            "maxCallbackCount": 10,
            "numOfLastCallsToMonitor": 200,
            "peakCallCount": 100,
            "previewURL": "",
            "recordingFileFormat": "tg729",
            "screenLogsEnabled": True,
            "timeZoneMapper": "lead.based.campaign.timezone.mapper",
            "voiceLogsEnabled": True,
            "wrapTimeOut": 300
        }
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/outboundVoiceCampaignSettings/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid,
                        'content-type': "application/json;charset=UTF-8"},
            'json': payload,
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'dialerAlgoType', 'customerProviderType', 'timeZoneMapper', 'peakCallCount', 'isAMDEnabled'
        ], response.json())
        return response

    def get_outbound_voice_campaign_setting(self, **kwargs):
        """
        Get all outbound campaign setting
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.supervisorToken)
        campaignId = kwargs.get('campaignId', None)
        self.check_required_args([sessionId, campaignId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/outboundVoiceCampaignSettings/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response


    def get_crm_adapter_setting(self, **kwargs):
        """
        Get CRM adapter Settings for a Campaign
        RPC Call: getCRMAdapterSetting
        :return:
        """
        campaignId = kwargs.get('campaignId', None)
        sessionId = kwargs.get('sessionId', self.executiveToken)
        self.check_required_args([campaignId, sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'params': {'campaignId': campaignId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/crmAdapterSettings/{campaignId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignName', 'campaignId'], response.json())
        return response

    def update_campaign_advanced_settings(self, **kwargs):
        """
        Update Campaign Advanced Settings
        RPC Call: updateOutboundCampaignAdvancedSettings
        :param kwargs:
        :return:
        """
        campaignId = kwargs.get('campaignId ', None)
        numLastCalls = kwargs.get('numLastCalls', None)
        recordingFileFormat = kwargs.get('recordingFileFormat', "")
        customerProviderType = kwargs.get('customerProviderType', "")
        disposeFromCRMOnlyEnabled = kwargs.get('disposeFromCRMOnlyEnabled', True)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([
            campaignId, numLastCalls, recordingFileFormat, customerProviderType, disposeFromCRMOnlyEnabled, sessionId
        ])
        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, f"ameyorestapi/voice/outboundVoiceCampaignSettings/"
                                           f"updateOutboundCampaignAdvancedSettings"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "campaignId": campaignId,
                "numLastCalls": numLastCalls,
                "recordingFileFormat": recordingFileFormat,
                "customerProviderType": customerProviderType,
                "disposeFromCRMOnlyEnabled": disposeFromCRMOnlyEnabled
            }
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'campaignId', 'numLastCalls', 'disposeFromCRMOnlyEnabled', 'customerProviderType'], response.json())
        return response

    def update_user_role(self, **kwargs):
        """
        Changes a user role i.e. from Administrator to Executive and so on
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        ccUserId = kwargs.get('ccUserId', None)
        userId = kwargs.get('userId', None)
        role_to_assign = kwargs.get('role_to_assign', None)
        self.check_required_args([sessionId, userId, ccUserId])
        response = self.rest.send_request(**{
            'method': 'PUT',
            'url': urljoin(self.creds.url,
                           f"ameyorestapi/cc/contactCenterUsers/{ccUserId}"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "userId": userId,
                "userType": role_to_assign,
                "userName": userId,
                "systemUserType": role_to_assign,
                "defaultReady": False
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)

    def get_all_cc_user_groups_of_cc(self, **kwargs):
        """
        getAllContactCenterUserGroupsOfContactCenter
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/usergroup/getAllContactCenterUserGroupsOfContactCenter"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response


    def is_grouphierarchylicense_enabled(self, **kwargs):
        """
        isGroupHierarchyLicenseEnabled
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/group/isGroupHierarchyLicenseEnabled"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def delete_cc_user_groups(self, **kwargs):
        """
        Delete cc user groups
        :param kwargs:
        :return:
        """
        userGroupId = kwargs.get('userGroupId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([userGroupId, sessionId])
        response = self.rest.send_request(**{
            'method': 'DELETE',
            'params': {'userGroupId': userGroupId},
            'url': urljoin(self.creds.url, f"ameyorestapi/cc/usergroup/contactCenterUserGroups"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def validate_and_create_group(self, **kwargs):
        """
        Create a Process
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        ccManagerUserIds = kwargs.get('ccManagerUserIds', None)
        name = kwargs.get('name', None)
        description = kwargs.get('description', None)
        ccUserIds = kwargs.get('ccUserIds', None)
        # childGroupIds = kwargs.get('childGroupIds', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([userId, ccManagerUserIds, name, description, sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/group/validateAndCreateGroup"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
                "userId": userId,
                "ccManagerUserIds": [ccManagerUserIds],
                "name": name,
                "ccUserIds": ccUserIds,
                "childGroupIds": [],
                "description": description,
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict(['groupErrorReason', 'managerAssignmentInGroupResponse',
                                   'userAssignmentInGroupResponse'], response.json())
        return response

    def get_all_available_groups(self, **kwargs):
        """
        getAllAvailableGroups
        :param kwargs:
        :return:
        """
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([sessionId])
        response = self.rest.send_request(**{
            'method': 'GET',
            'url': urljoin(self.creds.url, f"ameyorestapi/group/getAllAvailableGroups"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def delete_cc_user_group(self, **kwargs):
        """
        Delete a User from CC
        :param kwargs:
        :return:
        """
        id = kwargs.get('id', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        self.check_required_args([id, sessionId])
        response = self.rest.send_request(**{
            'method': 'DELETE',
            'params': {'id': id},
            'url': urljoin(self.creds.url, f"ameyorestapi/group/deleteContactCenterUserGroup"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
        })
        self.rest.raise_for_status(response)
        return response

    def modify_group(self, **kwargs):
        """
        MOdify Group
        :param kwargs:
        :return:
        """
        userId = kwargs.get('userId', None)
        groupId = kwargs.get('groupId', None)
        sessionId = kwargs.get('sessionId', self.adminToken)
        unassignUserIds = kwargs.get('unassignUserIds', None)
        assignChildGroupIds = kwargs.get('assignChildGroupIds', None)
        unassignChildGroupIds = kwargs.get('unassignChildGroupIds', None)
        assignManagerUserIds = kwargs.get('assignManagerUserIds', None)
        assignUserIds = kwargs.get('assignUserIds', None)
        unassignManagerIds = kwargs.get('unassignManagerIds', None)
        name = kwargs.get('name', None)
        description = kwargs.get('description', None)
        self.check_required_args([sessionId])

        response = self.rest.send_request(**{
            'method': 'POST',
            'url': urljoin(self.creds.url, "ameyorestapi/group/userGroupModifyAPI"),
            'headers': {"sessionId": sessionId, "correlation": self.uuid},
            'json': {
              "groupId": groupId,
              "sessionId": sessionId,
              "userId": userId,
              "unassignUserIds": [],
              "assignChildGroupIds": [],
              "unassignChildGroupIds": [],
              "assignManagerUserIds": [],
              "assignUserIds": assignUserIds,
              "unassignManagerIds": [],
              "name": name,
              "description": description
            },
        })
        if self.noop is True or kwargs.get('toFail', True) is False:
            return response
        self.rest.raise_for_status(response)
        self.is_key_there_in_dict([
            'groupAssignErrorReason', 'groupUnassignErrorReason', 'managerAssignmentInGroupResponse',
            'userAssignmentInGroupResponse', 'unassignManagerError'
        ], response.json())
        return response

