resource "random_pet" "sql_server_name" {
  prefix = "sql"
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.resource_group_location
}

resource "random_password" "admin_password" {
  count       = var.admin_password == null ? 1 : 0
  length      = 20
  special     = true
  min_numeric = 1
  min_upper   = 1
  min_lower   = 1
  min_special = 1
}

locals {
  admin_password = try(random_password.admin_password[0].result, var.admin_password)
}

resource "azurerm_mssql_server" "main" {
  name                          = random_pet.sql_server_name.id
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  administrator_login           = var.admin_username
  administrator_login_password  = local.admin_password
  version                       = "12.0"
  public_network_access_enabled = "true" # task 0 requires false; task 1 requires true

  # "the Managed Service Identity type is 'SystemAssigned'"
  # this setting is required to enable a server-level audit policy via Terraform
  # https://github.com/Azure/azure-quickstart-templates/issues/6514
  identity {
    type = "SystemAssigned" 
  }
}

resource "azurerm_mssql_database" "main" {
  name                         = var.sql_db_name
  server_id                    = azurerm_mssql_server.main.id
  max_size_gb                  = 2
  sku_name                     = "Basic"
  threat_detection_policy {
    state                      = "Enabled"
    storage_endpoint           = azurerm_storage_account.threat_detection_logs.primary_blob_endpoint
    storage_account_access_key = azurerm_storage_account.threat_detection_logs.primary_access_key
  }
}
