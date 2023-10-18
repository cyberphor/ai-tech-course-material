resource "azurerm_mssql_firewall_rule" "fw_rule_01" {
  name             = "ClientIPAddress_2023-10-18_11-23-23"
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