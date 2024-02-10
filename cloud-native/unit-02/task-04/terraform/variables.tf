variable "location" {
  type = string
  default = "eastus"
}

variable "resource_group_name" {
  type = string
  default = "SimpleLLM"
}

variable "storage_account_name" {
  type = string
  default = "simplellmstorageaccount"
}

variable "app_service_plan_name" {
  type = string
  default = "SimpleLLM"
}

variable "function_app_name" {
  type = string
  default = "SimpleLLM"
}