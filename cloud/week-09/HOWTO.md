# Diaster Recovery

## Backup and Restore an Azure Virtual Machine
**Step 1.** Define your environment variables.
```bash
export RESOURCE_GROUP="backup-disaster-recovery"
export LOCATION="eastus"
export VM_NAME="VM1"
export VM_IMAGE="Ubuntu2204"
export VM_SIZE="Standard_B1ls"
export VM_TAGS="project=bcdr"
export VM_AUTH_TYPE="password"
export VM_ADMIN_USER="azureuser"
export VM_ADMIN_PASSWORD="P@ssw0rd1.Aa"
export VM_VAULT_NAME="myRecoveryServicesVault"
export STORAGE_NAME="restorationlocationweek09"
export STORAGE_KIND="StorageV2"
export SUBMISSION_USERNAME=""
export SUBMISSION_PASSWORD=""
```

**Step 2.** Create a resource group.
```bash
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}"
```

**Step 3.** Create a virtual machine.
```bash
az vm create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${VM_NAME}" \
  --image "${VM_IMAGE}" \
  --size "${VM_SIZE}" \
  --tags "${VM_TAGS}" \
  --authentication-type "${VM_AUTH_TYPE}" \
  --admin-user "${VM_ADMIN_USER}" \
  --admin-password "${VM_ADMIN_PASSWORD}"
```

**Step 4.** Create a backup vault. 
```bash
az backup vault create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${VM_VAULT_NAME}"
```

**Step 5.** Create a backup policy.
* Resource Groups > (your resource group) > (your backup vault)
* Overview > Backup
  * Backup Goal
  * Where is your workload running?: Azure
  * What do you want to backup?: Virtual machine
  * Configure backup
    * Policy sub type: Standard
    * Backup policy > Create a new policy
    * Policy name: "DailyPolicy"
    * Backup schedule: 
        * Frequency: "Daily"
        * Time: "6:30 AM"
        * Timezone: "(UTC) Coordinated Universal Time"
        * Instant Restore: (default)
        * Retention range
        * Retention of daily backup point - For: "180 days"
    * Virtual machines: (your virtual machine)

**Step 6.** Trigger the backup.  
* Resource Groups > (your resource group) > (your backup vault)
* Protected items > Backup items > Azure Virtual Machine
  * (your virtual machine) > View Details > Backup now

**Step 7.** Wait for the backup to finish.   
* Resource Groups > (your resource group) > (your backup vault)
* Monitoring > Backup jobs
  * (your backup job) > View details
    * Wait for the "Take Snapshot" sub task to complete

**Step 8.** Create a storage account for the restoration staging location.
```bash
az storage account create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${STORAGE_NAME}" \
  --kind "${STORAGE_KIND}"
```

**Step 9.** Trigger the restoration.
* Resource Groups > (your resource group) > (your backup vault)
* Protected items > Backup items > Azure Virtual Machine
  * (your virtual machine) > View Details > Restore VM
    * Restore point > Select > (the snapshot created in Step 6)
    * Restore configuration: Create new
      * Restore type: Create new virtual machine
      * Virtual machine name: (e.g., "VM2")
      * Resource group: (your resource group)
      * Virtual network: (your virtual network)
      * Subnet: (your subnet)
      * Staging location: (the storage account designated as the "restoration staging location")

**Step 10.** Wait for the restoration to finish. 
* Resource Groups > (your resource group) > (your backup vault)
* Monitoring > Backup jobs
  * Wait for your restore job to complete

**Step 11.** Verify there is a backup of the first virtual machine in your backup vault. 
```bash
az backup item list \
  --resource-group "${RESOURCE_GROUP}" \
  --vault-name "${VM_VAULT_NAME}"
```

**Step 12.** Verify the virtual machine has been restored (ex: if your first virtual machine was compromised, you will have two virtual machines after it was restored). 
```bash
az vm list \
  --resource-group "${RESOURCE_GROUP}"
```

## Replicate an Azure Virtual Machine in Another Region
**Step 1.** Define your environment variables.
```bash
export RESOURCE_GROUP="myRG_WestUS"
export LOCATION="westus"
export VM_NAME="VM3"
export VM_IMAGE="Canonical:UbuntuServer:18.04-LTS:18.04.201912180"
export VM_SIZE="Standard_B1ls"
export VM_TAGS="project=p8"
export VM_AUTH_TYPE="password"
export VM_ADMIN_USER="azureuser"
export VM_ADMIN_PASSWORD="P@ssw0rd1.Aa"
```

**Step 2.** Create a resource group.
```bash
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}"
```

**Step 3.** Create a virtual machine.
```bash
az vm create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${VM_NAME}" \
  --image "${VM_IMAGE}" \
  --size "${VM_SIZE}" \
  --tags "${VM_TAGS}" \
  --authentication-type "${VM_AUTH_TYPE}" \
  --admin-user "${VM_ADMIN_USER}" \
  --admin-password "${VM_ADMIN_PASSWORD}"
```

**Step 4.** Add rules to the virtual machine's Network Security Group to allow outbound connections to the services listed below using service tags. A service tag represents a given Azure service and the network IDs they are known to use. 
| Azure Service          | Source      | Source Service Tag | Destination | Destination Service Tag | Protocol | Destination Port |
| ---------------------- | ----------- | ------------------ | ----------- | ----------------------- | -------- | ---------------- |
| Azure Storage          | Service Tag | VirtualNetwork     | Service Tag | `Storage.WestUS`        | TCP      | 443              |
| Azure Event Hub        | Service Tag | VirtualNetwork     | Service Tag | `EventHub.EastUS2`      | TCP      | 443              |
| Azure Site Recovery    | Service Tag | VirtualNetwork     | Service Tag | `AzureSiteRecovery`     | TCP      | 443              |
| Azure Active Directory | Service Tag | VirtualNetwork     | Service Tag | `AzureActiveDirectory`  | TCP      | 443              |

**Step 5.** Verify the rules were configured correctly. 
```bash
az network nsg rule list \
  --nsg-name "${VM_NAME}NSG" \
  --resource-group "${RESOURCE_GROUP}" \
  --query "[?direction=='Outbound']" \
  --output "table"
```

**Step 6.** Enable replication of your virtual machine in the West US region to the East US region.
* Resource Groups > (your resource group) > (your backup vault)
* Protected items > Replicated items > Replicate > Azure virtual machines
  * Source
    * Region: West US
    * Subscription: (your subscription)
    * Resource group: (your second resource group; e.g., `myRG_WestUS`)
    * Virtual machine deployment mode: Resource manager
  * Virtual machines
    * (your virtual machine; e.g., `VM3`)
  * Replication settings
    * Target location: East US
    * Target subscription: (your subscription)
    * Target resource group: (use the default value provided)
    * (use the default value provided for the remaining options)

**Step 7.** Wait for the replication to finish. 
* Resource Groups > (your resource group) > (your backup vault)
* Monitoring > Site Recovery jobs
  * Wait for your recovery jobs to complete

**Step 8.** Verify your virtual machine was replicated. 
* Resource Groups > (your resource group) > (your backup vault)
* Protected items > Replicated items
  * Confirm for your virtual machine's "Replication Health" status is "Protected" 