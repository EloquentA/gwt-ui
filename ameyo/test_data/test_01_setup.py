__author__ = "Developed by EA"

import random
import pytest
import uuid
import time
import re
import json
import os


@pytest.mark.SETUP
@pytest.mark.run(order=1)
@pytest.mark.usefixtures('class_fixture')
class TestSetup:
    """
    Test Suite to Test Contact Centers Flow
    Keep alive is not handled in this Class as its taking less than 2 minutes
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
        Create CC
        :param ameyo:
        :return:
        """
        test_data = TestSetup.read_json("test_data.json")
        calling.update({"test_data": test_data})
        group_name = calling['test_data']['group_name']

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                try:
                    ccs = [x for x in ameyo.get_all_cc().json() if x['contactCenterName'] == calling['test_data']['ccn']]
                    for cc in ccs:
                        if len(cc['processIds']) == 0:
                            pytest.skip(msg="No Process to Delete !!")

                        for processId in cc['processIds']:
                            ameyo.delete_process(sessionId=ameyo.ccManagerToken, processId=processId)
                            ameyo.logger.info(f"Process {processId} Deleted Successfully :)")

                        # delete all groups
                        response = ameyo.get_all_available_groups(sessionId=ameyo.ccManagerToken).json()
                        for item in response:
                            if item['name'] == group_name:
                                ameyo.delete_cc_user_groups(sessionId=ameyo.ccManagerToken, userGroupId=item['id'])

                    users = list(filter(lambda a: a['userID'].startswith(f"{calling['test_data']['ccn']}_"),
                                        ameyo.get_all_users(sessionId=ameyo.ccManagerToken).json()))
                    for user in users:
                        userId = user['userID']
                        ameyo.logger.info(f'Terminate and Delete User: {userId} ...')
                        ameyo.terminate_all_sessions_for_user(userId=userId, sessionId=ameyo.ccManagerToken)
                        ameyo.delete_user(userId=userId, sessionId=ameyo.ccManagerToken)

                    ameyo.delete_cc(contactCenterId=cc['contactCenterId'])
                except:
                    pass
        else:
            # Create Contact Center
            try:
                ameyo.create_cc(contactCenterName=calling['test_data']['ccn']).json()
            except:
                pass

            # Check if cc has been created
            for cc in ameyo.get_all_cc().json():
                if cc['contactCenterName'] == calling['test_data']['ccn']:
                    calling.update({
                        'ccname': calling['test_data']['ccn'], 'ccIdSpecial': cc['contactCenterId']
                    })
                    break
            else:
                raise Exception(f"Cannot Find CC {calling['test_data']['ccn']} !!")

    def test_02_delete_existing_users(self, ameyo, calling):
        """
        Delete all Existing Users (which match the userId)
        Login, Logout and Delete
        :param ameyo:
        :param suffix:
        :return:
        """
        users = list(filter(lambda a: a['userID'].startswith(f"{calling['ccname']}_"),
                            ameyo.get_all_users(sessionId=ameyo.ccManagerToken).json()))
        for user in users:
            userId = user['userID']
            ameyo.logger.info(f'Terminate and Delete User: {userId} ...')
            ameyo.terminate_all_sessions_for_user(userId=userId, sessionId=ameyo.ccManagerToken)
            ameyo.delete_user(userId=userId, sessionId=ameyo.ccManagerToken)

    def test_03_create_user_with_multi_cc_manager(self, ameyo, calling):
        """
        Create user with multi CC manager token
        :param ameyo:
        :return:
        """
        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']

        for multi_cc_created_user in multi_cc_created_users_list:
            userId = f"{multi_cc_created_user['name']}"
            response = ameyo.create_cc_user(**{
                'userId': userId,
                'userData': multi_cc_created_user['password'],
                'userType': multi_cc_created_user['role'],
                'isRoot': multi_cc_created_user['isRoot']
            }).json()
            calling['userType'] = response['userType']
            ameyo.logger.info(f"Newly created users: {calling['userType']} ...")

    def test_04_assign_user_to_cc_with_multi_cc_manager(self, ameyo, calling):
        """
        Assign user to CC with multi CC manager token
        :param ameyo:
        :param role:
        :return:
        """
        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
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

    def test_05_create_user_using_admin_token(self, ameyo, calling):
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
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        for admin_created_user in admin_created_users_list:
            userId = f"{admin_created_user['name']}"
            ameyo.create_user(**{
                'userId': userId,
                'userType': admin_created_user['role'],
                'password': 'Test300!@#$',
                'contactCenterId': ccId
            })

            # Check user is assigned to CC
            users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
            for user in users:
                if userId == user['userId']:
                    break
            else:
                raise Exception(f"User {userId} not assigned to CC !!")

    def test_06_login_admin_created_users(self, ameyo, calling):
        """
        Login Users
        :param ameyo:
        :param role:
        :return:
        """
        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        admin_created_users_list = calling['test_data']['admin_created_users']

        if ameyo.supervisorToken is None:
            ameyo.supervisorToken = ameyo.user_login(userId=f"{admin_created_users_list[0]['name']}",
                                                    token='Test300!@#$').json()['userSessionInfo']['sessionId']
            time.sleep(1)
            ameyo.get_password_policy_for_user(sessionId=ameyo.supervisorToken,
                                               userId=f"{admin_created_users_list[0]['name']}").json()
            ameyo.change_password(sessionId=ameyo.supervisorToken, userId=f"{admin_created_users_list[0]['name']}",
                                  oldPassword='Test300!@#$', newPassword='Test300!@#')
            time.sleep(1)
            ameyo.user_logout(sessionId=ameyo.supervisorToken)
            time.sleep(1)
            ameyo.supervisorToken = ameyo.user_login(userId=f"{admin_created_users_list[0]['name']}",
                                                    token='Test300!@#').json()['userSessionInfo']['sessionId']

        if ameyo.groupAdminToken is None:
            ameyo.groupAdminToken = ameyo.user_login(userId=f"{admin_created_users_list[1]['name']}",
                                                    token='Test300!@#$').json()['userSessionInfo']['sessionId']
            time.sleep(1)
            ameyo.get_password_policy_for_user(sessionId=ameyo.groupAdminToken,
                                               userId=f"{admin_created_users_list[1]['name']}").json()
            ameyo.change_password(sessionId=ameyo.groupAdminToken, userId=f"{admin_created_users_list[1]['name']}",
                                  oldPassword='Test300!@#$', newPassword='Test300!@#')
            time.sleep(1)
            ameyo.user_logout(sessionId=ameyo.groupAdminToken)
            time.sleep(1)
            ameyo.groupAdminToken = ameyo.user_login(userId=f"{admin_created_users_list[1]['name']}",
                                                    token='Test300!@#').json()['userSessionInfo']['sessionId']
            # time.sleep(1)
            # ameyo.user_logout(sessionId=ameyo.groupAdminToken)

    def test_07_verify_all_user_assigned_to_cc(self, ameyo, calling):
        """
        Verify that all users are assigned to CC
        :param ameyo:
        :return:
        """
        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        admin_created_users_list = calling['test_data']['admin_created_users']
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        ccUsers = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        for admin_created_user in admin_created_users_list:
            userId = f"{admin_created_user['name']}"
            if userId not in [x['userId'] for x in ccUsers]:
                raise Exception(f"User {userId} not assigned to CC")
        for multi_cc_created_users in multi_cc_created_users_list:
            userId = f"{multi_cc_created_users['name']}"
            if userId not in [x['userId'] for x in ccUsers]:
                raise Exception(f"User {userId} not assigned to CC")

    def test_08_update_the_break_reasons(self, ameyo, calling):
        """
        Update the break reasons for a cc
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        breakReasons = ['Lunch', 'Break', 'Snack', 'Training']
        # for _ in range(1, 3):
        #     breakReasons.append(f"BREAK_REASON_{_}")
        response = ameyo.update_break_reasons(breakReasons=breakReasons, sessionId=ameyo.adminToken).json()
        assert response["contactCenterId"] == ccId, "Failed to update break reasons"

    def test_09_update_knowledge_base_url(self, ameyo, calling):
        """
        Update the knowledge_base_url for a cc
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        response = ameyo.update_knowledge_base_url(knowledge_base_url='https://www.ameyo.com',
                                                   sessionId=ameyo.adminToken).json()
        assert response["contactCenterId"] == ccId, "Failed to update knowledge base url"

    def test_10_assign_call_contexts_to_cc(self, ameyo, calling):
        """
        Assign Call Contexts to Contact Center
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
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
        assigned = ameyo.assign_call_contexts_to_cc(contactCenterId=ccId, callContexts=callContexts,
                                                    sessionId=ameyo.adminToken).json()
        assigned = {x['callContextId'] for x in assigned['contactCenterCallContextBeans']}
        if len({x['callContextId'] for x in callContexts}.intersection(assigned)) != len(callContexts):
            raise Exception(f"Some Call Context not assigned !!")

        # Verify Call Contexts in Get Call
        response = ameyo.get_cc_call_contexts(sessionId=ameyo.adminToken)
        assigned = {x['callContextId'] for x in response.json()}
        if len({x['callContextId'] for x in callContexts}.intersection(assigned)) != len(callContexts):
            raise Exception(f"Some Call Context not assigned !!")

    def test_11_create_table_definition(self, ameyo, calling):
        """
        Create Table Definitions
        :param ameyo:
        :return:
        """
        tableDefinitionName = f"{calling['ccname']}_TABLE_DEFINITION"
        tds = ameyo.get_table_definitions(sessionId=ameyo.adminToken).json()
        TableDefinitions = [x for x in tds if x['tableDefinitionName'] == tableDefinitionName]
        if len(TableDefinitions) > 0:
            pytest.skip(msg=f'Table Definition {tableDefinitionName} already Exists !!')

        ameyo.create_table_definitions(**{
            'tableDefinitionName': tableDefinitionName,
            'columns': [
                {'columnName': 'name', 'nullable': True, 'displayName': 'name'},
                {'columnName': 'phone1', 'unique': True, 'primaryKey': False, 'isMaskable': True,
                 'displayName': 'phone1'},
                {'columnName': 'phone2', 'nullable': True, 'displayName': 'phone2'},
                {'columnName': 'phone3', 'nullable': True, 'displayName': 'phone3'},
                {'columnName': 'email', 'nullable': True, 'unique': True, 'displayName': 'email'},
                {'columnName': 'timezone', 'nullable': True, 'displayName': 'timezone'},
                {'columnName': 'priority', 'nullable': True, 'displayName': 'priority', 'columnType': 0, },
            ],
            'sessionId': ameyo.adminToken,
        })

        # Verify Table Definition is Created
        tableDefinitions = ameyo.get_table_definitions(sessionId=ameyo.adminToken).json()
        if tableDefinitionName not in [x['tableDefinitionName'] for x in tableDefinitions]:
            raise Exception(f"Failed to Create Table Definition !!")

    def test_12_create_agent_table_definitions(self, ameyo, calling):
        """
        Create agent table definition
        :param ameyo:
        :return:
        """
        for count, TableDefinition in enumerate(ameyo.get_table_definitions(sessionId=ameyo.adminToken).json(),
                                                start=1):
            name = f"{calling['ccname']}_AGENT_TABLE_DEFINITION_{count:03}"
            tableDefinitionId = TableDefinition['tableDefinitionId']

            # Skip if Table Definitions already Exist
            tds = ameyo.get_agent_table_definitions(tableDefinitionId=tableDefinitionId,
                                                    sessionId=ameyo.adminToken).json()
            for td in tds:
                if td['agentTableDefinitionName'] == name:
                    break

            if len([x for x in tds if x['agentTableDefinitionName'] == name]) > 0:
                pytest.skip(msg=f'Agent Table Definition {name} already Exists !!')

            ameyo.create_agent_table_definitions(**{
                'name': name,
                'tableDefinitionId': tableDefinitionId,
                'columnDefinitionIds': [y['columnId'] for x, y in TableDefinition['columnDefinitionsMap'].items()],
                'sessionId': ameyo.adminToken,
            })

            # Verify Json Structure
            atds = ameyo.get_agent_table_definitions(tableDefinitionId=tableDefinitionId,
                                                     sessionId=ameyo.adminToken).json()
            if name not in [x['agentTableDefinitionName'] for x in atds]:
                raise Exception(f"Agent Table Definition: {name} not Found !!")

    def test_13_create_table_mappings(self, ameyo, calling):
        """
        Create Table Mappings
        :param ameyo:
        :return:
        """
        toSkip = ['Video Chat Campaign', 'Interaction Campaign']
        campaigns = ameyo.get_all_campaign_types(sessionId=ameyo.adminToken).json()
        campaigns = [x for x in campaigns if x['campaignTypeName'] not in toSkip]

        for count, TableDefinition in enumerate(ameyo.get_table_definitions(sessionId=ameyo.adminToken).json(),
                                                start=1):
            for campaign in campaigns:
                columnMappingName = f"{calling['ccname']}_" + str(campaign['campaignTypeName']).replace(" ",
                                                                                                        "_").upper()
                columnMappingName = columnMappingName.replace("_", "") + f"{count:02}"
                existing = ameyo.get_all_column_mappings(tableDefinitionId=TableDefinition['tableDefinitionId'],
                                                         sessionId=ameyo.adminToken).json()
                if len(existing) > 0 and columnMappingName in [y['columnMappingName'] for y in existing]:
                    continue

                ameyo.create_table_column_mapping(**{
                    'columnMappingName': columnMappingName,
                    'campaignType': campaign['campaignTypeName'],
                    'tableDefinitionId': TableDefinition['tableDefinitionId'],
                    'campaignMappings': campaign['columnMappingAttributes'],
                    'sessionId': ameyo.adminToken,
                })

                mappings = ameyo.get_all_column_mappings(tableDefinitionId=TableDefinition['tableDefinitionId'],
                                                         sessionId=ameyo.adminToken).json()
                if columnMappingName not in [x['columnMappingName'] for x in mappings]:
                    raise Exception(f"Table Mapping {columnMappingName} not created !!")

    def test_14_create_process(self, ameyo, calling):
        """
        Create Process
        :param ameyo:
        :return:
        """

        process_names_list = calling['test_data']['process_names']

        for process_name in process_names_list:
            ameyo.create_process(processName=process_name, sessionId=ameyo.adminToken)
            processes = ameyo.get_all_processes(sessionId=ameyo.adminToken).json()
            if process_name not in [x['processName'] for x in processes]:
                raise Exception(f"Process {process_name} not Found !!")

        processIds = []
        for Process in ameyo.get_all_processes(sessionId=ameyo.adminToken).json():
            processIds.append(Process['processId'])
        calling.update({'processIds': processIds})

    def test_15_update_process_crm_settings(self, ameyo):
        """
        Update Process
        :param ameyo:
        :return:
        """
        for _, Process in enumerate(ameyo.get_all_processes(sessionId=ameyo.adminToken).json()):
            response = ameyo.get_process_crm_settings(**{
                'processId': Process['processId'],
                'toFail': False,
                'sessionId': ameyo.adminToken,
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

            ameyo.update_process_crm_settings(processId=Process['processId'], sessionId=ameyo.adminToken)

    def test_16_init_process_td(self, ameyo):
        """
        Init Process
        :param ameyo:
        :return:
        """
        for _, Process in enumerate(ameyo.get_all_processes(sessionId=ameyo.adminToken).json()):
            for td in ameyo.get_table_definitions(sessionId=ameyo.adminToken).json():
                ameyo.initialize_process_td(**{
                    'processName': Process['processName'],
                    'processId': Process['processId'],
                    'tableDefinitionId': td['tableDefinitionId'],
                    'sessionId': ameyo.adminToken,
                })

    def test_17_create_campaigns(self, ameyo, calling):
        """
        Create Campaign
        :param ameyo:
        :return:
        """

        process_ids_list = sorted(calling['processIds'])
        inbound_campaigns_list = calling['test_data']['inbound_campaigns']
        outbound_campaigns_list = calling['test_data']['outbound_campaigns']
        preview_dial_campaigns_list = calling['test_data']['preview_dial_campaigns']
        predictive_dial_campaigns_list = calling['test_data']['predictive_dial_campaigns']
        progressive_dial_campaigns_list = calling['test_data']['progressive_dial_campaigns']
        group_manager_campaigns_list = calling['test_data']['group_manager_campaigns']
        interaction_campaigns_list = calling['test_data']['interaction_campaigns']
        proc_inbound_campgn_dict = dict(zip(process_ids_list, inbound_campaigns_list))
        proc_outbound_campgn_dict = dict(zip(process_ids_list, outbound_campaigns_list))
        proc_preview_dial_campgn_dict = dict(zip(process_ids_list, preview_dial_campaigns_list))
        proc_predictive_dial_campgn_dict = dict(zip(process_ids_list, predictive_dial_campaigns_list))
        proc_progressive_dial_campgn_dict = dict(zip(process_ids_list, progressive_dial_campaigns_list))
        proc_group_manager_campgn_dict = dict(zip(process_ids_list, group_manager_campaigns_list))
        proc_interaction_campgn_dict = dict(zip(process_ids_list, interaction_campaigns_list))
        campaignIds = []
        grpCampaignIds = []
        # campaign_type_interaction
        for process_id, campaign_name in proc_interaction_campgn_dict.items():
            campaignName = f"{campaign_name}"
            response = ameyo.create_campaign(**{
                "processId": process_id,
                "campaignType": calling['test_data']['campaign_type_interaction'],
                "campaignName": campaignName,
                "description": f"{campaignName} Description",
            })
            grpCampaignId = response.json()['campaignId']
            grpCampaignIds.append(grpCampaignId)

            Campaigns = ameyo.get_all_campaigns().json()
            if campaignName not in [x['campaignName'] for x in Campaigns]:
                raise Exception(f"Campaign {campaignName} is not Present !!")
        for process_id, campaign_name in proc_group_manager_campgn_dict.items():
            campaignName = f"{campaign_name}"
            response = ameyo.create_campaign(**{
                "processId": process_id,
                "campaignType": calling['test_data']['campaign_type_outbound'],
                "campaignName": campaignName,
                "description": f"{campaignName} Description",
            })
            grpCampaignId = response.json()['campaignId']
            grpCampaignIds.append(grpCampaignId)

            Campaigns = ameyo.get_all_campaigns().json()
            if campaignName not in [x['campaignName'] for x in Campaigns]:
                raise Exception(f"Campaign {campaignName} is not Present !!")
        for process_id, campaign_name in proc_inbound_campgn_dict.items():
            campaignName = f"{campaign_name}"
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
        for process_id, campaign_name in proc_preview_dial_campgn_dict.items():
            campaignName = f"{campaign_name}"
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
        for process_id, campaign_name in proc_predictive_dial_campgn_dict.items():
            campaignName = f"{campaign_name}"
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
        for process_id, campaign_name in proc_progressive_dial_campgn_dict.items():
            campaignName = f"{campaign_name}"
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
        calling.update({'grpCampaignIds': grpCampaignIds})

    def test_18_assign_call_contexts_to_campaign(self, ameyo, calling):
        """
        Assign all Call Contexts to a Given Campaign
        25-03 - Assigning call contexts(which starts with customer i.e. customer_success_*, customer_notreachable*) to campaigns
        1 cc to 1 campaign
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        CallContexts = list(filter(
            lambda a: a['callContextName'] is not None and 'customer_' in a['callContextName'],
            ameyo.get_cc_call_contexts(sessionId=ameyo.adminToken).json()
        ))
        for Count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            CallContext = CallContexts[Count % len(CallContexts)]
            ameyo.logger.info(
                f"Assigning <{CallContext['callContextName']}> "
                f"to <{Campaign['campaignName']}> with id <{Campaign['campaignId']}>")
            for assigned in ameyo.get_call_contexts_in_campaign(campaignId=Campaign['campaignId'],
                                                                sessionId=ameyo.adminToken).json():
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
                    'sessionId': ameyo.adminToken,
                })

                ameyo.get_call_contexts_in_campaign(campaignId=Campaign['campaignId'],
                                                    sessionId=ameyo.adminToken)

    def test_19_create_routing_policy_for_campaign(self, ameyo, calling):
        """
        Create Routing Policy for a Campaign
        :param ameyo:
        :return:
        """

        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            policyName = f"{Campaign['campaignName']}_ROUTING_POLICY".upper()
            policies = ameyo.get_routing_policies_for_campaign(campaignId=Campaign['campaignId'],
                                                               sessionId=ameyo.adminToken).json()
            if policyName in [x['policyName'] for x in policies]:
                policy = [x for x in policies if x['policyName'] == policyName][0]
                ameyo.delete_routing_policy(policyId=policy['policyId'], sessionId=ameyo.adminToken)
                ameyo.logger.debug(f"Routing Policy {policyName} already Exists, thus deleted !!")

            campaignCallContextIds = []
            for callContext in ameyo.get_call_contexts_in_campaign(campaignId=Campaign['campaignId'],
                                                                   sessionId=ameyo.adminToken).json():
                campaignCallContextIds.append(callContext['campaignCallContextId'])

            if Campaign['campaignName'] not in calling['test_data']['interaction_campaigns']:
                ameyo.create_routing_policy_for_campaign(**{
                    'policyName': policyName,
                    'campaignId': Campaign['campaignId'],
                    'campaignCallContextIds': campaignCallContextIds,
                    'policyType': "basic.single.call.context.type",
                    'sessionId': ameyo.adminToken,
                })
            time.sleep(1)
            # response = ameyo.get_routing_policies_for_campaign(campaignId=Campaign['campaignId'],
            #                                                    sessionId=ameyo.adminToken)
            # if policyName not in [x['policyName'] for x in response.json()]:
            #     raise Exception(f"Routing Policy {policyName} Not Found !!")

    def test_20_update_dial_profiles(self, ameyo, calling):
        """
        Update Dial Profiles
        :param ameyo:
        :return:
        """
        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            if Campaign['campaignName'] not in calling['test_data']['interaction_campaigns']:
                RoutingPolicy = random.choice(
                    ameyo.get_routing_policies_for_campaign(campaignId=Campaign['campaignId'],
                                                            sessionId=ameyo.adminToken).json()
                )
                # Manual Dial Profiles
                ameyo.update_manual_dial_profile(**{
                    'campaignId': Campaign['campaignId'],
                    'policyId': RoutingPolicy['policyId'],
                    'sessionId': ameyo.adminToken,
                })

                # Conference Dial Profiles
                ameyo.update_conference_dial_profile(**{
                    'campaignId': Campaign['campaignId'],
                    'policyId': RoutingPolicy['policyId'],
                    'sessionId': ameyo.adminToken,
                })

                # Auto Dial Profiles
                if Campaign['campaignType'] != calling['test_data']['campaign_type_inbound']:
                    ameyo.update_auto_dial_profile(campaignId=Campaign['campaignId'],
                                                   policyId=RoutingPolicy['policyId'],
                                                   sessionId=ameyo.adminToken)
                else:
                    pass
            else:
                pass

    def test_21_update_default_atd_for_campaign(self, ameyo):
        """
        Updated Default Agent Table Definition for Campaign
        :param ameyo:
        :return:
        """
        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            for td in ameyo.get_table_definitions(sessionId=ameyo.adminToken).json():
                tableDefinitionId = td['tableDefinitionId']
                for _, atd in enumerate(ameyo.get_agent_table_definitions(tableDefinitionId=tableDefinitionId,
                                                                          sessionId=ameyo.adminToken).json()):
                    ameyo.update_default_atd_for_campaign(**{
                        'atdId': atd['agentTableDefinitionId'],
                        'campaignId': Campaign['campaignId'],
                        'sessionId': ameyo.adminToken,
                    })
                    return

    def test_22_set_column_mapping_for_campaign(self, ameyo):
        """
        Set Column Mapping for Campaign
        :param ameyo:
        :return:
        """
        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            for td in ameyo.get_table_definitions(sessionId=ameyo.adminToken).json():
                for tm in ameyo.get_all_column_mappings(tableDefinitionId=td['tableDefinitionId'],
                                                        sessionId=ameyo.adminToken).json():
                    if tm['campaignType'] != Campaign['campaignType']:
                        continue
                    response = ameyo.set_column_mapping_for_campaign(**{
                        'columnMappingId': tm['columnMappingId'],
                        'campaignId': Campaign['campaignId'],
                        'sessionId': ameyo.adminToken,
                    })
                    assert response.text == 'ok', "Failed to set Column Mapping for Campaign"

    def test_23_assign_supervisor_to_campaign(self, ameyo, calling):
        """
        Assign Supervisor user to Campaign
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        users = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                    sessionId=ameyo.adminToken)
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
                'sessionId': ameyo.adminToken,
            })

            # validate users assigned to campaign
            returnedusers = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                         sessionId=ameyo.adminToken).json()
            returneduserids = [returneduser['userId'] for returneduser in returnedusers]
            assert (len(userIds) == len(returneduserids) and sorted(userIds) == sorted(returneduserids))

    def test_24_create_disposition_class(self, ameyo, calling):
        """
        Create Disposition Class
        :param ameyo:
        :return:
        """
        dp_cls_name = f"{calling['ccname']}_D_CLASS"
        Classes = ameyo.get_disposition_classes(sessionId=ameyo.adminToken).json()
        for Class in Classes:
            if Class['dispositionClassName'] == dp_cls_name and Class['dispositionClassId'] > 0:
                break
        else:
            ameyo.create_disposition_class(dispositionClassName=dp_cls_name, dispositionCodes=[],
                                           sessionId=ameyo.adminToken)

            # Verify the created Class is there
            Classes = ameyo.get_disposition_classes(sessionId=ameyo.adminToken).json()
            for Class in Classes:
                if Class['dispositionClassName'] == dp_cls_name and Class['dispositionClassId'] > 0:
                    break
            else:
                raise Exception(f"dispositionClassName {dp_cls_name} Not Found !!")

    def test_25_add_disposition_codes_to_dp_class(self, ameyo, calling):
        """
        Add Disposition Codes to Disposition Class
        :param ameyo:
        :return:
        """
        dp_cls_name = f"{calling['ccname']}_D_CLASS"

        for dpClass in ameyo.get_disposition_classes(sessionId=ameyo.adminToken).json():
            if dpClass['dispositionClassName'] == dp_cls_name and dpClass['dispositionClassId'] > 0:
                break
        else:
            raise Exception(f"dispositionClass {dp_cls_name} Not Found !!")

        dp_code_name = f"{calling['ccname']}_D_CODE_1"
        Codes = ameyo.get_disposition_codes(sessionId=ameyo.adminToken).json()
        for Code in Codes:
            if dp_code_name == Code['dispositionCodeName']:
                break
        else:
            ameyo.create_disposition_code(**{
                'dispositionCodeName': dp_code_name,
                'dispositionClassId': dpClass['dispositionClassId'],
                'sessionId': ameyo.adminToken,
            })

        Codes = ameyo.get_disposition_codes(sessionId=ameyo.adminToken).json()
        for Code in Codes:
            if dp_code_name == Code['dispositionCodeName']:
                break
        else:
            raise Exception(f"dispositionCodeName {dp_code_name} Not Found !!")

    def test_26_add_disposition_codes_for_callback(self, ameyo):
        """
        Add Disposition Codes for callback
        :param ameyo:
        :return:
        """
        dp_cls_name = f"schedule.callback"

        for dpClass in ameyo.get_disposition_classes(sessionId=ameyo.adminToken).json():
            if dpClass['dispositionClassName'] == dp_cls_name and dpClass['dispositionClassId'] > 0:
                break
        else:
            raise Exception(f"dispositionClass {dp_cls_name} Not Found !!")

        dp_code_name = f"callback"
        Codes = ameyo.get_disposition_codes(sessionId=ameyo.adminToken).json()
        for Code in Codes:
            if dp_code_name == Code['dispositionCodeName']:
                break
        else:
            ameyo.create_disposition_code(**{
                'dispositionCodeName': dp_code_name,
                'dispositionClassId': dpClass['dispositionClassId'],
                'sessionId': ameyo.adminToken,
            })

        Codes = ameyo.get_disposition_codes(sessionId=ameyo.adminToken).json()
        for Code in Codes:
            if dp_code_name == Code['dispositionCodeName']:
                break
        else:
            raise Exception(f"dispositionCodeName {dp_code_name} Not Found !!")

    def test_27_create_disposition_plan_from_dp_class_and_code(self, ameyo, calling):
        """
        Create Disposition Plan from Disposition Class and Code
        :param ameyo:
        :return:
        """
        Codes = list(filter(lambda a: a['dispositionCodeId'] > 0,
                            ameyo.get_disposition_codes(sessionId=ameyo.adminToken).json()))
        dpp_name = f"{calling['ccname']}_D_PLAN"
        Plans = ameyo.get_disposition_plans(sessionId=ameyo.adminToken).json()
        for Plan in Plans:
            if dpp_name == Plan['dispositionPlanName']:
                pytest.skip(msg=f'dispositionPlan {dpp_name} already exists !!')

        ameyo.create_disposition_plan(**{
            'dispositionPlanName': dpp_name,
            'dispositionCodeIds': list({x['dispositionCodeId'] for x in Codes}),
            'sessionId': ameyo.adminToken,
        })

    def test_28_assign_disposition_plan_to_campaign(self, ameyo, calling):
        """
        Assign Disposition Plan to Campaign
        :param ameyo:
        :return:
        """
        dp_plan_name = f"{calling['ccname']}_D_PLAN"
        for dpp in ameyo.get_disposition_plans(sessionId=ameyo.adminToken).json():
            if dp_plan_name == dpp['dispositionPlanName']:
                break
        else:
            raise Exception(f"{dp_plan_name} Disposition Plan Not Found !!")

        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            dispositionPlanId = dpp['dispositionPlanId']
            campaignId = Campaign['campaignId']
            ameyo.assign_disposition_plan_to_campaign(dispositionPlanId=dispositionPlanId, campaignId=campaignId,
                                                      sessionId=ameyo.adminToken)

    def test_29_create_new_lead(self, ameyo, calling):
        """
        Create a new Lead
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['ccname']} not found !!")

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Supervisor'],
            ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        ))

        for Process in ameyo.get_all_processes(sessionId=ameyo.adminToken).json():
            leadName = f"{Process['processName']}_LEAD"
            for lead in ameyo.get_all_leads_for_process(processId=Process['processId'],
                                                        sessionId=ameyo.adminToken).json():
                if lead['leadName'] == leadName:
                    ameyo.logger.debug(f"Lead Already Exists !!")
                    break
            else:
                for user in Users:
                    ameyo.add_lead(**{
                        'leadName': leadName,
                        'processId': Process['processId'],
                        'ownerUserId': user['userId'],
                        'sessionId': ameyo.adminToken,
                    })
                    break  # One Lead Per Process

                for lead in ameyo.get_all_leads_for_process(processId=Process['processId'],
                                                            sessionId=ameyo.adminToken).json():
                    if lead['leadName'] == leadName:
                        break
                else:
                    raise Exception(f"New Created Lead not Found !!")

    def test_30_assign_lead_to_campaign(self, ameyo):
        """
        Assign Lead to Campaign
        :param ameyo:
        :return:
        """
        for Campaign in ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json():
            Leads = ameyo.get_all_leads_for_process(processId=Campaign['processId'],
                                                    sessionId=ameyo.adminToken).json()
            leadIds = []
            for Lead in Leads:
                if Campaign['campaignId'] in Lead['campaignContextIds']:
                    continue
                else:
                    leadIds.append(Lead['leadId'])
                    # # upload new customer data in lead
                    # data = ameyo.create_customer_data_to_upload(count=50)
                    # data.update({'campaignId': Campaign['campaignId']})
                    # data.update({'leadId': Lead["leadId"]})
                    # response = ameyo.upload_contacts(data=data)

            if len(leadIds) > 0:
                ameyo.assign_lead_to_campaign(campaignContextId=Campaign['campaignId'], leadIds=leadIds,
                                              sessionId=ameyo.adminToken)

    # def test_31_upload_lead_csv(self, ameyo):
    #     """
    #     Uploads a csv (containing customer data) to the lead
    #     :param ameyo:
    #     :param request:
    #     :return:
    #     """
    #     for Process in ameyo.get_all_processes().json():
    #         for Lead in ameyo.get_all_leads_for_process(processId=Process['processId']).json():
    #             csvPath = ameyo.create_customer_csv(count=50)
    #             response = ameyo.upload_csv_to_lead(**{
    #                 "processId": Lead['processId'],
    #                 "leadIds": Lead['leadId'],
    #                 'csvPath': csvPath
    #             })
    #             assert "failed" not in response.text.lower(), "Upload Failed !!"
    #             assert "invalid" not in response.text.lower(), "Upload File is Invalid !!"

    def test_31_enable_lead_for_process(self, ameyo):
        """
        Enables lead for a process
        :param ameyo:
        :param request:
        :return:
        """
        for Process in ameyo.get_all_processes(sessionId=ameyo.adminToken).json():
            for Lead in ameyo.get_all_leads_for_process(processId=Process['processId'],
                                                        sessionId=ameyo.adminToken).json():
                response = ameyo.enable_lead_for_process(**{
                    "leadId": Lead['leadId'],
                    "enabled": True,
                    'sessionId': ameyo.supervisorToken,
                })

    def test_32_enable_lead_for_campaign(self, ameyo):
        """
        Enables lead for a campaign
        :param ameyo:
        :param request:
        :return:
        """
        for Process in ameyo.get_all_processes(sessionId=ameyo.adminToken).json():
            for Campaign in ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json():
                for Lead in ameyo.get_all_leads_for_campaign(processId=Process['processId'],
                                                             campaignId=Campaign['campaignId'],
                                                             sessionId=ameyo.supervisorToken).json()[
                    'leadManagementContactLeadListBeans']:
                    leadName = Lead["leadName"]
                    campaignLeadId = Lead["campaignLeadId"]
                    leadDialingConfigurationEnabled = True
                    response = ameyo.enable_lead_for_campaign(**{
                        "leadId": Lead['leadId'],
                        "leadName": leadName,
                        "campaignLeadId": campaignLeadId,
                        "campaignId": Campaign['campaignId'],
                        "leadDialingConfigurationEnabled": leadDialingConfigurationEnabled,
                        "sessionId": ameyo.supervisorToken,
                    })
                    leads = ameyo.get_all_leads_for_campaign(processId=Process['processId'],
                                                             campaignId=Campaign['campaignId'],
                                                             sessionId=ameyo.supervisorToken).json()[
                        'leadManagementContactLeadListBeans']
                    lead = [x for x in leads if x["leadName"] == leadName][0]
                    assert lead[
                        "isEnable"], f"Lead <{Lead['leadName']}> can not be enabled for <{Campaign['campaignName']}>"

    def test_33_set_dialer_settings_in_campaigns(self, ameyo, calling):
        """
        Set dialer settings in campaigns
        :param ameyo:
        :return:
        """
        for Campaign in ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json():
            if Campaign['campaignName'] in calling['test_data']['predictive_dial_campaigns']:
                ameyo.set_outbound_voice_campaign_setting(campaignId=Campaign['campaignId'],
                                                          dialerAlgoType="Predictive")
                ameyo.set_predictive_algo_setting(campaignId=Campaign['campaignId'],
                                                  maxPacingRatio=4,
                                                  callDropRatio=50,
                                                  peakCallCount=4)
                response = ameyo.get_outbound_voice_campaign_setting(campaignId=Campaign['campaignId'])
                assert response.json()["dialerAlgoType"] == "Predictive", f"Dialer Algo could not be set" \
                                                                          f" to Predictive.{response.text}"
                # response = ameyo.enable_auto_dial(campaignId=Campaign['campaignId'])
                # if isinstance(response, bool):
                #     assert response, "Auto dial can not be enabled"
                # else:
                #     assert response.ok, f"Auto dial can not be enabled !! {response.text}"
            elif Campaign['campaignName'] in calling['test_data']['progressive_dial_campaigns']:
                ameyo.set_outbound_voice_campaign_setting(campaignId=Campaign['campaignId'],
                                                          dialerAlgoType="Progressive")
                ameyo.set_progressive_algo_setting(campaignId=Campaign['campaignId'])
                response = ameyo.get_outbound_voice_campaign_setting(campaignId=Campaign['campaignId'])
                assert response.json()[
                           "dialerAlgoType"] == "Progressive", \
                    f"Dialer Algo could not be set to Progressive.{response.text}"
                # response = ameyo.enable_auto_dial(campaignId=Campaign['campaignId'])
                # if isinstance(response, bool):
                #     assert response, "Auto dial can not be enabled"
                # else:
                #     assert response.ok, f"Auto dial can not be enabled !! {response.text}"
            elif Campaign['campaignName'] in calling['test_data']['preview_dial_campaigns']:
                ameyo.set_outbound_voice_campaign_setting(campaignId=Campaign['campaignId'],
                                                          dialerAlgoType="Preview")
                ameyo.set_preview_algo_setting(campaignId=Campaign['campaignId'])
                response = ameyo.get_outbound_voice_campaign_setting(campaignId=Campaign['campaignId'])
                assert response.json()[
                           "dialerAlgoType"] == "Preview", \
                    f"Dialer Algo could not be set to Preview.{response.text}"
                # response = ameyo.enable_auto_dial(campaignId=Campaign['campaignId'])
                # if isinstance(response, bool):
                #     assert response, "Auto dial can not be enabled"
                # else:
                #     assert response.ok, f"Auto dial can not be enabled !! {response.text}"
            else:
                pass

    def test_34_create_agents(self, ameyo, calling):
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
        # 'userId', 'userType', 'assigned', 'contactCenterUserId', 'skillLevelIds', 'systemUserType',
        # 'privilegePlanId', 'maskedPrivileges', 'processUserIds', 'contactCenterTeamIds', 'userBusinessMetadata',
        # 'contactCenterId', 'defaultReady', 'extensions', 'root', 'description', 'userName'
        for agent in calling['test_data']['agents']:
            response = ameyo.create_user(**{
                'userId': agent, 'userName': agent, 'userType': 'Executive', 'contactCenterId': ccId,
                'password': 'Test300!@#$',
            }).json()
            agents.append(response)
        calling.update({'agents': agents})

        # Create a new user
        group_agents = []
        # 'userId', 'userType', 'assigned', 'contactCenterUserId', 'skillLevelIds', 'systemUserType',
        # 'privilegePlanId', 'maskedPrivileges', 'processUserIds', 'contactCenterTeamIds', 'userBusinessMetadata',
        # 'contactCenterId', 'defaultReady', 'extensions', 'root', 'description', 'userName'
        for agent in calling['test_data']['group_agents']:
            response = ameyo.create_user(**{
                'userId': agent, 'userName': agent, 'userType': 'Executive', 'contactCenterId': ccId,
                'password': 'Test300!@#$',
            }).json()
            group_agents.append(response)
        calling.update({'group_agents': group_agents})

    def test_35_change_password(self, ameyo, calling):
        """
        Change Executive Agent Password
        :param ameyo:
        :return:
        """
        inbound_campaigns_list = calling['test_data']['inbound_campaigns']
        agents_list = calling['test_data']['agents']
        group_agents_list = calling['test_data']['group_agents']
        campgn_agents_dict = dict(zip(inbound_campaigns_list, agents_list))

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['test_data']['ccn']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['test_data']['ccn']} not found !!")

        # Login agents and change passwords
        for agent in agents_list:
            ameyo.executiveToken = ameyo.user_login(userId=agent,
                                                    token='Test300!@#$').json()['userSessionInfo']['sessionId']
            time.sleep(1)
            ameyo.get_password_policy_for_user(sessionId=ameyo.executiveToken, userId=agent).json()
            ameyo.change_password(sessionId=ameyo.executiveToken, userId=agent,
                                  oldPassword='Test300!@#$', newPassword='Test300!@#')
            time.sleep(1)
            ameyo.user_logout(sessionId=ameyo.executiveToken)
            time.sleep(1)
            ameyo.executiveToken = ameyo.user_login(userId=agent,
                                                    token='Test300!@#').json()['userSessionInfo']['sessionId']
        else:
            pass

        # Login group agents and change passwords
        for agent in group_agents_list:
            ameyo.groupExecutiveToken = ameyo.user_login(userId=agent,
                                                    token='Test300!@#$').json()['userSessionInfo']['sessionId']
            time.sleep(1)
            ameyo.get_password_policy_for_user(sessionId=ameyo.groupExecutiveToken, userId=agent).json()
            ameyo.change_password(sessionId=ameyo.groupExecutiveToken, userId=agent,
                                  oldPassword='Test300!@#$', newPassword='Test300!@#')
            time.sleep(1)
            ameyo.user_logout(sessionId=ameyo.groupExecutiveToken)
            time.sleep(1)
            ameyo.groupExecutiveToken = ameyo.user_login(userId=agent,
                                                    token='Test300!@#').json()['userSessionInfo']['sessionId']
        else:
            pass

    def test_36_assign_user_to_campaigns(self, ameyo, calling):
        """
        Assign user to campaign
        25-03 - Assigning random number of agents to all campaigns
        :param ameyo:
        :return:
        """
        inbound_campaigns_list = calling['test_data']['inbound_campaigns']
        outbound_campaigns_list = calling['test_data']['outbound_campaigns']
        campaign_ids_list = calling['campaignIds']
        grp_campaign_ids_list = calling['grpCampaignIds']

        for campaign_id in campaign_ids_list:
            # unassign any user assigned to campaign
            assigned = ameyo.get_all_campaign_users(campaignId=campaign_id).json()
            ameyo.un_assign_agent_from_campaign(**{
                'campaignId': campaign_id,
                'campaignContextUserIds': [x['campaignUserId'] for x in assigned],
            })
            assigned = ameyo.get_all_campaign_users(campaignId=campaign_id).json()

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            # n = int(len(calling['agents']) / len(campaign_ids_list))
            # agents_lists = [calling['agents'][i * n:(i + 1) * n] for i in range((len(calling['agents']) + n - 1) // n)]
            for agent in calling['agents']:
                # if agent['userId'] not in [x['userId'] for x in assigned]
                # 'userId', 'userType', 'assigned', 'contactCenterUserId', 'skillLevelIds', 'systemUserType',
                # 'privilegePlanId', 'maskedPrivileges', 'processUserIds', 'contactCenterTeamIds', 'userBusinessMetadata',
                # 'contactCenterId', 'defaultReady', 'extensions', 'root', 'description', 'userName'
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
        for campaign_id in grp_campaign_ids_list:
            # unassign any user assigned to campaign
            assigned = ameyo.get_all_campaign_users(campaignId=campaign_id).json()
            ameyo.un_assign_agent_from_campaign(**{
                'campaignId': campaign_id,
                'campaignContextUserIds': [x['campaignUserId'] for x in assigned],
            })
            assigned = ameyo.get_all_campaign_users(campaignId=campaign_id).json()

            contactCenterUserIds, privilegePlanIds, userIds, contactCenterUserTypes = [], [], [], []
            # n = int(len(calling['agents']) / len(campaign_ids_list))
            # agents_lists = [calling['agents'][i * n:(i + 1) * n] for i in range((len(calling['agents']) + n - 1) // n)]
            for agent in calling['group_agents']:
                # if agent['userId'] not in [x['userId'] for x in assigned]
                # 'userId', 'userType', 'assigned', 'contactCenterUserId', 'skillLevelIds', 'systemUserType',
                # 'privilegePlanId', 'maskedPrivileges', 'processUserIds', 'contactCenterTeamIds', 'userBusinessMetadata',
                # 'contactCenterId', 'defaultReady', 'extensions', 'root', 'description', 'userName'
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

    def test_37_assign_grp_mngr_to_campaigns(self, ameyo, calling):
        """
        Assign grp manager to Campaigns
        :param ameyo:
        :return:
        """

        grp_campaign_ids_list = calling['grpCampaignIds']
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['ccname']} not found !!")

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Group Manager'],
            ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        ))

        for campaign_id in grp_campaign_ids_list:
        # for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            response = ameyo.get_all_campaign_users(campaignId=campaign_id,
                                                    sessionId=ameyo.adminToken)
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
                'campaignId': campaign_id,
                'contactCenterUserIds': contactCenterUserIds,
                'privilegePlanIds': privilegePlanIds,
                'userIds': userIds,
                'contactCenterUserTypes': contactCenterUserTypes,
                'sessionId': ameyo.adminToken,
            })

            # Get users assigned to campaign
            response = ameyo.get_all_campaign_users(campaignId=campaign_id,
                                                    sessionId=ameyo.adminToken)
            ameyo.logger.info(
                f"All {len(response.json())} users in <{campaign_id}> <{campaign_id}> {[x['userId'] for x in response.json()]}")

    def test_38_assign_supervisor_to_all_campaigns(self, ameyo, calling):
        """
        Assign Supervisor user to all Campaigns (required for supervisor monitoring)
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                ccId = cc['contactCenterId']
                break
        else:
            raise Exception(f"{calling['ccname']} not found !!")

        Users = list(filter(
            lambda a: a['systemUserType'] in ['Supervisor'],
            ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        ))

        for count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                    sessionId=ameyo.adminToken)
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
                'sessionId': ameyo.adminToken,
            })

            # Get users assigned to campaign
            response = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                    sessionId=ameyo.adminToken)
            ameyo.logger.info(
                f"All {len(response.json())} users in <{Campaign['campaignId']}> <{Campaign['campaignName']}> {[x['userId'] for x in response.json()]}")

    def test_39_assign_user_to_atd(self, ameyo):
        """
        Assign user to agent table definition
        :param ameyo:
        :return:
        """
        for td in ameyo.get_table_definitions(sessionId=ameyo.adminToken).json():
            for atd in ameyo.get_agent_table_definitions(tableDefinitionId=td['tableDefinitionId'],
                                                         sessionId=ameyo.adminToken).json():
                for Campaign in ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json():
                    assigned = ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                            sessionId=ameyo.adminToken).json()
                    ameyo.assign_user_to_atd(**{
                        'campaignId': Campaign['campaignId'],
                        'atdId': atd['agentTableDefinitionId'],
                        'userIds': [x['userId'] for x in assigned],
                        'sessionId': ameyo.adminToken,
                    })

    def test_40_create_queue(self, ameyo):
        """
        Create Queue
        :param ameyo:
        :return:
        """
        for Campaign in ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json():
            queueName = f"{Campaign['campaignName']}_QUEUE"
            response = ameyo.get_all_queue(campaignId=Campaign['campaignId'],
                                           sessionId=ameyo.adminToken).json()

            userIdList = []
            for user in ameyo.get_all_campaign_users(campaignId=Campaign['campaignId'],
                                                     sessionId=ameyo.adminToken).json():
                if user['user']['userType'] in ['Supervisor', 'Executive']:
                    userIdList.append(user['campaignUserId'])

            if len(response) > 0 and queueName in [x['queueName'] for x in response]:
                ameyo.logger.debug(f'Queue {queueName} already Present !!')
                continue

            response = ameyo.create_queue(**{
                'campaignId': Campaign['campaignId'],
                "queueName": queueName,
                "description": "Automation queue",
                "userIdList": userIdList,
                "sessionId": ameyo.adminToken,
            }).json()

            # verify the agent queue assign user
            users = ameyo.get_users_in_queue(agentQueueId=response['agentQueueId'],
                                             sessionId=ameyo.adminToken).json()
            for user in users:
                if user['agentQueueUserId'] not in response['userIdList']:
                    raise Exception("User not assigned in Queue !!")

    def test_41_update_queue(self, ameyo):
        """
        update queue data
        :param ameyo:
        :return:
        """
        for _, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            for Queue in ameyo.get_all_queue(campaignId=Campaign['campaignId'],
                                             sessionId=ameyo.adminToken).json():
                ameyo.update_queue_data(**{
                    "queueId": Queue['agentQueueId'],
                    "queueName": Queue['queueName'],
                    "description": f"Queue Updated By: {ameyo.faker.first_name()}",
                    "sessionId": ameyo.adminToken,
                }).json()

    def test_42_create_tpv(self, ameyo, calling):
        """
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        for Campaign in ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json():
            tpv_name = f"{calling['test_data']['tpv_name']}"
            tpv_number = f"{calling['test_data']['tpv_number']}"
            try:
                response = ameyo.create_tpv_info(thirdPartyName=tpv_name, thirdPartyPhone=tpv_number,
                                                 campaignId=Campaign['campaignId'],sessionId=ameyo.adminToken).json()
                time.sleep(1)
            except:
                pass

    def test_43_create_local_IVR(self, ameyo, calling):
        """
        :param ameyo:
        :return:
        """
        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']

        CallContexts = list(filter(
            lambda a: a['callContextName'] is not None and 'customer_' in a['callContextName'],
            ameyo.get_cc_call_contexts(sessionId=ameyo.adminToken).json()
        ))
        for Count, Campaign in enumerate(ameyo.get_all_campaigns(sessionId=ameyo.adminToken).json()):
            CallContext = CallContexts[Count % len(CallContexts)]
            ameyo.logger.info(
                f"Assigning <{CallContext['callContextName']}> "
                f"to <{Campaign['campaignName']}> with id <{Campaign['campaignId']}>")
            local_ivr_name = f"{calling['test_data']['local_ivr_name']}"
            ivr_src_number = f"{calling['test_data']['ivr_src_number']}"
            ivr_dst_number = f"{calling['test_data']['ivr_dst_number']}"
            if Campaign['campaignName'] not in calling['test_data']['interaction_campaigns']:
                ameyo.create_local_IVR(name=local_ivr_name,
                                       contactCenterCallContextId=CallContext['contactCenterCallContextId'],
                                       campaignId=Campaign['campaignId'],
                                       dstPhone=ivr_dst_number,
                                       srcPhone=ivr_src_number,
                                       desc="LocalIVR",
                                       sessionId=ameyo.adminToken).json()
                response = ameyo.get_all_local_IVR_for_campaign(campaignId=Campaign['campaignId'],
                                                                sessionId=ameyo.adminToken).json()
                ameyo.logger.info(f"response for  <{CallContext['callContextName']}> is {response} ")
            else:
                pass

    def test_44_create_group_and_assign_grp_manager(self, ameyo, calling):
        """
        Create group and assign group manager
        :param ameyo:
        :param role:
        :return:
        """

        multi_cc_created_users_list = calling['test_data']['multi_cc_created_users']
        group_name = calling['test_data']['group_name']
        group_manager_name = calling['test_data']['admin_created_users'][1]['name']
        adminId = calling['test_data']['multi_cc_created_users'][0]['name']
        group_desc = calling['test_data']['group_desc']
        group_agents = calling['test_data']['group_agents']

        for cc in ameyo.get_all_cc().json():
            if cc['contactCenterName'] == calling['ccname']:
                break
        else:
            raise Exception(f"Cannot Find CC {calling['ccname']} !!")
        ccId = cc['contactCenterId']
        ccGrpUserIds = []
        ccGrpMngrIds = []

        # ccUsers = ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()
        ccGrpUsers = list(filter(lambda a: a['userId'].startswith(f"{calling['ccname']}_GRP_"),
                            ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()))
        for ccGrpUser in ccGrpUsers:
            ccGrpUserId = ccGrpUser['ccUserId']
            ccGrpUserIds.append(ccGrpUserId)

        # ccGrpMngrs = list(filter(lambda a: a['userId'].startswith(f"{group_manager_name}"),
        #                          ameyo.get_all_users_assigned_to_cc(ccId=ccId, sessionId=ameyo.adminToken).json()))
        # for ccGrpMngr in ccGrpMngrs:
        #     ccGrpMngrId = ccGrpMngr['ccUserId']
        #     ccGrpMngrIds.append(ccGrpMngrId)

        ameyo.is_grouphierarchylicense_enabled()


        # create group
        response = ameyo.validate_and_create_group(userId=multi_cc_created_users_list[0]['name'],
                                                   ccManagerUserIds=group_manager_name,
                                                   name=group_name,
                                                   ccUserIds=ccGrpUserIds,
                                                   description=group_desc,
                                                   sessionId=ameyo.adminToken).json()
        time.sleep(2)

        # get all groups
        response = ameyo.get_all_available_groups(sessionId=ameyo.adminToken).json()

        for item in response:
            if item['name'] == group_name:
                ameyo.modify_group(sessionId=ameyo.adminToken,
                                   groupId=item['id'],
                                   userId=adminId,
                                   name=group_name,
                                   description=group_desc,
                                   assignUserIds=group_agents)
            else:
                pass

    def test_45_logout_users(self, ameyo, calling):
        """
        Logout
        :param ameyo:
        :return:
        """


        users = list(filter(lambda a: a['userID'].startswith(f"{calling['test_data']['ccn']}_"),
                            ameyo.get_all_users(sessionId=ameyo.ccManagerToken).json()))
        for user in users:
            userId = user['userID']
            ameyo.logger.info(f'Terminate User: {userId} ...')
            ameyo.terminate_all_sessions_for_user(userId=userId, sessionId=ameyo.ccManagerToken)

    def test_46_generate_yaml_test_data(self, ameyo, calling):
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