variable "resource_group_location" {
  type        = string
  description = "Location of all resources relating to the Azure SQL database"
  default     = "eastus"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
  default     = "cloud-security"
}

variable "sql_db_name" {
  type        = string
  description = "Azure SQL database name"
  default     = "cloud-security-db"
}

variable "admin_username" {
  type        = string
  description = "Username of Azure SQL database server administrator"
  default     = "clouduser"
}

variable "admin_password" {
  type        = string
  description = "Password of Azure SQL database server administrator"
  sensitive   = true
  default     = null
}