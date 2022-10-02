"""Utility file for testrail apis."""
import json
import os
import re
import shutil
from datetime import datetime
from uuid import uuid4

from robot.libraries.BuiltIn import BuiltIn

from testrail_api import TestRailAPI


class AmeyoTestrail:
    """Testrail operation class."""
    TEST_STATUS = {
        "PASS": "Passed",
        "FAIL": "Failed",
        "SKIP": "Skipped",
    }

    def __init__(self, server_url, username, password, project_id):
        self.project_id = project_id
        self._api = TestRailAPI(server_url, username, password)
        self._server_url = server_url
        self._run = None
        self._tests = {}
        self._statuses = self.create_map(
            self._get_statuses(),
            'label'
        )
        self._global_vars = None

    def _get_statuses(self, retries=0):
        """Gets available status list from testrail."""
        response = None
        try:
            response = self._api.statuses.get_statuses()
            if not isinstance(response, list):
                raise ValueError(f'No status list found in response: {response}')
            return response
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while fetching test status list from test rail : {err} after {retries} retries.")
            else:
                print(f"Retrying to fetch statuses...{retries} err: {err} response:{response}")
                return self._get_statuses(retries)
            return {}

    def get_client(self):
        """Gets testrail api client."""
        return self._api

    @staticmethod
    def set_global_var(var_name, var_value):
        """Sets global variable value."""
        BuiltIn().set_global_variable(f'${var_name}', var_value)

    def get_global_var(self, var_name):
        """Gets global variable value."""
        if self._global_vars is None:
            self._global_vars = BuiltIn().get_variables()
        return self._global_vars[f'${{{var_name}}}']

    def create_run(self, test_case_ids, retries=0):
        """Creates run for automation."""
        try:
            self._run = self._api.runs.add_run(
                project_id=self.project_id,
                description="Automated test run for AMEYO UI.",
                name=self.get_unique_test_run_name(),
                include_all=False,
                case_ids=test_case_ids
            )
            if not self._run.get('id'):
                raise ValueError(f'No run id found in response: {self._run}')
            self._get_tests()
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while creating new test run in testrail : {err} after {retries} retries.")
            else:
                print(f"Retrying to create test run...{retries} err: {err} response:{self._run}")
                return self.create_run(test_case_ids,retries)

    def _get_tests(self, retries=0):
        """Gets test from current run id."""
        response = None
        try:
            tests = []
            # TODO: Put a logic to fetch all test cases requested while creating run, current limit: 256
            response = self._api.tests.get_tests(self._run['id'])
            if not response.get('tests'):
                raise ValueError(f'No tests found in response: {response}')
            tests.extend(response.get('tests'))
            self._tests = self.create_map(tests, 'case_id')
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while fetching tests cases for test run : {err} after {retries} retries.")
            else:
                print(f"Retrying to test list from test run...{retries} err: {err} response:{response}")
                return self._get_tests(retries)

    def post_ss_to_result(self, result_id, comment, retries=0):
        """Posts screenshot to test result based on id."""
        response = None
        try:
            ss_path = re.search(r'\<(?P<path>.*)\>', comment)
            if ss_path:
                ss_path = ss_path.group('path')
            else:
                print(f"No screenshot to post as no path was captured in error message: {comment}")
            if ss_path and result_id:
                response =  self._api.attachments.add_attachment_to_result(result_id, ss_path)
                if not response.get('attachment_id'):
                    raise ValueError(f'No attachment id found in response:{response}')
                return response
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while posting ss to test result to testrail: {err} after {retries} retries.")
            else:
                print(f"Retrying to post screenshot to result...{retries} err: {err} response:{response}")
                return self.post_ss_to_result(result_id,comment,retries)

    def get_tests(self):
        """Gets current run tests."""
        return self._tests

    def format_result(self, result):
        """Formats result to update test case."""
        return {
            "test_id": self._tests.get(result.get('case_id'), {}).get('id'),
            "status_id": self._statuses.get(self.TEST_STATUS.get(result.get("status"))).get('id'),
            "comment": result.get('comment') or "This test was marked as 'Passed' via robot automation",
        }

    def handle_result(self, status, comment, test_ids):
        """Handler for formating and posting result to testrail."""
        response_list = []
        if len(test_ids) > 1:
            test_results = {
                "results": [
                    self.format_result({
                        "case_id": test_id,
                        "status": status,
                        "comment": comment
                    }) for test_id in test_ids
                ]
            }
            response_list = self.add_results(test_results)
        elif len(test_ids) == 1:
            response_list = [
                self.add_result({
                    "case_id": test_ids[0],
                    "status": status,
                    "comment": comment
                }
            )]

        if status == 'FAIL':
            for response in response_list:
                    self.post_ss_to_result(response.get('id'), comment)

    def add_result(self, result_obj, retries=0):
        """Updates generated test in the current run."""
        response = None
        try:
            result = self.format_result(result_obj)
            if result.get('test_id'):
                response =  self._api.results.add_result(**result)
                if not response.get('id'):
                    raise ValueError(f"No test result id returned in response:{response}")
                return response
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while posting result to testrail: {err} after {retries} retries.")
            else:
                print(f"Retrying to add result...{retries} err: {err} response:{response}")
                return self.add_result(result_obj, retries)

    def add_results(self, test_results, retries=0):
        """Updates generated tests in the current run."""
        response = None
        try:
            test_results["run_id"] = self._run["id"]
            response =  self._api.results.add_results(**test_results)
            if not isinstance(response, list) or not len(response) == len(test_results.get('results')):
                raise ValueError(f"No test result ids returned in response:{response}")
            return response
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while posting results to testrail: {err} after {retries} retries.")
            else:
                print(f"Retrying to add results...{retries} err: {err} response:{response}")
                return self.add_results(test_results, retries)

    def get_test_ids_from_tags(self, data):
        """Parse and get all the test rail ids from tags in suite."""
        tags = set()
        for suite in data.suites:
            for test in suite.tests:
                tags.update(self.parse_test_ids_from_tags(test.tags))
            if suite.suites:
                tags.update(self.get_test_ids_from_tags(suite))
        for test in data.tests:
            tags.update(self.parse_test_ids_from_tags(test.tags))
        return list(tags)

    @staticmethod
    def get_testrail_id_tags(tags):
        """Identifies tags carrying testrail id."""
        test_tags = ''
        for t in tags:
            if 'testrailid=' in t or 'testrailids=[' in t:
                test_tags += f' {t}'
        return test_tags

    def parse_test_ids_from_tags(self, tags):
        """Parse id from tag string."""
        test_tags = self.get_testrail_id_tags(tags)
        id_group = re.search(r'testrailids=\[(?P<ids>.*)\]', test_tags)
        if id_group:
            return [i.strip() for i in id_group.group('ids').split(',')]
        return re.findall(r'testrailid=(\d+)', test_tags)

    @staticmethod
    def create_map(results, key):
        """Creates test map using test case id."""
        source = {}
        for result in results:
            source[f'{result[key]}'] = result
        return source

    def is_run_created(self):
        """Checks if run is created."""
        return self._run is not None

    def upload_log_file_to_run(self, path, retries=0):
        """Uploads log file to test run in testrail."""
        response = None
        try:
            response =  self._api.attachments.add_attachment_to_run(self._run['id'], path)
            if not response.get('attachment_id'):
                raise ValueError(f'No attachment id found in response: {response}')
            return response
        except Exception as err:
            retries+=1
            if retries > 3:
                print(f"Error while posting log file to testrail: {err} after {retries} retries.")
            else:
                print(f"Retrying to upload log file...{retries} err:{err} response:{response}")
                return self.upload_log_file_to_run(path, retries)

    def post_suite_cleanup(self):
        """Remove logs."""
        self._save_post_run_details()
        if self.get_global_var('SKIP_POST_RUN_CLEANUP'):
            return
        try:
            output_dir = self.get_global_var('OUTPUT DIR')
            ss_path = self.get_global_var('OUTPUT DIR')
            if ss_path == output_dir:
                shutil.rmtree(os.path.normpath(ss_path))
                return
            shutil.rmtree(os.path.normpath(ss_path))
            shutil.rmtree(os.path.normpath(output_dir))
        except Exception as err:
            print(f"Error removing directory from: {output_dir} or {ss_path}", err)

    def _save_post_run_details(self):
        """Saves post run details like test rail link to
            output dir with file name: post_run_details.json
        """
        testrail_link = self._server_url + self.get_global_var('TESTRAIL_RUN_URL')
        post_run_details = {
            "testrail_run_link": testrail_link.format(run_id=self._run["id"])
        }
        with open(os.path.join(self.get_global_var('OUTPUT DIR'), 'post_run_details.json'), 'w') as f:
            json.dump(post_run_details, f)

    def close_run(self, retries=0):
        """Closes an existing test run and archives its tests & results."""
        response = None
        try:
            response =  self._api.runs.close_run(self._run['id'])
            if not response.get('id'):
                raise ValueError(f'No closed run id returned in response:{response}')
            return response
        except Exception as err:
            retries += 1
            if retries > 3:
                print(f"Error while closing run: {err} after {retries} retries.")
            else:
                print(f"Retrying to close run...{retries} err: {err} response: {response}")
                return self.close_run(retries)

    def get_unique_test_run_name(self):
        """Gets unique test run name."""
        return f"{self.get_global_var('AUTOMATION_NAME')} - " + \
               f"{self.get_global_var('RUN_AS')} - " + \
               datetime.now().strftime('%Y-%m-%d-%H-%M-%S-') + str(uuid4())[:8]
