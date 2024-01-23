data "azurerm_client_config" "main" {}

resource "azurerm_resource_group" "packer" {
  name     = "${var.resource_group_name}-packer"
  location = var.location
}

resource "azuread_application" "packer" {
  display_name = "packer"
}

resource "azuread_service_principal" "packer" {
  client_id = azuread_application.packer.client_id
}

resource "azuread_service_principal_password" "packer" {
  service_principal_id = azuread_service_principal.packer.object_id
}

resource "azurerm_role_assignment" "packer" {
  scope                = "/subscriptions/${data.azurerm_client_config.main.subscription_id}"
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.packer.object_id
}

output "tenant_id" {
  value = data.azurerm_client_config.main.tenant_id
}

output "subscription_id" {
  value = data.azurerm_client_config.main.subscription_id
}

output "service_principal_client_id" {
  value = azuread_application.packer.client_id
}

output "service_principal_client_secret" {
  value     = azuread_service_principal_password.packer.value
  sensitive = true
}