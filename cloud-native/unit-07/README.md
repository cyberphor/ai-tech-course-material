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

### Subtask 02: 
**Step 1.** Download, unzip, and decompress the Tekton program (make sure to use the [correct version for your machine](https://github.com/tektoncd/cli/releases)). 

**Step 2.** Download credentials from your AKS instance for kubectl to use.
```bash
az aks get-credentials --name "p7cluster" --resource-group "p7aks"
```

**Step 3.** Install the Tekton Kubernetes Operator in your AKS instance. 
```bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

**Step 4.** Create an SSH key pair using `tekton-access` as the filename (do not enter a passphrase). This step will generate two files in your current working directory (i.e., the root of the repository): `tekton-access` and `tekton-access.pub`. 
```bash
ssh-keygen -t rsa -f tekton-access
```

**Step 5.** Add the keys you generated to the provided `.gitignore` file. The code block below also references a file you're about to create. 
```bash
echo "\ntekton-access" >> .gitignore
echo "\ntekton-access.pub" >> .gitignore
echo "\nkubernetes/tekton-secret.yaml" >> .gitignore
```

**Step 6.** Print the contents of the `tekton-access.pub` file to the console and then, copy it. 
```bash
cat tekton-access.pub
```

**Step 7.** Login to GitHub and go to the repository provided for Task 02.

**Step 8.** Click the "Settings" tab. 

**Step 9.** Under "Security", click "Deploy keys."

**Step 10.** Click "Add deploy key."

**Step 11.** In the "Title" field, enter `Tekton`.

**Step 12.** In the "Key" field, paste the contents of the `tekton-access.pub` file.

**Step 13.** Click "Add key."

**Step 14.** Print the contents of the `tekton-access` file to the console, pipe it to `base64` program, and then, copy it. 
```bash
cat tekton-access | base64
```

You should get output similar to below.
```
VF0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFZRUF2N1VleW03LyttYzVsU0o0N05oa2xNMmE2SndYcmF6RjcvQ2oxV2xVUHFJWFcxeVpxSncrCnZLWGRaUDllcFBzUDcvallCQzEycVh0bHN5K2JrWS9vVHNDdjNOdmZyNUZXalJqSmlKNzF6NG01T2I1Rk40WTBCRHVYN0IKeGxyL1VoV0pQSnhHSkZzYUlxZGRqWXRYRWlneWRhR1RXTlFOUzhpUjViQjhWTC91dTlKT0hEN2lzRUpDNGhoTllLU05jbwpybzhsckh5bWdtZUVqb3ZoZWRFYm5JWldyZ1g5VXBRUnp3Q3V5RXN6STdLeURwK3VnUlJTdSthcFYxOWRVVmlvK1FVZUhUCk1xcHlDMUsrbGNMYU1pQllDbVQzNFpESnZvTWJLV296WmV2YUlBSTIwSms0Q0tVcndkQlZmM0tUVEVrMEhqRFlWaHlpZnQKYWNOUCtLZXR3UDRwSFlaTStQdFVrU1dSMzV1SkNQa0NDcE01TDdiQVFUTzVMSFpzZ1ZSQlNHMm9pdXY5SjVzTDEvOGUyWApJd1c5Y3NMN3k3N1pBWktINU5RSU4ybkhuUXN2b0x2cnRSZ3pxUzN1dDFsdGNnQUFTc3J3ZElNSnpWQ25TL21rejhRMzhpCmltR21BQk5xUUg2dnNrUzZES1hBOXl1OVBrYmlFb3M5WCtRSWRxcVZBQUFGaUUwZTZxUk5IdXFrQUFBQUIzTnphQzF5YzIKRUFBQUdCQUwrMUhzcHUvL3BuT1pVaWVPellaSlRObXVpY0Y2MnN4ZS93bzlWcFZENmlGMXRjbWFpY1ByeWwzV1QvWHFUNwpEKy80MkFRdGRxbDdaYk12bTVHUDZFN0FyOXpiMzYrUlZvMFl5WWllOWMrSnVUbStSVGVHTkFRN2wrd2NaYS8xSVZpVHljClJpUmJHaUtuWFkyTFZ4SW9NbldoazFqVURVdklrZVd3ZkZTLzdydlNUaHcrNHJCQ1F1SVlUV0NralhLSzZQSmF4OHBvSm4KaEk2TDRYblJHNXlHVnE0Ri9WS1VFYzhBcnNoTE15T3lzZzZmcm9FVVVydm1xVmRmWFZGWXFQa0ZIaDB6S3FjZ3RTdnBYQwoyaklnV0FwazkrR1F5YjZER3lscU0yWHIyaUFDTnRDWk9BaWxLOEhRVlg5eWsweEpOQjR3MkZZY29uN1duRFQvaW5yY0QrCktSMkdUUGo3VkpFbGtkK2JpUWo1QWdxVE9TKzJ3RUV6dVN4MmJJRlVRVWh0cUlyci9TZWJDOWYvSHRseU1GdlhMQys4dSsKMlFHU2grVFVDRGRweDUwTEw2Qzc2N1VZTTZrdDdyZFpiWElBQUVySzhIU0RDYzFRcDB2NXBNL0VOL0lvcGhwZ0FUYWtCKwpyN0pFdWd5bHdQY3J2VDVHNGhLTFBWL2tDSGFxbFFBQUFBTUJBQUVBQUFHQU9COWIva04wcU9malVhZWY0eWFPZTRtZG1nCjlvVnkzSFhMRUVKWXdLWDdPd1JzemJKeU5tc20rVVd1YnYzRGlydDhNUDZsa3M3ZnowRHZzVy9ndzFKQ2tBMHhXRGJMQ04KdUF6VG95MTJKT1hhMWU2LzhMdFhLdzRQTWM0MmJzYkNsbDNkcWFKamFOZGl1dEZhei9ObytTQmlIaE14WVJObWhuWGVqRwozVUM3TVQwbUpOcThIb0duZHUxS2FjcUNway9JVm5zQkZsNWJOTWVUYTJNYVZvQWZES0czUWhielZ0NlQzMzdTY210NEt1CjRkMFpoeXhkOUNoWTF2MVNJbWhqdkY0MW9yWlE3bHQxK1dnNmNNcHZTQllpd1BVVEdndTZDSE5ubWxYbkJyQUNnRk1hdEoKbTZJUFlvREFDSi9abUp3MENUajNFd2loTDVZcDEzbC92VVYvQjNEL01PYm5URmRMNHNxNWhnNHFla29iMmlkWm9yRUJWcwpUOVJ2cWlkWVdYcGFiclVIVVJCcWNNdTI3ai9GWjk3ZmpUL1BCeFIvVXc5VkFyNFdLS3NNbHdXb2NZbmIrdWx0Wi9VSk0vCnpWc3lhV0lvSVQ0REF6a3VDdXUxSkZvM0JTL3ExVVg5d3pTS2UyTktCMUcrMnY1anNhN29vWmhQcGxidUl5eUpmQkFBQUEKd1FEVTIzL1B0OFNuS0ZRb0xlbjNEZlM2VXByLzA3VXpsMFNROUVINmI5ZmZTK3hYWTUrR2YxSE5ja0s2SXdRWWI2R1NSUwpzdXdMRmhHSG5aRU9JbDFKS0FsVVE3SnFLMXYzV0VIWm11OW9RWW83TUQ3aGxBMUxtNytiV3ZvNS9LK2wxcHY5eWdJSU1RCmYwQlNTbEJxb1orQVZxVU1OVWhxNzkyaU95d2dOaTVZWHpLYlJ5SjZZWnBkaU15S3ZxYnFVVjdKRG1iTUJDb2tpYm1kRjgKVmFKYkh6c3AvNldvZ2JwU2FlVWlEck5tT1dQeUl0aE1rbjNPUHhYd21DTDNMQXE2d0FBQURCQVA1ek43TWVsMndmZlRxYQo0NXJVakIzdmVQMGQyN05UaG1BQUVVaCtzOUl1WjdQWkY5Qm1STUo3Vm9qZHdlVXlZdm9ZRVE4bFA0dlZmVUJmNlJiZEJHCkJNQUlibmJBNWVobERaaUJtNm9TOTlaQ2QxNmVSbDI1V0hSSERsdEZhMzI0b0I0TVVNVCtLK1pvOEFHSlZ1T2dnOU5jaEcKMmRvbjkrbWRPbWQ4dWg3ejRvMWhTenF6cXdnb2w3VUJXSUN6YktYaG5LbndhUHNxTXdETTBOSjRoRWRmZDVoZGhiUzYzWgo2NmRIT255QXBaQzhDeVg2Z0ZYTkVsR0RmdjFXei9hUUFBQU1FQXdPQVFUSjZadTZCc2JER0V3V09uUGx1djFEdWdJRGQ5CkhkMzNHQmE3YmpuMjJNNTY0UjVsK2xwdkZrblRnelZWWkdaK1lzSTdjZW1zOVVrYy90VjNFOVJBQTJSRlVQQVJTdzUwVlcKK1hCN2tPeHhjclZOeDZ3QUNERXJaVHIzRGtjRVpRY2ZQOEVtYnB2dDNpU3hQenFha1RGeEJQNEpwTFhMdHgrNWpOMmxrYgpneWVwMFFyQW1KNmpzZC9aeFRvRHJYSjljZkJ3VXdxcXYrczJzeHV1WUFLbmRudFJyS21iUld0VUZiaVlmNkk5TzZvYkNWCmJsTkZMczl2YU5YQmhOQUFBQUQzWnBZM1J2Y2tCdFlXTXRiV2x1YVFFQ0F3PT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==
```

**Step 15.** Create a folder called `kubernetes` in the root of your repository (your local instance, not the one in GitHub) and then, change directories to it.
```bash
mkdir kubernetes
cd kubernetes/
```

**Step 16.** Create and open a file called `tekton-secret.yaml` in the `kubernetes` folder.
```bash
vim tekton-secret.yaml
```

**Step 17.** Add the content below to the `tekton-secret.yaml` file (paste the contents of your `tekton-access` file in the `id_rsa` field).
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: git-credentials
data:
  id_rsa: |
    VF0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFZRUF2N1VleW03LyttYzVsU0o0N05oa2xNMmE2SndYcmF6RjcvQ2oxV2xVUHFJWFcxeVpxSncrCnZLWGRaUDllcFBzUDcvallCQzEycVh0bHN5K2JrWS9vVHNDdjNOdmZyNUZXalJqSmlKNzF6NG01T2I1Rk40WTBCRHVYN0IKeGxyL1VoV0pQSnhHSkZzYUlxZGRqWXRYRWlneWRhR1RXTlFOUzhpUjViQjhWTC91dTlKT0hEN2lzRUpDNGhoTllLU05jbwpybzhsckh5bWdtZUVqb3ZoZWRFYm5JWldyZ1g5VXBRUnp3Q3V5RXN6STdLeURwK3VnUlJTdSthcFYxOWRVVmlvK1FVZUhUCk1xcHlDMUsrbGNMYU1pQllDbVQzNFpESnZvTWJLV296WmV2YUlBSTIwSms0Q0tVcndkQlZmM0tUVEVrMEhqRFlWaHlpZnQKYWNOUCtLZXR3UDRwSFlaTStQdFVrU1dSMzV1SkNQa0NDcE01TDdiQVFUTzVMSFpzZ1ZSQlNHMm9pdXY5SjVzTDEvOGUyWApJd1c5Y3NMN3k3N1pBWktINU5RSU4ybkhuUXN2b0x2cnRSZ3pxUzN1dDFsdGNnQUFTc3J3ZElNSnpWQ25TL21rejhRMzhpCmltR21BQk5xUUg2dnNrUzZES1hBOXl1OVBrYmlFb3M5WCtRSWRxcVZBQUFGaUUwZTZxUk5IdXFrQUFBQUIzTnphQzF5YzIKRUFBQUdCQUwrMUhzcHUvL3BuT1pVaWVPellaSlRObXVpY0Y2MnN4ZS93bzlWcFZENmlGMXRjbWFpY1ByeWwzV1QvWHFUNwpEKy80MkFRdGRxbDdaYk12bTVHUDZFN0FyOXpiMzYrUlZvMFl5WWllOWMrSnVUbStSVGVHTkFRN2wrd2NaYS8xSVZpVHljClJpUmJHaUtuWFkyTFZ4SW9NbldoazFqVURVdklrZVd3ZkZTLzdydlNUaHcrNHJCQ1F1SVlUV0NralhLSzZQSmF4OHBvSm4KaEk2TDRYblJHNXlHVnE0Ri9WS1VFYzhBcnNoTE15T3lzZzZmcm9FVVVydm1xVmRmWFZGWXFQa0ZIaDB6S3FjZ3RTdnBYQwoyaklnV0FwazkrR1F5YjZER3lscU0yWHIyaUFDTnRDWk9BaWxLOEhRVlg5eWsweEpOQjR3MkZZY29uN1duRFQvaW5yY0QrCktSMkdUUGo3VkpFbGtkK2JpUWo1QWdxVE9TKzJ3RUV6dVN4MmJJRlVRVWh0cUlyci9TZWJDOWYvSHRseU1GdlhMQys4dSsKMlFHU2grVFVDRGRweDUwTEw2Qzc2N1VZTTZrdDdyZFpiWElBQUVySzhIU0RDYzFRcDB2NXBNL0VOL0lvcGhwZ0FUYWtCKwpyN0pFdWd5bHdQY3J2VDVHNGhLTFBWL2tDSGFxbFFBQUFBTUJBQUVBQUFHQU9COWIva04wcU9malVhZWY0eWFPZTRtZG1nCjlvVnkzSFhMRUVKWXdLWDdPd1JzemJKeU5tc20rVVd1YnYzRGlydDhNUDZsa3M3ZnowRHZzVy9ndzFKQ2tBMHhXRGJMQ04KdUF6VG95MTJKT1hhMWU2LzhMdFhLdzRQTWM0MmJzYkNsbDNkcWFKamFOZGl1dEZhei9ObytTQmlIaE14WVJObWhuWGVqRwozVUM3TVQwbUpOcThIb0duZHUxS2FjcUNway9JVm5zQkZsNWJOTWVUYTJNYVZvQWZES0czUWhielZ0NlQzMzdTY210NEt1CjRkMFpoeXhkOUNoWTF2MVNJbWhqdkY0MW9yWlE3bHQxK1dnNmNNcHZTQllpd1BVVEdndTZDSE5ubWxYbkJyQUNnRk1hdEoKbTZJUFlvREFDSi9abUp3MENUajNFd2loTDVZcDEzbC92VVYvQjNEL01PYm5URmRMNHNxNWhnNHFla29iMmlkWm9yRUJWcwpUOVJ2cWlkWVdYcGFiclVIVVJCcWNNdTI3ai9GWjk3ZmpUL1BCeFIvVXc5VkFyNFdLS3NNbHdXb2NZbmIrdWx0Wi9VSk0vCnpWc3lhV0lvSVQ0REF6a3VDdXUxSkZvM0JTL3ExVVg5d3pTS2UyTktCMUcrMnY1anNhN29vWmhQcGxidUl5eUpmQkFBQUEKd1FEVTIzL1B0OFNuS0ZRb0xlbjNEZlM2VXByLzA3VXpsMFNROUVINmI5ZmZTK3hYWTUrR2YxSE5ja0s2SXdRWWI2R1NSUwpzdXdMRmhHSG5aRU9JbDFKS0FsVVE3SnFLMXYzV0VIWm11OW9RWW83TUQ3aGxBMUxtNytiV3ZvNS9LK2wxcHY5eWdJSU1RCmYwQlNTbEJxb1orQVZxVU1OVWhxNzkyaU95d2dOaTVZWHpLYlJ5SjZZWnBkaU15S3ZxYnFVVjdKRG1iTUJDb2tpYm1kRjgKVmFKYkh6c3AvNldvZ2JwU2FlVWlEck5tT1dQeUl0aE1rbjNPUHhYd21DTDNMQXE2d0FBQURCQVA1ek43TWVsMndmZlRxYQo0NXJVakIzdmVQMGQyN05UaG1BQUVVaCtzOUl1WjdQWkY5Qm1STUo3Vm9qZHdlVXlZdm9ZRVE4bFA0dlZmVUJmNlJiZEJHCkJNQUlibmJBNWVobERaaUJtNm9TOTlaQ2QxNmVSbDI1V0hSSERsdEZhMzI0b0I0TVVNVCtLK1pvOEFHSlZ1T2dnOU5jaEcKMmRvbjkrbWRPbWQ4dWg3ejRvMWhTenF6cXdnb2w3VUJXSUN6YktYaG5LbndhUHNxTXdETTBOSjRoRWRmZDVoZGhiUzYzWgo2NmRIT255QXBaQzhDeVg2Z0ZYTkVsR0RmdjFXei9hUUFBQU1FQXdPQVFUSjZadTZCc2JER0V3V09uUGx1djFEdWdJRGQ5CkhkMzNHQmE3YmpuMjJNNTY0UjVsK2xwdkZrblRnelZWWkdaK1lzSTdjZW1zOVVrYy90VjNFOVJBQTJSRlVQQVJTdzUwVlcKK1hCN2tPeHhjclZOeDZ3QUNERXJaVHIzRGtjRVpRY2ZQOEVtYnB2dDNpU3hQenFha1RGeEJQNEpwTFhMdHgrNWpOMmxrYgpneWVwMFFyQW1KNmpzZC9aeFRvRHJYSjljZkJ3VXdxcXYrczJzeHV1WUFLbmRudFJyS21iUld0VUZiaVlmNkk5TzZvYkNWCmJsTkZMczl2YU5YQmhOQUFBQUQzWnBZM1J2Y2tCdFlXTXRiV2x1YVFFQ0F3PT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==
```

**Step 18.** Copy, paste, and run the commands below to your shell environment (use the correct ACR name). NOTE: this script assumes `jq` is installed. Also, if you're not on a Mac, you may need to replace `base64` with `base64 -w0`.
```bash
ACR_NAME=p7acrcyberphor
SERVICE_PRINCIPAL_NAME=tektonUser
ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query id --output tsv)
PASSWORD=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role acrpush --query "password" --output tsv)
USER_NAME=$(az ad sp list --display-name $SERVICE_PRINCIPAL_NAME --query "[].appId" --output tsv)
echo $USER_NAME:$PASSWORD | base64 | jq -R -c '{  "auths": { "p7acr.azurecr.io": { "auth" : . } } }'  > config.json
kubectl create secret generic docker-credentials --from-file=config.json=./config.json 
```