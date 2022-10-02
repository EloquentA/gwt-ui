PROJECT = "ameyo"
BROWSER_CONFIG = {
  "name": "chrome",
  "is_remote_driver": False,
  "server": "",
  "port": '',
}
SKIP_POST_RUN_CLEANUP = True
AMEYO_URL = ""
# Automatically updated to True if run triggered with testrail reporting
TESTRAIL_REPORTING = False
TESTRAIL_RUN_URL = "/index.php?/runs/view/{run_id}&group_by=cases:section_id&group_order=asc"
CLOSE_TESTRAIL_RUN = True
AUTOMATION_NAME = 'Ameyo UI Robot Automation Run'
RUN_AS = "admin"
CREDENTIALS = {
  "admin":{
    "username": '<admin-email>',
    "password": '<admin-pass>',
    "is_mfa": False
  },
  "agent": {
    "username": '<agent-email>',
    "password": '<agent-pass>',
    "is_mfa": False
  },
  "supervisor": {
    "username": '<supervisor-email>',
    "password": '<supervisor-pass>',
    "is_mfa": False
  }
}
