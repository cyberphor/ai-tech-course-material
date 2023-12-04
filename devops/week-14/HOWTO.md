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

**Step 2.** Add the content below to the file you just created (the code is also [included in this repository](/devops/week-14/task-1/main.tf)).
```hcl
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
* Update your root module's `main.tf` file
* Add a `variables.tf` file to the root module
* Create and install two child modules (i.e., `vpc` and `vm`)
* Apply the updated Terraform execution plan

**Step 1.** Update your `main.tf` with the content below (the code is also [included in this repository](/devops/week-14/task-2/main.tf)).
```hcl
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
    location = var.location
    tags = {
        environment = "TF sandbox"
    }
}

module "vpc" {
    source              = "./vpc"
    location            = var.location
    resource_group_name = azurerm_resource_group.rg.name
}

module "vm" {
    source               = "./vm"
    location             = var.location
    admin_username       = var.admin_username
    admin_password       = var.admin_password
    resource_group_name  = azurerm_resource_group.rg.name
    public_ip_address    = module.vpc.public_ip_address
    network_interface_id = module.vpc.network_interface_id
}

output "vm_ip" {
    value = module.vpc.public_ip_address
}
```

**Step 2.** Create a file called `variables.tf` in your "terraform_project" folder.
```bash
touch variables.tf
```

**Step 3.** Add the content below to it (the code is also [included in this repository](/devops/week-14/task-2/variables.tf)).
```hcl
variable "location" {
  type = string
  default = "eastus"
}

variable "admin_username" {
  default = "student"
}

variable "admin_password" {
  default = "p@55w0rd"
}
```

**Step 4.** Create a folder called `vpc` within your "terraform_project" folder. 
```bash
mkdir vpc
```

**Step 5.** Change your current working directory to it. 
```bash
cd vpc
```

**Step 6.** Create a file called `main.tf` within your "vpc" folder. 
```bash
touch main.tf
```

**Step 7.** Add the content below to it (the code is also [included in this repository](/devops/week-14/task-2/vpc/main.tf)).
```hcl
resource "azurerm_virtual_network" "vnet" {
    name                = "terraform_project_vnet"
    address_space       = ["10.0.0.0/16"]
    location            = var.location
    resource_group_name = var.resource_group_name
}
    
resource "azurerm_subnet" "subnet" {
    name                 = "terraform_project_subnet"
    resource_group_name  = var.resource_group_name
    virtual_network_name = azurerm_virtual_network.vnet.name
    address_prefixes     = ["10.0.1.0/24"]
}
    
resource "azurerm_public_ip" "publicip" {
    name                         = "terraform_project_public_ip"
    location                     = var.location
    resource_group_name          = var.resource_group_name
    allocation_method            = "Static"
}
    
resource "azurerm_network_security_group" "nsg" {
    name                = "terraform_project_nsg"
    location            = var.location
    resource_group_name = var.resource_group_name
    security_rule {
        name                       = "HTTP"
        priority                   = 103
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "80"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
}
    
resource "azurerm_network_interface" "nic" {
    name                      = "terraform_project_nic"
    location                  = var.location
    resource_group_name       = var.resource_group_name
    ip_configuration {
        name                          = "terraform_project_nic_config"
        subnet_id                     = azurerm_subnet.subnet.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.publicip.id
    }

}

resource "azurerm_network_interface_security_group_association" "sg_association" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

output "public_ip_address" {
    value = azurerm_public_ip.publicip.ip_address
}

output "network_interface_id" {
    value = azurerm_network_interface.nic.id
}
```

**Step 8.** Create a file called `variables.tf` within your "vpc" folder. 
```bash
touch variables.tf
```

**Step 9.** Add the content below to it (the code is also [included in this repository](/devops/week-14/task-2/vpc/variables.tf)).
```hcl
variable "location" {
    type = string
    description = "The location of the vpc resources"
}

variable "resource_group_name" {
    type = string
    description = "The resource group name of the vpc resources"
}
```

**Step 10.** Create a folder called `vm` within your "terraform_project" folder. 
```bash
mkdir vm
```

**Step 11.** Change your current working directory to it. 
```bash
cd vm
```

**Step 12.** Create a file called `main.tf` within your "vm" folder. 
```bash
touch main.tf
```

**Step 13.** Add the content below to it (the code is also [included in this repository](/devops/week-14/task-2/vm/main.tf)).
```hcl
resource "azurerm_virtual_machine" "vm" {
    name                  = "terraform_project_vm"
    location              = var.location
    resource_group_name   = var.resource_group_name
    network_interface_ids = [var.network_interface_id]
    vm_size               = "Standard_DS1_v2"
    storage_os_disk {
        name              = "terraform_project_os_disk"
        caching           = "ReadWrite"
        create_option     = "FromImage"
        managed_disk_type = "Premium_LRS"
    }
    storage_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "16.04.0-LTS"
        version   = "latest"
    }
    os_profile {
        computer_name  = "terraformProjectVm"
        admin_username = var.admin_username
        admin_password = var.admin_password
    }
    os_profile_linux_config {
        disable_password_authentication = false
    }
    provisioner "remote-exec" {
        connection {
            type = "ssh"
            user = var.admin_username
            password = var.admin_password
            host = var.public_ip_address
        }
        inline = [
            "sudo apt-get -y update",
            "sudo apt-get -y install apache2",
            "echo Welcome to the cloud course! | sudo tee /var/www/html/index.html"
        ]
    }
}
```

**Step 14.** Create a file called `variables.tf` within your "vm" folder. 
```bash
touch variables.tf
```

**Step 15.** Add the content below to it (the code is also [included in this repository](/devops/week-14/task-2/vm/variables.tf)).
```hcl
variable "location" {
    type = string
    description = "The location of the vpc resources"
}

variable "admin_username" {
    type = string
    description = "The username of the admin account to ssh to the VM"
}

variable "admin_password" {
    type = string
    description = "The password of the admin account to ssh to the VM"
}

variable "public_ip_address" {
    type = string
    description = "The public IP address for the VM"
}

variable "resource_group_name" {
    type = string
    description = "The resource group name of the vm resources"
}

variable "network_interface_id" {
    type = string
    description = "The network interface id of the vm resources"
}
```

**Step 16.** Initialize your `vpc` child module.
```bash
cd vpc
terraform init
cd ..
```

**Step 17.** Initialize your `vm` child module.
```bash
cd vm
terraform init
cd ..
```

**Step 18.** Reinitialize your root module (i.e., the "terraform_project" folder). If you don't do this, your child modules will not be installed within your Terraform configuration plan. 
```bash
terraform init
```

**Step 19.** Generate a new Terraform execution plan and review it. 
```bash
terraform plan
```

**Step 20.** Apply your Terraform execution plan.
```bash
terraform apply
```

**Step 21.** Verify your Terraform execution plan worked. 
```bash
curl $(terraform output vm_ip | cut -d'"' -f2)
# Welcome to the cloud course!
```

## Task 3
In this task, you're going to do the following:
* Duplicate your Terraform configuration files so there's two folders: `terraform_project` and `terraform_project_t3`
* Update the new root module in the `terraform_project_t3` folder
* Update the new `vpc` child module in the `terraform_project_t3` folder
* Update the new `vm` child module in the `terraform_project_t3` folder
  * The update will include two conditional statements
    * If the workspace is "prod", do not delete the virtual machine's operating system disk
    * If the workspace is "prod", do not delete the virtual machine's data disk
* Create two Terraform workspaces (i.e. `staging` and `prod`)
* Create and apply the updated Terraform configuration plan within each Terraform workspace

**Step 1.** Create a new directory called `terraform_project_t3`.
```bash
cd ~
mkdir terraform_project_t3
```

**Step 2.** Copy everything from `terraform_project` to `terraform_project_t3`.
```bash
cp terraform_project/* terraform_project_t3/
``` 

**Step 3.** Change your current working directory to the new folder you created. 
```bash
cd terraform_project_3
```

**Step 4.** Update the `main.tf` in your root module with the content below (the code is also [included in this repository](/devops/week-14/task-3/main.tf)).
```hcl
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
    name = "terraform_project_${terraform.workspace}_rg"
    location = var.location
    tags = {
        environment = "TF sandbox"
    }
}

module "vpc" {
    source              = "./vpc"
    location            = var.location
    resource_group_name = azurerm_resource_group.rg.name
}

module "vm" {
    source               = "./vm"
    location             = var.location
    admin_username       = var.admin_username
    admin_password       = var.admin_password
    resource_group_name  = azurerm_resource_group.rg.name
    public_ip_address    = module.vpc.public_ip_address
    network_interface_id = module.vpc.network_interface_id
}

output "vm_ip" {
    value = module.vpc.public_ip_address
}
```

**Step 5.** Update the `main.tf` in your `vpc` module with the content below (the code is also [included in this repository](/devops/week-14/task-3/vpc/main.tf)).
```hcl
resource "azurerm_virtual_network" "vnet" {
    name                = "terraform_project_${terraform.workspace}_vnet"
    address_space       = ["10.0.0.0/16"]
    location            = var.location
    resource_group_name = var.resource_group_name
}
    
resource "azurerm_subnet" "subnet" {
    name                 = "terraform_project_${terraform.workspace}_subnet"
    resource_group_name  = var.resource_group_name
    virtual_network_name = azurerm_virtual_network.vnet.name
    address_prefixes     = ["10.0.1.0/24"]
}
    
resource "azurerm_public_ip" "publicip" {
    name                         = "terraform_project_${terraform.workspace}_public_ip"
    location                     = var.location
    resource_group_name          = var.resource_group_name
    allocation_method = "Static"
}
    
resource "azurerm_network_security_group" "nsg" {
    name                = "terraform_project_${terraform.workspace}_nsg"
    location            = var.location
    resource_group_name = var.resource_group_name
    security_rule {
        name                       = "HTTP"
        priority                   = 103
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "80"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
}

resource "azurerm_network_interface" "nic" {
    name                      = "terraform_project_${terraform.workspace}_nic"
    location                  = var.location
    resource_group_name       = var.resource_group_name
    ip_configuration {
        name                          = "terraform_project_nic_${terraform.workspace}_config"
        subnet_id                     = azurerm_subnet.subnet.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.publicip.id
    }

}

resource "azurerm_network_interface_security_group_association" "sg_association" {
    network_interface_id      = azurerm_network_interface.nic.id
    network_security_group_id = azurerm_network_security_group.nsg.id
}

output "public_ip_address" {
    value = azurerm_public_ip.publicip.ip_address
}

output "network_interface_id" {
    value = azurerm_network_interface.nic.id
}
```

**Step 6.** Update the `main.tf` in your `vm` module with the content below (the code is also [included in this repository](/devops/week-14/task-3/vm/main.tf)).
```hcl
resource "azurerm_virtual_machine" "vm" {
    name                  = "terraform_project_${terraform.workspace}_vm"
    location              = var.location
    resource_group_name   = var.resource_group_name
    network_interface_ids = [var.network_interface_id]
    vm_size               = "Standard_DS1_v2"
    storage_os_disk {
        name              = "terraform_project_${terraform.workspace}_os_disk"
        caching           = "ReadWrite"
        create_option     = "FromImage"
        managed_disk_type = "Premium_LRS"
    }
    storage_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "16.04.0-LTS"
        version   = "latest"
    }
    os_profile {
        computer_name  = "terraformProject${terraform.workspace}Vm"
        admin_username = var.admin_username
        admin_password = var.admin_password
    }
    os_profile_linux_config {
        disable_password_authentication = false
    }
    provisioner "remote-exec" {
        connection {
            type = "ssh"
            user = var.admin_username
            password = var.admin_password
            host = var.public_ip_address
        }
        inline = [
            "sudo apt-get -y update",
            "sudo apt-get -y install apache2",
            "echo Welcome to the cloud course! | sudo tee /var/www/html/index.html"
        ]
    }
    delete_data_disks_on_termination = terraform.workspace == "prod" ? false : true
    delete_os_disk_on_termination    = terraform.workspace == "prod" ? false : true
}
```

**Step 7.** Initialize your new Terraform root module (i.e., `terraform_project_3` folder). 
```bash
terraform init
```

**Step 8.** Create two new Terraform workspaces called `staging` and `prod`.
```bash
terraform workspace new staging
terraform workspace new prod
```

**Step 9.** Select the first workspace you created. 
```bash
terraform workspace select staging
```

**Step 10.** Create an execution plan within the `staging` workspace for the updated Terraform configuration. 
```bash
terraform plan
```

**Step 11.** Apply the execution plan within the `staging` workspace.
```bash
terraform apply
```

**Step 12.** Verify your Terraform execution plan worked. 
```bash
curl $(terraform output vm_ip | cut -d'"' -f2)
# Welcome to the cloud course!
```

**Step 13.** Select the second workspace you created. 
```bash
terraform workspace select prod
```

**Step 14.** Create an execution plan within the `prod` workspace for the updated Terraform configuration. 
```bash
terraform plan
```

**Step 15.** Apply the execution plan within the `prod` workspace.
```bash
terraform apply
```

**Step 16.** Verify your Terraform execution plan worked. 
```bash
curl $(terraform output vm_ip | cut -d'"' -f2)
# Welcome to the cloud course!
```

## Task 4
In this task, you're going to do the following:
* Text goes here

## Task 5
In this task, you're going to do the following:
* Text goes here