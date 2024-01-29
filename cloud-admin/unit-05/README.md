# Terraform

## Training Objectives  
1. [Set Your Azure Subscription](#task-01)
2. [Create an Azure Web App Using Terraform](#task-02)
3. [Create an Azure Resource Group Using Terraform and Variables](#task-03)
4. [Change an Azure Network Security Group Rule Using Terraform](#task-04)
5. [Visualize Infrastructure in Azure Using Terraform](#task-05)

## Task 01
### Set Your Azure Subscription
**Step 1.** List your Azure subscriptions.
```bash
az account list --query "[].name" --output tsv
```

**Step 2.** Set the Azure subscription you want to use.
```bash
az account set --subscription "AI2C Subscription 1"
```

**Step 3.** Verify your Azure subscription.
```bash
az account show
```

## Task 02
### Create an Azure Web App Using Terraform
**Step 1.** Create a folder and then make it your current working directory.
```bash
mkdir task2 &&\
cd task2
```

**Step 2.** Download or create a Terraform configuration. Below is an example.
```bash
vim main.tf
```
```bash
# This Terraform module declares the following resources:
#
# A `random_uuid` resource to generate the unique app name for your web app, the resource `random_uuid` generates a random UUID string that is intended to be used as unique identifiers for other resources
# A resource group named "task1TF-resources" in your current Azure default subscription
# A "Standard B1" Azure app service plan for your web app under the resource group
# An Azure app service resource under the resource group and per the app service plan, using the random_uuid unique id as app name

# Generate a unique id for app name
# Reference: https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/uuid
resource "random_uuid" "server" {
}


# Configure the provider
# One best practice is to pin the concrete provider version
# to ensure that new versions with breaking changes will not be automatically installed by `terraform init` in future.
# "=3.22.0" means to use the exact version 3.22.0
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.22.0"
    }
  }

}

provider "azurerm" {
  # features block gives users more control on the decleared resources to be configured
  # Example include log analytics, api managements configurations.
  # leave the content blank when no config is needed
  # Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/features-block
  features {}
}


# Create a new resource group, referred to as "azurerm_resource_group.main"
# Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group
#
# This resource declaration is similar to the outcome of the following Azure CLI command:
# az group create --location eastus --name task1TF-resources
resource "azurerm_resource_group" "main" {
  name     = "task1TF-resources"
  location = "eastus"
  tags = {
    environment = "task1TF"
  }
}


# Create an azure service plan called Service Plan, which manages an App Service.
# Reference: https://registry.terraform.io/providers/hashicorp/azurerm/3.22.0/docs/resources/service_plan
#
# This resource declaration is similar to the outcome of the following Azure CLI command:
# az appservice plan create --name task1TF-servicePlan --resource-group task1TF-resources --location eastus --is-linux --sku B1
resource "azurerm_service_plan" "main" {
  name     = "task1TF-servicePlan"
  location = "eastus"

  # This is an example on how to reference the attributes of other resources to configure subsequent resources.
  #
  # resource_group_name: The name of the resource group in which to create the Service Plan component.
  # The value is set the name attribute of azurerm_resource_group.main (i.e., azurerm_resource_group.main.name)
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
  tags = {
    environment = "task1TF"
  }
}


# Create the azure web app service resource
# Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app
#
# This resource declaration is similar to the outcome of the following Azure CLI command:
# az webapp create --name <uuid> --plan task1TF-servicePlan --resource-group task1TF-resources --startup-file index.html
resource "azurerm_linux_web_app" "main" {
  name = random_uuid.server.result
  # Specifies the supported Azure location where the resource exists.
  location = "eastus"

  # The name of the resource group in which to create the App Service.
  resource_group_name = azurerm_resource_group.main.name
  # The ID of the Service Plan within which to create this App Service.
  service_plan_id = azurerm_service_plan.main.id

  site_config {
    default_documents = [
      "index.html",
      "hostingstart.html"
    ]
  }
  tags = {
    environment = "task1TF"
  }
}
```

**Step 3.** Initialize Terraform within your current working directory.
```bash
terraform init
```

**Step 4.** Inspect the changes Terraform will make to your infrastructure.
```bash
terraform plan
```

**Step 5.** Apply your infrastructure changes using Terraform. Enter "yes" when prompted. Do NOT destroy anything yet. The next task expects the resources defined in this task.
```bash
terraform apply
```

## Task 03
### Create an Azure Resource Group Using Terraform and Variables
**Step 1.** Create a folder and then make it your current working directory.
```bash
mkdir task3 &&\
cd task3
```

**Step 2.** Download or create a Terraform configuration. Below is an example.
```bash
vim main.tf
```
```
# This prepared Terraform module declares an Azure resource group, an Azure virtual machine
# and other supportive resources for networking.
#
# You are NOT required to dive deep into all the resources below such as the networking resources,
# however, please read the following resources carefully:
# resource "random_password" "password"
# resource "azurerm_virtual_machine" "myterraformvm"
#
# in resource "azurerm_virtual_machine" "myterraformvm", please pay attention to
# the provisioner "remote-exec" section

# Configure the provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.22.0"
    }
  }
}
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Create a new resource group
resource "azurerm_resource_group" "myterraformgroup" {
  name     = "${var.prefix}-resources"
  location = var.location
  tags     = local.common_tags
}


# Create a virtual network
resource "azurerm_virtual_network" "myterraformnetwork" {
  name                = "${var.prefix}-network"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  tags                = local.common_tags
}

# Create a subnet
resource "azurerm_subnet" "myterraformsubnet" {
  name                 = "${var.prefix}-subnet"
  resource_group_name  = azurerm_resource_group.myterraformgroup.name
  virtual_network_name = azurerm_virtual_network.myterraformnetwork.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create a static public IP
resource "azurerm_public_ip" "myterraformpublicip" {
  name                = "${var.prefix}-ip"
  location            = var.location
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  allocation_method   = "Static"
  tags                = local.common_tags
}

# Create a network security group
resource "azurerm_network_security_group" "myterraformnsg" {
  name                = "${var.prefix}-nsg"
  location            = var.location
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  tags                = local.common_tags
}

# Create a network security group rule
# This rule opens the port 80 to the public
resource "azurerm_network_security_rule" "http" {
  name                        = "http"
  priority                    = 300
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.myterraformgroup.name
  network_security_group_name = azurerm_network_security_group.myterraformnsg.name
}

# Create a network security group rule
# This rule opens the port 22 to the public
resource "azurerm_network_security_rule" "ssh" {
  name                        = "ssh"
  priority                    = 320
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.myterraformgroup.name
  network_security_group_name = azurerm_network_security_group.myterraformnsg.name
}

# Create a network interface
resource "azurerm_network_interface" "myterraformnic" {
  name                = "${var.prefix}-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  ip_configuration {
    name                          = "${var.prefix}-nic-conf"
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.myterraformpublicip.id
  }
  tags = local.common_tags
}

resource "azurerm_network_interface_security_group_association" "myterraformNISG" {
  network_interface_id      = azurerm_network_interface.myterraformnic.id
  network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}

# Use a cryptographic random number to generate a password.
# Reference: https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password
resource "random_password" "password" {
  length           = 16
  special          = true
  lower            = true
  upper            = true
  numeric          = true
  override_special = "_%@"
}

# Create a virtual machine
# Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_machine
resource "azurerm_virtual_machine" "myterraformvm" {
  name                  = "${var.prefix}-vm"
  location              = var.location
  resource_group_name   = azurerm_resource_group.myterraformgroup.name
  network_interface_ids = [azurerm_network_interface.myterraformnic.id]
  vm_size               = "Standard_B1ms"
  storage_os_disk {
    name              = "myOsDisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Premium_LRS"
  }
  # Select Ubuntu 18.04 as the OS Image
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
  # SSH username and password
  os_profile {
    computer_name  = "myvm"
    admin_username = var.admin_username
    admin_password = random_password.password.result
  }
  os_profile_linux_config {
    # Enable SSH password authentication.
    disable_password_authentication = false
  }
  tags = local.common_tags

  # The remote-exec provisioner invokes a script on a remote resource after it is created.
  # This can be used to run a configuration management tool, bootstrap into a cluster, etc.
  provisioner "remote-exec" {
    # The remote-exec provisioner supports both different type connections and we are using SSH here.
    # This is similar to the Linux command `ssh var.admin_username@azurerm_public_ip.myterraformpublicip.ip_address`
    connection {
      type     = "ssh"
      user     = var.admin_username
      password = random_password.password.result
      host     = azurerm_public_ip.myterraformpublicip.ip_address
    }
    # The commands to execute
    inline = [
      # install Apache2 and start the web server
      "sudo apt-get -y update",
      "sudo apt-get -y install apache2",
      # modify the index.html page
      "echo Welcome to the cloud course! | sudo tee /var/www/html/index.html"
    ]
  }
}

locals {
  # Common tags to be assigned to all resources
  # Referred to as "local.common_tags"
  #
  # A local value is used here, instead of an input variable.
  #
  # (Optional Reading) Local Values
  #
  # Comparing modules to functions in a traditional programming language:
  # if input variables are analogous to function arguments,
  # and outputs values are analogous to function return values,
  # then local values are comparable to a function's local temporary symbols.
  #
  # "local.common_tags" depends on "var.prefix", therefore "local.common_tags" cannot
  # be directly defined as an input variable, instead, the value of "local.common_tags" is
  # constructed with the reference of "var.prefix", similar to how a function's local
  # values get computed from function input arguments.
  #
  # Reference:
  # https://www.terraform.io/docs/configuration/locals.html
  common_tags = {
    environment = var.prefix
  }
}
```

**Step 3.** Define input variables in a file called `variables.tf`.
```bash
vim variables.tf
```
```
variable "prefix" {
  type    = string
  default = "task3TF"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "admin_username" {
  type    = string
  default = "clouduser"
}
```

**Step 4.** Define output variables in a file called `output.tf`.
```bash
vim output.tf
```
```bash
output "public_ip" {
  description = "The public IP of the virtual machine. You can access this IP using your browser to see the hosted web page."
  value       = azurerm_public_ip.myterraformpublicip.ip_address
}

output "vm_connection_guide" {
  value     = "To connect to your virtual machine via SSH: ssh ${var.admin_username}@${azurerm_public_ip.myterraformpublicip.ip_address}\nPassword: ${random_password.password.result}"
  sensitive = true
}
```

**Step 5.** Initialize Terraform within your current working directory.
```bash
terraform init
```

**Step 6.** Inspect the changes Terraform will make to your infrastructure.
```bash
terraform plan
```

**Step 7.** Apply your infrastructure changes using Terraform. Enter "yes" when prompted.
```bash
terraform apply
```

**Step 8.** Display the contents of your sensitive output variables. Below is an example.
```bash
terraform output vm_connection_guide
```

## Task 04
### Change an Azure Network Security Group Rule Using Terraform
**Step 1.** Open the Terraform configuration file created in the previous step.
```bash
vim main.tf
```

**Step 2.** Change the rule. For example, shown below is a rule created in the previous task albeit with a different value for `access`. It now denies traffic inbound to TCP port 80.  
```bash
# Create a network security group rule
# This rule opens the port 80 to the public
resource "azurerm_network_security_rule" "http" {
  name                        = "http"
  priority                    = 300
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.myterraformgroup.name
  network_security_group_name = azurerm_network_security_group.myterraformnsg.name
}
```

**Step 3.** Inspect the changes Terraform will make to your infrastructure.
```bash
terraform plan
```

**Step 4.** Apply your infrastructure changes using Terraform. Enter "yes" when prompted.
```bash
terraform apply
```

**Step 5.** Destroy the infrastructure created by Terraform.
```bash
terraform destroy
```

## Task 05
### Visualize Infrastructure in Azure Using Terraform
**Step 1.** Create a folder and then make it your current working directory.
```bash
mkdir task5 &&\
cd task5
```

**Step 2.** Download or create a Terraform configuration. Below is an example.
```bash
vim main.tf
```
```bash
# This prepared Terraform module declares an Azure resource group, an Azure virtual machine
# and other supportive resources for networking.
#
# Please read each resource declaration, and pay attention to the dependencies
# between the resources.

# Configure the provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.22.0"
    }
  }
}
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Create a new resource group
# All the other resources will be created within this resource group.
# The other resources refers to the resource group with:
# resource_group_name = azurerm_resource_group.myterraformgroup.name
resource "azurerm_resource_group" "myterraformgroup" {
  name     = "${var.prefix}-resources"
  location = var.location
  tags     = local.common_tags
}


# Create a virtual network
resource "azurerm_virtual_network" "myterraformnetwork" {
  name          = "${var.prefix}-network"
  address_space = ["10.0.0.0/16"]
  location      = var.location
  # dependency: a virtual network belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  tags                = local.common_tags
}

# Create a subnet
resource "azurerm_subnet" "myterraformsubnet" {
  name = "${var.prefix}-subnet"
  # dependency: a subnet belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  # dependency: a subnet is within a virtual network
  virtual_network_name = azurerm_virtual_network.myterraformnetwork.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create a static public IP
resource "azurerm_public_ip" "myterraformpublicip" {
  name     = "${var.prefix}-ip"
  location = var.location
  # dependency: a public IP belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  allocation_method   = "Static"
  tags                = local.common_tags
}

# Create a network security group
resource "azurerm_network_security_group" "myterraformnsg" {
  name     = "${var.prefix}-nsg"
  location = var.location
  # dependency: a network security group belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  tags                = local.common_tags
}

# Create a network security group rule
# This rule opens the port 22 to the public
resource "azurerm_network_security_rule" "ssh" {
  name                       = "ssh"
  priority                   = 320
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "22"
  source_address_prefix      = "*"
  destination_address_prefix = "*"
  # dependency: a network security group rule belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  # dependency: a network security group rule is attached to a network security group
  network_security_group_name = azurerm_network_security_group.myterraformnsg.name
}

# Create a network interface
# Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
resource "azurerm_network_interface" "myterraformnic" {
  name     = "${var.prefix}-nic"
  location = var.location
  # dependency: a network interface belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  # One or more IP addresses associated with this network interface
  ip_configuration {
    name = "${var.prefix}-nic-conf"
    # dependency: a Subnet ID must be specified for an IPv4 network interface
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
    # dependency: reference to a Public IP Address to associate with this  network interface
    public_ip_address_id = azurerm_public_ip.myterraformpublicip.id
  }
  tags = local.common_tags
}

# dependency: a network interface belongs to a network security group
resource "azurerm_network_interface_security_group_association" "myterraformNISG" {
  network_interface_id      = azurerm_network_interface.myterraformnic.id
  network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}


# Use a cryptographic random number generate a password.
# Reference: https://www.terraform.io/docs/providers/random/r/password.html
resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "_%@"
}

# Create a virtual machine
# Reference: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_machine
# The virtual machine depends on the resource group, the network interface, etc.
# All those associated resources are created before or already exist.
resource "azurerm_virtual_machine" "myterraformvm" {
  name     = "${var.prefix}-vm"
  location = var.location
  # dependency: a virtual machine belongs to a resource group
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  # dependency: a virtual machine interface is attached to a network interface
  network_interface_ids = [azurerm_network_interface.myterraformnic.id]
  vm_size               = "Standard_B1ms"
  storage_os_disk {
    name              = "myOsDisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Premium_LRS"
  }
  # Select Ubuntu 18.04 as the OS Image
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
  # SSH username and password
  os_profile {
    computer_name  = "myvm"
    admin_username = var.admin_username
    admin_password = random_password.password.result
  }
  os_profile_linux_config {
    # Enable SSH password authentication.
    disable_password_authentication = false
  }
  tags = local.common_tags
}

locals {
  # Common tags to be assigned to all resources
  # Referred to as "local.common_tags"
  #
  # A local value is used here, instead of an input variable.
  #
  # (Optional Reading) Local Values
  #
  # Comparing modules to functions in a traditional programming language:
  # if input variables are analogous to function arguments,
  # and outputs values are analogous to function return values,
  # then local values are comparable to a function's local temporary symbols.
  #
  # "local.common_tags" depends on "var.prefix", therefore "local.common_tags" cannot
  # be directly defined as an input variable, instead, the value of "local.common_tags" is
  # constructed with the reference of "var.prefix", similar to how a function's local
  # values get computed from function input arguments.
  #
  # Reference:
  # https://www.terraform.io/docs/configuration/locals.html
  common_tags = {
    environment = var.prefix
  }
}
```

**Step 3.** Define input variables in a file called `variables.tf`.
```bash
vim variables.tf
```
```bash
variable "prefix" {
  type    = string
  default = "task4TF"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "admin_username" {
  type    = string
  default = "clouduser"
}
```

**Step 4.** Initialize Terraform within your current working directory.
```bash
terraform init
```

**Step 5.** Inspect the changes Terraform will make to your infrastructure.
```bash
terraform plan
```

**Step 6.** Apply your infrastructure changes using Terraform. Enter "yes" when prompted.
```bash
terraform apply
```

**Step 7.** Create a dependency graph of the resources created by Terraform.
```bash
terraform graph > task05.graph
```

**Step 8.** To view the graph, browse to [http://www.webgraphviz.com/](http://www.webgraphviz.com/) and enter the contents of `task05.graph` (see below) into the text-field.
```bash
digraph {
        compound = "true"
        newrank = "true"
        subgraph "root" {
                "[root] azurerm_network_interface.myterraformnic (expand)" [label = "azurerm_network_interface.myterraformnic", shape = "box"]
                "[root] azurerm_network_interface_security_group_association.myterraformNISG (expand)" [label = "azurerm_network_interface_security_group_association.myterraformNISG", shape = "box"]
                "[root] azurerm_network_security_group.myterraformnsg (expand)" [label = "azurerm_network_security_group.myterraformnsg", shape = "box"]
                "[root] azurerm_network_security_rule.ssh (expand)" [label = "azurerm_network_security_rule.ssh", shape = "box"]
                "[root] azurerm_public_ip.myterraformpublicip (expand)" [label = "azurerm_public_ip.myterraformpublicip", shape = "box"]
                "[root] azurerm_resource_group.myterraformgroup (expand)" [label = "azurerm_resource_group.myterraformgroup", shape = "box"]
                "[root] azurerm_subnet.myterraformsubnet (expand)" [label = "azurerm_subnet.myterraformsubnet", shape = "box"]
                "[root] azurerm_virtual_machine.myterraformvm (expand)" [label = "azurerm_virtual_machine.myterraformvm", shape = "box"]
                "[root] azurerm_virtual_network.myterraformnetwork (expand)" [label = "azurerm_virtual_network.myterraformnetwork", shape = "box"]
                "[root] provider[\"registry.terraform.io/hashicorp/azurerm\"]" [label = "provider[\"registry.terraform.io/hashicorp/azurerm\"]", shape = "diamond"]
                "[root] provider[\"registry.terraform.io/hashicorp/random\"]" [label = "provider[\"registry.terraform.io/hashicorp/random\"]", shape = "diamond"]
                "[root] random_password.password (expand)" [label = "random_password.password", shape = "box"]
                "[root] var.admin_username" [label = "var.admin_username", shape = "note"]
                "[root] var.location" [label = "var.location", shape = "note"]
                "[root] var.prefix" [label = "var.prefix", shape = "note"]
                "[root] azurerm_network_interface.myterraformnic (expand)" -> "[root] azurerm_public_ip.myterraformpublicip (expand)"
                "[root] azurerm_network_interface.myterraformnic (expand)" -> "[root] azurerm_subnet.myterraformsubnet (expand)"
                "[root] azurerm_network_interface_security_group_association.myterraformNISG (expand)" -> "[root] azurerm_network_interface.myterraformnic (expand)"
                "[root] azurerm_network_interface_security_group_association.myterraformNISG (expand)" -> "[root] azurerm_network_security_group.myterraformnsg (expand)"
                "[root] azurerm_network_security_group.myterraformnsg (expand)" -> "[root] azurerm_resource_group.myterraformgroup (expand)"
                "[root] azurerm_network_security_rule.ssh (expand)" -> "[root] azurerm_network_security_group.myterraformnsg (expand)"
                "[root] azurerm_public_ip.myterraformpublicip (expand)" -> "[root] azurerm_resource_group.myterraformgroup (expand)"
                "[root] azurerm_resource_group.myterraformgroup (expand)" -> "[root] local.common_tags (expand)"
                "[root] azurerm_resource_group.myterraformgroup (expand)" -> "[root] provider[\"registry.terraform.io/hashicorp/azurerm\"]"
                "[root] azurerm_resource_group.myterraformgroup (expand)" -> "[root] var.location"
                "[root] azurerm_subnet.myterraformsubnet (expand)" -> "[root] azurerm_virtual_network.myterraformnetwork (expand)"
                "[root] azurerm_virtual_machine.myterraformvm (expand)" -> "[root] azurerm_network_interface.myterraformnic (expand)"
                "[root] azurerm_virtual_machine.myterraformvm (expand)" -> "[root] random_password.password (expand)"
                "[root] azurerm_virtual_machine.myterraformvm (expand)" -> "[root] var.admin_username"
                "[root] azurerm_virtual_network.myterraformnetwork (expand)" -> "[root] azurerm_resource_group.myterraformgroup (expand)"
                "[root] local.common_tags (expand)" -> "[root] var.prefix"
                "[root] provider[\"registry.terraform.io/hashicorp/azurerm\"] (close)" -> "[root] azurerm_network_interface_security_group_association.myterraformNISG (expand)"
                "[root] provider[\"registry.terraform.io/hashicorp/azurerm\"] (close)" -> "[root] azurerm_network_security_rule.ssh (expand)"
                "[root] provider[\"registry.terraform.io/hashicorp/azurerm\"] (close)" -> "[root] azurerm_virtual_machine.myterraformvm (expand)"
                "[root] provider[\"registry.terraform.io/hashicorp/random\"] (close)" -> "[root] random_password.password (expand)"
                "[root] random_password.password (expand)" -> "[root] provider[\"registry.terraform.io/hashicorp/random\"]"
                "[root] root" -> "[root] provider[\"registry.terraform.io/hashicorp/azurerm\"] (close)"
                "[root] root" -> "[root] provider[\"registry.terraform.io/hashicorp/random\"] (close)"
        }
}
```

**Step 8.** Destroy the infrastructure created by Terraform.
```bash
terraform destroy
```