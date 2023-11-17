# CI/CD Pipeline for a Containerized Microservice

## Setup
**Step 1.** Create an SSH key-pair to authenticate with. 
```bash
ssh-keygen -t rsa -b 4096 -C Desktop
```

**Step 2.** Create a virtual machine using the information below and Azure Portal. Make sure to copy the SSH public key from the previous step to the appropiate field.
| Field                        | Value                                   |
| ---------------------------- | --------------------------------------- |
| Resource group               | `devops-dev`                            |
| Virtual machine name         | `dev-vm`                                |
| Region                       | `(US) East US`                          |
| Image                        | `Ubuntu Server 22.04 LTS`               |
| Run with Azure Spot discount | `No`                                    |
| Size                         | `Standard_B1ms - 1 vcpus, 2 GiB memory` |
| Authentication type          | `SSH`                                   |

**Step 3.** Connect to the virtual machine via SSH. 
```bash
ssh victor@172.178.78.169
```

**Step 4.** Install Docker. 
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
```

**Step 5.** Add your account to the Docker group (to allow a non-privileged user to run Docker). Then, logout and login again.
```bash
sudo usermod -aG docker $(whoami)
```

**Step 6.** Install Kubernetes. 
```bash
sudo snap install kubectl --classic
```

**Step 7.** Install the Azure CLI. 
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Step 8.** Login to Azure. 
```bash
az login
```

**Step 9.** Identify which Azure subscription you want to use. 
```bash
az account list
```

**Step 10.** Configure the Azure CLI to use the correct Azure subscription. 
```bash
az account set --subscription "AI2C Subscription 1"
```

**Step 11.** Get the provided source code. 
```bash
git clone git@github.com:SAIL-Classroom/ci-cd-pipelines-for-containerized-microservices-cyberphor.git
```

**Step 12.** Create a [GitHub Personal Access Token](/INSTALL.md#how-to-create-a-github-personal-access-token) and update to the `meta.json`.

## Task 1
### Build container images and push them to a container registry
**Step 1.** Build container images for the Dockerfiles provided. 
```bash
cd ci-cd-pipelines-for-containerized-microservices-cyberphor/
docker image build --rm --tag frontend:latest frontend/
docker image build --rm --tag auth-api:latest auth-api/
docker image build --rm --tag todos-api:latest todos-api/
docker image build --rm --tag log-message-processor:latest log-message-processor/
docker image build --rm --tag users-api:latest users-api/
```

**Step 2.** Verify all container images were created.
```bash
docker image ls
```

**Step 3.** Define your Azure-related environment variables. 
```bash
export LOCATION="eastus"
export RESOURCE_GROUP="cicd_microservices"
export ACR_NAME="devopsweek12acrcyberphor"
export ACR_SKU="Basic"
export K8S_CLUSTER_NAME="myAKSCluster"
```

**Step 4.** Create a resource group in Azure. 
```bash
az group create --location "${LOCATION}" --name "${RESOURCE_GROUP}"
```

**Step 5.** Create an Azure Container Registry (ACR). 
```bash
az acr create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${ACR_NAME}" \
  --sku "${ACR_SKU}"
```

**Step 6.** Enable the admin user for the ACR you created. 
```bash
az acr update --name "${ACR_NAME}" --admin-enabled true
```

**Step 7.** Login to the ACR. 
```bash
az acr login --name "${ACR_NAME}"
```

**Step 8.** Review the name of login server for your ACR. For example, the name of the login server for the environment variables I defined early is `devopsweek12acrcyberphor.azurecr.io`.
```bash
az acr list \
  --resource-group "${RESOURCE_GROUP}" \
  --query "[].{acrLoginServer:loginServer}" \
  --output "tsv"
```

**Step 9.** Tag and push each of the container images created earlier to your ACR. 
```bash
export IMAGES=$(docker image ls | grep latest | grep -v azure | cut -d" " -f1)
for IMAGE in $IMAGES; do 
  docker tag ${IMAGE}:latest ${ACR_NAME}.azurecr.io/${IMAGE}:latest
  docker push ${ACR_NAME}.azurecr.io/${IMAGE}:latest
done
```

**Step 10.** Verify each of the newly-tagged container images were pushed to the ACR. 
```bash
az acr repository list --name "${ACR_NAME}" 
```

## Task 2
### Provision a Kubernetes cluster
**Step 1.** Create a new Kubernetes cluster with ACR integration.
```bash
az aks create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${K8S_CLUSTER_NAME}" \
  --attach-acr "${ACR_NAME}" \
  --generate-ssh-keys
```

**Step 2.** Verify the Kubernetes cluster was created. 
```bash
az aks list --resource-group "${RESOURCE_GROUP}" --output "table"
```

## Task 3
### Deploy microservices onto a Kubernetes cluster
**Step 1.** Text goes here.

## Task 4
### Use GitHub Actions to create a CI/CD pipeline for a containerized microservice
**Step 1.** Text goes here.

## Task 5
### Implement CD for an environment with immutable infrastructure
**Step 1.** Text goes here.