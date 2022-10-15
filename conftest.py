__author__ = "Developed by EA"

import json
import os
import subprocess
import time

import pytest
import yaml
import pytz
import socket
from datetime import datetime
# from library.psql import Database
from pathlib import Path
from threading import Thread
# from library.lib import SSHClient

from ameyo.test_data_lib.rest import AmeyoRest


def pytest_configure(config):
    """
    Configuration changes for PyTest
    :param config:
    :return:
    """
    os.environ["ROOT_PATH"] = config.rootdir.strpath
    options = {
        "cacheclear": True,
        "capture": "sys",
        "clean_alluredir": True,
        "color": "yes",
        "disable_warnings": True,
        "instafail": True,
        "failedfirst": False,
        # "maxfail": 1,
        "json_report_indent": 2,
        "json_report_omit": ["warnings"],
        "json_report": True,
        "pythonwarnings": ["ignore:Unverified HTTPS request"],
        "tbstyle": "short",
        "self_contained_html": True,
        "verbose": 1,
        "repeat_scope": "class",
        "emoji": True,
    }
    for option, value in options.items():
        if hasattr(config.option, option):
            setattr(config.option, option, value)
        else:
            print(f"option: {option} not present in config !!")

    if config.getoption("allure_report_dir") is None:
        config.option.allure_report_dir = "allure-results"

    if config.getoption("json_report_file") == ".report.json":
        config.option.json_report_file = "report.json"

    if config.getoption("htmlpath") is None:
        config.option.htmlpath = "report.html"

    if config.getoption("xmlpath") is None:
        config.option.xmlpath = "report.xml"


def pytest_addoption(parser):
    """
    Adds custom command line options for running the pytest harness
    All options will be stored in pytest config
    :param parser:
    :return:
    """
    parser.addoption(
        "--url",
        action="store",
        type=str,
        default="https://vapt.ameyo.net:8443/app/",
        help="URL",
        required=True
    )
    parser.addoption(
        "--username", action="store", default='MultiCCManager', help="Username for the Environment", required=False
    )
    parser.addoption(
        "--password", action="store", default='MultiCCManager', help="Password for the Environment", required=False
    )
    parser.addoption(
        "--ccn",
        action="store",
        type=str,
        default='E2E_0001',
        required=False,
        help="Contact Center Name",
    )
    parser.addoption(
        "--debug-tests",
        action="store_true",
        default=False,
        help="Flag to be present when using artifact file contents for debugging",
    )

    # DB Connection Strings
    parser.addoption(
        "--db-host", action="store", type=str, default="fluidcxdemo.ameyo.com", help="Database Host", required=False
    )
    parser.addoption(
        "--db-port", action="store", type=str, default="5432", help="Database Port", required=False
    )
    parser.addoption(
        "--db-user", action="store", type=str, default="postgres", help="Database Username", required=False
    )
    parser.addoption(
        "--db-name", action="store", type=str, default="ameyodb", help="Database Name", required=False
    )

    # SSH Connection Strings
    parser.addoption(
        "--ssh-logs", action="store_true", default=False, help="Save SSH Logs?", required=False
    )
    parser.addoption(
        "--ssh-host", action="store", type=str, default="fluidcxdemo.ameyo.com", help="SSH Host", required=False
    )
    parser.addoption(
        "--ssh-port", action="store", type=str, default="20222", help="SSH Port", required=False
    )
    parser.addoption(
        "--ssh-user", action="store", type=str, default="anshuman", help="SSH Username", required=False
    )
    parser.addoption(
        "--ssh-pass", action="store", type=str, default="drishti@anshuman", help="SSH Password", required=False
    )

    # setup version
    parser.addoption(
        "--system-version", action="store", type=str, default="4.x", help="The build version of system e.g. 4.x or 5.x",
        required=False,
    )


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="class")
def class_fixture(request):
    """
    Class Fixture(s)
    :return:
    """
    request.cls.rootPath = Path(request.config.rootdir.strpath)
    request.cls.ccn = request.config.option.ccn


@pytest.fixture(scope="function", autouse=True)
def function_fixture(request, ameyo):
    """
    Function Fixture(s)
    :return:
    """
    ameyo.tc_name = request.node.name


@pytest.fixture(scope="session")
def ameyo(request):
    """
    Ameyo Rest Library
    :param request:
    :return:
    """
    return AmeyoRest(
        url=request.config.option.url,
        username=request.config.option.username,
        password=request.config.option.password,
        system_version=request.config.option.system_version,
        noop=False,
    )


@pytest.fixture(scope="session")
def artifacts(ameyo, request):
    """
    Fixture which will hold all Artifacts Data
    :return:
    """
    toYield = dict()
    if request.config.option.debug_tests:
        with open(Path(__file__).parent / "artifacts.yaml", "r") as fp:
            try:
                toYield = yaml.safe_load(fp)
            except yaml.YAMLError:
                toYield = dict()
    yield toYield

    with open(Path(__file__).parent / "artifacts.yaml", "w") as fp:
        fp.write(yaml.safe_dump(toYield))


@pytest.fixture(scope="session")
def calling(ameyo, request):
    """
    Fixture which will hold all Artifacts Data
    :return:
    """
    toYield = dict()
    if request.config.option.debug_tests:
        with open(Path(__file__).parent / "calling.yaml", "r") as fp:
            try:
                toYield = yaml.safe_load(fp)
            except yaml.YAMLError:
                toYield = dict()
    yield toYield

    with open(Path(__file__).parent / "calling.yaml", "w") as fp:
        fp.write(yaml.safe_dump(toYield))


def pytest_sessionstart(session):
    """
    Runs at the Start of execution
    :param session:
    :return:
    """
    pass


def pytest_sessionfinish(session):
    """
    Runs at the end of execution
    Here we Generate the Allure Report
    :param session:
    :return:
    """
    if os.environ.get("NODE_NAME", None) is None:
        p = subprocess.Popen(
            args="allure --help",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if p.wait() != 0:
            return

        # Running from Local System
        resultsPath = (
                Path(session.config.rootdir.strpath)
                / session.config.option.allure_report_dir
        )
        if os.path.isdir(resultsPath):
            cmd = "allure generate --clean allure-results"
            cwd = session.config.rootdir.strpath
            p = subprocess.Popen(
                args=cmd,
                shell=True,
                cwd=cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            p.communicate()
            if p.wait() != 0:
                print("Failed to Generate allure report !!")
            # shutil.rmtree(resultsPath)


@pytest.fixture(scope="session", autouse=True)
def logout(ameyo, request, calling):
    """
    Fixture To Logout user at the end of Session
    :return:
    """
    yield
    if 'Campaign' in calling:
        campaign = calling['Campaign']
        try:
            response = ameyo.disable_auto_dial(**{'campaignId': campaign['campaignId']})
            ameyo.logger.debug(f"{ameyo.is_auto_dial_enabled}")
            if isinstance(response, bool):
                assert response, "Auto dial can not be disabled"
            else:
                assert response.ok, f"Auto dial can not be disabled !! {response.text}"
        except Exception as e:
            ameyo.logger.info(
                f"Exception in teardown while disabling Auto dial. "
                f"The supervisor has already been logged out. So, ignoring. {e}")
        try:
            response = ameyo.request_live_monitoring_data_for_supervisor(
                sessionId=ameyo.supervisorToken, campaignId=campaign["campaignId"]
            )
            ameyo.logger.debug(f"All agent live state : {response.json()}")
        except Exception as e:
            ameyo.logger.debug(
                f"Exception in getting get_user_run_time. The admin does not have a session. So, ignoring. {e}")

    for cc in ameyo.get_all_cc().json():
        if cc['contactCenterName'] == request.config.option.ccn:
            for userId in cc['contactCenterUserIds']:
                if hasattr(ameyo, 'supMon') and userId != ameyo.supMon:
                    ameyo.terminate_all_sessions_for_user(userId=userId, sessionId=ameyo.ccManagerToken)
    ameyo.user_logout(sessionId=ameyo.ccManagerToken)


@pytest.fixture(scope='session', autouse=True)
def _refresh(ameyo, request):
    """
    Refresh Tokens by sending KeepAlive (threaded)
    :param ameyo:
    :param request:
    :return:
    """
    ka_logs = open('keepAliveWithPingPush.log', 'w')
    setattr(request.config.option, 'send_keep_alive', True)
    setattr(request.session, 'timestamp', int(datetime.now(tz=pytz.timezone("Asia/Calcutta")).timestamp()))

    def _inner(interval):
        while True:
            time.sleep(interval)
            c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
            try:
                if request.config.option.send_keep_alive is False:
                    c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                    ka_logs.write(f"{c_time} :: not refreshing: send_keep_alive is False\n")
                    return

                # now = int(datetime.now(tz=pytz.timezone("Asia/Calcutta")).timestamp())
                # if hasattr(request.session, 'timestamp') and now - request.session.timestamp < interval:
                #     ka_logs.write(
                #         f"{c_time} :: not refreshing: time less than 15sec since last refresh. Sleeping for 15s\n")
                #     time.sleep(interval)
                # else:
                #     ka_logs.write(f"{c_time} :: Refreshing after {now - request.session.timestamp}s\n")
                #
                # setattr(request.session, 'timestamp', now)
                # c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                for _role in ['adminToken', 'ccManagerToken', 'supervisorToken', 'executiveToken', 'executiveToken2']:
                    sessionId = getattr(ameyo, _role, None)
                    if sessionId is None:
                        c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                        ka_logs.write(f"{c_time} :: not refreshing : {_role} is None\n")
                        continue
                    # ameyo.logger.info(f"{c_time} :: KeepAlive_{_role} → '{sessionId}' ...")

                    if request.config.option.send_keep_alive is True:
                        try:
                            response = ameyo.keep_alive(sessionId=sessionId)
                            debugJson = {
                                'sessionId': sessionId,
                                'url': response.request.url, 'body': response.request.body.decode(),
                                'headers': {x: y for x, y in response.request.headers.items()}
                            }
                            c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                            toLog = f"{c_time} :: {_role} :: {sessionId} :: {json.dumps(debugJson, indent=2)} :: {response.text}\n"
                            ka_logs.write(toLog)
                            ka_logs.flush()
                        except Exception as e:
                            c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                            toLog = f"{c_time} :: Exception in keep-alive thread {e} for {_role}\n"
                            ka_logs.write(toLog)
                            ka_logs.flush()

                    else:
                        c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                        ka_logs.write(f"{c_time} :: not refreshing: send_keep_alive is False")
                        return
                for _role in ameyo.logged_in_agents:
                    if ameyo.logged_in_agents[_role]["token"] == ameyo.executiveToken:
                        continue
                    sessionId = ameyo.logged_in_agents[_role]["token"]
                    if sessionId is None:
                        c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                        ka_logs.write(f"{c_time} :: not refreshing : {_role} is None\n")
                        continue
                    # ameyo.logger.info(f"{c_time} :: KeepAlive_{_role} → '{sessionId}' ...")

                    if request.config.option.send_keep_alive is True:
                        try:
                            response = ameyo.keep_alive(sessionId=sessionId)
                            debugJson = {
                                'sessionId': sessionId,
                                'url': response.request.url, 'body': response.request.body.decode(),
                                'headers': {x: y for x, y in response.request.headers.items()}
                            }
                            c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                            toLog = f"{c_time} :: {_role} :: {sessionId} :: {json.dumps(debugJson, indent=2)} :: {response.text}\n"
                            ka_logs.write(toLog)
                            ka_logs.flush()
                        except Exception as e:
                            c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                            toLog = f"{c_time} :: Exception in keep-alive thread {e} for {_role}\n"
                            ka_logs.write(toLog)
                            ka_logs.flush()
                    else:
                        c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                        ka_logs.write(f"{c_time} :: not refreshing: send_keep_alive is False")
                        return
            except Exception as e:
                c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                toLog = f"{c_time} :: Exception in keep-alive thread {e} \n"
                ka_logs.write(toLog)
                ka_logs.flush()

    at = Thread(target=_inner, args=(15,))
    at.start()
    yield
    setattr(request.config.option, 'send_keep_alive', False)


# @pytest.fixture(scope="session")
# def postgres(ameyo, request):
#     """
#     Postgres Connection
#     :param ameyo:
#     :param request:
#     :return:
#     """
#     host = request.config.option.db_host
#     port = request.config.option.db_port
#     username = request.config.option.db_user
#     database = getattr(request.config.option, 'db_name', 'ameyodb')
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         s.connect((host, int(port)))
#         s.shutdown(2)
#     except (Exception, ValueError):
#         raise Exception(f"Cannot Connect to {host} and Port: {port}")
#
#     return Database(host=host, port=port, username=username, database=database)
#
#
# @pytest.fixture(scope="session", autouse=True)
# def _ssh(ameyo, request):
#     """
#     Saves a copy of server logs
#     **** Ameyo VPN needed for this to run ****
#     :param ameyo:
#     :param request:
#     :return:
#     """
#     if request.config.option.ssh_logs is False:
#         return None
#
#     try:
#         ssh = SSHClient(
#             hostname=request.config.option.ssh_host, port=request.config.option.ssh_port,
#             username=request.config.option.ssh_user, password=request.config.option.ssh_pass
#         )
#     except (Exception, ValueError) as Exp:
#         ameyo.logger.error(f"SSH Connection Failed, Not Capturing Server Logs !!")
#         return None
#     ameyo.logger.info(f"Started Capturing Ameyo Server Debug Logs ...")
#     return ssh
#
#
# @pytest.fixture(scope="function", autouse=True)
# def _logs(_ssh, request):
#     """
#     Saves a copy of server logs
#     **** Ameyo VPN needed for this to run ****
#     :param _ssh:
#     :return:
#     """
#     if request.config.option.ssh_logs is True and _ssh:
#         _ssh.get_file_bytes()
#
#     yield
#
#     if request.config.option.ssh_logs is True and _ssh:
#         if hasattr(request.node, 'rep_call') and request.node.rep_call.failed is True:
#             # if test-case has failed, collect the logs
#             # + after collection, set the log pointer to the new location
#             _ssh.get_delta_logs()


@pytest.fixture(scope="function", autouse=True)
def set_test_case_details(ameyo, request):
    """
    Set Test-Case Details (Required for Porting)
    """
    setattr(ameyo.rest, 'testCaseName', request.node.name)
    setattr(ameyo.rest, 'testCaseClass', request.node.parent.name)
    yield
    pass