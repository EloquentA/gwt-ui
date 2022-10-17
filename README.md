# AMEYO UI AUTOMATION
Automation for quality analysis of AMEYO UI.

## Setting up automation framework
### Prerequisites
- Any browser out of following must be installed on your machine
  - chrome
  - edge
  - firefox
- Python 3.8.10 or later
- Ubuntu 20.04 Machine (Script has been tested to run on Windows 11 and Ubuntu 20.04)
- Create a virtual environment and install dependencies based on the os
  - python3 -m pip install -r requirements.txt
- You can use any IDE for the development: pycharm or vscode are suggested
- Variable file
  - Setup variable in any of format from following to use in later commands to run automation
    - ameyo/variables/sample_variable.py
    - ameyo/variables/sample_variables.yml
### Initiate automation 
To run automation command please ensure virtual environment is activated and above all prerequisites are fulfilled.


## Running Tests

### Command line arguments
#### Variable file
  - --variablefile .\ameyo\variables\sample_variables.yml
  - --variablefile .\ameyo\variables\sample_variables.py
#### Report directory
  - --outputdir <path-to-dir>
#### To include specific tags
  - --include 'testrailid=617' 
  - --include regressionANDsanity: For running tests having both regression and sanity tags
  - --include regressionORsanity: For running tests having either regression or sanity or both tags
### MISC
  - To terminate on first failure `--exitonfailure`
  - To terminate on first error `--exitonerror`
  - For more arguments run `python -m robot --help`


### Run individual test suite files on Windows
`python -m robot --variablefile .\ameyo\variables\sample_variables.yml .\ameyo\tests\TS001_LoginSuite\TC001_Login.robot`

### Run individual test suite files on Mac/Ubuntu
`python3 -m robot --variablefile ./ameyo/variables/sample_variables.yml ./ameyo/tests/TS001_LoginSuite/TC001_Login.robot`

### Run individual test suite directory
`python -m robot --variablefile ./ameyo/variables/sample_variables.yml ./ameyo/tests/TS001_LoginSuite` 

### Run individual test suite directory on Mac/Ubuntu
`python3 -m robot --variablefile ./ameyo/variables/sample_variables.yml ./ameyo/tests/TS001_LoginSuite`

### Run test with Testrail reporting
`python -m robot --listener ".\ameyo\testrail\TestrailListener.py;server_url=<testrail-server-url>;testrail_username=<testrail-username>;<testrail-password>;project_id=<testrail-project-id>" --variablefile .\ameyo\variables\local_variables.yml --outputdir <log-dir> .\ameyo\tests\TS001_LoginSuite`

### Python debugger
`import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()`

### Allure report for Robot runs
`Install allure_robotframework: 
pip3 install allure_robotframework`

`Run Robot test case(s)/suite(s) with --listener arg as mentioned below:
 python3 -m robot --variablefile ./ameyo/variables/sample_variables.yml --listener allure_robotframework ./ameyo/tests/TS001_LoginSuite/TC001_Login.robot`

`Download latest allure-commandline from "https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/".
FOr e.g. Download "allure-commandline-2.19.0.zip" from "https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.9.0/"
Extract the Zip and add to PATH in bash_profile file, below is an e.g. on mac:

1. vim ~/.bash_profile
2. Add **export PATH="/Users/dummy/Desktop/allure-2.19.0/bin:$PATH"** line in the end and save the bash_profile file.
3. source ~/.bash_profile
`

Run  below command to generate allure report from Robot runs:****

**allure serve ./output/allure**

