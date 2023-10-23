# Source Code for AITP-Related Projects
Vic's source code and notes relating to the Army AI Technician Program (AITP).

## Getting Started
### Install the Azure CLI within a GitHub Codespace
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

### Install Terraform within a GitHub Codespace
**Step 1.** Install the following packages if not already done: `gnupg`, `software-properties-common`, and `curl`. They are required to verify the identity of HashiCorp's package repository. 
```bash
sudo apt-get update 
sudo apt-get install -y gnupg software-properties-common
```

**Step 2.** Install HashiCorp's GPG key.
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
```

**Step 3.** Verify HashiCorp's GPG key fingerprint.
```bash
gpg --no-default-keyring \
--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
--fingerprint
```

**Step 4.** Add HashiCorp's package repository to your list of trusted package repositories. 
```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list
```

**Step 5.** Download package information from HashiCorp's package repository. 
```bash
sudo apt update
```

**Step 6.** Install Terraform. 
```bash
sudo apt install terraform
```

### Install sqlcmd within a GitHub Codespace
**Step 1.** Import the GPG keys for Microsoft's Ubuntu package repository.
```bash
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
```

**Step 2.** Register Microsoft's Ubuntu package repository to your list of trusted package repositories. 
```bash
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit
```

**Step 3.** Download package information from HashiCorp's package repository. 
```bash
sudo apt update
```

**Step 4.** Install `sqlcmd`. 
```bash
sudo apt install mssql-tools18 unixodbc-dev
```

**Step 5.** Update your execution path environment variable to include `sqlcmd`. 
```bash
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
```

## Copyright
This project is licensed under the terms of the [MIT license](/LICENSE).
