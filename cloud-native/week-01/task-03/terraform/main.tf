data "azurerm_client_config" "main" {}

resource "random_pet" "value" {
  length    = 2
  separator = ""
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group
  location = var.location
}

resource "azurerm_container_registry" "main" {
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  name                = random_pet.value.id
  sku                 = "Basic" 
  admin_enabled       = true
}

resource "azurerm_role_assignment" "main" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPush"
  principal_id         = data.azurerm_client_config.main.client_id
  principal_type       = "User"
}