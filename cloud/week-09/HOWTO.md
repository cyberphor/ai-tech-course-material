# Diaster Recovery

## Environment Variables
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
```

## Backup and Restore an Azure Virtual Machine
**Step 1.** Create a resource group.
```bash
az group create \
    --name "${RESOURCE_GROUP}" \
    --location "${LOCATION}"
```

**Step 2.** Create a virtual machine.
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

**Step 2.** Create a recovery vault. 
```bash
az backup vault create \
    --location "${LOCATION}" \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${VM_VAULT_NAME}"
```