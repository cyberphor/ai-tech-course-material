# echo $TENANT_ID
variable "tenant_id" {
  type      = string
  default   = "da3cb2a3-95dd-4a37-b857-c1264e363deb"
  sensitive = true
}

# echo $SUBSCRIPTION_ID
variable "subscription_id" {
  type    = string
  default = "17408d59-f3b6-43a5-a48c-c3667527f330" 
}

# echo $PACKER_CLIENT_ID
variable "client_id" {
  type    = string
  default = "e146372a-dea4-4274-88b2-e7735ec4deec"
}

# echo $PACKER_CLIENT_SECRET
variable "client_secret" {
  type      = string
  default   = "i2U8Q~LO_0kT6EYbShDV8-SHmRMIMWrSxrybhbsD"
  sensitive = true
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "resource_group" {
  type    = string
  default = "cloud-native-week-01-packer"
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