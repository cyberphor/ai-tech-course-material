resource "azurerm_mssql_firewall_rule" "fw_rule_01" {
  name             = "ClientIPAddress_2023-10-18_11-23-23"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "13.72.67.135"
  end_ip_address   = "13.72.67.135"
}

resource "azurerm_mssql_firewall_rule" "fw_rule_02" {
  name             = "Allow Azure services and resources to access this server"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}