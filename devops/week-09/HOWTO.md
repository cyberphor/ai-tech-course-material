# Azure DevOps

## Setup
**Step 1.** Create a GitHub Personal Access Token (PAT) for Azure DevOps to use and save it as an environment variable. Make sure it expires soon and only has the following scopes checked: `repo`, `admin:repo_hook`, and `user`. 
```bash
export AZURE_DEVOPS_EXT_GITHUB_PAT=""
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
```
cd terraform/
terraform init
terraform plan
terraform apply
export ansible_password="$(terraform output admin_username)"
export ansible_password="$(terraform output admin_password)"
cd ..
```

## Create Your Deployment Groups
Text goes here. 

## Register Multiple Virtual Machines with a Deployment Group
```bash
ansible-playbook playbook.yml \
  -i inventory.yml \
  --ssh-common-args='-o StrictHostKeyChecking=no'
```

### References
* [https://stackoverflow.com/questions/75081137/unable-to-create-pipeline-using-azure-devops-cli-in-azure-devops-portal-from-azu](https://stackoverflow.com/questions/75081137/unable-to-create-pipeline-using-azure-devops-cli-in-azure-devops-portal-from-azu)