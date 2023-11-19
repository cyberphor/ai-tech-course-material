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

**Step 12.** Create a [GitHub Personal Access Token](/INSTALL.md#how-to-create-a-github-personal-access-token) and update the `meta.json`.

**Step 13.** Define your environment variables. 
```bash
export SUBSCRIPTION_ID=$(az account show --query "id" --output "tsv")
export LOCATION="eastus"
export RESOURCE_GROUP="cicd_microservices"
export ACR_NAME="devopsweek12acrcyberphor"
export ACR_SKU="Basic"
export AKS_CLUSTER_NAME="myAKSCluster"
export SERVICE_PRINCIPAL_NAME="ghAKS"
export SERVICE_PRINCIPAL_SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}"
```

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

**Step 3.** Create a resource group in Azure. 
```bash
az group create --location "${LOCATION}" --name "${RESOURCE_GROUP}"
```

**Step 4.** Create an Azure Container Registry (ACR). 
```bash
az acr create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${ACR_NAME}" \
  --sku "${ACR_SKU}"
```

**Step 5.** Enable the admin user for the ACR you created. 
```bash
az acr update --name "${ACR_NAME}" --admin-enabled true
```

**Step 6.** Login to the ACR. 
```bash
az acr login --name "${ACR_NAME}"
```

**Step 7.** Review the name of login server for your ACR. For example, the name of the login server for the environment variables I defined early is `devopsweek12acrcyberphor.azurecr.io`.
```bash
az acr list \
  --resource-group "${RESOURCE_GROUP}" \
  --query "[].{acrLoginServer:loginServer}" \
  --output "tsv"
```

**Step 8.** Tag and push each of the container images created earlier to your ACR. 
```bash
export IMAGES=$(docker image ls | grep latest | grep -v azure | cut -d" " -f1)
for IMAGE in $IMAGES; do 
  docker tag ${IMAGE}:latest ${ACR_NAME}.azurecr.io/${IMAGE}:latest
  docker push ${ACR_NAME}.azurecr.io/${IMAGE}:latest
done
```

**Step 9.** Verify each of the newly-tagged container images were pushed to the ACR. 
```bash
az acr repository list --name "${ACR_NAME}" 
```

## Task 2
### Provision a Kubernetes cluster
**Step 1.** Create a new Azure Kubernetes Service (AKS) cluster with ACR integration.
```bash
az aks create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${AKS_CLUSTER_NAME}" \
  --attach-acr "${ACR_NAME}" \
  --generate-ssh-keys
```

**Step 2.** Setup access to the AKS cluster for `kubectl`. 
```bash
az aks get-credentials --resource-group "${RESOURCE_GROUP}" --name "${AKS_CLUSTER_NAME}"
```

You should get a message similar to below. 
```
Merged "myAKSCluster" as current context in /home/victor/.kube/config
```

**Step 3.** Verify the Kubernetes cluster was created. 
```bash
az aks list --resource-group "${RESOURCE_GROUP}" --output "table"
```

## Task 3
### Deploy microservices onto a Kubernetes cluster
**Step 1.** For every microservice, update its provided `deployment.yaml` and `service.yaml` files with the correct image name, pod port number, and service port number. If you get an error messaging saying `The connection to the server localhost:8080 was refused - did you specify the right host or port?`, make sure you've authenticated with both Azure and your ACR. Then, check if `kubectl` has the credentials needed to access your AKS cluster (see the previous task for more information). 
```yaml
# k8s/frontend/deployment.yaml
- image: devopsweek12acrcyberphor.azurecr.io/frontend:latest
- containerPort: 8080

# k8s/frontend/service.yaml
- port: 80
  targetPort: 8080

# k8s/auth-api/deployment.yaml
- image: devopsweek12acrcyberphor.azurecr.io/auth-api:latest
- containerPort: 8081

# k8s/auth-api/service.yaml
- port: 8081

# k8s/log-message-processor/deployment.yaml
- image: devopsweek12acrcyberphor.azurecr.io/log-message-processor:latest

# k8s/todo-api/deployment.yaml
- image: devopsweek12acrcyberphor.azurecr.io/todos-api:latest
- containerPort: 8082

# k8s/todo-api/service.yaml
- port: 8082

# k8s/users-api/deployment.yaml
- image: devopsweek12acrcyberphor.azurecr.io/users-api:latest
- containerPort: 8083

# k8s/users-api/service.yaml
- port: 8083
```

**Step 2.** Create the Kubernetes objects. 
```bash
kubectl create -R -f k8s/
```

If you need to troubleshoot and/or delete objects, use the command below. 
```bash
kubectl delete -R -f k8s/
```

**Step 3.** Verify the deployment objects were created. 
```bash
kubectl get deployments
```

**Step 4.** Verify the service objects were created. 
```bash
kubectl get services
```

**Step 5.** Verify you can reach the frontend using a public IP address. 
```bash
curl http://$PUBLIC_IP
```

## Task 4
This task uses GitHub Actions, an ACR, and Kubernetes to create a CI/CD pipeline with conditions to rebuild container images and redeploy containers. 

### Rebuilding All Container Images
Rebuilding all of your container images is not necessary during the situations described below.
* Your Kubernetes object manifest has changed
* Only one container's code has changed

### Use GitHub Actions to create a CI/CD pipeline for a containerized app
**Step 1.** Create an account for GitHub Actions to use when accessing Azure. More specifically, you need to create a service principal with Contributor access to your Azure subscription. 
```bash
az ad sp create-for-rbac \
  --name "${SERVICE_PRINCIPAL_NAME}" \
  --scope "${SERVICE_PRINCIPAL_SCOPE}" \
  --role "Contributor" \
  --sdk-auth
```

The output should be similar to below. Copy the entire JSON object and use it in the next step. 
```json
{
  "clientId": "db31b3a4-a040-4aa7-8986-ca85b38f5eea",
  "clientSecret": "lzk8Q~5szMH-lhFOifg-5-gL.QlJhIiaCVFRxcyB",       
  "subscriptionId": "17408d59-f3b6-43a5-a48c-c3667527f330",
  "tenantId": "da3cb2a3-95dd-4a37-b857-c1264e363deb",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",    
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",   
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**Step 2.** Add the Secrets listed below to the provided GitHub repository using information contained in the "Access keys" settings of your ACR. 
| Name                 | Secret                                                 |
| -------------------- | ------------------------------------------------------ | 
| `RESOURCE_GROUP`     | `cicd_microservices`                                   |
| `CONTAINER_REGISTRY` | `devopsweek12acrcyberphor.azurecr.io`                  |
| `REGISTRY_USERNAME`  | `devopsweek12acrcyberphor`                             | 
| `REGISTRY_PASSWORD`  | `SKIRUzya4xiVnKM2UTbQGWt29vykLw3uZ53OBM4Vih+ACRBA/iTd` |
| `AKS_CLUSTER_NAME`   | `myAKSCluster`                                         |
| `AKS_CREDENTIALS`    | (copy the entire JSON object from the previous step)   |

**Step 3.** Create a GitHub Actions workflow using inspiration from the [provided configuration file](/devops/week-12/cicd.yml). 
```bash
mkdir -p .github/workflows
touch .github/workflows/cicd.yml
```

The CI/CD pipeline you're creating includes the jobs described below. 
* Job 1: Create a strategy matrix
* Job 2: Rebuild and push container images to your ACR
* Job 3: Redeploy containers onto your AKS cluster

**Step 4.** Commit the GitHub Actions workflow configuration file to trigger the CI/CD pipeline.

## Task 5
### Implement CD for an environment with immutable infrastructure
**Step 1.** Text goes here.