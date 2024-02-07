# Cloud Native

## Setup
**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's project. These commands are meant to be ran on your personal computer.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/cloud-native/unit-02/setup/
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. This command is meant to be ran on your personal computer. `-t` defines the key pair type. `-b` defines the key lengths (i.e., the number of bits). `-C` is used to include a comment. 
```bash
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. These commands are meant to be ran on your personal computer. The first command starts the SSH authentication agent while the second command adds your SSH private key to it.
```bash
eval "$(ssh-agent -s)" 
ssh-add ~/.ssh/id_rsa  
```

**Step 4.** Install Ansible if you don't already have it installed. These commands are meant to be ran on your personal computer.
```bash
python -m pip install ansible
```

**Step 5.** Login to the Azure CLI and set your subscription if you haven't already. These commands are meant to be ran on your personal computer.
```bash
az login --use-device-code
az account set --subscription "AI2C Subscription 3"
```

**Step 6.** Deploy a virtual machine in Azure using the [provided Terraform files](setup/terraform). These commands are meant to be ran on your personal computer. 
```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply -auto-approve
export USERNAME=$(terraform -chdir=terraform output -raw username)
export IP_ADDRESS=$(terraform -chdir=terraform output -raw ip_address)
```

**Step 7.** Configure the virtual machine using Ansible. The [Ansible playbook](ansible/playbook.yaml) provided references multiple scripts in the [`ansible/scripts`](ansible/scripts/) folder. The scripts install software and download this week's handout. This command is meant to be ran on your personal computer.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

## Task 1
**Step 1.** Connect to the virtual machine you just created and change directories to `llmservice-handout`. 
```bash
cd llmservice-handout/
```

**Step 2.** Invoke the Python virtual environment created by Ansible and then change directories to `worker/src`. 
```bash
source venv/bin/activate
cd worker/src
```

**Step 3.** Edit the `simplellm.py` file using the [provided example](task-01/src/simplellm.py).

**Step 4.** Start a local Flask server as a background process. 
```bash
flask --app simplellm run --debug &
```

**Step 5.** Query the `healthcheck` endpoint of your Flask-based application. 
```bash
curl http://127.0.0.1:5000/healthcheck
```

**Step 6.** Query the `API` endpoint of your Flask-based application. 
```bash
curl -G --data-urlencode message="what is 1 + 1?" http://localhost:5000/api
```

The output should be similar to below. If these queries worked, stop your Flask server. 
```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "\nYes, the answer to your question is 1 + 1 = 2."
    }
  ],
  "created": 1707148633,
  "id": "cmpl-85a9a50a-35bf-419f-9bf4-110372ba8122",
  "model": "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 18,
    "prompt_tokens": 35,
    "total_tokens": 53
  }
}
```

**Step 7.** Edit the `pyproject.toml` file using the [provided example](task-01/src/pyproject.toml).

**Step 8.** Change directories to `worker` (the parent directory of `src`, your current working directory).
```bash
cd ../
```

**Step 9.** Build your Flask-based application and save the artifact in folder called `dist/`.
```bash
python3 -m pip wheel src/ -w dist/
```

**Step 10.** Validate your artifact was built correctly by importing it using `pip` 
```bash
python3 -m pip install dist/simplellm-1.0.0-py2.py3-none-any.whl
```

**Step 11.** Change directories back to `src` and serve your imported artifact as a background process using `waitress`. 
```bash
cd src/
waitress-serve simplellm:app &
```

**Step 12.** Test your imported artifact now that it's being served by `waitress`. Pay attention to the change in port number. 
```bash
curl -G --data-urlencode message="what is 1 + 1?" http://localhost:8080/api
```

**Step 13.** Use the [provided Dockerfile example](task-01/docker/Dockerfile) to containerize the application. 

**Step 14.** Build a container image using the Dockerfile you just created. If you have issues running `docker` as a non-privileged user, reboot your virtual machine and try again. Also, don't forget, your working directory should be `~/llmservice-handout/worker/`.
```bash
docker build -t griffin/simplellm:v1.0.0 -f docker/Dockerfile .
```

**Step 15.** Create a container using the image you just created.
```bash
docker run --name demo -d -p 8080:8080 griffin/simplellm:v1.0.0
```

**Step 16.** Test your application now that it's been containerized.
```bash
curl -G --data-urlencode message="what is 1 + 1?" http://localhost:8080/api
```

**Step 17.** Stop the container and remove it. 
```bash
docker container stop demo
docker container rm demo
```

**Step 18.** In a separate terminal on your personal computer, change directories to the `setup` folder used in the [Setup](#setup) section, and run the Terraform commands below. 
```bash
export ACR_REGISTRY_ID=$(terraform -chdir=terraform output -raw acr_registry_id)
export SERVICE_PRINCIPAL_NAME=$(terraform -chdir=terraform output -raw service_principal_username)
export SERVICE_PRINCIPAL_PASSWORD=$(terraform -chdir=terraform output -raw service_principal_password)
```

**Step 19.** Run the commands below and copy the output to memory. 
```bash
echo "export ACR_REGISTRY_ID=${ACR_REGISTRY_ID}" && echo "export SERVICE_PRINCIPAL_NAME=${SERVICE_PRINCIPAL_NAME}" && echo "export SERVICE_PRINCIPAL_PASSWORD=${SERVICE_PRINCIPAL_PASSWORD}"
```

**Step 20.** Go back to your virtual machine and paste the output from the previous step. 
```bash
export ACR_REGISTRY_ID=amazingant.azurecr.io
export SERVICE_PRINCIPAL_NAME=d875c1b5-cb6b-4492-bb4b-2364ede53059
export SERVICE_PRINCIPAL_PASSWORD=ZoL8Q~6PVUpPS3-IwKj3qww93k5GMpG9LEK7bbM9
```

**Step 21.** Login to Azure, set your subscription, and login to the Azure Container Registry created automatically in the [Setup](#setup) section.
```bash
az login --use-device-code
az account set --subscription "AI2C Subscription 3"
az acr login -n $ACR_REGISTRY_ID
```

**Step 22.** Tag and push the container image you created earlier. 
```bash
docker image tag griffin/simplellm:v1.0.0 $ACR_REGISTRY_ID/worker:v1
docker image push $ACR_REGISTRY_ID/worker:v1
```

**Step 23.** Deploy a container using the image you just pushed to your Azure Container Registry (use your existing resource group).
```bash
RESOURCE_GROUP="project2task1"
ACI_NAME=$(echo ${ACR_REGISTRY_ID} | cut -d. -f1)
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $ACI_NAME \
  --image $ACR_REGISTRY_ID/worker:v1 \
  --cpu 2 \
  --memory 2 \
  --registry-login-server $ACR_REGISTRY_ID \
  --registry-username $SERVICE_PRINCIPAL_NAME \
  --registry-password $SERVICE_PRINCIPAL_PASSWORD \
  --ip-address Public \
  --dns-name-label $ACI_NAME \
  --ports 8080
```

**Step 24.** Test your application now that it's been containerized and deployed as an Azure Container Instance (make sure to use the correct region). 
```bash
curl http://${ACI_NAME}.eastus2.azurecontainer.io:8080/healthcheck
```

## Task 2
**Step 1.** From the virtual machine, create a Azure Kubernetes Service (AKS) cluster.
```bash
az aks create \
  --resource-group project2task1 \
  --name project2cluster \
  --enable-managed-identity \
  --node-count 3 --generate-ssh-keys
```

**Step 2.** Attach your Azure Container Registry to your AKS cluster. 
```bash
az aks update \
  --resource-group project2task1 \
  --name project2cluster \
  --attach-acr $ACI_NAME
```

**Step 3.** Save your AKS cluster's credentials to a file so `kubectl` can use them.
```bash
az aks get-credentials \
  --resource-group project2task1 \
  --name project2cluster
```

**Step 4.** Verify all nodes in your AKS cluster are working. 
```bash
kubectl -n default get nodes
```

Your output should be similar to below. 
```bash
NAME                                STATUS   ROLES   AGE     VERSION
aks-nodepool1-19130009-vmss000000   Ready    agent   5m43s   v1.27.7
aks-nodepool1-19130009-vmss000001   Ready    agent   5m32s   v1.27.7
aks-nodepool1-19130009-vmss000002   Ready    agent   5m49s   v1.27.7
```

**Step 5.** Enable the "Vertical Pod Autoscaler" feature on your AKS pod.
```bash
az aks update \
  --resource-group project2task1 \
  --name project2cluster \
  --enable-vpa
```

**Step 6.** Create a folder called `k8s` under `~/llmservice-handout/worker/` and then change directories to it. 
```bash
mkdir ~/llmservice-handout/worker/k8s/
cd ~/llmservice-handout/worker/k8s/
```

**Step 7.** Create a `deployment.yaml` file using the [provided example](task-02/kubernetes/deployment.yaml).

**Step 8.** Create a `service.yaml` file using the [provided example](task-02/kubernetes/service.yaml).

**Step 9.** Create a `vpa.yaml` file using the [provided example](task-02/kubernetes/vpa.yaml).

**Step 10.** Deploy the `simplellm` service defined by the files you just created. 
```bash
kubectl -n default apply -f .
```

**Step 11.** Verify all the pods you just deployed onto your AKS cluster are working. 
```bash
kubectl -n default get pods
```

Your output should be similar to below. 
```bash
NAME                                   READY   STATUS    RESTARTS   AGE
simplellm-deployment-9b7587974-rpd8g   1/1     Running   0          2m36s
simplellm-deployment-9b7587974-stl5h   1/1     Running   0          2m33s
simplellm-deployment-9b7587974-zp7qf   1/1     Running   0          2m35s
```

**Step 12.** Create a new `kubectl` namespace called `goldilocks`.
```bash
kubectl create namespace goldilocks
```

**Step 13.** In the `goldilocks` namespace you just created, install Goldilocks via Helm. 
```bash
helm install goldilocks --namespace goldilocks fairwinds-stable/goldilocks
```

**Step 14.** Enable Goldilocks in the `goldilocks` namespace.
```bash
kubectl label ns default goldilocks.fairwinds.com/enabled=true
```

**Step 15.** Expose the "Goldilocks dashboard" object created earlier by Helm.
```bash
kubectl -n goldilocks expose deployment goldilocks-dashboard --type=LoadBalancer --name=goldilocks-service
```

**Step 16.** Determine the external IP address of the `goldilocks-service` object created in the previous step.
```bash
kubectl -n goldilocks get svc
```

Your output should be similar to below. 
```bash
NAME                   TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)          AGE
goldilocks-dashboard   ClusterIP      10.0.122.52   <none>         80/TCP           22m
goldilocks-service     LoadBalancer   10.0.23.232   4.152.73.108   8080:30513/TCP   17m
```

**Step 17.** Verify the "Goldilocks dashboard" is accessible on TCP port 8080 from its external public IP address.

**Step 18.** Determine the external IP address of the `simplellm-service` object created in step 10.
```bash
kubectl -n default get svc
```

Your output should be similar to below. 
```bash
NAME                TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
kubernetes          ClusterIP      10.0.0.1       <none>          443/TCP        18h
simplellm-service   LoadBalancer   10.0.169.146   52.232.230.217  80:30549/TCP   17h
```

**Step 19.** Change directories to `~/llmservice-handout/worker/loadtester/` and load test your application using `locust`. After 20 minutes, stop `locust`.
```bash
cd ~/llmservice-handout/worker/loadtester/
locust --headless -H http://52.232.230.217
```

**Step 20.** Open "Goldilocks" to see what recommendations it has for your resource requests now that it's seen your deployment under load.

![goldilocks-01.png](task-02/goldilocks.png)

**Step 21.** Change directories to `~/llmservice-handout/worker/k8s/`, update your `vpa.yaml` file with new values, and patch your `simplellm-service` object.
```bash
cd ~/llmservice-handout/worker/k8s/
vim vpa.yaml
kubectl -n default apply -f vpa.yaml
```

**Step 22.** Make sure to the old pods are terminated and the new pods are `running` before testing the change you made. 
```bash
kubectl get pods
```

**Step 23.** Test your application now that it's AKS cluster has been modified.
```bash
curl -G --data-urlencode message="what is 1 + 1?" http://52.232.230.217/api
```

**Misc.** I found myself repeating these commands over and over again from the `~/llmservice-handout/` directory when submitting (as I changed the resource values).
```bash
cd ~/llmservice-handout/
vim worker/k8s/vpa.yaml
kubectl -n default apply -f worker/k8s/vpa.yaml
kubectl get vpa
kubectl describe vpa simplellm-vpa
kubectl get pods
curl http://52.232.230.217/healthcheck
curl -G --data-urlencode message="what is 1 + 1?" http://52.232.230.217/api
./submitter task2
```

## Task 3
**Step 1.** Delete the Vertical Pod Autoscaler object from your cluster. 
```bash
kubectl delete vpa/
```

**Step 2.** Change directories to `~/llmservice-handout/worker/k8s/` and delete the Vertical Pod Autoscaler's manifest file (`vpa.yaml`). 
```bash
cd ~/llmservice-handout/worker/k8s/
rm vpa.yaml
```

**Step 3.** Update your `deployment.yaml` file (using the [provided example](task-03/kubernetes/deployment.yaml)) so it has a `startupProbe` and `readinessProbe`.

**Step 4.** Create a `hpa.yaml` file using the [provided example](task-03/kubernetes/hpa.yaml).

**Step 5.** From the `~/llmservice-handout/worker/k8s/` directory, deploy the changes you made. 
```bash
kubectl -n default apply -f .
```

**Step 6.** Determine the external IP address of your AKS cluster's load balancer.
```bash
kubectl get svc
```

Your output should be similar to below. 
```bash
NAME                TYPE           CLUSTER-IP    EXTERNAL-IP      PORT(S)        AGE
kubernetes          ClusterIP      10.0.0.1      <none>           443/TCP        38h
simplellm-service   LoadBalancer   10.0.112.34   52.232.230.217   80:30416/TCP   12h
```

**Step 7.** Change directories to `~/llmservice-handout/worker/loadtester/`
```bash
cd ~/llmservice-handout/worker/loadtester/
```

**Step 8.** Using `locust`, run a load test against your load balancer's external IP address. Submit your work once at least 90 queries pass.
```bash
locust --headless -H http://52.232.230.217 -u 5 -r 0.008 
```

## Task 4
**Step 1.** Text goes here.