# Cloud Monitoring
## Training Objectives
Knowledge
* Describe the benefits of cloud monitoring
* Describe the workflow behind triggering an action group using an alert

Skills
* Register a resource provider with a subscription
* Create a resource group, web app, and App Service Plan (ASP) using the Azure CLI
* Configure autoscaling for an Azure Web App using the Azure Portal
* Configure autoscaling for an Azure Web App using Terraform
* Configure an availability test for an Azure Web App using the Azure Portal and CLI
* Configure an availability test for an Azure Web App using Terraform

## Tasks
### Task 1
Register the `microsoft.insights` resource provider with your subscription.  

**Step 1.** Browse to the [Subscriptions](https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade) web page.  

**Step 2.** Click "Resource Providers."  

**Step 3.** Search for and select `microsoft.insights`.  

**Step 4.** Click "Register." 

### Task 2
Create an web app and ASP using the Azure CLI. 

**Step 1.** Define your variables. 
```bash
export SUBSCRIPTION_NAME="AI2C Subscription 1"
export RESOURCE_GROUP="web_app_monitor"
export LOCATION="eastus"
export ASP_NAME="myAppServicePlan"
export ASP_SKU="S1" # S1 (Standard) pricing tier
export WEB_APP_NAME="cyberphor-web-app"
```

**Step 2.** Set your subscription.
```bash
az account set \
  --subscription "${SUBSCRIPTION_NAME}"
```

**Step 3.** Create a Resource Group. 
```bash
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}"
```

**Step 4.** Create an App Service Plan (ASP). 
```bash
az appservice plan create \
  --name "${ASP_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --sku "${ASP_SKU}"
```

**Step 5.** Create a web app. 
```bash
az webapp create \
  --resource-group "${RESOURCE_GROUP}" \
  --plan "${ASP_NAME}" \
  --name "${WEB_APP_NAME}"
```

### Task 3
Configure Autoscaling for an Azure Web App Using the Azure Portal. 

**Step 1.** Browse to [https://portal.azure.com](https://portal.azure.com).  

**Step 2.** Search for and select the "Monitor" service.  

**Step 3.** Click "Autoscale" under the "Settings" section.  

**Step 4.** Click your ASP.  

**Step 5.** Click "Custom autoscale."  

**Step 6.** Review the settings listed below for the "Default" scale condition (some of them will be auto-filled by the Azure Portal). 
* Autoscale setting name: "web_app_autoscale"
* Resource group: "web_app_monitor"
* Scale mode: "Scale to a specific instance count"
* Instance count: 1

**Step 7.** Click "Add a scale condition" and configure the settings listed below. 
* Scale mode: "Scale based on a metric"
* Rules:
  * Scale Out
    * Metric source: "Other resource"
    * Resource type: "App Services"
    * Resource: "${WEB_APP_NAME}" (i.e., whatever you named your web app)
    * Metric namespace: "Standard Metrics"
    * Metric name: "Requests"
    * Dimension: "Instance = All values" (i.e., use the total number of requests for all instances)
    * Operator: "Greater than"
    * Metric threshold to trigger scale action: 10
    * Duration (in minutes): 5
    * Time grain statistic: "Average"
    * Time aggregation: "Sum"
    * Action:
      * Operation: "Increase count by" (i.e., increase the count by 1 if the total number of requests for all instances is greater than 10 for 5 minutes)
      * Cool down (minutes): 3 (i.e., don't trigger for another 3 minutes) 
      * instance count: 1
* Instance limits:
  * Minimum: 1
  * Maximum: 2
  * Default: 1
* Schedule: "Specify start/end dates"
* Timezone: "(UTC-05:00) Eastern Time (US & Canada)"
* Start date: (e.g., yesterday)
* End date: (e.g., one week from today)

**Step 8.** Click "Add a scale condition" again and configure the settings listed below. 
* Scale mode: "Scale based on a metric"
* Rules:
  * Scale In
    * Metric source: "Other resource"
    * Resource type: "App Services"
    * Resource: "${WEB_APP_NAME}" (i.e., whatever you named your web app)
    * Metric namespace: "Standard Metrics"
    * Metric name: "Requests"
    * Dimension: "Instance = All values" (i.e., use the total number of requests for all instances)
    * Operator: "Less than"
    * Metric threshold to trigger scale action: 5
    * Duration (in minutes): 5
    * Time grain statistic: "Average"
    * Time aggregation: "Sum"
    * Action:
      * Operation: "Decrease count by" (i.e., decrease the count by 1 if the total number of requests for all instances is less than 5 for 5 minutes)
      * Cool down (minutes): 3 (i.e., don't trigger for another 3 minutes) 
      * instance count: 1
* Instance limits:
  * Minimum: 1
  * Maximum: 2
  * Default: 1
* Schedule: "Specify start/end dates"
* Timezone: "(UTC-05:00) Eastern Time (US & Canada)"
* Start date: (e.g., yesterday)
* End date: (e.g., one week from today)

**Step 9.** Click "Save."

### Task 4
Configure Autoscaling for an Azure Web App Using Terraform

**Step 1.** Create a directory and change directories to it. 
```bash
mkdir -p monitor/autoscale
cd monitor/autoscale
```

**Step 2.** Download the provided Terraform configuration template. 
```bash
wget https://cloudadministratorcourse.blob.core.windows.net/monitoring/terraform/sail/v1/task2/autoscale.tf -O autoscale.tf
```

**Step 3.** Use your favorite text-editor to open the Terraform configuration template. 
```bash
vim autoscale.tf
```

**Step 4.** Verify the following declarations are included in the Terraform configuration template. 
```bash
# Generate a unique id for app name
resource "random_uuid" "server" {
}

# Require provider
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "=3.22.0"
    }
  }
}

# Configure the provider
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Create a new resource group
resource "azurerm_resource_group" "main" {
  name     = "tf_web_app_monitor"
  location = "eastus"
}

# Create an azure service plan
resource "azurerm_service_plan" "main" {
  name                = "tf_web_app_monitor_plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "S1"
}

# Create the azure app service resource
resource "azurerm_linux_web_app" "main" {
  name                = random_uuid.server.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    default_documents = ["index.html"]
  }
}

# Configure an autoscale setting
resource "azurerm_monitor_autoscale_setting" "main" {
  name                = "tf_web_app_autoscale_setting"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  # TODO 1:
  # Specify the target_resource_id as the id of the azure Service plan defined as
  # resource "azurerm_service_plan" "main" (NOT azurerm_linux_web_app)
  target_resource_id = azurerm_service_plan.main.id

  profile {
    name = "defaultProfile"

    # TODO 2:
    # Add limitations to the capacity block:
    capacity {
      default = 1
      minimum = 1
      maximum = 2
    }

    # TODO 3:
    # Complete the scale-out rule which is already outlined in this configuration:
    # - Specify the metric_resource_id as the id of azurerm_linux_web_app (NOT azurerm_service_plan).
    # - Configure the operator and the threshold so that the rule would be triggered
    #   when the average number of requests is greater than 10,
    # - Set the direction and value parameters in the scale_action block to define
    #   the action as increase the count by one.
    rule {
      metric_trigger {
        metric_name        = "Requests"
        metric_resource_id = azurerm_linux_web_app.main.service_plan_id
        time_grain         = "PT5M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Count"
        operator           = "GreaterThan"
        threshold          = 10
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT3M"
      }
    }

    # TODO 4:
    # Add another scale-in rule based on the scale-out rule, which is to decrease
    # the number by one when the average number of requests received by the app
    # service plan is less than 5.
    rule {
      metric_trigger {
        metric_name        = "Requests"
        metric_resource_id = azurerm_linux_web_app.main.id
        time_grain         = "PT5M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Count"
        operator           = "LessThan"
        threshold          = 5
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT3M"
      }
    }
  }
}

# Print the ID of the web app
output "web_app_id" {
  value = "${azurerm_linux_web_app.main.id}"
}

# Print the URL of the web app
output "web_app_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

# Print the ID of the autoscale setting
output "autoscale_id" {
  value = "${azurerm_monitor_autoscale_setting.main.id}"
}
```

**Step 4.** Initialize Terraform. 
```bash
terraform init
```

**Step 5.** Create a Terraform execution plan. 
```bash
terraform plan
```

**Step 6.** Apply the Terraform execution plan. 
```bash
terraform apply
```

**Step 5.** Verify Terraform deployed a web app with autoscaling rules. 
```bash
export RESOURCE_GROUP="tf_web_app_monitor"
az monitor autoscale list \
  --resource-group "${RESOURCE_GROUP}" 
```

### Task 5
Configure an Availability Test Using the Azure Portal. 
* Steps 1 through 7 outline how to create an Azure Application Insights resource to collect monitoring data. 
* Steps 8 through 15 outline how to create an availability test. 
* Steps 16 through 22 outline how to add an action group with one rule to the availability test. 

**Step 1.** Browse to [https://portal.azure.com](https://portal.azure.com).  

**Step 2.** Search for and select "App Services."  

**Step 3.** Click your web app.  

**Step 4.** Click "Application Insights."  

**Step 5.** Click "Turn on Application Insights."  

**Step 6.** Select "Create new resource" and enter the settings listed below. 
* New resource name: "web_app_insights"
* Location: "East US"

**Step 7.** Click "Apply."  

**Step 8.** Click the "Overview" option of your app and copy the URL in the "Default domain" field. 

**Step 9.** Browse to [https://portal.azure.com](https://portal.azure.com).  

**Step 10.** Search for and select "Monitor."  

**Step 11.** Click "Applications" under the "Insights" section. 

**Step 12.** Click your web app. 

**Step 13.** Click "Availability" under the "Investigate" section.  

**Step 14.** Click "Add Classic Test" and enter the settings listed below. 
* Test name: "web-availability-test"
* SKU: "URL ping"
* URL: (e.g., the URL you copied in Step 8 prefixed with "https://")

**Step 15.** Click "Create."  

**Step 16.** Click the ellipses of your availability test and select "Open Rules (Alerts) page."  

**Step 17.** Click the first rule listed (e.g., "web-availability-test-web_app_insights").  

**Step 18.** Click "Edit."  

**Step 19.** Click "Select action groups."  

**Step 20.** Click "Create action group" and enter the settings listed below. 
* Basics tab
  * Resource group: "web_app_monitor"
  * Action group name: "web_app_notification"
  * Display name: "notification"
* Notifcations tab
  * Notifcation type: "Email/SMS message/Push/Voice"
    * Email: (e.g., your email)
  * Name: "email"

**Step 21.** Click "Review + create" and "Create." 

**Step 22.** Click "Save" to save the rule. 

### Task 6
Configure an Availability Test Using Terraform. 
* This task depends on resources created in Task 4 (i.e., `monitor/autoscale`). 

**Step 1.** Create a directory and change directories to it.  
```bash
mkdir -p monitor/availability
cd monitor/availability
```

**Step 2.** Download the provided Terraform configuration template. 
```bash
wget https://cloudadministratorcourse.blob.core.windows.net/monitoring/terraform/sail/v1/task4/availability.tf -O availability.tf
wget https://cloudadministratorcourse.blob.core.windows.net/monitoring/terraform/sail/v1/task4/variables.tf -O variables.tf
```

**Step 3.** Copy the name of the web app created in Task 4. 
```bash
az webapp list \
  --resource-group "tf_web_app_monitor" \
  --query "[].name" \
  --output "tsv"
```

**Step 4.** Use your favorite text-editor to open and edit the `variables.tf` Terraform configuration template. 
```bash
vim variables.tf
```

Below is an example of `variables.tf`. 
```bash
#TODO 1: provide the name of the web app
variable "web_app_name" {
  type    = string
  default = "b109bf63-abd7-5004-e856-6a8e388507f2"
}

#TODO 2: provide the resource group of the web app
variable "resource_group_name" {
  type    = string
  default = "tf_web_app_monitor"
```

**Step 5.** Use your favorite text-editor to open and edit the `availability.tf` Terraform configuration template. 
```bash
vim availability.tf
```

Below is an example of `availability.tf`.
```bash
# Fecth the exiting web app created in Task 2
#
# Data sources allow data to be fetched or computed for use elsewhere in Terraform configuration.
# Use of data sources allows a Terraform configuration to make use of information defined outside of Terraform,
# or defined by another separate Terraform configuration.
# For example, in Task 2 you have defined and provisioned a web app per the autoscale.tf.
#
# Please refer to https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_function_app
data "azurerm_linux_function_app" "main" {
  name                = var.web_app_name
  resource_group_name = var.resource_group_name
}

# Require provider
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "=3.22.0"
    }
  }
}

# Configure the provider
provider "azurerm" {
  features {}
}

# Create an Application Insights resource
resource "azurerm_application_insights" "main" {
  name = "tf_app_insights"
  # create the resource within the same resource group and the location as the web app
  location            = data.azurerm_linux_function_app.main.location
  resource_group_name = data.azurerm_linux_function_app.main.resource_group_name
  application_type    = "web"
}

# Set up a web test in the Application Insights for the web app
# Hint: You can find sample configurations at:
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_insights_web_test
resource "azurerm_application_insights_web_test" "main" {
  name = "tf_web_test"
  # create the resource within the same resource group and the location as the web app
  location            = data.azurerm_linux_function_app.main.location
  resource_group_name = data.azurerm_linux_function_app.main.resource_group_name

  # TODO: Specify the application_insights_id parameter as the ID of the Application Insights defined above
  # i.e., the id of "azurerm_application_insights" "main"
  application_insights_id = azurerm_application_insights.main.id
  kind                    = "ping"

  # TODO: Set the frequecy (in seconds) so that this test would run in each 5 minutes.
  frequency = 300

  # TODO: Set a timeout (in seconds) so that requests would be regarded as failed if no response is received within 1 minute.
  timeout       = 60
  enabled       = true
  geo_locations = ["us-tx-sn1-azr", "us-il-ch1-azr", "apac-sg-sin-azr", "apac-hk-hkn-azr", "us-ca-sjc-azr"]

  # An XML configuration specification for a WebTest.
  # The example is provided and you do not have to author it on your own.
  configuration = <<XML
<WebTest Name="WebTest1" Id="ABD48585-0831-40CB-9069-682EA6BB3583" Enabled="True" CssProjectStructure="" CssIteration="" Timeout="0" WorkItemIds="" xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010" Description="" CredentialUserName="" CredentialPassword="" PreAuthenticate="True" Proxy="default" StopOnError="False" RecordedResultFile="" ResultsLocale="">
  <Items>
    <Request Method="GET" Guid="a5f10126-e4cd-570d-961c-cea43999a200" Version="1.1" Url="http://${data.azurerm_linux_function_app.main.name}.azurewebsites.net" ThinkTime="0" Timeout="300" ParseDependentRequests="True" FollowRedirects="True" RecordResult="True" Cache="False" ResponseTimeGoal="0" Encoding="utf-8" ExpectedHttpStatusCode="200" ExpectedResponseUrl="" ReportingName="" IgnoreHttpStatusCode="False" />
  </Items>
</WebTest>
XML
}

# Create an action group for email notification
# Refer to https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_action_group
resource "azurerm_monitor_action_group" "main" {
  name = "tf_action_group"
  # create the resource within the same resource group as the web app
  resource_group_name = data.azurerm_linux_function_app.main.resource_group_name
  short_name          = "tf_act"

  # TODO: Provide a name and an email address within the email_receiver block.
  email_receiver {
    name          = "Victor Fernandez III"
    email_address = "goober@dev.edu"
  }
}

# Create a metric alert that get triggered by the result of the availability test
resource "azurerm_monitor_metric_alert" "main" {
  name = "tf_metric_alert"
  # create the resource within the same resource group as the web app
  resource_group_name = data.azurerm_linux_function_app.main.resource_group_name
  scopes = [
  azurerm_application_insights.main.id]
  description = "This is a metric alert configured by Terraform to check the result of availability test."
  enabled     = true

  # TODO: Complete the criteria block so that the alert would trigger actions when:
  # the average successful availability test percentage is less than 95.
  # Refer to the criteria block in https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_metric_alert
  criteria {
    metric_namespace = "microsoft.insights/components"
    metric_name      = "availabilityResults/availabilityPercentage"
    aggregation      = "Average"
    operator         = "LessThan"
    threshold        = 95
  }

  # TODO: Complete the action block to associate the alert with the action group you
  # configured above by specifying the action_group_id
  # i.e., the id of "azurerm_monitor_action_group" "main"
  # Refer to the action block in https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_metric_alert
  action {
    action_group_id = azurerm_monitor_action_group.main.id
  }
}
```

**Step 6.** Initialize Terraform. 
```bash
terraform init
```

**Step 7.** Create a Terraform execution plan. 
```bash
terraform plan
```

**Step 8.** Apply the Terraform execution plan. 
```bash
terraform apply
```