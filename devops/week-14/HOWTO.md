# Infrastructure as Code

## Setup
**Step 1.** Login to Azure and open the Cloud Shell. 

**Step 2.** Create a folder called `terraform_project`. 
```bash
mkdir terraform_project
```

**Step 3.** Change your current working directory the folder you just created. 
```bash
cd terraform_project
```

## Task 1
In this task, you're going to do the following:
* Create and apply a Terraform execution plan (i.e., `main.tf`)
  * The execution plan will deploy a resource group within Azure

**Step 1.** Create a file called `main.tf`. 
```bash
touch main.tf
```

**Step 2.** Add the code below to the file you just created. The code below is also [included in this repository](/devops/week-14/task-1/main.tf).
```json
terraform {
    required_providers {
        azurerm = {
            source  = "hashicorp/azurerm"
            version = "=3.0.0"
        }
    }
}

provider "azurerm" {
    features {}
}

resource "azurerm_resource_group" "rg" {
    name = "terraform_project_rg"
    location = "eastus"
    tags = {
        environment = "TF sandbox"
    }
}
```

**Step 3.** Initialize your Terraform configuration. 
```bash
terraform init
```

**Step 4.** Generate a Terraform execution plan and review it. 
```bash
terraform plan
```

**Step 5.** Apply your Terraform execution plan.
```bash
terraform apply
```

## Task 2
In this task, you're going to do the following:
* Text goes here

## Task 3
In this task, you're going to do the following:
* Text goes here

## Task 4
In this task, you're going to do the following:
* Text goes here

## Task 5
In this task, you're going to do the following:
* Text goes here