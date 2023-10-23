
output "admin_password" {
  sensitive = true
  value     = local.admin_password
}

output "prod_server_1_public_ip_address" {
  value = azurerm_linux_virtual_machine.prod_server_1.public_ip_address
}

output "prod_server_2_public_ip_address" {
  value = azurerm_linux_virtual_machine.prod_server_1.public_ip_address
}

output "qa_server_1public_ip_address" {
  value = azurerm_linux_virtual_machine.qa_server_1.public_ip_address
}