# Cloud Security
## Training Objectives
* Create an Azure SQL server and database
* Configure firewall rules for an Azure SQL server
* Insert and select data from an Azure SQL database
* Configure logging for an Azure SQL database
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
**Step 1.** Identify your public IP address. 
```bash
curl -4 icanhazip.com
```

**Step 2.** Add your public IP address to the `security.tf` file. For example, if your IP address is `13.92.118.23` the `security.tf` file would look like below. 
```t
resource "azurerm_mssql_firewall_rule" "fw_rule_01" {
  name             = "Allow_Client_IP_Address"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "13.92.118.23"
  end_ip_address   = "13.92.118.23"
}
```

**Step 3.** Run Terraform. 
```bash
cd terraform
terraform apply
cd ..
```

**Step 4.** Verify the firewall rules were added. 
```bash
az sql server firewall-rule list \
  --server "$SQL_SERVER" \
  --resource-group "${RESOURCE_GROUP}" \
  --output "table"
```

## Insert and Select Data From an Azure SQL Database
**Step 1.** Define your SQL server's other details as environment variables. 
```bash
# define environment variables
export SQL_SERVER_USER="clouduser"
export SQL_SERVER_ENDPOINT="${SQL_SERVER}.database.windows.net"
export SQL_SERVER_DB="SalesLT" # sample SQL database
```

**Step 2.** Create a sample SQL database. 
```bash
sqlcmd -S "${SQL_SERVER_ENDPOINT}" -U "${SQL_SERVER_USER}" -i sql/create_database.sql
```

**Step 3.** Insert data into the sample SQL database. 
```bash
sqlcmd -S "${SQL_SERVER_ENDPOINT}" -U "${SQL_SERVER_USER}" -d "${SQL_SERVER_DB}" -i sql/insert_data.sql 
```

**Step 4.** Select data from the sample SQL database. 
```bash
sqlcmd -S "${SQL_SERVER_ENDPOINT}" -U "${SQL_SERVER_USER}" -d "${SQL_SERVER_DB}" -i sql/select_data.sql
```

## Configure Defender for Cloud for an Azure SQL Database
Text goes here. 