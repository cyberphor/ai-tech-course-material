# Containers: Docker and Kubernetes

## Setup
**Step 1.** Define the environment variables needed to create and access a virtual machine.
```bash
code .env
```
```bash
export RESOURCE_GROUP="containers-rg"
export LOCATION="eastus"
export VM_NAME="VM1"
export VM_IMAGE="Ubuntu2204"
export VM_SIZE="Standard_B1ls"
export VM_AUTH_TYPE="password"
export VM_ADMIN_USER="clouduser"
export VM_ADMIN_PASSWORD="Password123!"
```

**Step 2.** Create a virtual machine
```bash
# text goes here
```

**Step 3.** Save the public IP address of the virtual machine as an environment variable. 
```bash
# text goes here
```

**Step 3.** Disable boot diagnostics on the virtual machine.
```bash
# text goes here
```

**Step 4.** Login to the virtual machine.
```bash
ssh $VM_ADMIN_USER@$VM_PUBLIC_IP
```

**Step 5.** Install Python 2.
```bash
sudo apt install -y python2
```

**Step 6.** Install the Docker on the virtual machine.
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
```

**Step 7.** Configure Docker to run as a non-root user.
```bash
sudo usermod -aG docker $(whoami)
```

**Step 8.** Install Kubectl.
```bash
sudo snap install kubectl --classic
```

**Step 9.** Install the Azure CLI on the virtual machine.
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Step 10.** Login to Azure. 
```bash
az login
```

**Step 11.** Review your Azure subscriptions.
```bash
az account list
```

**Step 12.** Configure the Azure CLI to use the correct subscription.
```bash
export SUBSCRIPTION_ID=""
az account set --subscription "${SUBSCRIPTION_ID}"
```

**Step 13.** Download the source code provided. 
```bash
wget https://cloudadministratorcourse.blob.core.windows.net/containers/handout/sail/handout_v2.tar.gz
```

**Step 14.** Unzip the source code. 
```bash
tar xvzf handout_v2.tar.gz
```

**Step 15.** Replace the provided `submitter` with a different version.
```bash
wget https://cloudadministratorcourse.blob.core.windows.net/docker-and-kubernetes/submitter/sail2/v4/submitter -O submitter
```

**Step 16.** In the `starter_code` directory, verify the `package.json` file's `typescript` field  value is `^4.2.4`.

**Step 17.** In the `starter_code/docker/` directory, update the Dockerfile by replacing the line `ADD . .` with `ADD starter_code/ .`.

## Build a Container Image Using a Dockerfile and the Docker Engine
**Step 1.** Build the image.
```bash
sudo docker build --rm -t "hello-message:latest" -f starter_code/docker/Dockerfile .
```

## Run a Container Using an Image and the Docker Engine
**Step 1.** Run the container as a daemon and expose its port. 
```bash
docker run --name "task1" -d -p 80:8080 "hello-message:latest" 
```

**Step 2.** Make a web request to the container.
```bash
curl localhost/hello/victor
```

**Step 3.** Stop the container using its name.
```bash
docker stop task1
```

## Create and Use a Container Registry in Azure
**Step 1.** Define and load the environment variables within your virtual machine. 
```bash
vim .env
```
```bash
export RESOURCE_GROUP="containers-rg"
export ACR_NAME="acrweek10cyberphor"
export ACR_SKU="Basic"
export ACR_URL="${ACR_NAME}.azurecr.io"
```
```bash
source .env
```

**Step 2.** Create a container registry in Azure. 
```bash
az acr create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${ACR_NAME}" \
  --sku "${ACR_SKU}" \
  --admin-enabled true # hack; better option: "system assigned managed identity"
```

**Step 3.** Login to your container registry.
```bash
az acr login --name "${ACR_NAME}"
```

**Step 4.** Tag the previously created image (to identify it as a different instance from the one hosted locally).
```bash
docker tag "hello-message:latest" "${ACR_URL}/hello-message:latest"
```

**Step 5.** Push the image to your container registry. 
```bash
docker push "${ACR_URL}/hello-message:latest"
```

## Deploy Containers Using the Azure Kubernetes Service
**Step 1.** Update and reload the environment variables within your virtual machine.
```bash
vim .env
```
```bash
export RESOURCE_GROUP="containers-rg"
export ACR_NAME="acrweek10cyberphor"
export ACR_SKU="Basic"
export ACR_URL="${ACR_NAME}.azurecr.io"
export AKS_CLUSER_NAME="myAKSCluster"
```
```bash
source .env
```

**Step 2.** Update the provided manifest.
```bash
cd starter_code/k8s
vim sample-app.yaml
```

**Step 3.** Create a Azure Kubernetes Service (AKS) cluster with integration support for your container registry in Azure. 
```bash
az aks create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${AKS_CLUSTER_NAME}" \ # i ended up not using an environment variable
  --attach-acr "${ACR_NAME}" \
  --generate-ssh-keys
```

**Step 4.** Setup access to the AKS cluster for `kubectl`. 
```bash
az aks get-credentials --resource-group "containers-rg" --name "myAKSCluster"
```

**Step 5.** Create all the objects defined in the manifest.
```bash
kubectl create -R -f starter_code/k8s/
```

**Step 6.** Review the services created by `kubectl`.
```bash
kubectl get services
```

**Step 7.** Delete all the objects defined the manifest.
```bash
kubectl delete -R -f starter_code/k8s/
```

**Step 8.** Delete all services. 
```bash
kubectl delete services --all
```