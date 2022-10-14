__author__ = "Developed by EA"

import pytest
import time
import json
import os


@pytest.mark.SETUP
@pytest.mark.run(order=1)
@pytest.mark.usefixtures('class_fixture')
class TestSetup:
    """
    Test Suite to create Test Data
    """

    @staticmethod
    def read_json(filename):
        path = os.getcwd()
        test_data_dir = os.path.join(path)
        # test_data_dir = os.path.join(path, "ameyo", "test_data")
        json_file = os.path.join(test_data_dir, filename)
        with open(json_file, 'r') as file_obj:
            return json.load(file_obj)

    def test_01_create_cc(self, ameyo, calling):
        """
        Create Contact Center
        :param ameyo:
        :return:
        """

        test_data = TestSetup.read_json("test_data.json")
        calling.update({"test_data": test_data})
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                pytest.skip(msg=f"Contact Center {calling['test_data']['ccn']} already Exists !!")
                break
        else:
            # Create Contact Center
            ameyo.create_cc(contactCenterName=calling['test_data']['ccn']).json()

            # Check if cc has been created
            for cc in ameyo.get_all_cc().json():
                if cc['contactCenterName'] == calling['test_data']['ccn']:
                    break
            else:
                raise Exception(f"Cannot Find CC {calling['test_data']['ccn']} !!")

    def test_02_create_user_with_multi_cc_manager(self, ameyo, calling):
        """
        Create user with multi CC manager token
        :param ameyo:
        :return:
        """
        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']

        for multi_cc_created_user in multi_cc_created_users_list:
            userId = f"{multi_cc_created_user['name']}"
            users = ameyo.get_all_users(sessionId=ameyo.ccManagerToken).json()
            for user in users:
                if user['userID'] == userId:
                    ameyo.logger.info(f"Delete Existing user {user['userID']} ...")
                    response = ameyo.delete_user(userId=userId, sessionId=ameyo.ccManagerToken)
                    assert response.text == 'ok', f"Failed to delete user with: {userId}"

            response = ameyo.create_cc_user(**{
                'userId': userId,
                'userData': multi_cc_created_user['password'],
                'userType': multi_cc_created_user['role'],
                'isRoot': multi_cc_created_user['isRoot']
            }).json()
            calling['userType'] = response['userType']

    def test_03_assign_user_to_cc_with_multi_cc_manager(self, ameyo, calling):
        """
        Assign user to CC with multi CC manager token
        :param ameyo:
        :param role:
        :return:
        """

        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['test_data']['ccn']} !!")
        ccId = cc['contactCenterId']

        for multi_cc_created_user in multi_cc_created_users_list:
            userId = f"{multi_cc_created_user['name']}"
            ameyo.assign_user_to_cc(**{
                'allocateContactCenterId': ccId,
                'userIds': userId,
                'userTypes': multi_cc_created_user['role']
            })

            # Check user is assigned to CC
            users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.ccManagerToken).json()
            for user in users:
                if userId == user['userId']:
                    break
            else:
                raise Exception(f"User {userId} not assigned to CC !!")

    def test_04_create_users_by_admin(self, ameyo, calling):
        """
        Create User using Admin Token
        :param ameyo:
        :param role:
        :return:
        """

        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        admin_created_users_list = calling['test_data']['admin_created_users']

        if ameyo.adminToken is None:
            ameyo.adminToken = \
                ameyo.user_login(userId=f"{multi_cc_created_users_list[0]['name']}").json()['userSessionInfo'][
                    'sessionId']
            # response = ameyo.user_login(userId=f"{multi_cc_created_users_list[0]['name']}")
            # if response.ok is False:
            #     response = response.json()
            #     message = f"SessionService.login.failed.not.able.to.fetch.user.info"
            #     if response['status_code'] == 512 and response['message'] == message:
            #         ameyo.adminToken = \
            #             ameyo.user_login(userId=f"{multi_cc_created_users_list[0]['name']}").json()['userSessionInfo'][
            #                 'sessionId']
            #     else:
            #         pass
            # else:
            #     ameyo.adminToken = \
            #     ameyo.user_login(userId=f"{multi_cc_created_users_list[0]['name']}").json()['userSessionInfo'][
            #         'sessionId']

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['test_data']['ccn']} !!")
        ccId = cc['contactCenterId']

        for admin_created_user in admin_created_users_list:
            userId = f"{admin_created_user['name']}"
            users = ameyo.get_all_users(sessionId=ameyo.adminToken).json()
            for user in users:
                if user['userID'] == userId:
                    ameyo.logger.info(f"Delete Existing user {userId} ...")
                    response = ameyo.delete_user(userId=userId, sessionId=ameyo.adminToken)
                    assert response.text == 'ok', f"Failed to delete user with: {userId}"

            ameyo.create_user(**{
                'userId': userId,
                'userType': admin_created_user['role'],
                'password': admin_created_user['password'],
                'contactCenterId': ccId
            })

            # Check user is assigned to CC
            users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
            for user in users:
                if userId == user['userId']:
                    break
            else:
                raise Exception(f"User {userId} not assigned to CC !!")

    def test_05_assign_call_contexts_to_cc(self, ameyo, calling):
        """
        Assign Call Contexts to Contact Center
        :param ameyo:
        :return:
        """

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['test_data']['ccn']} !!")
        ccId = cc['contactCenterId']

        SystemContexts = ameyo.get_all_call_context().json()
        assigned = ameyo.get_cc_call_contexts(ccId=ccId, sessionId=ameyo.adminToken).json()
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
        assigned = ameyo.assign_call_contexts_to_cc(contactCenterId=ccId,
                                                    callContexts=callContexts,
                                                    sessionId=ameyo.adminToken).json()
        assigned = {x['callContextId'] for x in assigned['contactCenterCallContextBeans']}
        if len({x['callContextId'] for x in callContexts}.intersection(assigned)) != len(callContexts):
            raise Exception(f"Some Call Context not assigned !!")

        # Verify Call Contexts in Get Call
        response = ameyo.get_cc_call_contexts(sessionId=ameyo.adminToken)
        assigned = {x['callContextId'] for x in response.json()}
        if len({x['callContextId'] for x in callContexts}.intersection(assigned)) != len(callContexts):
            raise Exception(f"Some Call Context not assigned !!")

    def test_06_create_process(self, ameyo, calling):
        """
        Create Process
        :param ameyo:
        :return:
        """

        process_names_list = calling['test_data']['process_names']

        for process_name in process_names_list:
            processes = ameyo.get_all_processes(sessionId=ameyo.adminToken).json()
            for process in processes:
                if process['processName'] == process_name:
                    ameyo.logger.info(f"Deleting Existing Process {process_name} ...")
                    ameyo.delete_process(processId=process['processId'], sessionId=ameyo.adminToken)
                    break
            ameyo.create_process(processName=process_name, sessionId=ameyo.adminToken)
            processes = ameyo.get_all_processes(sessionId=ameyo.adminToken).json()
            if process_name not in [x['processName'] for x in processes]:
                raise Exception(f"Process {process_name} not Found !!")

        processIds = []
        for Process in ameyo.get_all_processes(sessionId=ameyo.adminToken).json():
            processIds.append(Process['processId'])
        calling.update({'processIds': processIds})

    def test_07_create_campaign(self, ameyo, calling):
        """
        Create Campaign
        :param ameyo:
        :return:
        """

        process_ids_list = sorted(calling['processIds'])
        campaign_names_list = calling['test_data']['campaign_names']
        proc_campgn_dict = dict(zip(process_ids_list, campaign_names_list))
        campaignIds = []
        for process_id, campaign_name in proc_campgn_dict.items():
            campaignName = f"{campaign_name}"
            # Check if Existing, Skip in case
            for Campaign in ameyo.get_all_campaigns().json():
                if Campaign['campaignName'] == campaignName:
                    ameyo.logger.info(f"Delete Existing Campaign {campaignName} ...")
                    ameyo.delete_campaign(campaignId=Campaign['campaignId'])
                    break
            response = ameyo.create_campaign(**{
                        "processId": process_id,
                        "campaignType": calling['test_data']['campaign_type_outbound_voice'],
                        "campaignName": campaignName,
                        "description": f"{campaignName} Description",
                    })
            campaignId = response.json()['campaignId']
            campaignIds.append(campaignId)

            Campaigns = ameyo.get_all_campaigns().json()
            if campaignName not in [x['campaignName'] for x in Campaigns]:
                raise Exception(f"Campaign {campaignName} is not Present !!")
        calling.update({'campaignIds': campaignIds})

    def test_08_create_agents(self, ameyo, calling):
        """
        Get Contact Center Agents
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['test_data']['ccn']} not found !!")

        # Create a new user
        agents = []
        for agent in calling['test_data']['agents']:
            all_users = ameyo.get_all_users().json()
            for user in all_users:
                if user['userID'] == agent:
                    ameyo.logger.info(f"Delete Existing agent {user['userID']} ...")
                    response = ameyo.delete_user(userId=user['userID'], sessionId=ameyo.adminToken)
                    assert response.text == 'ok', f"Failed to delete user with: {user['userID']}"
            response = ameyo.create_user(**{
                'userId': agent, 'userName': agent, 'userType': 'Executive', 'contactCenterId': ccId,
                'password': 'Test300!@#$',
            }).json()
            agents.append(response)
        calling.update({'agents': agents})

    def test_09_assign_user_to_campaigns(self, ameyo, calling):
        """
        Assign user to campaign
        :param ameyo:
        :return:
        """

        campaign_names_list = calling['test_data']['campaign_names']
        campaign_ids_list = calling['campaignIds']

        for campaign_id in campaign_ids_list:
            # unassign any user assigned to campaign
            assigned = ameyo.get_all_campaign_users(campaignId=campaign_id).json()
            ameyo.un_assign_agent_from_campaign(**{
                'campaignId': campaign_id,
                'campaignContextUserIds': [x['campaignUserId'] for x in assigned],
            })
            assigned = ameyo.get_all_campaign_users(campaignId=campaign_id).json()

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            n = int(len(calling['agents']) / len(campaign_ids_list))
            agents_lists = [calling['agents'][i * n:(i + 1) * n] for i in range((len(calling['agents']) + n - 1) // n)]
            for agents in agents_lists:
                # if agent['userId'] not in [x['userId'] for x in assigned]
                for agent in agents:
                    contactCenterUserIds.append(agent['contactCenterUserId'])
                    privilegePlanIds.append(agent['privilegePlanId'])
                    userIds.append(agent['userId'])
                    contactCenterUserTypes.append(agent['userType'])

            if len(userIds) == 0:
                ameyo.logger.debug(f'all users already assigned to Campaign !!')
                continue

            time.sleep(1)
            ameyo.assign_agent_to_campaign(**{
                'campaignId': campaign_id,
                'contactCenterUserIds': contactCenterUserIds,
                'privilegePlanIds': privilegePlanIds,
                'userIds': userIds,
                'contactCenterUserTypes': contactCenterUserTypes,
            })
            time.sleep(1)

    def test_09_login_agents(self, ameyo, calling):
        """
        Login Agents, change password, assign and select campaign, set extension, logout
        :param ameyo:
        :param role:
        :return:
        """

        campaign_names_list = calling['test_data']['campaign_names']
        agents_list = calling['test_data']['agents']
        campgn_agents_dict = dict(zip(campaign_names_list, agents_list))

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['test_data']['ccn']} not found !!")

        # Login agents and change passwords
        for campaign_name, agent in campgn_agents_dict.items():
            ameyo.executiveToken = ameyo.user_login(userId=agent,
                                                    token='Test300!@#$').json()['userSessionInfo']['sessionId']
            time.sleep(1)
            ameyo.get_password_policy_for_user(sessionId=ameyo.executiveToken, userId=agent).json()
            ameyo.change_password(sessionId=ameyo.executiveToken, userId=agent,
                                  oldPassword='Test300!@#$', newPassword='Test300!@#')
            time.sleep(1)
            ameyo.user_logout(sessionId=ameyo.executiveToken)
            time.sleep(1)
        else:
            pass

    @pytest.mark.skip("WIP")
    def test_10_assign_supervisor_to_all_campaigns(self, ameyo):
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

