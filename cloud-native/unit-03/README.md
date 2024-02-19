# Cloud Native: API Gateway
* [References](#references)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)
* [Task 05](#task-05)

## References
If I find any helpful references, I will put them here. 
* [GitHub - cyberphor: virtualization/containers/kubernetes](https://github.com/cyberphor/knowledge-base/tree/main/virtualization/containers/kubernetes)
* [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
* [NGINX Gateway Fabric (NGF)](https://docs.nginx.com/nginx-gateway-fabric/overview/gateway-architecture/)

## Setup
<mark>The steps below assume you're working in a Linux environment (WSL, Azure Shell, GitHub Codespaces, a Linux virtual machine, etc.) with the following software already installed: Azure CLI, Kubernetes, and Helm.</mark>

**Step 1.** Accept the GitHub Classroom assignment titled "Project 3 - Productionizing API Gateways." The invitation is in the "Setup" section of task 1's instructions (in the course material, not here). After accepting the assignment, a GitHub repository will be created for you. To access it, do the following: (1) login to GitHub, (2) click your profile picture, (3) click "Your organizations", (4) click "CloudNativeSpring2024", and then (5) click the "project-3-productionizing-api-gateways-" repository. 

**Step 2.** Download the `vic-code` GitHub repository and change directories to the `setup` folder for this week's project. The commands below are meant to be ran on your personal computer (from any directory).
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/cloud-native/unit-03/setup/
```

**Step 3.** Login to the Azure CLI if you haven't already. The command below is meant to be ran on your personal computer (from any directory).
```bash
az login --use-device-code
```

**Step 4.** Set your subscription if you haven't already. The command below is meant to be ran on your personal computer (from any directory).
```bash
az account set --subscription "AI2C Subscription 3"
```

**Step 5.** Define and export an environment variable called `ACR_NAME`. 

*Option 1*  
Enter the command below (after replacing the string `cyberphorwashere`). 
```bash
export ACR_NAME="cyberphorwashere"
```

*Optional 2*  
Edit the provided [`.env`](setup/.env) file and then enter the command below (from the same directory as the `.env` file). Again, the `source` program reads and executes commands from files into your current shell environment. 
```bash
source .env
```

**Step 6.** Create an Azure resource group. The command below is meant to be ran on your personal computer (from any directory).
```bash
az group create \
  --name project3 \
  --location eastus
```

**Step 7.** Create an Azure Container Registry (ACR) resource. The command below is meant to be ran on your personal computer (from any directory).
```bash
az acr create \
  --resource-group project3 \
  --name $ACR_NAME \
  --sku Basic
```

**Step 8.** Login to your ACR resource. The command below is meant to be ran on your personal computer (from any directory).
```bash
az acr login \
  --name $ACR_NAME
```

**Step 9.** Create an Azure Kubernetes Service (AKS) resource. Again, an AKS resource is just a Kubernetes cluster running in Azure. The command below is meant to be ran on your personal computer (from any directory).
```bash
az aks create \
  --resource-group project3 \
  --name project3cluster \
  --enable-managed-identity \
  --node-count 2 \
  --generate-ssh-keys
```

**Step 10.** Attach your ACR resource to your AKS resource. The command below is meant to be ran on your personal computer (from any directory).
```bash
az aks update \
  --resource-group project3 \
  --name project3cluster \
  --attach-acr $ACR_NAME
```

**Step 11.** Download the credentials for your AKS resource to a file for `kubectl` to use. The command below is meant to be ran on your personal computer (from any directory).
```bash
az aks get-credentials \
  --resource-group project3 \
  --name project3cluster
```

**Step 12.** Install additional Custom Resource Defintions (CRDs) `kubectl` needs to manage a "Kubernetes Gateway API." A Kubernetes Gateway API (otherwise known simply as "Gateway API") is a newer alternative to a Kubernetes LoadBalancer. Again, LoadBalancers are what allow external traffic to reach applications within your Kubernetes cluster. Gateway APIs are cheaper than LoadBalancers (they also include more standardization, authorization levels, and support for protocols like gRPC). See the [References](#references) section above for more information about Gateway APIs. The command below is meant to be ran on your personal computer (from any directory).
```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

**Step 13.** Add a Nginx Gateway Fabric (NGF) container to your AKS resource. Creating an NGF container is the first step in deploying a Gateway API to your Kubernetes cluster. See the [References](#references) section above for more information about NGF containers. The command below is meant to be ran on your personal computer (from any directory).
```bash
helm install ngf oci://ghcr.io/nginxinc/charts/nginx-gateway-fabric --create-namespace -n nginx-gateway
```

**Step 14.** Add a Nginx container to your AKS resource. Creating an Nginx container is the second step in deploying a Gateway API to your Kubernetes cluster. The command below is meant to be ran on your personal computer (from any directory).
```bash
kubectl apply -f https://raw.githubusercontent.com/nginxinc/nginx-gateway-fabric/v1.0.0/deploy/manifests/service/loadbalancer.yaml
```

If you were able to complete the steps above, you've created the object in the image below. 
![nginx-gateway-fabric.png](setup/nginx-gateway-fabric.png)

The following instructions cover creating the objects in the image below.  
![gateway-api.png](setup/gateway-api.png)

## Task 01
**Step 1.** Text goes here.

## Task 02
**Step 1.** Text goes here.

## Task 03
**Step 1.** Text goes here.

## Task 04
**Step 1.** Text goes here.

## Task 05
**Step 1.** Text goes here.