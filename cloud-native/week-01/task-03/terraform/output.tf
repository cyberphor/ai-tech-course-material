output "acr_server" {
  value = "${azurerm_container_registry.main.name}.azurecr.io"
}

output "acr_server_username" {
  value = "${azurerm_container_registry.main.admin_username}"
}

output "acr_server_password" {
  value = "${azurerm_container_registry.main.admin_password}"
  sensitive = true
}