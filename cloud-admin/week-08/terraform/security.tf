resource "azurerm_mssql_firewall_rule" "fw_rule_01" {
  name             = "Allow_Client_IP_Address"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "13.72.67.135"
  end_ip_address   = "13.72.67.135"
}