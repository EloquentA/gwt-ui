__maintainer__ = ['anshuman.goyal']

import time
import json
import re

from urllib.parse import urljoin

from ameyo.test_data_lib.rest import AmeyoRest


class RestHelper(AmeyoRest):
    """
    RestHelper Class for Locust
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.ccn = kwargs.get('ccn', None)
        self.cxn = kwargs.get('cxn', None)
        self.call_context = None
        self.campaign = None
        if self.ccn is None:
            raise Exception(f"ccn name is mandatory !!")
        self.cc = [x for x in self.get_all_cc().json() if x['contactCenterName'] == self.ccn][0]

        # Update Admin Token
        userId = [x for x, _ in self.cc['contactCenterUserIds'].items() if 'ADMIN_USER' in x][0]
        self.adminToken = self.user_login(userId=userId, token='Test300!@#').json()['userSessionInfo']['sessionId']

        # Update Supervisor Token
        userId = [x for x, _ in self.cc['contactCenterUserIds'].items() if 'SUPERVISOR_USER' in x][0]
        self.supervisorToken = self.user_login(userId=userId, token='Test300!@#').json()['userSessionInfo']['sessionId']

        if self.cxn:
            self.ccUsers = self.get_agents_from_campaign_with_cxn(self.cxn)
        else:
            self.ccUsers = self.get_agents()
        self.count = 0

    def get_agents_from_campaign_with_cxn(self, cxn):
        """
        Get Executive/Agents that are in a campaign which has the desired call context
        :return:
        """
        # import pdb;pdb.set_trace();
        UsersInCampaign = []
        for campaign in self.get_all_campaigns().json():
            call_context = self.get_call_contexts_in_campaign(campaignId=campaign['campaignId']).json()[0]
            if call_context["callContextName"] == cxn:
                self.campaign = campaign
                self.call_context = call_context
                _users = [x['userId'] for x in self.get_all_campaign_users(campaignId=campaign['campaignId']).json()]
                UsersInCampaign.extend(_users)
                break

        Users = []
        for User in self.get_all_users_assigned_to_cc(ccId=self.cc['contactCenterId']).json():
            if User['userId'] not in UsersInCampaign:
                continue
            if User['userId'] in [x['userId'] for x in Users]:
                continue
            User.update({'token': 'Test300!@#'})
            if User['systemUserType'] in ['Executive']:
                Users.append(User)

        return sorted(Users, key=lambda a: a['userId'])

    def get_agents(self):
        """
        Get Executive/Agents that startswith
        :return:
        """
        UsersInCampaigns = []
        for campaign in self.get_all_campaigns().json():
            users = [x['userId'] for x in self.get_all_campaign_users(campaignId=campaign['campaignId']).json()]
            UsersInCampaigns.extend(users)

        Users = []
        for User in self.get_all_users_assigned_to_cc(ccId=self.cc['contactCenterId']).json():
            if User['userId'] not in UsersInCampaigns:
                continue
            if User['userId'] in [x['userId'] for x in Users]:
                continue
            User.update({'token': 'Test300!@#'})
            if User['systemUserType'] in ['Executive']:
                Users.append(User)

        return sorted(Users, key=lambda a: a['userId'])

    def push_params(self, sessionId):
        """
        Process Push Notifications
        :param sessionId:
        :return:
        """
        params = {
            'method': 'POST',
            'url': urljoin(self.creds.url, f'ameyorestapi/pushes'),
            'headers': {"sessionId": sessionId, },
            'params': {
                'listener-name': f'webcore_{round(time.time() * 1000)}',
                'lastProcessedPush': -1,
            },
            'stream': True,
            'timeout': 1,
        }
        return params

    @staticmethod
    def read_pushes(response):
        """
        Read Pushes from Response
        :param response:
        :return:
        """
        data = ''
        try:
            for chunk in response.iter_content(1024):
                data += chunk.decode()
        except (Exception, ValueError) as Exp:
            pass

        response = list(map(lambda a: json.loads(a), [x for x in re.findall(r'({.*})', data, re.I | re.M)]))
        response = list(filter(lambda a: a['pushType'] not in ['DefaultPush', 'VoiceBlockState'], response))
        return response

if __name__ == '__main__':
    c = RestHelper(
        url='https://fluidcxdemo.ameyo.com:8443', username='ANSHUMAN_MULTI_CC', password='ANSHUMAN_MULTI_CC',
        ccn='BULK_0001', level='ERROR'
    )
    print(c)
    # c.delete_stale_users()
