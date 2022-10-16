__author__ = "Developed by EA"

import base64
import csv
import json
import os
import random
import re
import socket
import subprocess
import tarfile
import uuid
import zipfile
import allure
import yaml
import sys
import logging
import requests
import time
import pytz
import paramiko

from requests.adapters import HTTPAdapter
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from types import SimpleNamespace as Namespace
from urllib.parse import quote
from urllib.parse import urlparse, urlunparse
from urllib3.connection import HTTPConnection
from functools import wraps
from faker import Faker
from types import SimpleNamespace
from threading import Semaphore
from datetime import datetime


class CustomAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra, mask, level='INFO'):
        self.mask = mask
        super().__init__(logger, extra)
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        self.logger.addHandler(console)
        self.setLevel(level)

    def process(self, msg, kwargs):
        for k, v in os.environ.items():
            if k in self.mask and v in msg:
                msg = msg.replace(v, "********")
        return msg, kwargs


class General:
    """
    Class that holds all general globally used functions
    """

    def __init__(self, **kwargs):
        """
        Future use, if something has to be initialized
        """
        self.configs = self.read_configs()
        self.curlCmds = []
        self.mask = []
        self.logger = CustomAdapter(
            logging.getLogger(name='AMEYO'), None, self.mask, level=kwargs.get('level', self.configs.log_level)
        )
        self.faker = Faker(locale=self.configs.locale)
        self.uuid = str(uuid.uuid4()).lower() + "-" + str(int(datetime.now(tz=pytz.timezone('UTC')).timestamp()))
        self.epoch = round(time.time() * 1000)
        self.listenerName = f"webcore_{self.epoch}"
        self.lastProcessed = -1

    @staticmethod
    def read_configs():
        """
        Read Configs File
        :return:
        """
        with open(Path(__file__).parent.parent / 'configs.yaml', 'r') as fp:
            data = yaml.safe_load(fp.read())
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

    @staticmethod
    def make_creds(url, username, password):
        """
        Make Simple Name Space Creds
        :param url:
        :param username:
        :param password:
        :return:
        """
        if not all([url, username, password]):
            raise Exception(f"Some mandatory params are missing !!")
        data = {
            'url': url, 'username': username, 'password': password, 'host': urlparse(url).hostname,
            'domain': urlparse(url).netloc
        }
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

    def run_cmd(self, cmd, wait=True, fail=True, cwd=None, env=None, timeout=None, verbose=False):
        """
        Run an external command and return it's output
        :param cmd:
        :param wait:
        :param fail:
        :param cwd:
        :param env:
        :param timeout:
        :param verbose:
        :return:
        """
        # cmd_env = dict()
        cmd_response = namedtuple("CmdResponse", ["cmd", "status", "output", "error", "outFile"])
        cmd_env = os.environ.copy()
        if env and isinstance(env, dict):
            for key, value in env.items():
                cmd_env[key] = str(value)

        if isinstance(cmd, str):
            if ' && ' in cmd:
                cmd = cmd.split(" && ")
            elif '&&' in cmd:
                cmd = cmd.split("&&")
            else:
                cmd = [cmd]

        cmd = "; ".join(map(lambda x: str(x).strip(), cmd))

        if not wait:
            subprocess.Popen(args=cmd, shell=True, stdin=None, stdout=None, stderr=None)
            return cmd_response(cmd=cmd, status=0, output=None, error=None, outFile=None)

        cwd = cwd if cwd else str(os.getcwd())
        options = {"cwd": cwd, "args": cmd, "env": cmd_env, "shell": True, "universal_newlines": True, }

        if timeout:
            options.update({"timeout": int(timeout)})

        cmdOutDir = Path(__file__).parent.parent / "cmdOut"
        if os.path.isfile(cmdOutDir):
            os.remove(cmdOutDir)
        if not os.path.isdir(cmdOutDir):
            os.makedirs(cmdOutDir)

        def _std(io, log='INFO'):
            out = ""
            for o in io:
                out += o
                if log == 'INFO' and verbose is True:
                    self.logger.info(o.strip())
                if log == 'ERROR' and verbose is True:
                    self.logger.error(o.strip())
                io.flush()
            return out

        stdout, stderr = "", ""
        with subprocess.Popen(**options, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            result = self.run_in_parallel(_std, [
                {'io': p.stdout, 'log': 'INFO'}, {'io': p.stderr, 'log': 'ERROR'}
            ])
            for r in result.values():
                if r['args']['log'] == 'ERROR':
                    stderr = r['result']
                elif r['args']['log'] == 'INFO':
                    stdout = r['result']
                else:
                    continue
        status = p.returncode

        content = []
        separator = '--' * 10

        # capture cwd
        if cwd:
            content.append(f"cwd → {cwd}")

        # capture env details
        if env and isinstance(env, dict):
            content.append("\n".join([f"export {x}={env[x]}" for x in env.keys()]))

        # Generate the final file name that has to be returned ...
        now = datetime.now(pytz.timezone("Asia/Calcutta"))
        name = f"{now.hour}_{now.minute}_{now.second}_{now.microsecond}.log"
        finalFileName = cmdOutDir / f"PassedCmd_{name}"
        if status != 0:
            finalFileName = cmdOutDir / f"FailedCmd_{name}"

        if stdout != "":
            content.extend([f"CmdRun → {cmd}", f"CmdOut → {stdout}", ])
        if stderr != "":
            content.extend(['----- ERROR -----', f"CmdError → {stderr}", ])
        content = f"\n{separator}\n".join(content)

        try:
            with open(finalFileName, 'w') as fp:
                fp.write(content)
            allure.attach.file(
                finalFileName, name=str(finalFileName).split('/')[-1], attachment_type=allure.attachment_type.TEXT,
            )
        except (Exception, ValueError):
            pass

        if fail is True and status != 0:
            raise Exception(f"Command '{cmd}' failed with code: {status} and ERROR: {stderr}")

        return cmd_response(cmd=cmd, status=status, output=stdout, error=stderr, outFile=finalFileName)

    @staticmethod
    def make_tar(source, destination=None):
        """
        Function to make a tar ball
        :param source:
        :param destination:
        :return:
        """

        if not Path(source).exists():
            raise Exception(f"File/Dir {source} not found !!")

        if destination is None:
            destination = f"{os.path.dirname(source)}.tar.gz"

        with tarfile.open(destination, "w:gz") as tar:
            tar.add(source, arcname=os.path.basename(source))

        return destination

    def extract_tar(self, source, destination=None, unique=None):
        """
        Function to un-tar a tar file
        :param: folder
        :param: destination
        :param: unique
        :return
        """
        if not os.path.isfile(source):
            raise Exception(f"Can't find tar file: {source} !!")

        if not os.path.basename(source).endswith('.tar.gz'):
            raise Exception(f"file: {source} is not a valid Tar File !!")

        if destination is None:
            destination = os.path.abspath(os.path.dirname(source))

        if unique:
            destination = os.path.join(destination, self.generate_guid())

        if not os.path.isdir(destination):
            os.makedirs(destination)

        tar = tarfile.open(source)
        tar.extractall(destination)
        tar.close()
        cmd = "find . -name '*.sh' -type f -exec dos2unix --quiet --safe {} \\; -exec chmod +x {} \\;"
        self.run_cmd(cmd=cmd, cwd=destination)
        return destination

    @staticmethod
    def generate_auth_header(username, password, header=True):
        """
        Function to Generate Auth Header
        :param username:
        :param password:
        :param header:
        """
        encoded = str(base64.b64encode(bytes(f"{username}:{password}", "utf-8")), "ascii").strip()
        if header:
            return {"Authorization": f"Basic {encoded}"}
        else:
            return f"Basic {encoded}"

    @staticmethod
    def save_allure(data, name, save_dump=True):
        """
        Save allure report by converting data to Json
        :param data:
        :param name:
        :param save_dump:
        :type name:
        :return:
        """
        if len(data) != 0:
            if isinstance(data, str):
                name = str(name).replace(".json", ".log")
                allure.attach(data, name=name, attachment_type=allure.attachment_type.TEXT)
                if save_dump:
                    with open(name, "w") as _fp:
                        _fp.write(data)
                return str
            else:
                dump = json.dumps(data, indent=2, sort_keys=True)
                allure.attach(dump, name=name, attachment_type=allure.attachment_type.JSON)
                if save_dump:
                    with open(name, "w") as _fp:
                        _fp.write(dump)
                return dump

    @staticmethod
    def create_auth_basic_token(login, secret):
        """
        Function to create basic token from id and secret
        :param login:
        :param secret:
        """
        return str(base64.b64encode(bytes(f"{login}:{secret}", "utf-8")), "ascii").strip()

    @staticmethod
    def read_file(file_name, return_lines=True):
        """
        Func to read any file and return its contents
        :param file_name
        :param return_lines
        :return:
        """
        if not os.path.isfile(file_name):
            raise Exception(f"File {file_name} Does Not Exist !!")

        with open(file_name, "r") as _fp:
            if return_lines:
                data = [x.strip() for x in _fp]
            else:
                data = _fp.read()

        return data

    def read_json_file(self, file_name, nt=True):
        """
        This function will read Json and return it back in Named-Tuples format
        :param file_name
        :param nt
        """
        if os.path.isfile(file_name):
            data = self.read_file(file_name, return_lines=False)
        else:
            data = file_name

        if nt:
            data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        else:
            data = json.loads(data)

        return data

    def read_yaml_file(self, file_name, nt=False):
        """
        Func to read the yaml file
        :param file_name
        :param nt
        :return:
        """
        # check if given file_name is a name of a file or Yaml Raw data
        if len(str(file_name).split('\n')) == 1:
            data = re.sub(r'({{.*?}})', r"'\1'", self.read_file(file_name, return_lines=False))
        else:
            data = re.sub(r'({{.*?}})', r"'\1'", file_name)

        try:
            data = yaml.safe_load(data)
        except (Exception, ValueError):
            raise Exception("Yaml Parsing Error !!")

        if nt is True:
            return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
        else:
            return data

    @staticmethod
    def json_to_yaml(json_file, yml_file):
        with open(json_file, 'r') as file:
            configuration = json.load(file)

        with open(yml_file, 'w+') as yaml_file:
            yaml.dump(configuration, yaml_file)

    @staticmethod
    def uncurl_from_curl(command):
        """
        Uncurl the curl command and return args for request command
        :param command:
        :return:
        """
        if re.search(r"--request", command):
            url = str(command.split(" ")[4]).replace("'", "")
            method = str(re.search(r"--request\s+(.*?)\s+", command, re.I | re.M).group(1)).upper()
            if re.search(r"--data-raw\s*'([^']*)'", command) is not None:
                data = json.loads(re.search(r"--data-raw\s*'([^']*)'", command, re.I | re.M).group(1))
            else:
                data = None
            headers = {
                str(x.split(":")[0]).strip(): str(x.split(":")[1]).strip()
                for x in re.findall(r"--header \'(.*?)\'", command, re.I | re.M)
            }
        else:
            url = re.search(r"'(http.*?)'$", command, re.I | re.M).group(1)
            method = str(re.search(r"-x\s+(.*?)\s+", command, re.I | re.M).group(1)).upper()
            if re.search(r"-d\s*'(.*?)'", command) is not None:
                data = json.loads(re.search(r"-d\s*'(.*?)'", command, re.I | re.M).group(1))
            else:
                data = None
            headers = {
                str(x.split(":")[0]).strip(): str(x.split(":")[1]).strip()
                for x in re.findall(r"-H \"(.*?)\"", command, re.I | re.M)
            }

        return {"method": method, "url": url, "data": data, "headers": headers}

    @staticmethod
    def base64_encode(username, password):
        """
        Return Base64 encoded string
        :param username:
        :param password:
        :return:
        """
        encoded = str(base64.b64encode(bytes(f"{username}:{password}", "utf-8")), "ascii").strip()
        return encoded

    @staticmethod
    def base64_decode(data):
        """
        Return Base64 encoded string
        :param data:
        :return:
        """
        decoded = base64.b64decode(data).decode()
        if len(decoded.split(":")) != 2:
            raise Exception("This is not a valid username password encoded string !!")
        username = decoded.split(":")[0]
        password = decoded.split(":")[1]
        return username, password

    @staticmethod
    def get_base_auth(username, password):
        """
        Return Base64 encoded authorization
        :param username:
        :param password:
        :return:
        """
        auth = str(base64.b64encode(bytes("%s:%s" % (username, password), "utf-8")), "ascii").strip()
        return {"Authorization": f"Basic {auth}"}

    @staticmethod
    def urljoin(*args):
        """
        This function will join a URL and returns proper url
        :param args:
        :return:
        """
        parsed = list(urlparse("/".join(args)))
        parsed[2] = re.sub("/{2,}", "/", parsed[2])
        _host = urlunparse(parsed)
        return _host

    @staticmethod
    def compress_file(file_name):
        """
        Compress a file and return its path
        :param file_name
        """
        if str(file_name).endswith("zip"):
            return file_name
        else:
            zip_name = ".".join([*[x for x in file_name.split(".")[0:-1]], *["zip"]])

        _zip = zipfile.ZipFile(zip_name, "w")
        _zip.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
        _zip.close()

        return zip_name

    @staticmethod
    def find_file(name, folder):
        """
        Function to find the file and return it's full path
        :param name:
        :param folder:
        :return:
        """
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder):
            raise Exception(f"folder: {folder} is not a valid directory !!")

        for root, dirs, files in os.walk(folder):
            for file in files:
                if file == name:
                    return os.path.join(root, file)

        return None

    def run_in_parallel(self, function, arguments, max_workers=None, logs=False):
        """
        Run function → function in parallel with arguments → arguments
        :param function: function to be called in parallel
        :param arguments: list of arguments to be passed to the function
        :param max_workers: max number of workers
        :param logs: print logs
        :return:
        """
        if max_workers is None:
            max_workers = self.configs.max_workers

        if len(arguments) == 0:
            raise Exception('no arguments provided !!')

        to_return = dict()
        totalCount = len(arguments)
        count = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if isinstance(arguments[0], list):
                thread_executor = {executor.submit(function, *args): args for args in arguments}
            elif isinstance(arguments[0], dict):
                thread_executor = {executor.submit(function, **kwargs): kwargs for kwargs in arguments}
            else:
                raise Exception("arguments provided are not supported !!")
            for completed_thread in as_completed(thread_executor):
                args = thread_executor[completed_thread]
                if logs is True:
                    self.logger.info(f"#{count}/{totalCount} → {args}")
                exp = completed_thread.exception()
                if exp:
                    result = None
                else:
                    result = completed_thread.result()
                to_return[count] = {'args': args, 'result': result, 'exception': exp}
                count += 1

        return to_return

    @staticmethod
    def is_port_open(ip, port):
        """
        Check port is open or not
        :param ip:
        :param port:
        :return:
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, int(port)))
            sock.shutdown(2)
            return True
        except (Exception, ValueError):
            return False

    def curl_command(self, **kwargs):
        """
        Get Curl Command Before it is being Hit !!
        param kwargs:
        :return:
        """
        url = kwargs.get('url', None)
        method = kwargs.get('method', None)
        headers = kwargs.get('headers', {})
        data = kwargs.get('data', kwargs.get('json', None))
        params = kwargs.get('params', None)

        if not any([url, method]):
            raise Exception(f"method and url are mandatory params for generating curl request")

        if params:
            try:
                url = f'{url}?{"&".join([f"{k}={v}" for k, v in params.items()])}'
            except (Exception, ValueError):
                url = f'{url}?{quote("&".join([f"{k}={v}" for k, v in params.items()]), safe="")}'

        # Generate the Final Params
        finalParams = [f"curl --request {method} --location --silent --show-error '{url}'"]

        # Check if data is in Json/dict format, convert it into string after that
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
            contentType = headers.get('Content-Type', None)
            if contentType is None:
                headers.update({'Content-Type': 'application/json'})
                finalParams.append(f"--data-raw '{data}'")
            elif str(contentType).lower() == 'application/json':
                finalParams.append(f"--data-raw '{data}'")
            elif str(contentType).lower() == 'application/x-www-form-urlencoded':
                finalParams.append(f"--data '{data}'")
            else:
                raise Exception(f"Content Type {contentType} is not supported !!")

        if len(headers) > 0:
            for k, v in headers.items():
                finalParams.append(f"--header '{k}: {v}'")

        command = "\n".join(finalParams)
        now = datetime.now(pytz.timezone("Asia/Calcutta"))
        name = f"CurlCmd_{now.minute}{now.second}{now.microsecond}.json"
        allure.attach(command, name=name, attachment_type=allure.attachment_type.TEXT)

        curlFile = f"CurlCommands.log"
        if len(self.curlCmds) == 0 and os.path.isfile(curlFile):
            os.remove(curlFile)

        command = " ".join(finalParams)
        self.curlCmds.append(command)
        with open(curlFile, "w") as _fp:
            _fp.write("\n".join(self.curlCmds))

        return command, name

    @staticmethod
    def dict_to_ns(dictionary):
        """
        Convert Dictionary to Name-Spaced Items
        :param dictionary:
        :return:
        """
        return json.loads(json.dumps(dictionary), object_hook=lambda d: Namespace(**d))

    @staticmethod
    def create_csv(name, header, rows):
        """
        :param name:
        :param header:
        :param rows:
        :return:
        """
        if not isinstance(rows, list):
            raise Exception(f"Rows Should be list !!")

        with open(name, 'w') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(header)  # Write header
            csvWriter.writerows(rows)  # write Rows

    @staticmethod
    def check_required_args(args):
        """
        This function will check the given kwargs are not not-none
        :param args:
        :return:
        """
        for arg in args:
            if arg is None:
                raise Exception(f"One of the mandatory parameter is None, Please check API Swagger !!. Args <{args}>")

    @staticmethod
    def generate_guid():
        """
        Function to generate GUID
        :return:
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_first_name():
        """
        Function to generate First Name
        :return:
        """
        return str(Faker().first_name())

    @staticmethod
    def generate_phone_number(max_digits=10):
        """
        Function to generate phone number
        :param max_digits:
        :return:
        """
        return random.randint(10 ** (max_digits - 1), 10 ** max_digits - 1)

    @staticmethod
    def generate_last_name():
        """
        Function to generate Last Name
        :return:
        """
        return str(Faker().last_name())

    @staticmethod
    def is_key_there_in_dict(_list, _dict):
        """
        Check if key is there in dictionary
        :param _list:
        :param _dict:
        :return:
        """
        if isinstance(_list, str):
            _list = [_list]

        if not isinstance(_list, list):
            raise Exception(f"{_list} should be list, other formats not accepted !!")

        for x in _list:
            if x not in _dict.keys():
                raise Exception(f"'{x}' not found in {_dict} !!")


class SendRestRequest:
    """
    Class to send Rest Requests on a remote server
    """

    def __init__(self, name='rest', noop=False, debug=False):
        """
        Init Function to get the Auth Token
        """
        super().__init__()
        self.name = name
        self.noop = noop
        self.debug = debug
        self.configs = self.read_configs()
        self.semaphore = Semaphore(1)
        self.session = requests.Session()
        self.session.verify = self.configs.rest.verify
        self.session.timeout = self.configs.rest.timeout
        self.sequence = 0
        self.testCaseName = None
        self.testCaseClass = None

        mount = HTTPAdapter(
            pool_connections=self.configs.rest.pool.connections, pool_maxsize=self.configs.rest.pool.maxsize,
            max_retries=self.configs.rest.retries
        )
        self.session.mount("http://", mount)
        self.session.mount("https://", mount)

        self.FailedCmds = []
        self.FailResFile = Path(__file__).parent.parent / 'FailedResponse.log'
        if os.path.isfile(self.FailResFile):
            os.remove(self.FailResFile)

        self.CurlCmds = []
        self.CurlCmdFile = Path(__file__).parent.parent / f"{self.name.lower()}CurlCmds.log"
        if os.path.isfile(self.CurlCmdFile):
            os.remove(self.CurlCmdFile)

        self.apiCalls = list()
        self.apiCallsFile = Path(__file__).parent.parent / f"apiCalls.csv"
        if os.path.isfile(self.apiCallsFile):
            os.remove(self.apiCallsFile)

        self.session.headers.update({
            "Content-Type": "application/json", "Accept": "*/*"
        })

    @staticmethod
    def read_configs():
        """
        Read Configs File
        :return:
        """
        with open(Path(__file__).parent.parent / 'configs.yaml', 'r') as fp:
            data = yaml.safe_load(fp.read())
        return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

    def write_rest_to_file(self, response):
        """
        Write rest response
        :param response:
        :return:
        """
        self.sequence += 1
        # Generate the Curl Command

        # Save Curl Command
        CurlCmd = self.curl_command(response)
        if response.ok is True:
            name = f"{self.sequence:04}-PassCurl: {urlparse(response.url).path}"
        else:
            name = f"{self.sequence:04}-FailCurl: {urlparse(response.url).path}"
        try:
            allure.attach(CurlCmd, name=name, attachment_type=allure.attachment_type.TEXT)
        except (Exception, ValueError):
            pass

        self.CurlCmds.append({self.sequence: CurlCmd})
        with open(self.CurlCmdFile, 'w') as fp:
            for cmd in self.CurlCmds:
                for seq, _cmd in cmd.items():
                    fp.write(f"{seq:03}. {_cmd}\n")

        # Save Curl Response (allure: always and Console: when Error)
        if response.ok is True:
            name = f"{self.sequence:04}-PassResponse: {urlparse(response.url).path}"
        else:
            name = f"{self.sequence:04}-FailResponse: {urlparse(response.url).path}"
        try:
            restResponse = response.json()
        except (Exception, ValueError, KeyError, json.JSONDecodeError):
            restResponse = response.text

        # Save the API Call (for reporting)
        self.apiCalls.append([self.testCaseName, self.testCaseClass, urlparse(response.request.url).path, response.request.method])
        with open(self.apiCallsFile, 'w') as csvFile:
            header = ['S. No.', 'test-case-name', 'test-case-class', 'Endpoint', 'Request-Type']
            rows = []
            for count, apiCall in enumerate(self.apiCalls, start=1):
                _row = [f"{count:02}"] + apiCall
                rows.append(_row)
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(header)
            csvWriter.writerows(rows)

        try:
            allure.attach(json.dumps(restResponse, indent=2), name=name, attachment_type=allure.attachment_type.JSON)
        except (Exception, ValueError):
            pass

        # When Fails, save it on local file system as well
        if response.ok is False:
            self.FailedCmds.append({self.sequence: {'Curl': CurlCmd, 'Response': json.dumps(restResponse, indent=2)}})
            with open(self.FailResFile, 'w') as fp:
                for cmd in self.FailedCmds:
                    for seq, _cmd in cmd.items():
                        c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
                        fp.write(f"{seq:03}. {c_time} {_cmd['Curl']}\n{_cmd['Response']}\n")

    @staticmethod
    def curl_command(response):
        """
        Get Curl Command Before it is being Hit
        :param response:
        :return:
        """
        url = response.request.url
        method = response.request.method
        toRemove = ['User-Agent', 'Connection', 'Cookie', 'Content-Length']
        headers = {k: v for k, v in response.request.headers.items() if k not in toRemove}
        data = json.loads(response.request.body.decode()) if response.request.body else None
        params = getattr(response.request, 'params', None)

        if not any([url, method]):
            raise Exception(f"method and url are mandatory params for generating curl request")

        if params:
            try:
                url = f'{url}?{"&".join([f"{k}={v}" for k, v in params.items()])}'
            except (Exception, ValueError):
                url = f'{url}?{quote("&".join([f"{k}={v}" for k, v in params.items()]), safe="")}'

        # Generate the Final Params
        finalParams = [f"curl --request {method} --location --silent --show-error '{url}'"]

        # Check if data is in Json/dict format, convert it into string after that
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
            contentType = headers.get('Content-Type', None)
            if contentType is None:
                headers.update({'Content-Type': 'application/json'})
                finalParams.append(f"--data-raw '{data}'")
            elif str(contentType).lower() == 'application/json':
                finalParams.append(f"--data-raw '{data}'")
            elif str(contentType).lower() == 'application/x-www-form-urlencoded':
                finalParams.append(f"--data '{data}'")
            else:
                raise Exception(f"Content Type {contentType} is not supported !!")

        if len(headers) > 0:
            for k, v in headers.items():
                finalParams.append(f"--header '{k}: {v}'")

        return " ".join(finalParams)

    def send_request(self, **kwargs):
        """
        Send any Request
        :param kwargs
        """
        if self.noop:
            return kwargs

        self.semaphore.acquire()
        if kwargs.get('files', None):
            self.session.headers.pop('Content-Type', None)

        method = kwargs.get('method', None)
        url = kwargs.get('url', None)
        if not all([method, url]):
            self.semaphore.release()
            raise Exception(f"method and url are mandatory parameters for Rest Request !!")

        # Update Headers
        Headers = kwargs.get('headers', None)
        if Headers and isinstance(Headers, dict):
            self.session.headers = Headers

        # Perform the Rest Request
        response = self.session.request(**kwargs)

        # Write Curl and Response to a file for debugging
        if 'files' not in kwargs and 'stream' not in kwargs and "webaccess" not in kwargs["url"]:
            self.write_rest_to_file(response)

        # Send back the Response as it is
        self.semaphore.release()
        return response

    @staticmethod
    def raise_for_status(response):
        """
        Raise for Status (custom)
        """
        try:
            c_time = datetime.now(tz=pytz.timezone("Asia/Calcutta")).ctime()
            response.raise_for_status()
        except (Exception, ValueError) as Exp:
            ExpParams = {
                'url': response.url,
                'method': response.request.method,
                'status_code': response.status_code,
                'reason': response.reason,
                'text': response.text,
            }
            if hasattr(response.request, 'body') and response.request.body:
                ExpParams.update({'body': response.request.body.decode()})
            if hasattr(response.request, 'headers') and response.request.headers:
                ExpParams.update({'headers': {k: v for k, v in response.request.headers.items()}})
            if hasattr(response.request, 'params') and response.request.params:
                ExpParams.update({'params': {k: v for k, v in response.request.params.items()}})

            ExpParams = json.dumps(ExpParams, indent=2)
            raise Exception(f"{c_time} Request Failed with Exception: {Exp} :: \n{ExpParams}")


class SSHClient:
    """
    Class to connect and Talk to SSH Client
    """

    def __init__(self, **kwargs):
        """
        Init Class
        :param kwargs:
        """
        hostname = kwargs.get('hostname', None)
        port = int(kwargs.get('port', 22))
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)

        if not all([hostname, port, username, password]):
            raise Exception(f"Some Mandatory Parameters are missing {kwargs} !!")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=hostname, port=port, username=username, password=password)

        self.logLocation = r"/dacx/var/ameyo/dacxdata/com.drishti.dacx.server.product/logs"
        self.logFiles = ["ameyo-server.log", "ameyo-server-command.log", "root.log"]
        self.fileBytes = dict()

    def get_file_bytes(self, location=None):
        """
        Get Current Bytes in Log File
        :param location:
        :return:
        """
        if location is None:
            location = self.logLocation

        cmd = f'sudo bash -c "cd {location};ls -tdra -- */ | grep "__" | tail -n 1 | cut -d\'/\' -f1"'
        _, stdout, _ = self.ssh.exec_command(cmd, timeout=10)
        location = os.path.normpath(os.path.join(location, "".join(stdout.readlines()).strip()))
        for _file in self.logFiles:
            _file = str(os.path.normpath(os.path.join(location, _file)).replace("\\", "/"))
            cmd = f'sudo bash -c "ls -l {_file} | cut -d \' \' -f5"'
            _, stdout, _ = self.ssh.exec_command(cmd, timeout=10)
            self.fileBytes[_file] = int("".join(stdout.readlines()).strip())

    def get_delta_logs(self):
        """
        Get Delta Logs
        :return:
        """
        fileContents = dict()
        for _file, _start in self.fileBytes.items():
            cmd = f'sudo bash -c "tail {_file} -c +{_start}"'
            _, stdout, _ = self.ssh.exec_command(cmd, timeout=10)
            _file, _data = os.path.basename(_file), "".join(stdout.readlines())
            allure.attach(body=_data, name=_file, attachment_type=allure.attachment_type.TEXT, )
            fileContents[_file] = _data
        return fileContents


if __name__ == '__main__':
    s = SSHClient(hostname='vapt.ameyo.net', port="20222", username='', password='')
    s.get_file_bytes()
    s.get_delta_logs()
