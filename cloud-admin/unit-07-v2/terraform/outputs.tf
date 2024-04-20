output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "sql_server_name" {
  value = azurerm_mssql_server.main.name
}

output "admin_password" {
  sensitive = true
  value     = local.admin_password
}

output "sql_log_storage_account_name" {
  value = azurerm_storage_account.sql_logs.name
}

output "threat_detection_log_storage_account_name" {
  value = azurerm_storage_account.threat_detection_logs.name
}