# DevOps
## Training Objectives
1. Create a CI/CD pipeline for a Node.js web app
2. Create a VM deployment group
3. Register a VM to a VM deployment group
4. Create a CI/CD pipeline task to deploy a Node.js web app to different VM deployment groups
5. Add a trigger to an existing CI/CD pipeline
6. Configure health checks using Azure Traffic Manager

## Setup
**Step 1.** Create a GitHub Personal Access Token (PAT) and save it as an environment variable. Make sure it expires soon and only has the following scopes checked: `repo`, `admin:repo_hook`, and `user`. 
```bash
export AZURE_DEVOPS_EXT_GITHUB_PAT=""
```

**Step 2.** Verify you're using the correct Azure subscription.
```bash
az account show
```

**Step 3.** Create an Azure DevOps project. If prompted, enter "Y" to install the "azure-devops" extension. 
```bash
export PROJECT_ORG="victorfernandeziii"
export PROJECT_NAME="week09"
export PROJECT_VISIBILITY="Private"
az devops project create \
  --org "https://dev.azure.com/${PROJECT_ORG}" \
  --name "${PROJECT_NAME}" \
  --visibility "${PROJECT_VISIBILITY}"
```

**Step 4.** Create an Azure DevOps service endpoint connection to GitHub and save the ID to a variable.
```bash
export REPO_ORG="SAIL-Classroom"
export REPO_NAME="ci-cd-pipeline-for-vm-hosted-webservices-cyberphor"
export SERVICE_ENDPOINT="https://github.com"
export SERVICE_ENDPOINT_NAME="GitHub"
export SERVICE_ENDPOINT_ID=$(az devops service-endpoint github create \
  --github-url "${SERVICE_ENDPOINT}" \
  --name "${SERVICE_ENDPOINT_NAME}" \
  --org "https://dev.azure.com/${PROJECT_ORG}" \
  --project "${PROJECT_NAME}" \
  --query "id" \
  --output "tsv" \
)
```

**Step 5.** Create an Azure DevOps pipeline called "Build".
```bash
export PIPELINE_NAME="Build"
export PIPELINE_DESCRIPTION="Build pipeline"
export REPO_TYPE="github"
export REPO_BRANCH="master"
export REPO="${REPO_ORG}/${REPO_NAME}"
az pipelines create \
  --name "Build" \
  --org "https://dev.azure.com/victorfernandeziii" \
  --project "week09" \
  --repository "https://github.com/SAIL-Classroom/ci-cd-pipeline-for-vm-hosted-webservices-cyberphor"
```

**Step 6.** Download the provided source code. If you get a "Permission denied (publickey)" error, make sure you created an SSH key pair and added the public key to your GitHub profile. 
```bash
git clone git@github.com:SAIL-Classroom/ci-cd-pipeline-for-vm-hosted-webservices-cyberphor.git
cd ci-cd-pipeline-for-vm-hosted-webservices-cyberphor
```