"""Listener file to report test cases to testrail."""
import os
from TestrailUtils import AmeyoTestrail


class TestrailListener:
    """Listener class for test rail related operations."""
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(
            self,
            server_url='',
            testrail_username='',
            testrail_password='',
            project_id=2
    ):
        self.testrail_client = AmeyoTestrail(
            server_url=os.environ.get('SERVER_URL', server_url),
            username=os.environ.get('TESTRAIL_USER_NAME', testrail_username),
            password=os.environ.get('TESTRAIL_PASSWORD', testrail_password),
            project_id= int(os.environ.get('TESTRAIL_PROJECT_ID', project_id))
        )

    def start_suite(self, data, result):
        """Runs at start of each suite."""
        if not self.testrail_client.is_run_created():
            self.testrail_client.set_global_var('TESTRAIL_REPORTING', True)
            self.testrail_client.create_run(self.testrail_client.get_test_ids_from_tags(data))

    def end_test(self, data, result):
        """Runs at end of each test."""
        test_ids = self.testrail_client.parse_test_ids_from_tags(data.tags)
        if not test_ids:
            print("No associated test rail ids to update.")
            return
        self.testrail_client.handle_result(
            status=f'{result.status}',
            comment=f'{result.message}',
            test_ids=test_ids
        )

    def log_file(self, path):
        """Runs when log file is ready, after complete execution."""
        self.testrail_client.upload_log_file_to_run(path)

    def close(self):
        """Called when the whole test execution ends."""
        self.testrail_client.post_suite_cleanup()
        if self.testrail_client.get_global_var('CLOSE_TESTRAIL_RUN'):
            self.testrail_client.close_run()

