resource "azurerm_mssql_firewall_rule" "rule_01" {
  name             = "ClientIPAddress"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "20.228.236.229"
  end_ip_address   = "20.228.236.229"
}

resource "azurerm_mssql_firewall_rule" "rule_02" {
  name             = "AllowAllWindowsAzureIps"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "random_pet" "sql_log_storage_account_name" {
  separator = ""
}

resource "random_pet" "threat_detection_storage_account_name" {
  separator = ""
}

resource "azurerm_storage_account" "sql_logs" {
  name                     = random_pet.sql_log_storage_account_name.id
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_account" "threat_detection_logs" {
  name                     = random_pet.threat_detection_storage_account_name.id
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_mssql_server_extended_auditing_policy" "main" {
  server_id                  = azurerm_mssql_server.main.id
  storage_endpoint           = azurerm_storage_account.sql_logs.primary_blob_endpoint
  storage_account_access_key = azurerm_storage_account.sql_logs.primary_access_key
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-analytics"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

resource "azurerm_monitor_diagnostic_setting" "main" {
 depends_on = [
    azurerm_mssql_database.main
  ]

  name                       = "Diagnostic Settings"
  target_resource_id         = "${azurerm_mssql_server.main.id}/databases/${var.sql_db_name}"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  
  enabled_log {
    category = "SQLSecurityAuditEvents"
  }
}