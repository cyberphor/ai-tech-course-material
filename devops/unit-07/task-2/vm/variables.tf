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