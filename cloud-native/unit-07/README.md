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

**Tekton**  
Tekton is a CI system designed for Kubernetes. 

**Kaniko**  
Kaniko is used to build Docker containers inside Kubernetes clusters. 

## Setup
The steps in this tutorial assume (1) you're using a Linux-based environment (GitHub Codespaces, Azure Shell, Windows Subsystem for Linux, or a Linux virtual machine) and (2) you've installed the software required for the project (e.g., Python, the `venv` Python package, Poetry, Terraform, Docker, Kubernetes, Helm, and Azure CLI). 

## Task 01
### Subtask 01: Create a Git Hook
**Step 1.** Accept and download the first GitHub Assignment provided. Then, change directories to the root of the repository.  

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

### Subtask 02: Identify and Fix "ruff" Findings
**Step 1.** Run `ruff` using the `pre-commit` Git hook. 
```bash
pre-commit run --all-files ruff
```

**Step 2.** Fix all the `ruff` findings.

### Subtask 04: Identify and Fix "pydoclint" Findings
**Step 1.** Run `pydoclint` using the `pre-commit` Git hook. 
```bash
pre-commit run --all-files pydoclint
```

**Step 2.** Fix all the `pydoctlint` findings.

### Subtask 05: Create Missing Code Tests and Achieve 100% Code Coverage for the FastAPI-based Application
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

### Subtask 06: Create Missing Code Tests and Achieve 100% Code Coverage for the Django-based Application
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

**Step 3.** While in the `fastapi-p4/` folder, activate the virtual environment in the `django/` folder.
```bash
source django/env/bin/activate
```

**Step 4.** While in the `fastapi-p4/` folder, install the exported `fastapi-p4` requirements. The purpose of this step is install the `fastapi-p4/` requirements in the virtual environment inside the `django/` folder. 
```bash
pip install -r requirements.txt
```

**Step 5.** While in the `fastapi-p4/` folder, install the requirements listed in the `devtools-reqs/` folder. The purpose of this step is install the `devtools-reqs/` requirements in the virtual environment inside the `django/` folder. 
```bash
pip install -r ../devtools-reqs/requirements.txt
```

**Step 6.** Change directories back to the root of the Task 01 project folder and run the submitter. 
```bash
cd ../
```

## Task 02
### Subtask 01: Deploy an ACR and AKS Instance Using Terraform
**Step 1.** Accept and download the second GitHub Assignment provided. Then, change directories to the root of the repository.  

**Step 2.** Change directories to `terraform/`.  
```bash
cd terraform/
```

**Step 3.** Create and open a file called `main.tf`.
```bash
vim main.tf
```

**Step 4.** Add the content below to the `main.tf` file.
```hcl
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_container_registry" "main" {
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  name                = var.container_registry_name
  sku                 = "Standard" 
  admin_enabled       = false
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = var.kubernetes_cluster_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  node_resource_group = "${azurerm_resource_group.main.name}-kubernetes-nodes"
  dns_prefix          = azurerm_resource_group.main.name
  default_node_pool {
    name       = "default"
    node_count = var.kubernetes_node_count
    vm_size    = var.kubernetes_node_size
  }
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "main" {
  principal_id                     = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.main.id
  skip_service_principal_aad_check = true
}
```

**Step 5.** Create and open a file called `variables.tf`.
```bash
vim variables.tf
```

**Step 6.** Add the content below to the `main.tf` file.
```hcl
variable "location" {
  type    = string
  default = "eastus"
}

variable "resource_group_name" {
  type    = string
  default = "p7aks"
}

variable "container_registry_name" {
  type    = string
  default = "p7acrcyberphor"
}

variable "kubernetes_cluster_name" {
  type    = string
  default = "p7cluster"
}

variable "kubernetes_node_size" {
  type    = string
  default = "Standard_D2S_v3" 
}

variable "kubernetes_node_count" {
  type    = number
  default = 5
}
```

**Step 7.** Initialize the `terraform/` folder for Terraform-use. The purpose of this step is to initialize the Terraform backend for your project (i.e., your file system) and install the Terraform plugin-providers specified in the provided `simpleacr.tf` file.  
```bash
terraform init
```

**Step 8.** Create and apply a Terraform execution plan using the `.tf` files you just created. 
```bash
terraform apply
```

**Step 9.** Change directories to the root of the repository.
```bash
cd ../
```

### Subtask 02: Configure Your AKS Instance
**Step 1.** Download credentials from your AKS instance for `kubectl` to use.
```bash
az aks get-credentials --name "p7cluster" --resource-group "p7aks"
```

**Step 2.** Install the Tekton Kubernetes Operator in your AKS instance. 
```bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

**Step 3.** Create an SSH key pair using `tekton/access` as the filename (do not enter a passphrase). This step will generate two files in the `tekton` folder: `access` and `access.pub`. 
```bash
ssh-keygen -t rsa -f tekton/access
```

**Step 4.** Change directories to the `tekton/` folder.
```bash
cd tekton/
```

**Step 5.** Print the contents of the `access.pub` file in the `tekton/` folder to the console and then, copy it. 
```bash
cat access.pub
```

**Step 6.** Login to GitHub and go to the repository provided for Task 02.

**Step 7.** Click the "Settings" tab. 

**Step 8.** Under "Security", click "Deploy keys."

**Step 9.** Click "Add deploy key."

**Step 10.** In the "Title" field, enter `Tekton`.

**Step 11.** In the "Key" field, paste the contents of the `access.pub` file.

**Step 12.** Click "Add key."

**Step 13.** Print the contents of the `access` file in the `tekton/` folder to the console, pipe it to the `base64` program, and then, copy it. 
```bash
cat access | base64
```

You should get output similar to below.
```
VF0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFZRUFsczZDMlNjRS9EbWlQYXV4WTB6bktLVGxPUUJkc2ZsZDVDNkNnRWlSZCtCb0pwZFBNQys4CngrT2piaVRGa0s1Y2xlcXFGZmNZRjF2QnZGbXRkUnZ6WTlsTXl0Q05uS3NUMm0wZnNvbW5aOE9rZDZEcG9TT1ZZS0I3MTgKdHFwaWx2WHE4V001Nmh6b3g4Y2d5Qzh4YkdKbW5HWjJtZFFEbElVSkxiNDE2N1lheFlQMnV2bXdJOWp5eDZGNHFUOXAyYQpMdEFZVDZRSmFWRWFYdy80Qm03VExkdkF2RGhEM3dBM3ZUVmcrVkpveC8vcHNNb0o3bnF2U0UzZkFCcldVWmlBc2tKVXF0CkZ6dVJkV3V3c3BNVXZCSE1pbS9sNmdpWnRXK3pwUHE5d2VYYXFYZld2TEs4MHNwazg5b3I1Uy8zM1JJeWFZczV0aEswQXQKWG92YVFuQkg0Y3hlV210cis1YjdhK21BYlF1d3QzQ2lUQUZaT0NmYXNJZEFTOXVGNlo0cTdWTTlydW5LTVovYkpCRExLYwpDcWxiSVlMSjFSaFhUNkxhYVhEWnd6VTBIdkpHWXRBb0RVNVViaWFjb3ZXZGszcHRIdGtwQUZkUnZPcDd0SGpvTUhBcFlLCmw4bi90T3hJWnBKUllwNjhvUzRwekVVYU4zZElnM1ZhYTJVN0tKckZBQUFGaUJKbWRoSVNabllTQUFBQUIzTnphQzF5YzIKRUFBQUdCQUpiT2d0a25CUHc1b2oycnNXTk01eWlrNVRrQVhiSDVYZVF1Z29CSWtYZmdhQ2FYVHpBdnZNZmpvMjRreFpDdQpYSlhxcWhYM0dCZGJ3YnhaclhVYjgyUFpUTXJRalp5ckU5cHRIN0tKcDJmRHBIZWc2YUVqbFdDZ2U5ZkxhcVlwYjE2dkZqCk9lb2M2TWZISU1ndk1XeGlacHhtZHBuVUE1U0ZDUzIrTmV1MkdzV0Q5cnI1c0NQWThzZWhlS2svYWRtaTdRR0Ura0NXbFIKR2w4UCtBWnUweTNid0x3NFE5OEFONzAxWVBsU2FNZi82YkRLQ2U1NnIwaE4zd0FhMWxHWWdMSkNWS3JSYzdrWFZyc0xLVApGTHdSeklwdjVlb0ltYlZ2czZUNnZjSGwycWwzMXJ5eXZOTEtaUFBhSytVdjk5MFNNbW1MT2JZU3RBTFY2TDJrSndSK0hNClhscHJhL3VXKzJ2cGdHMExzTGR3b2t3QldUZ24yckNIUUV2YmhlbWVLdTFUUGE3cHlqR2YyeVFReXluQXFwV3lHQ3lkVVkKVjAraTJtbHcyY00xTkI3eVJtTFFLQTFPVkc0bW5LTDFuWk42YlI3WktRQlhVYnpxZTdSNDZEQndLV0NwZkovN1RzU0dhUwpVV0tldktFdUtjeEZHamQzU0lOMVdtdGxPeWlheFFBQUFBTUJBQUVBQUFHQWJEbVh2YTg2N0tlUHZ5SlFFeXRGV08yOWNzCkxJZXNpeWtPYXYwTkJEVlB3K3dqTWtLVGlaQ2ZwYmR0ZjgwRy9SRWVWdVdvVVJUUElVZnM3OHBHYUNyTTF0UnIrVVlUS0UKOU9RTE0xMkdQZmt4Tm9qTUlWQWdDMUFna0NUelRIdS82UHROdTQzRUlTN0F3RGdxWWJtZVNrTHVsNWc3dWJOaUtqQzZqTgptWEwrazNDNHlFWVlHaUcvV1hTUDJ5WWZHSWpML2FNbzFPRTc2WVpsQlhkb1ppRnk3MWloMzIxenFZeGJoZzk0d2tsaU1aCjJqMmtFdmtJZ2FNZ3ZqcUVROXBrcDM4Q2dWaGtZL3FCN0ZlRUhqTndjMTc1ZWR6MzBuYXI4M1RlOEQrV2tPbURCUTkxaHUKeUN2NkxZUi9lZkw1bzFSV3Rlei9oVE5RRmV5emRCRExsSTVPU3lZSFNHaGw3ZWdKYUFkaUl3ZGhReE1LVjZ5TzdFNWNEQgpIUjlTMytXbG13Nkd4VnRUNHJuQkNrZjBtTERtVTFicVFucnlpTW9rb052Z1BHVnhPOUxleEdUbm5ucTRwd3lQZ3FuaG9jCllVU1RzSTdhVW9mOWdGVXFRR3FCMFpBVVEwS3BENjI5clFFMWNZQjJ0UHMwZ3kxeUdhb0pmRmloVHZWSVlXY1ZLaEFBQUEKd0RvSWNrdFpXRUhtQUtKcWFEUVVDNEdQV1BBblBaWXNxU2VoVE1zNW5vQ2FsT3I0TFJuSVVXRkx5aE9BaEw1RHpMQnh6bQpmTFZrbUE4M0RHZXl0Q2IrSklBNUlWaWJmeWJFU3NUM1puZFBwdnhkckRqa0JCak9LaGM0aUZQZ1FTK3Urek1nZ0MvUHdICnZPb01NNDNDamdOU2NMSldyQVNlZWpTWUVoU1VCZ3VRM2c1T0s0NVlUNGNSa2ZUZFdNb1lUaEVWd3VWQ1MzbDBMOHpnRnIKU3BTTkZHeThucWZpcWpkVlFEMzNmZERhZ0liWGQ0dDcxZ1luSHhDMVlUR1kzRU5nQUFBTUVBeHZ4a09QTmVYMlFmdWl2TQpmZUFIZjg0UTBTbGk4Y3RHOUVDTVNnc1BxQlE1cmpmR3c3S0lwbHhEMGpUNTRleGg0TWRjQ1lzelo2ZnV3b3RlRnFTTS9XCmhrU29oK01GN2FDL2JDL3BjbXQ1Lzd2NGlMSmF6Mi8yaHJRTGVxVGJOKzNrNEVoTldoRyt4RmVKT2d1T0hpbEhiVlU4bXQKNlFJMEpnTjZUelE4MjRWYzlXdlg4TXRrVHc2SExDYXZNZzBYY0MxeUd2ZStDZ1R2RVFIMXFMVWVTRmdRdkhNcTR5NTF2YgpBa1dmbmRnSU5qbjdjbHVZc2w1ZU0yZlhuVUZ4MUxBQUFBd1FEQ0JDejRYSmZxNG0zSi80b0xIMXJTbGUyY0t5d3RuWGpmCklLM2krb1RCc1VGNEwrandUUm1YZjRuNTU1VnQ1cFR0ZE1URWFaby9yQ3JiemtFd2tyTUZQSWQzdEFsaXJxMG9HTFNSRHgKWlh3QkJoUFRlTDMrRzFMdEcrNUFWcWs5dDVvNkVnMWZqQ3Q4bTZQc1dzdHVaSjkyTkh3Q1d6NUw2UlBHMTVjWmxjckVWcgpBWlVhN1hGeXMrYWh5TUJvWUR0NTdFYWt3dUE3d05nZ3pCU21yL3phcDVZUEN0d1FvZ1VZTzJ5cExQUTJBUzFoQUhmbDhCCnVqWkhSQytnUjhiaThBQUFBUGRtbGpkRzl5UUcxaFl5MXRhVzVwQVFJREJBPT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==
```

**Step 14.** Change directories to the root of your repository, create a folder called `kubernetes`, and then, change directories to it.
```bash
cd ../
mkdir kubernetes
cd kubernetes/
```

**Step 15.** Create and open a Kubernetes manifest file called `git-credentials.yaml` in the `kubernetes/` folder.
```bash
vim git-credentials.yaml
```

**Step 16.** Add the content below to the `git-credentials.yaml` file (paste the contents of *your* `access` file in the `id_rsa` field).
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: git-credentials
data:
  id_rsa: VF0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFZRUFsczZDMlNjRS9EbWlQYXV4WTB6bktLVGxPUUJkc2ZsZDVDNkNnRWlSZCtCb0pwZFBNQys4CngrT2piaVRGa0s1Y2xlcXFGZmNZRjF2QnZGbXRkUnZ6WTlsTXl0Q05uS3NUMm0wZnNvbW5aOE9rZDZEcG9TT1ZZS0I3MTgKdHFwaWx2WHE4V001Nmh6b3g4Y2d5Qzh4YkdKbW5HWjJtZFFEbElVSkxiNDE2N1lheFlQMnV2bXdJOWp5eDZGNHFUOXAyYQpMdEFZVDZRSmFWRWFYdy80Qm03VExkdkF2RGhEM3dBM3ZUVmcrVkpveC8vcHNNb0o3bnF2U0UzZkFCcldVWmlBc2tKVXF0CkZ6dVJkV3V3c3BNVXZCSE1pbS9sNmdpWnRXK3pwUHE5d2VYYXFYZld2TEs4MHNwazg5b3I1Uy8zM1JJeWFZczV0aEswQXQKWG92YVFuQkg0Y3hlV210cis1YjdhK21BYlF1d3QzQ2lUQUZaT0NmYXNJZEFTOXVGNlo0cTdWTTlydW5LTVovYkpCRExLYwpDcWxiSVlMSjFSaFhUNkxhYVhEWnd6VTBIdkpHWXRBb0RVNVViaWFjb3ZXZGszcHRIdGtwQUZkUnZPcDd0SGpvTUhBcFlLCmw4bi90T3hJWnBKUllwNjhvUzRwekVVYU4zZElnM1ZhYTJVN0tKckZBQUFGaUJKbWRoSVNabllTQUFBQUIzTnphQzF5YzIKRUFBQUdCQUpiT2d0a25CUHc1b2oycnNXTk01eWlrNVRrQVhiSDVYZVF1Z29CSWtYZmdhQ2FYVHpBdnZNZmpvMjRreFpDdQpYSlhxcWhYM0dCZGJ3YnhaclhVYjgyUFpUTXJRalp5ckU5cHRIN0tKcDJmRHBIZWc2YUVqbFdDZ2U5ZkxhcVlwYjE2dkZqCk9lb2M2TWZISU1ndk1XeGlacHhtZHBuVUE1U0ZDUzIrTmV1MkdzV0Q5cnI1c0NQWThzZWhlS2svYWRtaTdRR0Ura0NXbFIKR2w4UCtBWnUweTNid0x3NFE5OEFONzAxWVBsU2FNZi82YkRLQ2U1NnIwaE4zd0FhMWxHWWdMSkNWS3JSYzdrWFZyc0xLVApGTHdSeklwdjVlb0ltYlZ2czZUNnZjSGwycWwzMXJ5eXZOTEtaUFBhSytVdjk5MFNNbW1MT2JZU3RBTFY2TDJrSndSK0hNClhscHJhL3VXKzJ2cGdHMExzTGR3b2t3QldUZ24yckNIUUV2YmhlbWVLdTFUUGE3cHlqR2YyeVFReXluQXFwV3lHQ3lkVVkKVjAraTJtbHcyY00xTkI3eVJtTFFLQTFPVkc0bW5LTDFuWk42YlI3WktRQlhVYnpxZTdSNDZEQndLV0NwZkovN1RzU0dhUwpVV0tldktFdUtjeEZHamQzU0lOMVdtdGxPeWlheFFBQUFBTUJBQUVBQUFHQWJEbVh2YTg2N0tlUHZ5SlFFeXRGV08yOWNzCkxJZXNpeWtPYXYwTkJEVlB3K3dqTWtLVGlaQ2ZwYmR0ZjgwRy9SRWVWdVdvVVJUUElVZnM3OHBHYUNyTTF0UnIrVVlUS0UKOU9RTE0xMkdQZmt4Tm9qTUlWQWdDMUFna0NUelRIdS82UHROdTQzRUlTN0F3RGdxWWJtZVNrTHVsNWc3dWJOaUtqQzZqTgptWEwrazNDNHlFWVlHaUcvV1hTUDJ5WWZHSWpML2FNbzFPRTc2WVpsQlhkb1ppRnk3MWloMzIxenFZeGJoZzk0d2tsaU1aCjJqMmtFdmtJZ2FNZ3ZqcUVROXBrcDM4Q2dWaGtZL3FCN0ZlRUhqTndjMTc1ZWR6MzBuYXI4M1RlOEQrV2tPbURCUTkxaHUKeUN2NkxZUi9lZkw1bzFSV3Rlei9oVE5RRmV5emRCRExsSTVPU3lZSFNHaGw3ZWdKYUFkaUl3ZGhReE1LVjZ5TzdFNWNEQgpIUjlTMytXbG13Nkd4VnRUNHJuQkNrZjBtTERtVTFicVFucnlpTW9rb052Z1BHVnhPOUxleEdUbm5ucTRwd3lQZ3FuaG9jCllVU1RzSTdhVW9mOWdGVXFRR3FCMFpBVVEwS3BENjI5clFFMWNZQjJ0UHMwZ3kxeUdhb0pmRmloVHZWSVlXY1ZLaEFBQUEKd0RvSWNrdFpXRUhtQUtKcWFEUVVDNEdQV1BBblBaWXNxU2VoVE1zNW5vQ2FsT3I0TFJuSVVXRkx5aE9BaEw1RHpMQnh6bQpmTFZrbUE4M0RHZXl0Q2IrSklBNUlWaWJmeWJFU3NUM1puZFBwdnhkckRqa0JCak9LaGM0aUZQZ1FTK3Urek1nZ0MvUHdICnZPb01NNDNDamdOU2NMSldyQVNlZWpTWUVoU1VCZ3VRM2c1T0s0NVlUNGNSa2ZUZFdNb1lUaEVWd3VWQ1MzbDBMOHpnRnIKU3BTTkZHeThucWZpcWpkVlFEMzNmZERhZ0liWGQ0dDcxZ1luSHhDMVlUR1kzRU5nQUFBTUVBeHZ4a09QTmVYMlFmdWl2TQpmZUFIZjg0UTBTbGk4Y3RHOUVDTVNnc1BxQlE1cmpmR3c3S0lwbHhEMGpUNTRleGg0TWRjQ1lzelo2ZnV3b3RlRnFTTS9XCmhrU29oK01GN2FDL2JDL3BjbXQ1Lzd2NGlMSmF6Mi8yaHJRTGVxVGJOKzNrNEVoTldoRyt4RmVKT2d1T0hpbEhiVlU4bXQKNlFJMEpnTjZUelE4MjRWYzlXdlg4TXRrVHc2SExDYXZNZzBYY0MxeUd2ZStDZ1R2RVFIMXFMVWVTRmdRdkhNcTR5NTF2YgpBa1dmbmRnSU5qbjdjbHVZc2w1ZU0yZlhuVUZ4MUxBQUFBd1FEQ0JDejRYSmZxNG0zSi80b0xIMXJTbGUyY0t5d3RuWGpmCklLM2krb1RCc1VGNEwrandUUm1YZjRuNTU1VnQ1cFR0ZE1URWFaby9yQ3JiemtFd2tyTUZQSWQzdEFsaXJxMG9HTFNSRHgKWlh3QkJoUFRlTDMrRzFMdEcrNUFWcWs5dDVvNkVnMWZqQ3Q4bTZQc1dzdHVaSjkyTkh3Q1d6NUw2UlBHMTVjWmxjckVWcgpBWlVhN1hGeXMrYWh5TUJvWUR0NTdFYWt3dUE3d05nZ3pCU21yL3phcDVZUEN0d1FvZ1VZTzJ5cExQUTJBUzFoQUhmbDhCCnVqWkhSQytnUjhiaThBQUFBUGRtbGpkRzl5UUcxaFl5MXRhVzVwQVFJREJBPT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==
```

**Step 17.** Apply the Kubernetes manifest file you just created.
```bash
kubectl apply -f git-credentials.yaml
```

**Step 18.** While in the `kubernetes/` folder, copy, paste, and run the commands below to your shell environment. Use the name of *your* ACR (there's two spots where you'll need to put it). NOTE: this script assumes `jq` is installed. Also, if you're not on a Mac, you may need to replace `base64` with `base64 -w0`.
```bash
ACR_NAME=p7acrcyberphor
SERVICE_PRINCIPAL_NAME=tektonUser
ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query id --output tsv)
PASSWORD=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role acrpush --query "password" --output tsv)
USER_NAME=$(az ad sp list --display-name $SERVICE_PRINCIPAL_NAME --query "[].appId" --output tsv)
echo $USER_NAME:$PASSWORD | base64 | jq -R -c '{  "auths": { "p7acrcyberphor.azurecr.io": { "auth" : . } } }'  > config.json
kubectl create secret generic docker-credentials --from-file=config.json=./config.json 
```

**Step 19.** Download a Kubernetes manifest file called `git-clone.yaml` to your `kubernetes/` folder.
```bash
wget https://raw.githubusercontent.com/tektoncd/catalog/main/task/git-clone/0.9/git-clone.yaml
```

**Step 20.** Download a Kubernetes manifest file called `kanifko.yaml` to your `kubernetes/` folder.
```bash
wget  https://raw.githubusercontent.com/tektoncd/catalog/main/task/kaniko/0.6/kaniko.yaml
```

**Step 21.** Apply the Kubernetes manifest files you just downloaded to your AKS instance.
```bash
kubectl apply -f git-clone.yaml
kubectl apply -f kaniko.yaml
```

### Subtask 03: Create a Tekton CI Pipeline
**Step 1.** While in the `kubernetes/` folder, create and open a Kubernetes manifest file called `tekton-pipeline.yaml`. 
```bash
vim tekton-pipeline.yaml
```

**Step 2.** Add the content below to it. 
```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: p7ci
  namespace: default
spec:
  params:
    - name: repo-url           # the SSH url for your GitHub repository
      type: string
    - name: image-repository   # FQDN of your ACR
      type: string
  workspaces:
    - name: shared-data
    - name: git-credentials
    - name: docker-credentials 
  tasks:
    - name: fetch-source
      taskRef:
        name: git-clone
      workspaces:
      - name: output
        workspace: shared-data
      - name: ssh-directory
        workspace: git-credentials
      params:
      - name: url
        value: $(params.repo-url)
    - name: build-push-llm
      runAfter: ["fetch-source"]
      taskRef:
        name: kaniko
      workspaces:
      - name: source
        workspace: shared-data
      - name: dockerconfig
        workspace: docker-credentials    
      params:
      - name: IMAGE
        value: $(params.image-repository)/llm:$(tasks.fetch-source.results.committer-date)-$(tasks.fetch-source.results.commit)
      - name: DOCKERFILE
        value: src/fastapi-p4/docker/Dockerfile
      - name: CONTEXT
        value: src/fastapi-p4
```

**Step 3.** Apply the Kubernetes manifest file you just created. 
```bash
kubectl apply -f tekton-pipeline.yaml
```

### Subtask 04: Create a Tekton CI Pipeline Run
**Step 1.** While in the `kubernetes/` folder, create and open a Kubernetes manifest file called `tekton-pipeline-run.yaml`. 
```bash
vim tekton-pipeline-run.yaml
```

**Step 2.** Add the content below to it. Make sure to use the SSH URL for *your* GitHub repository (the one for Task 2) and the fully-qualified domain name for *your* ACR.
```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: p7ci-
spec:
  pipelineRef:
    name: p7ci
  podTemplate:
    securityContext:
      fsGroup: 65532
  workspaces:
  - name: shared-data
    volumeClaimTemplate:
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 3Gi
  - name: git-credentials
    secret:
      secretName: git-credentials
  - name: docker-credentials
    secret:
      secretName: docker-credentials
  params:
  - name: repo-url
    value: git@github.com:CloudNativeSpring2024/project-7-task-2-cloud-native-continuous-integration-cyberphor.git
  - name: image-reference
    value: p7acrcyberphor.azurecr.io
```

**Step 3.** Create a Tekton pipeline run using the Kubernetes manifest file you just created.
```bash
kubectl create -f tekton-pipeline-run.yaml
```

**Step 4.** Change directories to the root of your repository.
```bash
cd ../
```

**Step 5.** Download, unzip, and decompress the Tekton CLI program (make sure to use the [correct version for your machine](https://github.com/tektoncd/cli/releases)). 
```bash
curl -LO  https://github.com/tektoncd/cli/releases/download/v0.35.2/tektoncd-cli-0.35.2_Linux-64bit.deb
sudo dpkg -i tektoncd-cli-0.35.2_Linux-64bit.deb
```

**Step 6.** Change the access mode for the Tekton CLI program so you can execute it.
```bash
chmod u+x tkn
```

**Step 7.** Verify the Tekton CI pipeline run was successful using the Tekton CLI program. It will probe your Kubernetes cluster. 
```bash
tkn pipeline logs -f -L
```

You should eventually get output similar to below.
```
INFO[0235] Taking snapshot of full filesystem...        
INFO[0255] COPY ./fastapi_p4 /code/app                  
INFO[0255] Taking snapshot of files...                  
INFO[0255] CMD ["uvicorn", "app.llmserver:app", "--host", "0.0.0.0", "--port", "8080"] 
INFO[0255] Pushing image to p7acrcyberphor.azurecr.io/llm:1714162458-23d78d58222aaeee07bc758a600f672f8b47e78f 
INFO[0274] Pushed image to 1 destinations               

p7acrcyberphor.azurecr.io/llm:1714162458-23d78d58222aaeee07bc758a600f672f8b47e78f
```

### Subtask 05: Add a Task to the Tekton CI Pipeline to Build the Login Service
**Step 1.** Change directories to the `kubernetes/` folder.
```bash
cd kubernetes/
```

**Step 2.** Open the Kubernetes manifest file called `tekton-pipeline.yaml`.
```bash
vim tekton-pipeline.yaml
```

**Step 3.** Append the content below to it.
```yaml
    - name: build-push-django
      runAfter: ["build-push-llm"]
      taskRef:
        name: kaniko
      workspaces:
      - name: source
        workspace: shared-data
      - name: dockerconfig
        workspace: docker-credentials    
      params:
      - name: IMAGE
        value: $(params.image-reference)/login:$(tasks.fetch-source.results.committer-date)-$(tasks.fetch-source.results.commit)
      - name: DOCKERFILE
        value: src/django/docker/Dockerfile
      - name: CONTEXT
        value: src/django
```

**Step 5.** Apply the changes you made to the Kubernetes manifest file called `tekton-pipeline.yaml`.
```bash
kubectl apply -f tekton-pipeline.yaml
```

**Step 6.** Create a new Tekton pipeline run.
```bash
kubectl create -f tekton-pipeline-run.yaml
```

**Step 7.** Change directories to the root of your repository.
```bash
cd ../
```

**Step 8.** Verify the new Tekton CI pipeline run was successful. 
```bash
tkn pipeline logs -f -L
```

You should eventually get output similar to below.
```
INFO[0059] Taking snapshot of full filesystem...        
INFO[0067] COPY . code                                  
INFO[0067] Taking snapshot of files...                  
INFO[0067] WORKDIR /code                                
INFO[0067] cmd: workdir                                 
INFO[0067] Changed working directory to /code           
INFO[0067] No files changed in this command, skipping snapshotting. 
INFO[0067] CMD ["opentelemetry-instrument", "--service_name", "login", "--metrics_exporter", "otlp,console", "--exporter_otlp_endpoint", "http://simplest-collector:4317", "python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"] 
INFO[0067] Pushing image to p7acrcyberphor.azurecr.io/login:1714162458-23d78d58222aaeee07bc758a600f672f8b47e78f 
INFO[0075] Pushed image to 1 destinations               

p7acrcyberphor.azurecr.io/login:1714162458-23d78d58222aaeee07bc758a600f672f8b47e78f
```

### Subtask 06: Add Tasks to the Tekton CI Pipeline to Scan the Container Images
**Step 1.** While in the `kubernetes/` folder, create and open a Kubernetes manifest file called `grype.yaml`. 
```bash
vim grype.yaml
```

**Step 2.** Add the content below to it.
```yaml
---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: grype
  labels:
    app.kubernetes.io/version: "0.1"
  annotations:
    tekton.dev/pipelines.minVersion: "0.12.1"
    tekton.dev/categories: Security
    tekton.dev/tags: CLI, grype
    tekton.dev/displayName: "grype"
    tekton.dev/platforms: "linux/amd64,linux/arm64,linux/ppc64le,linux/390x"
spec:
  description: >-
    A vulnerability scanner for container images and filesystems.
    Works with Syft, the powerful SBOM (software bill of materials) tool for container images and filesystems.
  workspaces:
    - name: source-dir
      optional: true
    - name: docker-credentials
      mountPath: /docker
  params:
    - name: ARGS
      description: The Arguments to be passed to Grype command.
      type: array
    - name: GRYPE_IMAGE
      default: docker.io/anchore/grype@sha256:06d97d03bded18b392e08177a84f3436376d18b6c22fd8fde45c2f38f04fd6ed  # v0.64.2
      description: Grype image to be used
      type: string
  steps:
    - name: grype
      image: $(params.GRYPE_IMAGE)
      workingDir: $(workspaces.source-dir.path)
      args:
        - "$(params.ARGS)"
```

**Step 3.** Apply the Kubernetes manifest file you just created.
```bash
kubectl apply -f grype.yaml
```

**Step 4.** Open the Kubernetes manifest file called `tekton-pipeline.yaml`.
```bash
vim tekton-pipeline.yaml
```

**Step 5.** Insert the content below after the `build-push-llm` task. 
```yaml
    - name: scan-dep-llm 
      runAfter: ["build-push-llm"]
      taskRef:
        name: grype
      workspaces:
      - name: docker-credentials  
        workspace: docker-credentials  
      params:
      - name: ARGS
        value: ["-o", "json", "$(tasks.build-push-llm.results.IMAGE_URL)"]
```

Then, insert the content below after the `build-push-django` task.
```yaml
    - name: scan-dep-django 
      runAfter: ["build-push-django"]
      taskRef:
        name: grype
      workspaces:
      - name: docker-credentials  
        workspace: docker-credentials   
      params:
      - name: ARGS
        value: ["-o", "json", "$(tasks.build-push-django.results.IMAGE_URL)"]
```

**Step 6.** Apply the changes you made to the Kubernetes manifest file called `tekton-pipeline.yaml`.
```bash
kubectl apply -f tekton-pipeline.yaml
```

**Step 7.** Create a new Tekton pipeline run.
```bash
kubectl create -f tekton-pipeline-run.yaml
```

**Step 8.** Change directories to the root of your repository.
```bash
cd ../
```

**Step 9.** See if the new Tekton CI pipeline run was successful. 
```bash
tkn pipeline logs -f -L
```

### Subtask 07: Add Tasks to the Tekton CI Pipeline to Test Your Code
**Step 1.** While in the `kubernetes/` folder, create and open a Kubernetes manifest file called `tests.yaml`. 
```bash
vim tests.yaml
```

**Step 2.** Add the content below to it.
```yaml
---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: run-tests
  namespace: default
  labels:
    app.kubernetes.io/version: "0.1"
  annotations:
    tekton.dev/pipelines.minVersion: "0.12.1"
    tekton.dev/categories: Security
    tekton.dev/tags: CLI, grype
    tekton.dev/displayName: "grype"
    tekton.dev/platforms: "linux/amd64,linux/arm64,linux/ppc64le,linux/390x"
spec:
  description: >-
    A simple task that allows for easy testing of both repositories
  workspaces:
    - name: source
  steps:
    - name: run-fastapi-tests
      image: python:3.10
      workingDir: $(workspaces.source.path)/src/fastapi-p4
      script: |
        set -euxo
        pip install poetry
        poetry install --with dev
        poetry run coverage run -m pytest
        poetry run coverage report --format=text -m
    - name: run-django-tests
      image: python:3.10
      workingDir: $(workspaces.source.path)/src/django
      script: |
        set -euxo
        pip install -r requirements.txt
        python3 manage.py test
        coverage run --source='.' manage.py test task3
        coverage report --format=text -m
```

**Step 6.** Apply the the Kubernetes manifest file you just created.
```bash
kubectl apply -f tests.yaml
```

**Step 7.** Open the Kubernetes manifest file called `tekton-pipeline.yaml`.
```bash
vim tekton-pipeline.yaml
```

**Step 8.** Add the content below after the `fetch-source` task. Also, change the `runAfter` value for the `build-push-llm` task from `fetch-source` to `run-tests`.
```yaml
    - name: run-tests
      runAfter: ["fetch-source"]
      taskRef:
        name: run-tests
      workspaces:
      - name: source
        workspace: shared-data
```

**Step 9.** Apply the changes you made to the Kubernetes manifest file called `tekton-pipeline.yaml`.
```bash
kubectl apply -f tekton-pipeline.yaml
```

**Step 10.** Copy the `django/` and `fastapi-p4` folders from the first GitHub Assignment repository to the `src` folder of the one you're using for this one. You are replacing the Task 2 files with the properly formatted code and corresponding tests created in Task 1. 

**Step 11.** Create a new commit and push it to GitHub.
```bash
git add -A
git commit -m "Added files from Task 1 repo"
git push
```

**Step 12.** Change directories to the root of your repository.
```bash
cd ../
```

**Step 13.** Release the resources used in previous Tekton CI pipeline runs. 
```bash
tkn pipelinerun delete --all
```

**Step 14.** Create a new Tekton CI pipeline run.
```bash
kubectl create -f kubernetes/tekton-pipeline-run.yaml
```

**Step 15.** Monitor the Tekton CI pipeline run until it finishes.
```bash
tkn pipeline logs -f -L
```

**Step 16.** Verify the new Tekton CI pipeline run was successful. 
```bash
tkn pipelinerun describe -L
```

You should get output similar to below.
```
 NAME                             TASK NAME           STARTED          DURATION   STATUS
 ∙ p7ci-rdnnm-scan-dep-django     scan-dep-django     1 minute ago     39s        Succeeded
 ∙ p7ci-rdnnm-build-push-django   build-push-django   2 minutes ago    1m37s      Succeeded
 ∙ p7ci-rdnnm-scan-dep-llm        scan-dep-llm        3 minutes ago    49s        Succeeded
 ∙ p7ci-rdnnm-build-push-llm      build-push-llm      8 minutes ago    4m43s      Succeeded
 ∙ p7ci-rdnnm-run-tests           run-tests           11 minutes ago   3m26s      Succeeded
 ∙ p7ci-rdnnm-fetch-source        fetch-source        12 minutes ago   1m1s       Succeeded
```