terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.56.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "~>1.6.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_resource_group" "rg" {
  name     = "continuous-monitoring-rg-${random_integer.ri.result}"
  location = "eastus"
}

resource "azurerm_log_analytics_workspace" "ws" {
  name                = "workspace-test-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "ai" {
  name                = "continuous-monitoring-appinsights-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  workspace_id        = azurerm_log_analytics_workspace.ws.id
  application_type    = "Node.JS"
}

resource "azurerm_service_plan" "appserviceplan" {
  name                = "webapp-asp-2023-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}
       
resource "azurerm_linux_web_app" "webapp" {
  name                = "devopsweek15cyberphor" # change me
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.appserviceplan.id
  https_only          = true
  site_config {
    minimum_tls_version = "1.2"
    application_stack {
      node_version = "18-lts"
    }
  }
  app_settings = {
    APPINSIGHTS_INSTRUMENTATIONKEY                  = azurerm_application_insights.ai.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING           = azurerm_application_insights.ai.connection_string
    ApplicationInsightsAgent_EXTENSION_VERSION      = "~3"
  }
}