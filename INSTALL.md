## Installation Instructions

### How to Install the Azure CLI within a GitHub Codespace
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

### How to Install Terraform within a GitHub Codespace
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

### How to Install sqlcmd within a GitHub Codespace
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

### How to Install Ansible within a GitHub Namespace
**Step 1.** Install Ansible.
```bash
sudo python -m pip install ansible sshpass
```

### How to Create a GitHub Personal Access Token
**Step 1.** Login to GitHub.  

**Step 2.** Click your profile (top-right icon) and click "Settings."  

**Step 3.** Click "Developer Settings" at the bottom of the pane on the left-hand side.  

**Step 4.** Click "Personal access tokens" > "Tokens (classic)."  

**Step 5.** Click "Generate new token" > "Generate new token (classic)."  

**Step 6.** Enter a "Note" (e.g., AI2C-DevOps-Week03).  

**Step 7.** Set the "Expiration" date (e.g., 60 days).  

**Step 8.** Select "repo" as the scope.  

**Step 9.** Click "Generate token."  

### How to Create an Azure DevOps Personal Access Token
**Step 1.** Browse to [http://dev.azure.com/](http://dev.azure.com/).  

**Step 2.** Click your Azure DevOps project.  

**Step 3.** Click your profile (the person-and-gear icon in the top-right corner).  

**Step 4.** Click "Personal access tokens."  

**Step 5.** Click "New Token."  

**Step 6.** Enter a "Name."  

**Step 7.** Set the "Scopes" field to "Custom defined."  

**Step 8.** Under the "Build" section, select "Read."  

**Step 9.** Click "Create."  

**Step 10.** Record your PAT and use it as necessary.
