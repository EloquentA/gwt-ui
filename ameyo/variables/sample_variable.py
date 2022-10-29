PROJECT = "ameyo"
BROWSER_CONFIG = {
  "name": "chrome",
  "is_remote_driver": False,
  "server": "",
  "port": '',
}
SKIP_POST_RUN_CLEANUP = True
AMEYO_URL = "https://vapt.ameyo.net:8443/app/"
# Automatically updated to True if run triggered with testrail reporting
TESTRAIL_REPORTING = False
TESTRAIL_RUN_URL = "/index.php?/runs/view/{run_id}&group_by=cases:section_id&group_order=asc"
CLOSE_TESTRAIL_RUN = True
AUTOMATION_NAME = 'Ameyo UI Robot Automation Run'
RUN_AS = "executive"
CREDENTIALS = {
  "multi_cc_manager": {
    "username": '',
    "password": ''
  },
  "admin": {
    "username": '',
    "password": ''
  },
  "executive": {
    "username": '',
    "password": '',
    "campaign_details": {
          "interaction": '',
          "chat": '',
          "voice": '',
          "Video": '',
          "new_interaction": '',
          "new_chat": '',
          "new_voice": '',
          "new_video": ''
        }
  },
  "change_executive": {
    "username": '',
    "password": '',
    "campaign_details": {
      "interaction": '',
      "chat": '',
      "voice": '',
      "Video": '',
      "new_interaction": '',
      "new_chat": '',
      "new_voice": '',
      "new_video": ''
    }
  },
  "supervisor": {
    "username": '',
    "password": '',
    "campaign_details": {
      "interaction": '',
      "chat": '',
      "voice": '',
      "Video": ''
    },
  "call_back": {
      "callback_type": 'user',
      "user": 'rahul',
      "phone_number": "9988776655"
    },
    "call_details": {
      "user": "rahul"
    }
  }
}
CALLING_NUMBER = ""
DESIRED_STATE = ""
DISPOSITION = {
  'disposition': 'telecom.issues',
  'sub_disposition': 'Already hungup',
  'disposition_note': 'Automation dispose',
  'dial_number': '123456',
  'quick_disposition': 'Sale'
}
CALLBACK = {
  'disposition': 'schedule.callback',
  'sub_disposition': 'Callback',
  'disposition_note': 'Automation schedule',
  'specify_time': '00:00:10',
  'callback_type': 'self',
  'specify_date': ''
}
CALLBACK_DETAILS = {
  'campaign': 'finance_outbound',
  'actions': 'Reschedule'
}
CALL_HISTORY = {
  'campaign': 'finance_outbound',
  'disposition': 'select_all'
}
