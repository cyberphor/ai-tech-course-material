variable "tenant_id" {
  type      = string
  default   = null
}

variable "subscription_id" {
  type    = string
  default = null
}

variable "client_id" {
  type    = string
  default = null
}

variable "client_secret" {
  type    = string
  default = null
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "resource_group" {
  type    = string
  default = "cloud-native-week-01-packer" # this should exist already
}

variable "managed_image_name" {
  type    = string
  default = "template_image"
}

variable "vm_os_type" {
  type    = string
  default = "Linux" 
}

variable "vm_image_publisher" {
  type    = string
  default = "Canonical" 
}

variable "vm_image_offer" {
  type    = string
  default = "0001-com-ubuntu-server-jammy" 
}

variable "vm_image_sku" {
  type    = string
  default = "22_04-lts" 
}

variable "vm_size" {
  type    = string
  default = "Standard_B2s"
}