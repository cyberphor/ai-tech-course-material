# CI/CD Pipeline for a Containerized Microservice

## Setup
**Step 1.** Create an SSH key-pair to authenticate with. 
```bash
ssh-keygen -t rsa -b 4096 -C Desktop
```

**Step 1.** Create a virtual machine using the information below and Azure Portal. Make sure to copy the SSH public key from the previous step to the appropiate field.
| Field                        | Value                                   |
| ---------------------------- | --------------------------------------- |
| Resource group               | `devops-dev`                            |
| Virtual machine name         | `dev-vm`                                |
| Region                       | `(US) East US`                          |
| Image                        | `Ubuntu Server 22.04 LTS`               |
| Run with Azure Spot discount | `No`                                    |
| Size                         | `Standard_B1ms - 1 vcpus, 2 GiB memory` |
| Authentication type          | `SSH`                                   |

**Step 2.** Connect to the virtual machine via SSH. 
```bash
ssh victor@172.178.78.169
```

**Step 3.** Install the Azure CLI. 
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Step 4.** Login to Azure. 
```bash
az login
```

**Step 5.** Identify which Azure subscription you want to use. 
```bash
az account show
```

**Step 5.** Configure the Azure CLI to use the correct Azure subscription. 
```bash
az account set --subscription "AI2C Subscription 1"
```

**Step 6.** Get the provided source code. 
```bash
git clone git@github.com:SAIL-Classroom/ci-cd-pipelines-for-containerized-microservices-cyberphor.git
```

**Step 7.** Create a [GitHub Personal Access Token](/INSTALL.md#how-to-create-a-github-personal-access-token).

## Task 1

## Task 2

## Task 3

## Task 4

## Task 5