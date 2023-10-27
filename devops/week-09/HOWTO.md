# Azure DevOps

## Setup
**Step 1.** Create a GitHub Personal Access Token (PAT) for Azure DevOps to use and save it as an environment variable. Make sure it expires soon and only has the following scopes checked: `repo`, `admin:repo_hook`, and `user`. 
```bash
export AZURE_DEVOPS_EXT_GITHUB_PAT=""
```

**Step 2.** Create an Azure DevOps PAT with the `Deployment Groups: Read & Manage` scope checked. 
```bash
export DEPLOYMENT_GROUP_PAT="ijythyioedzyjrzqk6x47da7gjljsvjoscgrwf7a7obtn2xpj3da" # good luck :)
```

**Step 3.** Set other variables. 
```bash
export AZURE_PIPELINE_AGENT_URL_LINUX="https://vstsagentpackage.azureedge.net/agent/3.227.2/vsts-agent-linux-x64-3.227.2.tar.gz"
export DEPLOYMENT_GROUP_PROD="Prod"
export DEPLOYMENT_GROUP_QA="QA"
export DEPLOYMENT_GROUP_TAG="ci-cd-pipeline-for-vm-hosted-webservices"
export PROJECT_ORG="victorfernandeziii"
export PROJECT_NAME="week09"
```

**Step 2.** Download the provided source code. If you get a "Permission denied (publickey)" error, make sure you created an SSH key pair and added the public key to your GitHub profile. If the repo doesn't include a CI/CD pipeline file, add it.
```bash
git clone git@github.com:SAIL-Classroom/ci-cd-pipeline-for-vm-hosted-webservices-cyberphor.git
cd ci-cd-pipeline-for-vm-hosted-webservices-cyberphor
```

**Step 3.** Verify you're using the correct Azure subscription.
```bash
az account show
```

**Step 4.** Execute the script provided. 
```bash
bash Start-DevOps.sh
```

## Run Terraform
```bash
cd terraform/
terraform init
terraform plan
terraform apply
export ANSIBLE_USER=$(terraform output admin_username | tr -d '"')
cd ..
```

## Create Your Deployment Groups
Text goes here. 

## SSH
```bash
eval "$(ssh-agent -s)" # start the SSH authentication agent
ssh-add ~/.ssh/id_rsa  # add your SSH private key to the SSH authentication agent
```

## Register Multiple Virtual Machines with a Deployment Group
```bash
cd ansible/
ansible-playbook playbook.yml -i inventory.ini --ssh-common-args='-o StrictHostKeyChecking=no'
```

### References
* [https://stackoverflow.com/questions/75081137/unable-to-create-pipeline-using-azure-devops-cli-in-azure-devops-portal-from-azu](https://stackoverflow.com/questions/75081137/unable-to-create-pipeline-using-azure-devops-cli-in-azure-devops-portal-from-azu)