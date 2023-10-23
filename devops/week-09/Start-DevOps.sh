# GitHub variables
export REPO_ORG="SAIL-Classroom"
export REPO_NAME="ci-cd-pipeline-for-vm-hosted-webservices-cyberphor"
export REPO_BRANCH="master"

# Azure DevOps project variables
export PROJECT_ORG="victorfernandeziii"
export PROJECT_NAME="week09"
export PROJECT_VISIBILITY="Private"

# Azure DevOps build pipeline variables
export BUILD_PIPELINE_NAME="Build"
export BUILD_PIPELINE_DESCRIPTION="Build pipeline"
export BUILD_PIPELINE_FILE_PATH="azure-build-pipeline.yml"

# Azure DevOps release pipeline variables
export RELEASE_PIPELINE_NAME="Release"
export RELEASE_PIPELINE_DESCRIPTION="Release pipeline"
export RELEASE_PIPELINE_FILE_PATH="azure-release-pipeline.yml"

# Create an Azure DevOps project. If prompted, enter "Y" to install the "azure-devops" extension. 
function Create-AzureDevOpsProject {
    az devops project create \
        --org "https://dev.azure.com/${PROJECT_ORG}" \
        --name "${PROJECT_NAME}" \
        --visibility "${PROJECT_VISIBILITY}"
}

# Create an Azure DevOps service endpoint connection to GitHub and save the ID to a variable.
function Create-AzureDevOpsServiceEndpointGitHub {
    az devops service-endpoint github create \
        --github-url "https://github.com" \
        --name "GitHub" \
        --org "https://dev.azure.com/${PROJECT_ORG}" \
        --project "${PROJECT_NAME}" \
        --query "id" \
        --output "tsv"
}

# Create an build pipeline using Azure DevOps.
function Create-AzureDevOpsPipeline {
    az pipelines create \
        --org "https://dev.azure.com/${PROJECT_ORG}" \
        --project "${PROJECT_NAME}" \
        --repository "${REPO_ORG}/${REPO_NAME}" \
        --repository-type "github" \
        --service-connection $1 \
        --name $2 \
        --yml-path $3 \
        --skip-run
}

# Create an build pipeline using Azure DevOps.
if [ -n "$AZURE_DEVOPS_EXT_GITHUB_PAT" ]; then
    Create-AzureDevOpsProject
    export SERVICE_ENDPOINT_ID=$(Create-AzureDevOpsServiceEndpointGitHub)
    Create-AzureDevOpsPipeline "${SERVICE_ENDPOINT_ID}" "${BUILD_PIPELINE_NAME}" "${BUILD_PIPELINE_FILE_PATH}"
    Create-AzureDevOpsPipeline "${SERVICE_ENDPOINT_ID}" "${RELEASE_PIPELINE_NAME}" "${RELEASE_PIPELINE_FILE_PATH}"
else 
    echo "[x] Error: 'AZURE_DEVOPS_EXT_GITHUB_PAT' is not defined."
    echo " 1. Create a GitHub Personal Access Token (PAT) for Azure DevOps to use."
    echo " 2. Save it to an environment variable called 'AZURE_DEVOPS_EXT_GITHUB_PAT'."
fi