resource "azurerm_mssql_firewall_rule" "fw_rule_01" {
  name             = "ClientIPAddress"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "20.228.236.229"
  end_ip_address   = "20.228.236.229"
}

resource "azurerm_mssql_firewall_rule" "fw_rule_02" {
  name             = "AllowAllWindowsAzureIps"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "random_pet" "azurerm_storage_account_name" {
  separator = ""
}

resource "azurerm_storage_account" "logs" {
  name                     = random_pet.azurerm_storage_account_name.id
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_mssql_database_extended_auditing_policy" "audit_policy" {
  database_id                             = azurerm_mssql_database.db.id
  storage_endpoint                        = azurerm_storage_account.logs.primary_blob_endpoint
}