resource "random_pet" "main" {
  length    = 2
  separator = ""
}

resource "azurerm_resource_group" "main" {
  name     = random_pet.main.id
  location = var.location
}

resource "azurerm_application_insights" "main" {
  name                = random_pet.main.id
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = var.application_insights_type
}

resource "azurerm_key_vault" "main" {
  name                     = random_pet.main.id
  location                 = azurerm_resource_group.main.location
  resource_group_name      = azurerm_resource_group.main.name
  tenant_id                = data.azurerm_client_config.current.tenant_id
  sku_name                 = var.key_vault_sku
  purge_protection_enabled = false
}

resource "azurerm_storage_account" "main" {
  name                            = random_pet.main.id
  location                        = azurerm_resource_group.main.location
  resource_group_name             = azurerm_resource_group.main.name
  account_tier                    = var.storage_account_tier
  account_replication_type        = var.storage_account_replication_type
  allow_nested_items_to_be_public = false
}

resource "azurerm_machine_learning_workspace" "main" {
  name                          = random_pet.main.id
  location                      = azurerm_resource_group.main.location
  resource_group_name           = azurerm_resource_group.main.name
  application_insights_id       = azurerm_application_insights.main.id
  key_vault_id                  = azurerm_key_vault.main.id
  storage_account_id            = azurerm_storage_account.main.id
  public_network_access_enabled = true
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_machine_learning_compute_instance" "main" {
  name                          = random_pet.main.id
  machine_learning_workspace_id = azurerm_machine_learning_workspace.main.id
  virtual_machine_size          = var.vm_size
  node_public_ip_enabled        = true
  ssh {
    public_key                  = file("~/.ssh/id_rsa.pub")
  }
}