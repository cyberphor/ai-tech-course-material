output "username" {
  value = var.local_admin_username
}

output "ip_address" {
  value = azurerm_public_ip.main.ip_address
}

resource "local_file" "main" {
  content  = yamlencode({
    "all": {
      "hosts": {
        "${azurerm_public_ip.main.ip_address}": ""
      }
    }
  })
  filename = "${path.module}/../ansible/inventory.yaml"
}

output "acr_registry_id" {
  value = "${azurerm_container_registry.main.name}.azurecr.io"
}

output "service_principal_username" {
  value = azuread_service_principal.main.client_id
}

output "service_principal_password" {
  sensitive = true
  value = azuread_service_principal_password.main.value
}