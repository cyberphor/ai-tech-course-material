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