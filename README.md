# Sail() Projects
Vic's source code and notes relating to Sail()-based projects from the Army Artificial Intelligence (AI) Technician Cohort 4 program. 

## Set Up
**How to Install the Azure CLI within a GitHub Codespace**  
**Step 1.** Enter the command below. 
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Step 2.** Identify your tenant and subscription IDs and save them as environment variables. 
```bash
# your tentant and subscription IDs are NOT secrets
export TENANT_ID="da3cb2a3-95dd-4a37-b857-c1264e363deb"
export SUBSCRIPTION_ID="17408d59-f3b6-43a5-a48c-c3667527f330"
```

**Step 3.** Enter the command below and authenticate when prompted. 
```bash
az login --tenant "${TENANT_ID}" --use-device-code
```

**Step 4.** Set your default subscription. 
```bash
az account set --subscription "${SUBSCRIPTION_NAME}"
```

## Copyright
This project is licensed under the terms of the [MIT license](/LICENSE).
