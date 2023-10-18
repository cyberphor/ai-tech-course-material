# Cloud Security
## Training Objectives
* Describe security requirements for deploying apps to the cloud
* Describe how a defense-in-depth strategy mitigates security incidents
* Describe 3 ways access to an Azure SQL database can be controlled
* Configure firewall rules for an Azure SQL database
* Configure logging for an Azure SQL database

## Submitter
```bash
wget https://cloudadministratorcourse.blob.core.windows.net/security/submitter/sail2/v4/submitter -O submitter
chmod +x submitter
export SUBMISSION_USERNAME="vf@andrew.cmu.edu"
export SUBMISSION_PASSWORD=""
```

## Tasks
### Create an Azure SQL Database Server
**Step 1.** Run Terraform. 
```bash
cd terraform
terraform init
terraform plan
terraform apply
cd ..
``` 

**Step 2.** Get the name of your Azure SQL Database Server. 
```bash
terraform output
```

Another option is using the Azure CLI. 
```bash
export RESOURCE_GROUP="cloud-security"
az sql server list \
  --resource-group "${RESOURCE_GROUP}" --output tsv --query "[].name"
```

To get the `admin_password` (a variable with sensitive/secret information), enter the command below. 
```bash
terraform output admin_password
```