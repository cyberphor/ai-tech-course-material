# Cloud Native: Observability, Reliability, and Analytics
The purpose of this project is to add observability to a system consisting of the following elements: a Nginx Gateway Fabric service (i.e., load balancer), a KrakenD service (i.e., API manager), a MariaDB Operator service, a Django-based authentication service, and a FastAPI-based LLM service. It specifically involves (1) deploying Prometheus and (2) using OpenTelemetry's Operator and Python SDK to generate custom metrics. 
* [References](#references)
* [Notes](#notes)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)

## References
If I find any helpful references, I will put them here. 
* [Edited lru_cache decorator of pfsspy.Output.bg to conserve memory](https://github.com/dstansby/pfsspy/pull/150)
* [OpenTelemetry: Collector | Configuration](https://opentelemetry.io/docs/collector/configuration/)

## Notes
If I take any additional notes, I will put them here. 

**Adding Telemetry Functions**  
Don't add telemetry functions to a system if it will impact performance. 

**Kubernetes Operator** 
Operators create, configure, and manage applications within your cluster in a Kubernetes-native way. 

**OpenTelemetry**  
OpenTelemetry is a library used to add telemetry functions to microservices. 

**OpenTelemetry Collector**  
An OpenTelemetry Collector configuration includes four main sections:
* Receivers: collects telemetry from one or more sources
* Processors: takes data collected by the receivers and transforms it before sending it to the exporters
* Exporters: sends data to one or more backends
* Pipeline: join two pipelines together (e.g., connect a receiver to an exporter)

**OpenTelemetry Instrumentation** 
An Instrumentation resource configures the OpenTelemetry Operator to add an init container to deployments with specific attributes. The init container will identify what type of application server running and then add the correct instrumentation for it. 

```mermaid
flowchart LR
  subgraph PrometheusNamespace["Prometheus Namespace"]
    PrometheusOperator["Prometheus\nOperator"]
    Prometheus["Prometheus"]
  end
  subgraph DefaultNamespace["Default Namespace"]
    OpenTelemetryOperator["OpenTelemetry\nOperator"]
    subgraph OpenTelemetryCollector["OpenTelemetry\nCollector"]
      Port4318["TCP Port 4318"]
      Port9464["TCP Port 9464"]
    end
    OpenTelemetryInstrumentation["OpenTelemetry\nInstrumentation"]
    LLMService["LLM\nService"]
    AuthenticationService["Authentication\nService"]
    DatabaseService["Database\nService"]
    LoadBalancer["Load Balancer"]
  end
  Developer["Developer"]

  PrometheusOperator --"manages" --> Prometheus
  OpenTelemetryOperator -- "manages" --> OpenTelemetryCollector
  OpenTelemetryOperator -- "manages" --> OpenTelemetryInstrumentation
  
  OpenTelemetryInstrumentation -- "adds telemetry functions to" --> LLMService
  LLMService -- "sends metrics to" --> Port4318
  
  OpenTelemetryInstrumentation -- "adds telemetry functions to" --> AuthenticationService 
  AuthenticationService -- "sends metrics to" --> Port4318

  OpenTelemetryInstrumentation -- "adds telemetry functions to" -->  DatabaseService
  DatabaseService -- "sends metrics to" --> Port4318
  
  OpenTelemetryInstrumentation -- "adds telemetry functions to" -->  LoadBalancer
  LoadBalancer -- "sends metrics to" --> Port4318
  Prometheus --"collects metrics from" --> Port9464

  Developer -- "queries" --> Prometheus
```

**Customize a Helm Chart**  
If you want to customize a Helm chart, create a `values.yaml` file that includes the options you want. You can explore what options are available by running something like below. I'm assuming you will need the Helm chart repo installed first. 
```bash
helm show values prometheus-community/kube-prometheus-stack
```

## Setup
The following steps assume (1) you're using a Linux-based environment (GitHub Codespaces, Azure Shell, Windows Subsystem for Linux, or a Linux virtual machine), (2) you've installed the software required for this project (i.e., Python, Poetry, Docker, Kubernetes, Helm, and Azure CLI), (3) you've forked this repository, (4) you've downloaded this repository, and (5) you're running commands in this section from the `vic-code/cloud-native/unit-06/setup/` directory. FYI, I accepted this week's GitHub Classroom assignment and copied the contents of the `src` folder from the provided repository to my `setup` folder. I also moved the `submitter` program to the root of this week's project folder (i.e., `vic-code/cloud-native/unit-06/`). 

### Subtask 01: Create a Kubernetes Cluster in Azure
**Step 1.** Define your environment variables. Again, I usually save my environment variables in a file called something like `.env` and run `source .env` as needed. This makes it easy to pick up where I left off after leaving my workspace for an extended period of time. If you didn't know, the `source` command reads and executes shell commands from the file you provide it.   
```bash
export LOCATION="eastus"
export RESOURCE_GROUP_NAME="project6"
export ACR_NAME="project6cyberphorwashere"
export ACR_SKU="Basic"
export AKS_CLUSTER_NAME="project6cluster"
export AKS_NODE_COUNT=2
```

**Step 2.** Login to Azure using the CLI. 
```bash
az login --use-device-code
```

**Step 3.** Create a resource group.
```bash
az group create --name "${RESOURCE_GROUP_NAME}" --location eastus
```

**Step 4.** Create an container registry. 
```bash
az acr create --resource-group "${RESOURCE_GROUP_NAME}" --name "${ACR_NAME}" --sku "${ACR_SKU}"
```

**Step 6.** Login to your container registry.
```bash
az acr login --name "${ACR_NAME}"
```

**Step 7.** Create a Kubernetes cluster. 
```bash
az aks create --resource-group "${RESOURCE_GROUP_NAME}" --name "${AKS_CLUSTER_NAME}" --enable-managed-identity --node-count "${AKS_NODE_COUNT}" --generate-ssh-keys
```

**Step 8.** Attach your Azure Container Registry to your Kubernetes cluster. Do not skip this step. Otherwise, you'll get `ErrImagePull`, `Failed to pull image`, and `401 Unauthorized` errors.
```bash
az aks update --resource-group "${RESOURCE_GROUP_NAME}" --name "${AKS_CLUSTER_NAME}" --attach-acr "${ACR_NAME}"
```

**Step 9.** Download credentials from your Kubernetes cluster for Kubectl to use.
```bash
az aks get-credentials --resource-group "${RESOURCE_GROUP_NAME}" --name "${AKS_CLUSTER_NAME}"
```

### Subtask 02: Deploy a Nginx Gateway Fabric Service
**Step 1.** Create Custom Resource Definition (CRD) objects for a Nginx Gateway Fabric service in your Kubernetes cluster.
```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

**Step 2.** Create a namespace called `nginx-gateway` in your Kubernetes cluster. 
```bash
kubectl create namespace nginx-gateway
```

**Step 3.** Create a Nginx Gateway Fabric service under the `nginx-gateway` namespace in your Kubernetes cluster. FYI, in addition to creating a Service object in the `nginx-gateway` namespace, this command sentence will also create two identical Pod objects. They both contain two containers: (1) a load balancer for routing HTTP requests to applications within your cluster and (2) a controller to interact with the Kubernetes API and monitor objects within your cluster. 
```bash
helm install ngf oci://ghcr.io/nginxinc/charts/nginx-gateway-fabric -n nginx-gateway
```

**Step 4.** Confirm your Nginx Gateway Fabric service is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods -n nginx-gateway
```

**Step 5.** Configure your Nginx Gateway Fabric service using the provided YAML files. FYI, these YAML files define HTTP routes (i.e., `/v1/logintoken` and `/v1/llm`) for your load balancer to use when directing traffic (the HTTPRoute objects will be created in the default namespace). 
```bash
kubectl apply -f gateway/
```

### Subtask 03: Deploy a KrakenD Service
**Step 1.** Create a ConfigMap object in your default namespace called `krakend-cfg` for the KrakenD service you're about to add to your Kubernetes cluster. Again, the purpose of KrakenD is to manage APIs. It's the component in your system that requires users to authenticate with your Django-based authentication service before granting access to your FastAPI-based LLM service. 
```bash
kubectl create configmap krakend-cfg --from-file=./krakend/krakend.json
```

**Step 2.** Create an Secret object (of the Opaque type) in your default namespace called `krakendjwt` using the provided `publickey.json` file. FYI, this file was created using data from a provided key pair. If you wanted to deploy a KrakenD service in production, you'd need to make your own pair of keys and `publickey.json` file. 
```bash
kubectl create secret generic krakendjwt --from-file=./krakend/publickey.json
```

**Step 3.** Create a KrakenD service in the default namespace of your Kubernetes cluster using the provided YAML files.
```bash
kubectl apply -f krakend/krakend-deployment.yaml 
```

**Step 4.** Confirm your KrakenD service is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods 
```

### Subtask 04: Deploy a MariaDB Operator
**Step 1.** Create an Secret object (of the Opaque type) in your default namespace called `loginkeys` using the provided `private_key.pem` and `public_key.pem` file.
```bash
kubectl create secret generic loginkeys --from-file=./django/private_key.pem --from-file=./django/public_key.pem
```

**Step 2.** Add the Helm repository for the MariaDB Operator to your local list of known Helm repositories.
```bash
helm repo add mariadb-operator https://mariadb-operator.github.io/mariadb-operator
```

**Step 3.** Deploy a MariaDB Operator to the default namespace in your cluster. 
```bash
helm install mariadb-operator mariadb-operator/mariadb-operator
```

**Step 4.** Configure your MariaDB Operator using the provided YAML files. 
```bash
kubectl apply -f django/mariak8s/
```

**Step 3.** Confirm your MariaDB Operator is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods 
```

### Subtask 05: Deploy a Django-Based Authentication Service
**Step 1.** Build and tag a container image for your Django-based authentication service using the provided Dockerfile. Then, push the image to your container registry. Specifying `--platform linux/amd64` forces your local Docker host to build an image using the same CPU architecture as the Docker hosts that will be used in Azure. 
```bash
docker build --push --tag ${ACR_NAME}.azurecr.io/login:latest --platform linux/amd64 -f django/docker/Dockerfile src/django/
```

**Step 2.** Update the `deployment.yaml` file provided for your Django-based authentication service so it uses the correct container registry. 
```bash
vim django/k8s/deployment.yaml
```

**Step 3.** Deploy your Django-based authentication service in the default namespace of your Kubernetes cluster using the provided YAML files.
```bash
kubectl apply -f django/k8s/
```

**Step 4.** Confirm your Django-based authentication service (`login...`) is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods 
```

### Subtask 06: Deploy a FastAPI-Based LLM Service
**Step 1.** Build and tag a container image for your FastAPI-based LLM service using the provided Dockerfile. Then, push the image to your container registry.  
```bash
docker build --push --tag ${ACR_NAME}.azurecr.io/fastapillm:latest --platform linux/amd64 -f fastapi-p4/docker/Dockerfile fastapi-p4/
```

**Step 2.** Update the `deployment.yaml` file provided for your FastAPI-based LLM service so it uses the correct container registry. 
```bash
vim fastapi-p4/k8s/deployment.yaml
```

**Step 3.** Deploy your FastAPI-based LLM as a service in the default namespace of your Kubernetes cluster using the provided YAML files.
```bash
kubectl apply -f fastapi-p4/k8s
```

**Step 4.** Confirm your FastAPI-based LLM service (`llmserver...`) is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods 
```

### Subtask 07: Test the System
**Step 1.** Identify the IP address of the load balancer in your `nginx-gateway` namespace.
```bash
kubectl get gateway
```

**Step 2.** Request an OAuth token from your Django-based authentication service using the credentials an existing account. 
```bash
curl -H 'Content-Type: application/json' -d '{"username":"admin", "password":"asdasd" }' -X POST http://4.156.66.247/v1/logintoken
```

You should get output similar to below. 
```
{"access":"eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNjEwMTg0LCJpYXQiOjE3MTI1OTkzODQsImp0aSI6IjE2YjQ3NzU5MmMyYzQyZjViMjhjNmIxNTMzMGY0NGYxIiwidXNlcl9pZCI6MX0.ekRNR0EYybCDGkhLJ-GWJEvPwOiTqWDcpIH6P8wx-tRpkcW8d6STFrDHD9PrzgfORRsTNKCUvFbkqZ0EJFX45VCAdnYQkMlEeWWFIIQYxYJ3pG7_ckPxW44x9yreVPOzlMI27AfonK2NJtwnk_k3nXJEFI9R3nSAMxb485Zx7j6XFMSXwQX7BqxjkyAO3vKFFHOI56QtCM_6z1BaPtqdi0oc57g6gNXMK-DIbNcs_Jt-B8n0PAFiR42jn0hTz6bfyJVnCKtg2wyMNMlaHlelBzka4GqfCTg9MJPADHwXlUU7Nh6xw2WHaCLqK5FrwGk0nl1drLtKz-HWz2XqKIAgIA","refresh":"eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMjY5MTg2NCwiaWF0IjoxNzEyNjA1NDY0LCJqdGkiOiJlYTk1ZThiNDdiYjU0YTg0YTc2MmU1YzZlMjNjMGQ4MSIsInVzZXJfaWQiOjF9.qXXpZD_xBdJk6ewSLazwdGyc3hdnx217jvkqb7WDDMxzQenz5a8JgQxtLvCQVI2H58qxz05gfRBpz-oX12Mx5Ef1Dozzs3p7uMmoptjjSTpi9KRQs1v0XNkELSWD5TPbTNu3Yz91qi2CGSnPoAP_om1052Q-yTSomUhVY3t_GbPOGucVk93cs7r3HFK3_khxaJAfRnRnKY6dXp77vwTkRStgI5AGvocPWSuEuwEr_MzrMvWKDM6gy521kAFjVkDFOs_zN8OCt2l8-V2hHWF48udZ2rxyP5_eO1P8glj90DM4LbsMUEPilvJ-vhLnpxso0fCJufmlj4XSaGLdmaX5qA"}%     
```

**Step 3.** Use the OAuth token to access your FastAPI-based LLM service. 
```bash
curl -D - -H  "Authorization: BEARER eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNjEwMTg0LCJpYXQiOjE3MTI1OTkzODQsImp0aSI6IjE2YjQ3NzU5MmMyYzQyZjViMjhjNmIxNTMzMGY0NGYxIiwidXNlcl9pZCI6MX0.ekRNR0EYybCDGkhLJ-GWJEvPwOiTqWDcpIH6P8wx-tRpkcW8d6STFrDHD9PrzgfORRsTNKCUvFbkqZ0EJFX45VCAdnYQkMlEeWWFIIQYxYJ3pG7_ckPxW44x9yreVPOzlMI27AfonK2NJtwnk_k3nXJEFI9R3nSAMxb485Zx7j6XFMSXwQX7BqxjkyAO3vKFFHOI56QtCM_6z1BaPtqdi0oc57g6gNXMK-DIbNcs_Jt-B8n0PAFiR42jn0hTz6bfyJVnCKtg2wyMNMlaHlelBzka4GqfCTg9MJPADHwXlUU7Nh6xw2WHaCLqK5FrwGk0nl1drLtKz-HWz2XqKIAgIA" "http://4.156.66.247/v1/llm?message=hi"
```

You should get output similar to below.
```
HTTP/1.1 200 OK
Server: nginx/1.25.4
Date: Mon, 08 Apr 2024 18:06:22 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 756
Connection: keep-alive
X-Krakend: Version 2.5.1
X-Krakend-Completed: true

{"choices":[{"finish_reason":"length","index":0,"logprobs":null,"text":"\n     Hey there! I'm a friendly assistant who loves to help others. My name is [Your Name], and I've been working as an online assistant since [Date]. I've been trained in various skills, including [Skill 1], [Skill 2], and [Skill 3]. With my experience, I can provide assistance in [Skill 4] with ease. I'm always eager to learn new skills, so if you have any requests or challenges, feel free to reach out to me. In my spare time, I enjoy reading, cooking, and sp"}],"created":1712599502,"id":"cmpl-ecd39d5e-d94f-40d7-aed2-49ae0308f55b","model":"tinyllama-1.1b-chat-v1.0.Q2_K.gguf","object":"text_completion","usage":{"completion_tokens":128,"prompt_tokens":37,"total_tokens":165}}% 
```

## Task 01
### Subtask 01: Deploy a Prometheus Operator
**Step 1.** Create a namespace called `prometheus` in your Kubernetes cluster. 
```bash
kubectl create namespace prometheus
```

**Step 1.** Add the Helm repository for the Prometheus Operator to your local list of known Helm repositories.
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

**Step 3.** Deploy a Prometheus Operator to the `prometheus` namespace in your cluster. 
```bash
helm install prometheus prometheus-community/kube-prometheus-stack -n prometheus
```

**Step 4.** Confirm your Prometheus Operator is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods -n prometheus
```

### Subtask 02: Load Test the System Using Locust
**Step 1.** Identify the IP address of the load balancer in your `nginx-gateway` namespace.
```bash
kubectl get gateway
```

**Step 2.** Request an OAuth token from your Django-based authentication service using the credentials an existing account and save it as an environment variable. 
```bash
export TOKEN=$(curl -H 'Content-Type: application/json' -d '{"username":"admin", "password":"asdasd" }' -X POST http://4.156.66.247/v1/logintoken)
```

**Step 3.** Change directories from `setup/` to a child folder in `setup/` called `locustest/`. 
```bash
cd locustest/
```

**Step 3.** Using your favorite text-editor, create and open a file called `poetry.toml` in the `locustest/` folder. 
```bash
vim poetry.toml
```

**Step 5.** Add the content below to it.
```toml
[virtualenvs]
in-project = true
path = ".venv"
```

**Step 6.** Install the provided Python project using Poetry.
```bash
poetry install
```

**Step 7.** Use the OAuth token and Locust to load test your FastAPI-based service. The purpose of this step is to popluate Prometheus with telemetry data. Stop the load test after 10 minutes. 
```bash
poetry run locust -f locusttest/locustfile.py  --headless --host http://4.156.66.247 -u 1 --auth-tok $TOKEN -u 3
``` 

**Step 8.** In a separate terminal, forward traffic received on port 9090 on your local machine to the pod hosting Prometheus's dashboards.  
```bash
kubectl port-forward -n prometheus prometheus-prometheus-kube-prometheus-prometheus-0 9090
```

**Step 9.** Open Prometheus's dashboards using a web browser (URL: `http://localhost:9090`). 

**Step 10.** Click the "Graph" tab. 

**Step 11.** In the Expression text-box, enter `authenticated_user_requests` as a PromQL query and then, click "Execute." Review the data shown. 

**Step 12.** In the Expression text-box, enter `node_memory_Active_bytes` as a PromQL query and then, click "Execute." Review the data shown. The purpose of this step is to draw attention to the slow increase in memory usage despite the lack of user activity. 

**Step 13.** In the Expression text-box, enter `node_memory_Active_bytes/node_memory_MemTotal_bytes*100` as a PromQL query and then, click "Execute." Review the data shown. The purpose of this step is to compute the percentage of memory used by your system. It's specifically dividing active memory usage by total memory usage. 

**Step 14.** In the Expression text-box, enter `node_namespace_pod_container:container_memory_working_set_bytes` as a PromQL query and then, click "Execute." Review the data shown. The purpose of this step is to demonstrate looking at metrics by container. It also draws attention to a potential memory leak. 

**Step 15.** In the Expression text-box, enter `node_namespace_pod_container:container_memory_working_set_bytes{pod=~"llmserver.*"}` as a PromQL query and then, click "Execute." The purpose of this step is to demonstrate how to look at metrics relating to one container.  

**Step 16.** Change directories from `locustest/` to the `task-01/` folder directly under `unit-06`. 
```bash
cd ../../task-01/
```

### Subtask 03: Fix the Memory Leak
**Step 1.** Build and tag a new container image for your FastAPI-based LLM service using the provided Dockerfile and *updated code*. Then, push the image to your container registry. NOTE: I changed line 47 in `task-01/fastapi-p4/llmserver.py` after reading this: [Edited lru_cache decorator of pfsspy.Output.bg to conserve memory](https://github.com/dstansby/pfsspy/pull/150). 
```bash
docker build --no-cache --push --tag ${ACR_NAME}.azurecr.io/fastapillm:latest --platform linux/amd64 -f fastapi-p4/docker/Dockerfile fastapi-p4/
```

**Step 2.** Update the `deployment.yaml` file provided in `task-01/` for your FastAPI-based LLM service so it uses the correct container registry. 
```bash
vim fastapi-p4/k8s/deployment.yaml
```

**Step 3.** Delete the resources previously created for your FastAPI-based LLM service. 
```bash
kubectl delete -f fastapi-p4/k8s
```

**Step 4.** Re-deploy your FastAPI-based LLM as a service in the default namespace of your Kubernetes cluster using the provided YAML files in the `task-01/` folder. They're not different from the ones used in the `setup/` folder. I just felt like it would be easier to make a copy and compare changes between tasks. 
```bash
kubectl apply -f fastapi-p4/k8s
```

**Step 5.** Confirm your updated FastAPI-based LLM service is running again by checking the status of the pods created in the previous step. 
```bash
kubectl get pods 
```

## Task 02
The purpose of this task is to add telemetry functions to our system and send telemetry data to Prometheus using the OpenTelemetry Operator. 

### Subtask 01: LLM Service Instrumentation
**Step 1.** Change directories from `task-01/` under `unit-06` to `task-02/`. 
```bash
cd ../task-02/
```

**Step 2.** Deploy a Certificate Manager within your cluster. 
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.4/cert-manager.yaml
```

**Step 3.** Deploy an OpenTelemetry Operator to the `opentelemetry-operator-system` namespace in your cluster.
```bash
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```

**Step 4.** Confirm your OpenTelemetry Operator is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods -n opentelemetry-operator-system
```

**Step 5.** Apply [the provided Kubernetes manifest file](task-02/OpenTelemetry.yaml). It deploys an OpenTelemetry Collector resource and Instrumentation resource.  
```bash
kubectl apply -f OpenTelemetry.yaml
```

**Step 6.** Confirm your OpenTelemetry Collector is running by checking the status of the pods created in the previous step. 
```bash
kubectl get pods 
```

**Step 7.** Confirm your OpenTelemetry Instrumentation resource is working by checking the status of the pods created in the previous step. 
```bash
kubectl get instrumentation
```

You should get output similar to below. 
```
NAME                       AGE     ENDPOINT                         SAMPLER                    SAMPLER ARG
simplest-instrumentation   2m10s   http://simplest-collector:4318   parentbased_traceidratio   1
```

**Step 8.** Open and edit the Kubernetes manifest file for your LLM service. You need need to *annotation* so your Instrumentation resource knows whether to add telemetry functions to the LLM service or not. If you use the one I have in my `task-02/` folder, make sure the container registry mentioned is the one you made. FYI, I just copied the YAML files from the [Setup](#setup) section and put them into one file. Then, I added the line mentioned in the instructions. 
```bash
vim LLM.yaml
```

**Step 9.** Apply the Kubernetes manifest file you just edited.  
```bash
kubectl apply -f LLM.yaml
```

**Step 10.** Verify an init container has been added to your LLM pod (use the pod name specific to your cluster). Again, adding the annotation tells the Instrumentation resource to add an init container to whatever pod deployment you specify. The init container is what adds telemetry functions to your service of interest (e.g., LLM service, authentication service, database service, or load balancer). 
```bash
kubectl describe pod llmserver-f68ccb8b8-ljtj7 | grep -A2 "Init Containers" 
```

If you used the exact command above, you should get output similar to below. If not, just scroll the output until you see the `Init Containers` section. Then, confirm the `opentelemetry` container was added to your LLM pod. 
```
Init Containers:
  opentelemetry-auto-instrumentation-python:
    Container ID:  containerd://516809bfa353525446692261b011509c89363ffef74fe5fc757e53aaa707236b
```

**Step 11.** Confirm the OpenTelemetry Collector is recieving metrics from your LLM service by checking the logs on the `simplest-collector-0` pod. 
```bash
kubectl logs simplest-collector-0
```

**Step 12.** Uninstall Prometheus. 
```bash
helm uninstall prometheus -n prometheus
```

**Step 13.** Re-install Prometheus but include [the provided `values.yaml` file I created](task-02/values.yaml). If you get an error saying `INSTALLATION FAILED: repo prometheus-community not found`, try re-adding the Helm repo for it (i.e., `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`). 
```bash
helm install -f ./values.yaml prometheus prometheus-community/kube-prometheus-stack -n prometheus 
```

**Step 14.** In a separate terminal, forward traffic received on port 9090 on your local machine to the pod hosting Prometheus's dashboards.  
```bash
kubectl port-forward -n prometheus prometheus-prometheus-kube-prometheus-prometheus-0 9090
```

**Step 15.** Confirm Prometheus is able to get metrics from your LLM service by entering the PromQL queries below into the Prometheus dashboard (one at a time - make sure there's something returned). 
```
system_thread_count{exported_job="llmserver"}
process_runtime_cpython_context_switches_total
```