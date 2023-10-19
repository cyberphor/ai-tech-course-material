# Cloud Security
## Training Objectives
* Create an Azure SQL server and database
* Configure firewall rules for an Azure SQL server
* Insert data from an Azure SQL database
* Configure server-level auditing for an Azure SQL Server
* Configure Defender for Cloud for an Azure SQL database

## Submitter
```bash
wget https://cloudadministratorcourse.blob.core.windows.net/security/submitter/sail2/v4/submitter -O submitter
chmod +x submitter
export SUBMISSION_USERNAME="vf@andrew.cmu.edu"
export SUBMISSION_PASSWORD=""
```

## Tasks
### Create an Azure SQL Server and Database
**Step 1.** Run Terraform. 
```bash
cd terraform
terraform init
terraform plan
terraform apply
cd ..
``` 

**Step 2.** Save the name of your resource group and SQL server as environment variables. 
```bash
export RESOURCE_GROUP="cloud-security"
export SQL_SERVER=$(az sql server list \
  --resource-group "${RESOURCE_GROUP}" \
  --output "tsv" \
  --query "[].name"
)
```

To get the `admin_password` created by Terraform (a variable with sensitive/secret information), enter the command below. 
```bash
terraform output admin_password
```

### Add Firewall Rules to an Azure SQL Server
**Step 1.** Open the `main.tf` Terraform configuration file. Change `public_network_access_enabled` from `false` to `true` in the `azurerm_mssql_server` resource block.  

**Step 2.** Identify your public IP address. 
```bash
curl -4 icanhazip.com
```

**Step 3.** Open the `security.tf` Terraform configuration file. Set the `start_ip_address` and `end_ip_address` to your public IP address within the  `azurerm_mssql_firewall_rule` resource block.

**Step 3.** Enter the commands below to apply your new Terraform configuration plan. 
```bash
cd terraform
terraform apply
cd ..
```

**Step 4.** Enter the command below to verify the firewall rules were added. 
```bash
az sql server firewall-rule list \
  --server "$SQL_SERVER" \
  --resource-group "${RESOURCE_GROUP}" \
  --output "table"
```

## Insert Data Into an Azure SQL Database
**Step 1.** Define your SQL server's other details as environment variables. 
```bash
# define environment variables
export SQL_SERVER_USER="clouduser"
export SQL_SERVER_ENDPOINT="${SQL_SERVER}.database.windows.net"
export SQL_SERVER_DB="cloud-security-db" # sample SQL database
```

**Step 2.** Insert data into the SQL database using `sqlcmd`. 
```bash
sqlcmd -S "${SQL_SERVER_ENDPOINT}" -U "${SQL_SERVER_USER}" -d "${SQL_SERVER_DB}" -i sql/insert_data.sql 
```

## Configure Server-Level Auditing for an Azure SQL Server
**Step 1.** Add the block below to the Terraform `security.tf` configuration file if it doesn't already exist.
```hcl
resource "random_pet" "azurerm_storage_account_name" {
  separator = ""
}

resource "azurerm_storage_account" "sql_logs" {
  name                     = random_pet.sql_log_storage_account_name.id
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_mssql_server_extended_auditing_policy" "main" {
  server_id                  = azurerm_mssql_server.main.id
  storage_endpoint           = azurerm_storage_account.sql_logs.primary_blob_endpoint
  storage_account_access_key = azurerm_storage_account.sql_logs.primary_access_key
}
```

**Step 2.** Enter the commands below to apply your new Terraform configuration plan.  
```bash
cd terraform
terraform apply
cd ..
```

**Step 3.** Query the sample SQL database to generate some logs. 
```bash
sqlcmd -S "${SQL_SERVER_ENDPOINT}" -U "${SQL_SERVER_USER}" -d "${SQL_SERVER_DB}" -i sql/select_data.sql
```

**Step 4.** Verify logs generated.

## Configure Defender for Cloud for an Azure SQL Database
**Step 1.** Add the `threat_detection_policy` block below to the `azurerm_mssql_database` block (within the Terraform `security.tf` configuration file) if it doesn't already exist.
```t
  threat_detection_policy {
    state                      = "Enabled"
    storage_endpoint           = azurerm_storage_account.threat_detection_logs.primary_blob_endpoint
    storage_account_access_key = azurerm_storage_account.threat_detection_logs.primary_access_key
  }
```

**Step 2.** Enter the commands below to apply your new Terraform configuration plan.  
```bash
cd terraform
terraform apply
cd ..
```