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
  default = null # "cloud-native-week-01-packer" should exist already
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

variable "mysql_host" {
  type    = string
  default = null
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
  default = null
}

variable "spring_redis_port" {
  type    = string
  default = null
}

variable "spring_redis_password" {
  type    = string
  default = null
}

# tenant_id = "da3cb2a3-95dd-4a37-b857-c1264e363deb"
# subscription_id = "17408d59-f3b6-43a5-a48c-c3667527f330" 
# 
# mysql_host = "shared-mysql-fs-aqcjgslk.mysql.database.azure.com"
# mysql_user = "Monolithic_CloudChat_123"
# mysql_password = "Monolithic_CloudChat_123"
# 
# spring_redis_host = "redis-cache-npupfurd.redis.cache.windows.net"
# spring_redis_port = "6379"
# spring_redis_password = "hTEupVAvFqOm1hdYHNV9twBKRTVnjxtZtAzCaB4Gpqc="