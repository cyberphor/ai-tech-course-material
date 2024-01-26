# this file is for organizing variables. if you need to assign sensitive values, 
# declare the variable here first then set the value in a secret.pkrvars.hcl file.
# Packer will automatically load this file (because it ends with .pkr.hcl), but 
# you'll have to manually specify secret.pkrvars.hcl when you 
# invoke "packer validate" or "packer build"

variable "tenant_id" {
  type      = string
  default   = "da3cb2a3-95dd-4a37-b857-c1264e363deb"
}

variable "subscription_id" {
  type    = string
  default = "c60c349f-4b5c-4e39-98cb-4fc2323804c5"
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

variable "resource_group_name" {
  type    = string
  default = "cloud-native-week-01-task-01-packer" # this must exist already; this is where the image is stored
}

variable "managed_image_resource_group" {
  type    = string
  default = "template-rg"
}

variable "managed_image_name" {
  type    = string
  default = "template-vm" # this is what the image will be called in your "resource_group"
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

variable "mysql_host" {
  type    = string
  default = "shared-mysql-fs-aqcjgslk.mysql.database.azure.com"
}

variable "mysql_user" {
  type    = string
  default = null
}

variable "mysql_password" {
  type    = string
  default = null
}

variable "spring_redis_host" {
  type    = string
  default = "redis-cache-npupfurd.redis.cache.windows.net"
}

variable "spring_redis_port" {
  type    = string
  default = "6379"
}

variable "spring_redis_password" {
  type    = string
  default = null
}