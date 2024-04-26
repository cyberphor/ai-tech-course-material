# Cloud Native: DevOps for Cloud Native Applications
The purpose of this project is to build a DevOps pipeline with the following components: code style checks, docstring checks, code tests, Continuous Integration (CI), and Continuous Deployment (CD). 
* [References](#references)
* [Notes](#notes)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)

## References
If I find any helpful references, I will put them here. 
* [SuperFastPython - RuntimeWarning: Coroutine Was Never Awaited](https://superfastpython.com/asyncio-coroutine-was-never-awaited/)

## Notes
If I take any additional notes, I will put them here. 

**Git Hooks**  
A Git hook is a custom script you configured Git to run whenever a specific action occurs.  There's two different types of Git hooks: client-side and server-side. Client-side Git hooks are triggered by commit and/or merge actions. Server-side Git hooks are triggered by push actions. To "install" a Git hook, put it in the `.git/hooks/` directory of your project (this assumes you've already ran `git init` or downloaded the project from your Version Control System). Git hooks can be written in BASH or Python among other languages. Beware: Git hooks can add complexity, be disabled, and/or lead to bad practices (e.g., not committing early or often). 

**ruff**  
Ruff is a Python linter that combines multiple linters into one tool. 

**pydoclint**  
Pydoclint is another Python linter except it checks what your docstrings contains. Below is an example of a good, Google-style docstring. 

**coverage**  
Coverage is a Python package used to calculate code coverage. 

**httpx**  
httpx is a Python package used to test FastAPI applications. 

**Google Comment Style**  
```python
def eat_pizza(param1, param2):
    """
    This is an example of Google style.
    
    Args:
        param1: This is the first param.
        param2: This is a second param.
    
    Returns:
        This is a description of what is returned.
    
    Raises:
        KeyError: Raises an exception.
    """
```

## Setup
The steps in this tutorial assume (1) you're using a Linux-based environment (GitHub Codespaces, Azure Shell, Windows Subsystem for Linux, or a Linux virtual machine) and (2) you've installed the software required for the project (e.g., Python, the `venv` Python package, Poetry, Docker, Kubernetes, Helm, and Azure CLI). 

### Subtask 01: Create a Git Hook
**Step 1.** Accept and download the first GitHub Assignment provided. Then, change directories to the root of the project.  

**Step 2.** Change directories to `devtools-reqs/`.  
```bash
cd devtools-reqs/
```

**Step 3.** In the `devtools-reqs/` folder, create a virtual environment called `env` using the `venv` Python package. 
```bash
python3 -m venv env
```

**Step 4.** Activate the virtual environment you just created in the `devtools-reqs/` folder.
```bash
source env/bin/activate
```

**Step 5.** Install the "pre-commit" Python Package. 
```bash
pip install pre-commit
```

**Step 6.** Change directories to where the `.pre-commit-config.yaml` file is located (i.e., the root of the project directory). 
```bash
cd ../
``` 

**Step 7.** Create a Git hook using the "pre-commit" Python Package. The purpose of this step is to add a Python-based Git hook to the first GitHub Assignment provided. 
```bash
pre-commit install
```

**Step 8.** Run the Git hook you just created to make sure it works. 
```bash
pre-commit run --all-files
```

## Task 01
### Subtask 01: Identify and Fix "ruff" Findings
**Step 1.** Run `ruff` using the `pre-commit` Git hook. 
```bash
pre-commit run --all-files ruff
```

**Step 2.** Fix all the `ruff` findings.

### Subtask 02: Identify and Fix "pydoclint" Findings
**Step 1.** Run `pydoclint` using the `pre-commit` Git hook. 
```bash
pre-commit run --all-files pydoclint
```

**Step 2.** Fix all the `pydoctlint` findings.

### Subtask 03: Create Missing Code Tests and Achieve 100% Code Coverage for the FastAPI-based Application
**Step 1.** Change directories to the `fastapi-p4` folder. 
```bash
cd fastapi_p4/
```

**Step 2.** Use the `pyproject.toml` file within the `fastapi_p4/` folder to install the following Python dependencies: `coverage`, `pytest`, and `httpx`. 
```bash
poetry install --with dev
```

**Step 3.** Use `coverage` to run `pytest` and the provided tests. 
```bash
poetry run coverage run -m pytest
```

**Step 4.** Generate a report for the tests you just ran. The `Missing` column describes what lines are missing a test. 
```bash
poetry run coverage report --format=text -m
```

You should get output similar to below.
```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
fastapi_p4/__init__.py        0      0   100%
fastapi_p4/llmserver.py      48     11    77%   35-41, 85-92, 124, 134
tests/__init__.py             0      0   100%
tests/test_request.py         3      0   100%
-------------------------------------------------------
TOTAL                        51     11    78%
```

**Step 5.** Create tests for the lines listed in the `Missing` column in the coverage report. 

**Step 6.** From the `fastapi_p4/` folder, run the new tests you just added and then, print an updated code test coverage report. 
```bash
poetry run coverage run -m pytest && poetry run coverage report --format=text -m
```

### Subtask 04: Create Missing Code Tests and Achieve 100% Code Coverage for the Django-based Application
**Step 1.** Change directories to the `django` folder. 
```bash
cd ../django/
```

**Step 2.** In the `django/` folder, create a virtual environment called `env` using the `venv` Python package. 
```bash
python3 -m venv env
```

**Step 3.** Activate the virtual environment you just created in the `django/` folder. 
```bash
source env/bin/activate
```

**Step 4.** Install the Python dependencies listed in the `requirements.txt` file. 
```bash
pip install -r requirements.txt
```

**Step 5.** From the `django/` folder, run the tests built-in to the Django application called `task3`.  
```bash
coverage run --source='.' manage.py test task3
```

**Step 6.** Generate a report for the tests you just ran. 
```bash
coverage report --format=text -m
```

You should get output similar to below.
```
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
manage.py                               10      0   100%
task3/__init__.py                        0      0   100%
task3/login/__init__.py                  0      0   100%
task3/login/admin.py                     0      0   100%
task3/login/migrations/__init__.py       0      0   100%
task3/login/models.py                    0      0   100%
task3/login/serializers.py               6      0   100%
task3/login/tests.py                     2      0   100%
task3/login/views.py                    23      9    61%   42-74
task3/settings.py                       25      0   100%
task3/urls.py                            9      0   100%
------------------------------------------------------------------
TOTAL                                   75      9    88%
```

**Step 7.** In the `task3/` folder, create a directory called `tests`. 
```bash
mkdir task3/tests/
```

**Step 8.** In the `task3/` folder, create two files called `__init__.py` and `test_login.py`. *Nothing* goes in the `__init__.py` file. 
```bash
touch task3/tests/__init__.py task3/tests/test_login.py 
```

**Step 9.** Create tests for the lines listed in the `Missing` column in the previous coverage report and add them to `task3/tests/test_login.py`. 

**Step 10.** From the `django/` folder, run the new tests you just added and then, print an updated code test coverage report. 
```bash
coverage run --source='.' manage.py test task3 && coverage report --format=text -m
```

### How to Submit
Below is what I did to get credit for the work I did during Task 01. 

**Step 1.** From the root of the Task 01 project folder, change directories to the `fastapi-p4/` folder.
```bash
cd fastapi-p4/
```

**Step 2.** Export the requirements in the `fastapi-p4/` folders. 
```bash
poetry export -f requirements.txt --output requirements.txt
```

**Step 2.** While in the `fastapi-p4/` folder, activate the virtual environment in the `django/` folder.
```bash
source django/env/bin/activate
```

**Step 3.** While in the `fastapi-p4/` folder, install the exported `fastapi-p4` requirements. The purpose of this step is install the `fastapi-p4/` requirements in the virtual environment inside the `django/` folder. 
```bash
pip install -r requirements.txt
```

**Step 4.** While in the `fastapi-p4/` folder, install the requirements listed in the `devtools-reqs/` folder. The purpose of this step is install the `devtools-reqs/` requirements in the virtual environment inside the `django/` folder. 
```bash
pip install -r ../devtools-reqs/requirements.txt
```

**Step 6.** Change directories back to the root of the Task 01 project folder and run the submitter. 
```bash
cd ../
```

