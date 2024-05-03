variable "location" {
  type    = string
  default = "eastus"
}

variable "application_insights_type" {
  type    = string
  default = "web"
}

variable "key_vault_sku" {
  type    = string
  default = "premium" 
}

variable "storage_account_tier" {
  type    = string
  default = "Standard"
}

variable "storage_account_replication_type" {
  type    = string
  default = "LRS"
}

variable "vm_size" {
  type    = string
  default = "Standard_NC4as_T4_v3"
}

variable "vm_authorization_type" {
  type    = string
  default = "personal"
}