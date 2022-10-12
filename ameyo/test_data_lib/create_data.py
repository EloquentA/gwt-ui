__author__ = "Developed by EA"

from urllib.parse import urljoin
from datetime import datetime

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
                    "numOfInteractionExtensions": 5,
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




