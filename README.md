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
- Use setup-python.sh script on your ubuntu machine to setup Chrome Driver
  - It will also install all required packages and dependencies.
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


### Run individual test suite files
`python -m robot --variablefile .\ameyo\variables\sample_variables.yml .\ameyo\tests\TS001_LoginSuite\TC001_Login.robot` 

### Run individual test suite directory
`python -m robot --variablefile ./ameyo/variables/sample_variables.yml ./ameyo/tests/TS001_LoginSuite` 

### Run test with Testrail reporting
`python -m robot --listener ".\ameyo\testrail\TestrailListener.py;server_url=<testrail-server-url>;testrail_username=<testrail-username>;<testrail-password>;project_id=<testrail-project-id>" --variablefile .\ameyo\variables\local_variables.yml --outputdir <log-dir> .\ameyo\tests\TS001_LoginSuite`

### Python debugger
`import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()`