__author__ = "Developed by EA"

import yaml
from pathlib import Path
from ameyo.test_data_lib.lib import General, SendRestRequest


class Wrapper(General):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instance = kwargs.get('instance', None)
        self.noop = kwargs.get('noop', False)
        self.rest = SendRestRequest(name='AMEYO', noop=self.noop)

        self.creds = self.make_creds(
            url=kwargs.get('url', None),
            username=kwargs.get('username', None),
            password=kwargs.get('password', None)
        )

        self.raise_for_status = kwargs.get('raise_for_status', True)
        self.system_version = kwargs.get("system_version", None)
        # Set all Tokens to None (rest.py) will generate these
        self.adminToken, \
        self.supervisorToken, \
        self.ccManagerToken, \
        self.executiveToken, \
        self.voiceAdminToken = None, None, None, None, None
        self.logged_in_agents = dict()
        self.logged_in_agents_special = dict()
        self.executiveToken2 = None
        self.callId = None
        self.customerId = None
        self.tc_name = None
        self.skip_case = False
        self.is_auto_dial_enabled = False
        self.process_during_call_deleted = False
        self.webaccess_api_token = None

        self.SavedPushes = Path(__file__).parent.parent / 'PushesDump.yaml'
        with open(Path(__file__).parent.parent / 'PushSeq.yaml', "r") as fp:
            self.CustomerCx = yaml.safe_load(fp.read())
