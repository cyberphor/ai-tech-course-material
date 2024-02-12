variable "location" {
  type    = string
  default = "eastus"
}

variable "resource_group_name" {
  type    = string
  default = "multi-model-databases"
}

variable "vm_name" {
  type    = string
  default = "multimodelengg"
}

variable "vm_size" {
  type    = string
  default = "Standard_B2ms"
}

variable "vm_image_publisher" {
  type    = string
  default = "Canonical" 
}

variable "vm_image_offer" {
  type    = string
  default = "0001-com-ubuntu-server-focal" 
}

variable "vm_image_sku" {
  type    = string
  default = "20_04-lts" 
}

variable "vm_image_version" {
  type    = string
  default = "latest" 
}

variable "vm_os_disk_storage_type" {
  type    = string
  default = "StandardSSD_LRS"
}

variable "local_admin_username" {
  type    = string
  default = "clouduser"
}

variable "local_admin_password" {
  type    = string
  default = "Password123!"
}
