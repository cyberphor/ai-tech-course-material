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

resource "azapi_resource" "azapi_application_insights_web_test" {
    type      = "Microsoft.Insights/webtests@2022-06-15"
    name      = "tf-test-appinsights-webtest"
    location  = azurerm_application_insights.ai.location
    parent_id = azurerm_resource_group.rg.id
    tags = {
        "hidden-link:${azurerm_application_insights.ai.id}" = "Resource"
    }
    body = jsonencode({
        properties = {
          Description = "Web Test to monitor the health of the update todo endpoint."
          Enabled     = true
          Frequency   = 300
          Kind        = "standard"
          Locations = [
            {Id = "us-tx-sn1-azr"},
            {Id = "us-va-ash-azr"}
          ]
          Name = "App Insights WebTest Config"
          Request = {
              Headers = [
                {key   = "Content-Type", value = "application/json"},
                {key   = "Accept", value = "application/json"}
              ]
              HttpVerb               = "PUT"
              ParseDependentRequests = false
              RequestBody            = "eyJwcmlvcml0eSI6IDEwfQ==" # {"priority":10}
              RequestUrl             = "http://${azurerm_linux_web_app.webapp.name}.azurewebsites.net/todos/1"
          }
          SyntheticMonitorId = "App Insights WebTest Config"
          ValidationRules = {
              ExpectedHttpStatusCode        = 404
              SSLCheck                      = false
          }
        }
        kind = "standard"
    })
}

resource "azurerm_monitor_action_group" "main" {
    name = "tf_action_group"
    resource_group_name = azurerm_resource_group.rg.name
    short_name          = "tf_act"
    email_receiver {
        name          = "ALERT: Something bad happened" # change me
        email_address = "vf@andrew.cmu.edu"             # change me
    }
}

resource "azurerm_monitor_metric_alert" "ma" {
    name                = "endpoint-failure-metricalert"
    resource_group_name = azurerm_resource_group.rg.name
    scopes              = [azurerm_application_insights.ai.id]
    description         = "This is a metric alert configured by Terraform to check the result of availability test."
    criteria {
        metric_namespace = "microsoft.insights/components"
        metric_name      = "availabilityResults/availabilityPercentage"
        aggregation      = "Average"
        operator         = "LessThan"
        threshold        = 95
    }
    action {
        action_group_id = azurerm_monitor_action_group.main.id
    }
}