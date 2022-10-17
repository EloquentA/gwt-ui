__author__ = "Developed by EA"

import pytest
import time
import json
import yaml
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
        # test_data_dir = os.path.join(path)
        test_data_dir = os.path.join(path, "ameyo", "test_data")
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
                ameyo.logger.info(f"Contact Center {calling['test_data']['ccn']} already Exists, deleting it")
                ameyo.delete_cc(contactCenterId=cc['contactCenterId'])
                ameyo.logger.info(f"CC {cc['contactCenterName']} Deleted Successfully :)")
                break
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
            ameyo.logger.info(f"Newly created users: {calling['userType']} ...")

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
            ameyo.adminToken = ameyo.user_login(userId=f"{multi_cc_created_users_list[0]['name']}").json()[
                'userSessionInfo']['sessionId']

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

    def test_07_create_campaigns(self, ameyo, calling):
        """
        Create Campaign
        :param ameyo:
        :return:
        """

        process_ids_list = sorted(calling['processIds'])
        inbound_campaigns_list = calling['test_data']['inbound_campaigns']
        outbound_campaigns_list = calling['test_data']['outbound_campaigns']
        proc_inbound_campgn_dict = dict(zip(process_ids_list, inbound_campaigns_list))
        proc_outbound_campgn_dict = dict(zip(process_ids_list, outbound_campaigns_list))
        campaignIds = []
        for process_id, campaign_name in proc_inbound_campgn_dict.items():
            campaignName = f"{campaign_name}"
            # Check if Existing, Skip in case
            for Campaign in ameyo.get_all_campaigns().json():
                if Campaign['campaignName'] == campaignName:
                    ameyo.logger.info(f"Delete Existing Campaign {campaignName} ...")
                    ameyo.delete_campaign(campaignId=Campaign['campaignId'])
                    break
            response = ameyo.create_campaign(**{
                        "processId": process_id,
                        "campaignType": calling['test_data']['campaign_type_inbound'],
                        "campaignName": campaignName,
                        "description": f"{campaignName} Description",
                    })
            campaignId = response.json()['campaignId']
            campaignIds.append(campaignId)

            Campaigns = ameyo.get_all_campaigns().json()
            if campaignName not in [x['campaignName'] for x in Campaigns]:
                raise Exception(f"Campaign {campaignName} is not Present !!")
        for process_id, campaign_name in proc_outbound_campgn_dict.items():
            campaignName = f"{campaign_name}"
            # Check if Existing, Skip in case
            for Campaign in ameyo.get_all_campaigns().json():
                if Campaign['campaignName'] == campaignName:
                    ameyo.logger.info(f"Delete Existing Campaign {campaignName} ...")
                    ameyo.delete_campaign(campaignId=Campaign['campaignId'])
                    break
            response = ameyo.create_campaign(**{
                        "processId": process_id,
                        "campaignType": calling['test_data']['campaign_type_outbound'],
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

        inbound_campaigns_list = calling['test_data']['inbound_campaigns']
        outbound_campaigns_list = calling['test_data']['outbound_campaigns']
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

    def test_10_assign_supervisor_to_campaign(self, ameyo, calling):
        """
        Assign Supervisor user to Campaign
        :param ameyo:
        :return:
        """
        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['test_data']['ccn']} !!")
        ccId = cc['contactCenterId']

        users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                    sessionId=ameyo.adminToken)
            assigned = [x['userId'] for x in response.json()]

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            for User in [x for x in users if
                         x['systemUserType'] == 'Supervisor' and
                         x['userId'] == multi_cc_created_users_list[1]['name']]:
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
                'sessionId': ameyo.adminToken,
            })

    def test_11_login_agents(self, ameyo, calling):
        """
        Login Agents, change password and logout
        :param ameyo:
        :param role:
        :return:
        """

        inbound_campaigns_list = calling['test_data']['inbound_campaigns']
        agents_list = calling['test_data']['agents']
        campgn_agents_dict = dict(zip(inbound_campaigns_list, agents_list))

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

    def test_12_create_new_lead(self, ameyo, calling):
        """
        Create a new Lead
        :param ameyo:
        :return:
        """

        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        process_ids_list = sorted(calling['processIds'])
        lead_names_list = calling['test_data']['lead_names']
        proc_lead_dict = dict(zip(process_ids_list, lead_names_list))
        leadIds = []
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['test_data']['ccn']} not found !!")

        if ameyo.supervisorToken is None:
            ameyo.supervisorToken = ameyo.user_login(userId=f"{multi_cc_created_users_list[1]['name']}").json()[
                'userSessionInfo']['sessionId']

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Supervisor'],
            ameyo.get_all_users_assigned_to_cc(ccId=ccId).json()
        ))

        for process_id, lead_name in proc_lead_dict.items():
            lead_name = f"{lead_name}"
            for lead in ameyo.get_all_leads_for_process(processId=process_id).json():
                if lead['leadName'] == lead_name:
                    ameyo.logger.debug(f"Lead Already Exists, deleting it...")
                    ameyo.delete_lead(leadId=lead['leadId'], sessionId=ameyo.supervisorToken)
                for user in Users:
                    response = ameyo.add_lead(**{
                        'leadName': lead_name,
                        'processId': process_id,
                        'ownerUserId': user['userId']
                    }).json()
                    leadIds.append(response['leadId'])
                    # for lead in ameyo.get_all_leads_for_process(processId=process_id).json():
                    #     if lead['leadName'] == lead_name:
                    #         leadIds.append(lead['leadId'])
                    #         break

                for lead in ameyo.get_all_leads_for_process(processId=process_id).json():
                    if lead['leadName'] == lead_name:
                        break
                else:
                    raise Exception(f"New Created Lead not Found !!")
        calling.update({"leadIds": leadIds})

    def test_13_assign_lead_to_campaign(self, ameyo, calling):
        """
        Assign Lead to Campaign
        :param ameyo:
        :return:
        """
        campaign_ids_list = calling['campaignIds']
        lead_ids_list = sorted(calling['leadIds'])

        for campaign_id in campaign_ids_list:
            ameyo.assign_lead_to_campaign(campaignContextId=campaign_id, leadIds=lead_ids_list)

    def test_14_upload_lead_csv(self, ameyo, request, calling):
        """
        Uploads a csv (containing customer data) to the lead
        :param ameyo:
        :param request:
        :return:
        """
        process_ids_list = sorted(calling['processIds'])
        lead_ids_list = sorted(calling['leadIds'])
        for process_id in process_ids_list:
            for Lead in ameyo.get_all_leads_for_process(processId=process_id).json():
                csvPath = ameyo.create_customer_csv(count=request.config.option.leads)
                response = ameyo.upload_csv_to_lead(**{
                    "processId": Lead['processId'],
                    "leadIds": Lead['leadId'],
                    'csvPath': csvPath
                })
                assert "failed" not in response.text.lower(), "Upload Failed !!"
                assert "invalid" not in response.text.lower(), "Upload File is Invalid !!"

    def test_15_enable_lead_for_process(self, ameyo, calling):
        """
        Enables lead for a process
        :param ameyo:
        :param request:
        :return:
        """
        process_ids_list = sorted(calling['processIds'])
        for process_id in process_ids_list:
            for Lead in ameyo.get_all_leads_for_process(processId=process_id).json():
                response = ameyo.enable_lead_for_process(**{
                    "leadId": Lead['leadId'],
                    "enabled": True,
                })
                is_enabled = ameyo.is_lead_enabled_for_process(processId=process_id,
                                                               lead_name=Lead["leadName"])
                assert is_enabled, f"Lead <{Lead['leadName']}> can not be enabled for <{process_id}>"

    def test_16_enable_lead_for_campaign(self, ameyo, calling):
        """
        Enables lead for a campaign
        :param ameyo:
        :param request:
        :return:
        """
        process_ids_list = sorted(calling['processIds'])
        for process_id in process_ids_list:
            for Campaign in ameyo.get_all_campaigns().json():
                for Lead in ameyo.get_all_leads_for_campaign(processId=process_id,
                                                             campaignId=Campaign['campaignId']).json()[
                    'leadManagementContactLeadListBeans']:
                    leadName = Lead["leadName"]
                    campaignLeadId = Lead["campaignLeadId"]
                    leadDialingConfigurationEnabled = True
                    response = ameyo.enable_lead_for_campaign(**{
                        "leadId": Lead['leadId'],
                        "leadName": leadName,
                        "campaignLeadId": campaignLeadId,
                        "campaignId": Campaign['campaignId'],
                        "leadDialingConfigurationEnabled": leadDialingConfigurationEnabled
                    })
                    leads = ameyo.get_all_leads_for_campaign(processId=process_id,
                                                             campaignId=Campaign['campaignId']).json()[
                        'leadManagementContactLeadListBeans']
                    lead = [x for x in leads if x["leadName"] == leadName][0]
                    assert lead[
                        "isEnable"], f"Lead <{Lead['leadName']}> can not be enabled for <{Campaign['campaignName']}>"

    def test_17_logout_admin(self, ameyo, calling):
        """
        Login logout admin
        :param ameyo:
        :param calling:
        :return:
        """

        ameyo.user_logout(sessionId=ameyo.adminToken)

    def test_18_logout_supervisor(self, ameyo, calling):
        """
        logout supervisor
        :param ameyo:
        :param calling:
        :return:
        """

        ameyo.user_logout(sessionId=ameyo.supervisorToken)

    def test_19_generate_yaml_test_data(self, ameyo, calling):
        """
        Convert test data from JSON to YAML for UI automation consumption
        :param ameyo:
        :param calling:
        :return:
        """
        path = os.getcwd()
        # test_data_dir = os.path.join(path)
        test_data_dir = os.path.join(path, "ameyo", "test_data")
        json_file = os.path.join(test_data_dir, "test_data.json")
        yaml_file = os.path.join(test_data_dir, "sample_variables.yml")
        ameyo.json_to_yaml(json_file, yaml_file)

