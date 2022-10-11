__author__ = "Developed by EA"

import pytest
import time
import random, string


@pytest.mark.SETUP
@pytest.mark.run(order=1)
@pytest.mark.usefixtures('class_fixture')
class TestSetup:
    """
    Test Suite to create Test Data
    """

    def test_01_create_cc(self, ameyo):
        """
        Create Contact Center
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                pytest.skip(msg=f"Contact Center {self.ccn} already Exists !!")
                break
        else:
            # Create Contact Center
            ameyo.create_cc(contactCenterName=self.ccn).json()

            # Check if cc has been created
            for cc in ameyo.get_all_cc().json():
                if cc['contactCenterName'] == self.ccn:
                    break
            else:
                raise Exception(f"Cannot Find CC {self.ccn} !!")

    @pytest.mark.parametrize("suffix,isRoot,role", [
        ("ADMIN_USER", True, 'Administrator'), ("SUPERVISOR_USER", False, 'Supervisor'),
        ("EXECUTIVE_USER", False, 'Executive')
    ])
    def test_02_create_user_with_multi_cc_manager(self, ameyo, suffix, isRoot, role, calling):
        """
        Create user with multi CC manager token
        :param ameyo:
        :return:
        """
        userId = f"{self.ccn}_{suffix}"
        users = ameyo.get_all_users(sessionId=ameyo.ccManagerToken).json()
        for user in users:
            if user['userID'] == userId:
                pytest.skip(msg=f"{userId} already Exists !!")

        response = ameyo.create_cc_user(**{
            'userId': userId,
            'userData': 'Test300!@#',
            'userType': role,
            'isRoot': isRoot
        }).json()
        calling['userType'] = response['userType']

    @pytest.mark.parametrize("suffix,role", [
        ("ADMIN_USER", 'Administrator'), ("SUPERVISOR_USER", 'Supervisor'), ("EXECUTIVE_USER", 'Executive')])
    def test_03_assign_user_to_cc_with_multi_cc_manager(self, ameyo, suffix, role):
        """
        Assign user to CC with multi CC manager token
        :param ameyo:
        :param role:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                break
        else:
            raise Exception(f"Cannot Find CC {self.ccn} !!")
        ccId = cc['contactCenterId']

        userId = f"{self.ccn}_{suffix}"

        users = sorted(ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.ccManagerToken).json(),
                       key=lambda a: a['userId'])
        if userId in [x['userId'] for x in users]:
            pytest.skip(msg=f"User {userId} already assigned to CC")

        ameyo.assign_user_to_cc(**{
            'allocateContactCenterId': ccId,
            'userIds': userId,
            'userTypes': role
        })

        # Check user is assigned to CC
        users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.ccManagerToken).json()
        for user in users:
            if userId == user['userId']:
                break
        else:
            raise Exception(f"User {userId} not assigned to CC !!")

    @pytest.mark.parametrize("suffix,isRoot,role", [
        ("ADMIN_USER_01", True, 'Administrator'), ("SUPERVISOR_USER_01", False, 'Supervisor'),
        ("EXECUTIVE_USER_01", False, 'Executive')])
    def test_04_create_user_using_admin_token(self, ameyo, suffix, isRoot, role):
        """
        Create User using Admin Token
        :param ameyo:
        :param role:
        :return:
        """
        if ameyo.adminToken is None:
            ameyo.adminToken = ameyo.user_login(userId=f"{self.ccn}_ADMIN_USER").json()['userSessionInfo']['sessionId']

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                break
        else:
            raise Exception(f"Cannot Find CC {self.ccn} !!")
        ccId = cc['contactCenterId']

        userId = f"{self.ccn}_{suffix}"
        users = sorted(
            ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json(), key=lambda a: a['userId']
        )
        if userId in [x['userId'] for x in users]:
            pytest.skip(msg=f"User {userId} already assigned to CC")

        ameyo.create_user(**{
            'userId': userId,
            'userType': role,
            'password': 'Test300!@#',
            'contactCenterId': ccId
        })

        # Check user is assigned to CC
        users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        for user in users:
            if userId == user['userId']:
                break
        else:
            raise Exception(f"User {userId} not assigned to CC !!")

    @pytest.mark.parametrize("suffix,role", [
        ("ADMIN_USER_01", 'Administrator'), ("SUPERVISOR_USER_01", 'Supervisor'), ("EXECUTIVE_USER_01", 'Executive')])
    def test_05_login_users(self, ameyo, suffix, role):
        """
        Login Users
        :param ameyo:
        :param role:
        :return:
        """
        userId = f"{self.ccn}_{suffix}"
        if role == 'Administrator':
            ameyo.adminToken = ameyo.user_login(userId=userId).json()['userSessionInfo']['sessionId']
        elif role == 'Supervisor':
            ameyo.supervisorToken = ameyo.user_login(userId=userId).json()['userSessionInfo']['sessionId']
        elif role == 'Executive':
            ameyo.executiveToken = ameyo.user_login(userId=userId).json()['userSessionInfo']['sessionId']
        else:
            pass

    def test_06_assign_call_contexts_to_cc(self, ameyo):
        """
        Assign Call Contexts to Contact Center
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                break
        else:
            raise Exception(f"Cannot Find CC {self.ccn} !!")
        ccId = cc['contactCenterId']

        SystemContexts = ameyo.get_all_call_context().json()
        assigned = ameyo.get_cc_call_contexts(ccId=ccId).json()
        callContexts = []
        for SystemContext in SystemContexts:
            if SystemContext['name'] in [x['callContextName'] for x in assigned] or SystemContext['id'] <= 0:
                continue
            callContexts.append({
                'callContextId': SystemContext['id'],
                'maxOutboundCalls': 1000,
                'maxInboundCalls': 1000,
                'maxTotalActiveCalls': 1000
            })

        if len(callContexts) == 0:
            return

        # assign and verify call contexts in response
        assigned = ameyo.assign_call_contexts_to_cc(contactCenterId=ccId, callContexts=callContexts, ).json()
        assigned = {x['callContextId'] for x in assigned['contactCenterCallContextBeans']}
        if len({x['callContextId'] for x in callContexts}.intersection(assigned)) != len(callContexts):
            raise Exception(f"Some Call Context not assigned !!")

        # Verify Call Contexts in Get Call
        response = ameyo.get_cc_call_contexts()
        assigned = {x['callContextId'] for x in response.json()}
        if len({x['callContextId'] for x in callContexts}.intersection(assigned)) != len(callContexts):
            raise Exception(f"Some Call Context not assigned !!")

    def test_07_create_process(self, ameyo, pn):
        """
        Create Process
        :param ameyo:
        :return:
        """
        processName = f"{self.ccn}_{pn}"
        ameyo.create_process(processName=processName)
        Processes = ameyo.get_all_processes().json()
        if processName not in [x['processName'] for x in Processes]:
            raise Exception(f"Process {processName} not Found !!")

    def test_08_update_process_crm_settings(self, ameyo):
        """
        Update Process
        :param ameyo:
        :return:
        """
        for _, Process in enumerate(ameyo.get_all_processes().json()):
            response = ameyo.get_process_crm_settings(**{
                'processId': Process['processId'],
                'toFail': False
            })
            if response.ok is False:
                response = response.json()
                message = f"No configuration for process with id {Process['processId']} exists"
                if response['status'] == 512 and response['message'] == message:
                    pass
            else:
                response = response.json()
                if response['propagateCustomerRemoval'] is True and response['propagateLeadRemoval'] is True:
                    continue

            ameyo.update_process_crm_settings(processId=Process['processId'])

    def test_09_create_campaign(self, ameyo):
        """
        Create Campaign
        :param ameyo:
        :return:
        """
        for Process in ameyo.get_all_processes().json():
            campaignName = f"{Process['processName']}_CAMPAIGN"

            # Check if Existing, Skip in case
            for Campaign in ameyo.get_all_campaigns().json():
                if Campaign['campaignName'] == campaignName:
                    ameyo.logger.info(f"Delete Existing Campaign {campaignName} ...")
                    ameyo.delete_campaign(campaignId=Campaign['campaignId'])
                    break

            # ameyo.logger.info(f"Creating new Campaign : {campaignName}")
            ameyo.create_campaign(**{
                "processId": Process['processId'],
                "campaignType": 'Outbound Voice Campaign',
                "campaignName": campaignName,
                "description": f"{campaignName} Description",
            })

            Campaigns = ameyo.get_all_campaigns().json()
            if campaignName not in [x['campaignName'] for x in Campaigns]:
                raise Exception(f"Campaign {campaignName} is not Present !!")

    def test_10_assign_call_contexts_to_campaign(self, ameyo):
        """
        Assign all Call Contexts to a Given Campaign
        25-03 - Assigning call contexts(which starts with customer i.e. customer_success_*, customer_notreachable*) to campaigns
        1 cc to 1 campaign
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                break
        else:
            raise Exception(f"Cannot Find CC {self.ccn} !!")
        ccId = cc['contactCenterId']

        CallContexts = list(filter(
            lambda a: a['callContextName'] is not None and 'customer_' in a['callContextName'],
            ameyo.get_cc_call_contexts().json()
        ))
        for Count, Campaign in enumerate(ameyo.get_all_campaigns().json()):
            CallContext = CallContexts[Count % len(CallContexts)]
            ameyo.logger.info(
                f"Assigning <{CallContext['callContextName']}> to <{Campaign['campaignName']}> with id <{Campaign['campaignId']}>")
            for assigned in ameyo.get_call_contexts_in_campaign(campaignId=Campaign['campaignId']).json():
                if 'campaignId' in assigned and assigned['campaignId'] == Campaign['campaignId']:
                    if assigned['callContextId'] == CallContext['callContextId']:
                        break
            else:
                ameyo.assign_call_context_to_campaign(**{
                    'contactCenterCallContextId': CallContext['contactCenterCallContextId'],
                    'callContextId': CallContext['callContextId'],
                    "maxOutboundCalls": CallContext['maxOutboundCalls'],
                    "maxInboundCalls": CallContext['maxInboundCalls'],
                    "maxTotalActiveCalls": CallContext['maxTotalActiveCalls'],
                    'campaignId': Campaign['campaignId'],
                    'contactCenterId': ccId,
                })

                ameyo.get_call_contexts_in_campaign(campaignId=Campaign['campaignId'])

    def test_11_assign_supervisor_to_campaign(self, ameyo):
        """
        Assign Supervisor user to Campaign
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                break
        else:
            raise Exception(f"Cannot Find CC {self.ccn} !!")
        ccId = cc['contactCenterId']

        users = ameyo.get_all_users_assigned_to_cc(ccId=ccId).json()
        for count, Campaign in enumerate(ameyo.get_all_campaigns().json()):
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'])
            assigned = [x['userId'] for x in response.json()]

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            for User in [x for x in users if x['systemUserType'] == 'Supervisor']:
                if User['userId'] not in assigned:
                    contactCenterUserIds.append(User['ccUserId'])
                    privilegePlanIds.append(User['privilegePlanId'])
                    userIds.append(User['userId'])
                    contactCenterUserTypes.append(User['systemUserType'])

            if all([contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes]) is False:
                continue

            # assign agent to Campaign
            ameyo.assign_agent_to_campaign(**{
                'campaignId': Campaign['campaignId'],
                'contactCenterUserIds': contactCenterUserIds,
                'privilegePlanIds': privilegePlanIds,
                'userIds': userIds,
                'contactCenterUserTypes': contactCenterUserTypes,
            })

            # validate users assigned to campaign
            returnedusers = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId']).json()
            returneduserids = [returneduser['userId'] for returneduser in returnedusers]
            assert (len(userIds) == len(returneduserids) and sorted(userIds) == sorted(returneduserids))

    def test_12_create_new_lead(self, ameyo):
        """
        Create a new Lead
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{self.ccn} not found !!")

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Supervisor'],
            ameyo.get_all_users_assigned_to_cc(ccId=ccId).json()
        ))

        for Process in ameyo.get_all_processes().json():
            leadName = f"{Process['processName']}_LEAD"
            for lead in ameyo.get_all_leads_for_process(processId=Process['processId']).json():
                if lead['leadName'] == leadName:
                    ameyo.logger.debug(f"Lead Already Exists !!")
                    break
            else:
                for user in Users:
                    ameyo.add_lead(**{
                        'leadName': leadName,
                        'processId': Process['processId'],
                        'ownerUserId': user['userId']
                    })
                    break  # One Lead Per Process

                for lead in ameyo.get_all_leads_for_process(processId=Process['processId']).json():
                    if lead['leadName'] == leadName:
                        break
                else:
                    raise Exception(f"New Created Lead not Found !!")

    def test_13_assign_lead_to_campaign(self, ameyo):
        """
        Assign Lead to Campaign
        :param ameyo:
        :return:
        """
        for Campaign in ameyo.get_all_campaigns().json():
            Leads = ameyo.get_all_leads_for_process(processId=Campaign['processId']).json()
            leadIds = []
            for Lead in Leads:
                if Campaign['campaignId'] in Lead['campaignContextIds']:
                    continue
                else:
                    leadIds.append(Lead['leadId'])

            if len(leadIds) > 0:
                ameyo.assign_lead_to_campaign(campaignContextId=Campaign['campaignId'], leadIds=leadIds)

    def test_14_create_executive_agents(self, ameyo, request):
        """
        Get Contact Center Agents
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{self.ccn} not found !!")

        all_users = ameyo.get_all_users().json()
        users_runtime = ameyo.get_user_run_time().json()

        def _create(userId):
            for _user in all_users:
                if _user['userID'] == userId and _user['contactCenterId'] != ccId:
                    # when _user is created, but not assigned to any cc - delete the user
                    ameyo.delete_cc_user(userId=userId, sessionId=ameyo.ccManagerToken)
                    break

                if _user['userID'] == userId and _user['contactCenterId'] == ccId:
                    for _logged in users_runtime:
                        if userId == _logged['userId']:
                            ameyo.user_logout(sessionId=_logged['sessionId'])
                            break
                    return

            # Create a new user
            ameyo.create_user(**{
                'userId': userId, 'userName': userId, 'userType': 'Executive', 'contactCenterId': ccId,
            })

        notCreated = []
        arguments = [{'userId': f"{self.ccn}_EXECUTIVE_USER_{i:04}"} for i in
                     range(1, request.config.option.agents + 1)]
        batch = 100
        for i in range(0, len(arguments), batch):
            response = ameyo.run_in_parallel(_create, arguments=arguments[i: i + batch], max_workers=batch, logs=False)
            users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
            for count, metadata in response.items():
                _userId, reason = metadata['args']['userId'], metadata['exception']
                if metadata['exception']:
                    ameyo.logger.error(f"userId: {_userId} Creation Failed !! Reason: {reason}")
                    notCreated.append({'userId': _userId, 'Exception': metadata['exception']})
                    continue
                for user in users:
                    if user['userId'] == _userId:
                        # ameyo.logger.info(
                        #     f"User: {user['userId']} with ccUserId: {user['ccUserId']} Created Successfully :)"
                        # )
                        break
                else:
                    raise Exception(f"User {_userId} Not Found !!")

        if len(notCreated) > 0:
            raise Exception(f"Users {notCreated} Not Created !!")

    def test_15_assign_user_to_campaigns(self, ameyo):
        """
        Assign user to campaign
        25-03 - Assigning random number of agents to all campaigns
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{self.ccn} not found !!")

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Executive'] and a['mappingUserId'] is None,
            ameyo.get_all_users_assigned_to_cc(ccId=ccId).json()
        ))

        Campaigns = ameyo.get_all_campaigns().json()
        for Campaign in Campaigns:
            # unassign any user assigned to campaign
            assigned = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId']).json()
            ameyo.un_assign_agent_from_campaign(**{
                'campaignId': Campaign['campaignId'],
                'campaignContextUserIds': [x['campaignUserId'] for x in assigned],
            })
            assigned = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId']).json()

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            n = int(len(Users) / len(Campaigns))
            Users = random.sample(Users, n)
            for User in Users:
                if User['userId'] not in [x['userId'] for x in assigned]:
                    contactCenterUserIds.append(User['ccUserId'])
                    privilegePlanIds.append(User['privilegePlanId'])
                    userIds.append(User['userId'])
                    contactCenterUserTypes.append(User['systemUserType'])

            if len(userIds) == 0:
                ameyo.logger.debug(f'all users already assigned to Campaign !!')
                continue

            ameyo.assign_agent_to_campaign(**{
                'campaignId': Campaign['campaignId'],
                'contactCenterUserIds': contactCenterUserIds,
                'privilegePlanIds': privilegePlanIds,
                'userIds': userIds,
                'contactCenterUserTypes': contactCenterUserTypes,
            })

            # Verify agent has been assigned
            assigned = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId']).json()
            for User in Users:
                if User['userId'] not in [x['userId'] for x in assigned]:
                    raise Exception(f"User {User['userId']} not assigned to Campaign !!")

    def test_22_assign_supervisor_to_all_campaigns(self, ameyo):
        """
        Assign Supervisor user to all Campaigns (required for supervisor monitoring)
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == self.ccn:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{self.ccn} not found !!")

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Supervisor'],
            ameyo.get_all_users_assigned_to_cc(ccId=ccId).json()
        ))

        for count, Campaign in enumerate(ameyo.get_all_campaigns().json()):
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'])
            assigned = [x['userId'] for x in response.json()]

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            for User in Users:
                if User['userId'] not in assigned:
                    contactCenterUserIds.append(User['ccUserId'])
                    privilegePlanIds.append(User['privilegePlanId'])
                    userIds.append(User['userId'])
                    contactCenterUserTypes.append(User['systemUserType'])

            if all([contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes]) is False:
                continue

            # assign agent to Campaign
            ameyo.assign_agent_to_campaign(**{
                'campaignId': Campaign['campaignId'],
                'contactCenterUserIds': contactCenterUserIds,
                'privilegePlanIds': privilegePlanIds,
                'userIds': userIds,
                'contactCenterUserTypes': contactCenterUserTypes,
            })

            # Get users assigned to campaign
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'])
            ameyo.logger.info(
                f"All {len(response.json())} users in <{Campaign['campaignId']}> <{Campaign['campaignName']}> {[x['userId'] for x in response.json()]}")

