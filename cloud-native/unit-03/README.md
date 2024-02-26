# Cloud Native: API Gateway
* [References](#references)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)

## References
If I find any helpful references, I will put them here. 
* [GitHub - cyberphor: virtualization/containers/kubernetes](https://github.com/cyberphor/knowledge-base/tree/main/virtualization/containers/kubernetes)
* [Kubernetes Gateway API: Overview](https://gateway-api.sigs.k8s.io/)
* [Kubernetes Gateway API: Deploying a Simple Gateway](https://gateway-api.sigs.k8s.io/guides/simple-gateway/)
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

If you were able to complete the steps above, you've created the object in the image below. Also, FYSA, your Gateway API is in its own namespace, not the default one where your objects will live. If you want to check the status of it, run this command: `kubectl -n nginx-gateway get pods`. 
![nginx-gateway-fabric.png](setup/nginx-gateway-fabric.png)

## Task 01
The following instructions cover creating the objects in the image below in the ordered specified. The object with the green checkmark was created in the previous section. Also, the objects shown are logically within the NGF pod circled above. 

![gateway-api.png](setup/gateway-api.png)

**Step 1.** Using your favorite text-editor and [the provided example](task-01/gateway.yaml), create a Kubernetes manifest for a Gateway object. If you're curious about how I determined the `GatewayClass` name, I ran the command `kubectl get gatewayclass -o yaml` and looked at the `name` field.  
```bash
vim gateway.yaml
```

**Step 2.** Apply the Kubernetes manifest file you just created to your Kubernetes cluster. The command below is meant to be ran in the same directory as your `gateway.yaml` file.
```bash
kubectl apply -f gateway.yaml
```

**Step 3.** Update [the files provided to deploy a containerized Large Language Model (LLM)](task-01/llm-service/) so they use the ACR you created earier. For example, when I downloaded the files they originally had `p3acr.azurecr.io` from the GitHub repository created in the first step of the [Setup](#setup) section. I updated them to use `cyberphorwashere.azurecr.io` instead. 

**Step 4.** Change directories to the files you just updated.  
```bash
cd task-01/llm-service/
```

**Step 5.** Run the `wheel` target in [the provided Makefile](task-01/llm-service/Makefile) using the command below. This step creates the Python wheels the LLM needs to work. 
```bash
make wheel
```

**Step 6.** Run the `push` target in the same Makefile mentioned above using the command below. This step builds, tags, and pushes the containerized LLM (along with the Python wheels you just created) to your ACR. This is why you had to specify the correct name for your ACR. 
```bash
make push
```

**Step 7.** Deploy the containerized LLM mentioned above using [the provided Kubernetes manifest files](task-01/llm-service/k8s/) and the command below. If you're following along with the instructions in Sail(), this step is implied at the end Task 1, Subtask 1 (my instructions skip the "Interim Validation" part for Subtask 1). 
```bash
kubectl apply -f k8s/
```

**Step 8.** Using your favorite text-editor and [the provided example](task-01/httproute.yaml), create a Kubernetes manifest for a HTTPRoute object. The provided example configures Kubernetes to send everything recieved on TCP port 80 (with the prefix `/api`) of the Gateway object to the `llmservice` pod. 
```bash
vim httproute.yaml
```

**Step 9.** Apply the Kubernetes manifest file you just created to your Kubernetes cluster. The command below is meant to be ran in the same directory as your `httproute.yaml` file.
```bash
kubectl apply -f httproute.yaml
```

**Step 11.** Take note of your Gateway API's IP address.
```bash
kubectl get gateway 
```

Your output should be similar to below.
```bash
NAME              CLASS   ADDRESS        PROGRAMMED   AGE
project3gateway   nginx   4.156.73.214   True         98m
```

**Step 10.** Verify your Gateway API routes traffic to the containerized LLM you deployed. If you're following along with the instructions in Sail(), this step is at the end of Task 1, Subtask 2. 
```bash
curl http://4.156.73.214/api?message=hi
```

Your output should be similar to below. 
```json
{"choices":[{"finish_reason":"length","index":0,"logprobs":null,"text":"\n     I'm not capable of being a human being, but I can provide you with some examples of how to use the phrase \"you are a helpful assistant\" in a sentence:\n\n1. You are a helpful assistant.\n2. You are a helpful assistant.\n3. You are a helpful assistant.\n4. You are a helpful assistant.\n5. You are a helpful assistant.\n6. You are a helpful assistant.\n7. You are a helpful assistant.\n8. You are a helpful assistant.\n9. You are a helpful assistant.\n10. You are a helpful"}],"created":1708362027,"id":"cmpl-df049fe9-fd87-44a9-990a-245dc665be68","model":"tinyllama-1.1b-chat-v1.0.Q2_K.gguf","object":"text_completion","usage":{"completion_tokens":128,"prompt_tokens":34,"total_tokens":162}}
```

**Step 11.** Go to [no-ip.com](https://no-ip.com) and create an account. 

**Step 12.** Create a DNS "Host A" record. Use whatever string you want (that isn't taken) for the hostname field. Pick whatever domain name is available. Finally, use your Gateway API's IP address for the target field. The image below is an example of how your DNS "Host A" record should be configured. 

![no-ip.png](task-01/no-ip.png)

**Step 13.** Verify no-ip.com redirects traffic sent to your domain name to your your Gateway API. If you're following along with the instructions in Sail(), this step is in the middle of Task 1, Subtask 3. 
```bash
curl http://cyberphorwashere.zapto.org/api?message=hi
```

**Step 14.** Add `jetstack` to your list of known Helm repositories.  
```bash
helm repo add jetstack https://charts.jetstack.io
```

**Step 15.** Update your Helm installation so its aware of the Kubernetes plugins within the `jetstack` repository. 
```bash
helm repo update
```

**Step 16.** Install a Kubernetes plugin, from the `jetstack` Helm repository, called `cert-manager`. FYSA, this plugin will be in its own namespace, not the default one where most of your objects live. If you want to check the status of it, run this command: `kubectl -n cert-manager get pods`.
```bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.12.0 \
  --set installCRDs=true \
  --set "extraArgs={--feature-gates=ExperimentalGatewayAPISupport=true}"
```

**Step 17.** Using your favorite text-editor and [the provided example](task-01/clusterissuer.yaml), create a Kubernetes manifest for a ClusterIssuer object. The provided example subscribes to certificate expiration alerts using your email address (in order for Let's Encrypt to confirm you own a certificate, it sends a challenge to your domain name only your web server should be able to solve). 
```bash
vim clusterissuer.yaml
```

**Step 10.** Apply the Kubernetes manifest file you just created to your Kubernetes cluster. The command below is meant to be ran in the same directory as your `clusterissuer.yaml` file.
```bash
kubectl apply -f clusterissuer.yaml
```

**Step 11.** Validate you are able to interact with your containerized LLM via HTTPS. 
```bash
curl https://cyberphorwashere.zapto.org/api?message=hello
```

**Misc.** The commands below are helpful while troubleshooting the configuration of this task. 
```bash
# look at gateways
kubectl get gatewayclass
kubectl get gateway
kubectl describe gateway

# look at services
kubectl get svc 
kubectl get svc -n nginx-gateway
kubectl get svc -n cert-manager

# look at httproutes (configuration of gateway object)
kubectl get httproutes
kubectl describe httproutes

# look at clusterissuer
kubectl describe clusterissuer

# look at certificates
kubectl get certificates 
kubectl get certificates -n nginx-gateway
kubectl get secrets -n cert-manager

# look at secrets
kubectl get secrets 
kubectl get secrets -n nginx-gateway
kubectl get secrets -n cert-manager

# look at events
kubectl get events
```

## Task 02
The first five steps of this task focus on installing KrakenD, an API management system. Steps 9 through 18 use a web application called "KrakenDesigner" to generate a KrakenD configuration file. The instructions below assume your current working directory is `task-02`.

**Step 1.** Install `ca-certificates` and `gnupg`. These software packages allow you to securely download and verify the authencity of KrakenD packages. 
```bash
sudo apt install -y ca-certificates gnupg
```

**Step 2.** Add KrakenD's software repository to your operating system's list of known software repositories. 
```bash
echo "deb https://repo.krakend.io/apt stable main" | sudo tee /etc/apt/sources.list.d/krakend.list
```

**Step 3.** Add the public key of Krakend's software repository to your operating system's list of trusted keys. Without it, your operating system can't verify KrakenD software packages. If your operating system can't verify the authenticity of a software package, it can't trust them and therefore won't download them.  
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 5DE6FD698AD6FDD2
```

**Step 4.** Update your operating system's cache of known software packages (the cache is built using information collected from the operating system's list of known software repositories).  
```bash
sudo apt update
```

**Step 5.** Install the KrakenD software package. 
```bash
sudo apt install -y krakend
```

**Step 6.** Create a KrakenD configuration file called `krakend.json` using the example below. 
```json
{
  "$schema": "https://www.krakend.io/schema/krakend.json",
  "version": 3,
  "endpoints": [],
  "extra_config": {}
}
```

**Step 7.** Validate the KrakenD configuration file you just created. 
```bash
krakend validate --config krakend.json
```

Your output should be similar to below. 
```bash
Parsing configuration file: krakend.json
Syntax OK!
```

**Step 8.** Audit the KrakenD configuration you just created. This step is optional, but helpful in situations where you need to identify issues before a deployment. For example, the purpose of Task 2 is to resolve `3.1.2 [HIGH] Implement a rate-limiting strategy and avoid having an All-You-Can-Eat API`. 
```bash
krakend audit --config krakend.json
```

Your putput should be similar to below. 
```
1.2.1   [HIGH]          Prioritize using JWT for endpoint authorization to ensure security.
2.1.2   [HIGH]          Enable TLS or use a terminator in front of KrakenD.
2.1.7   [HIGH]          Enable HTTP security header checks (security/http).
2.2.1   [MEDIUM]        Hide the version banner in runtime.
2.2.2   [HIGH]          Enable CORS.
3.1.1   [LOW]           Enable a bot detector.
3.1.2   [HIGH]          Implement a rate-limiting strategy and avoid having an All-You-Can-Eat API.
3.1.3   [HIGH]          Protect your backends with a circuit breaker.
4.1.1   [MEDIUM]        Implement a telemetry system for collecting metrics for monitoring and troubleshooting.
4.2.1   [MEDIUM]        Implement a telemetry system for tracing for monitoring and troubleshooting.
4.3.1   [MEDIUM]        Use the improved logging component for better log parsing.
5.1.7   [MEDIUM]        Avoid using sequential proxy.
5.2.2   [LOW]           Benefit from the backend for frontend pattern capabilities.
5.2.3   [LOW]           Avoid coupling clients by overusing no-op encoding.
```

**Step 9.** Open a web browser, go to [https://designer.krakend.io/](https://designer.krakend.io/), and click "Service settings."

**Step 10.** In the "HTTP Server settings" section, there is a subsection called "Debug endpoints." Click "Enable /__debug/ endpoint" and "Enable /__echo/ endpoint."

**Step 11.** In the "Hosts (Upstream services or backends)" section, add `http://llmservice`.

**Step 12.** In the navigation pane on the left, there is a section called "Endpoints." Click "Add endpoint" underneath it. Then, replace the endpoint's auto-generated route with `/v1/llm`.

**Step 13.** In the "Parameter forwarding" tab, add a parameter called `message`.

**Step 14.** In the "Throttling" tab, set "Timeout" to `300s` and "cache_ttl" to `100s`. 

**Step 15.** In the "Throttling" tab, check the box for "Endpoint rate limit." Set the capacity to `1` token. 

**Step 16.** In the "Response manipulation" tab, check the box for "Static Response (stub data)." Replace the JSON object in the "Response" field with the JSON object provided below. 
```json
{
  "choices": [
    {
        "finish_reason": "length",
        "index": 0,
        "logprobs": null,
        "text": "Beep boop I'm a fake response"
    }
  ],
  "created": 1708201942,
  "id": "cmpl-a",
  "model": "fake_model",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 999,
    "prompt_tokens": 10,
    "total_tokens": 10
  }
}
```

**Step 17.** In the "Response manipulation" tab, there is a section called "Backends (Upstream) for /v1/llm." In the "Request" tab of this section, there is a "Connection" section. Check the box next to the host you previously added. Then, enter `/api` in the URL field.

**Step 18.** In the top-right corner, click "Download config" and use it to replace the content of the `krakend.json` file you created near the beginning of this task. 

**Step 19.** Validate the KrakenD configuration file you just updated. 
```bash
krakend validate --config krakend.json
```

Your output should be similar to below. 
```bash
Parsing configuration file: krakend.json
Syntax OK!
```

**Step 20.** Create a Kubernetes configmap object using your KrakenD configuration file. 
```bash
kubectl create configmap krakend-cfg --from-file=./krakend.json
```

**Step 21.** Create a Kubernetes deployment object and a Kubernetes service object by applying [the provided Kubernetes file](task-02/deployment.yaml). The purpose of this step is to deploy KrakenD to your Kubernetes cluster. Again, KrakenD is an API management system. 
```bash
kubectl apply -f deployment.yaml
```

**Step 22.** Determine the external IP address of the Kubernetes service object you just created.
```bash
kubectl get svc
```

Your output should be similar to below.
```bash
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)          AGE
apigateway   LoadBalancer   10.0.245.122   52.186.97.202   8080:30018/TCP   30s
kubernetes   ClusterIP      10.0.0.1       <none>          443/TCP          4d14h
llmservice   ClusterIP      10.0.250.211   <none>          80/TCP           4d11h
```

**Step 23.** Query the Kubernetes service object using its external IP address. For example, based on the output above, I would use `52.186.97.202`. 
```bash
curl http://52.186.97.202:8080/v1/llm?message=hello
```

If your output is similar to below, KrakenD has successfully been deployed to your Kubernetes cluster.
```json
{"choices":[{"finish_reason":"stop","index":0,"logprobs":null,"text":"\nCertainly! Here's an example of how to use the \"helpful\" verb in a sentence:\n\nExample:\n- \"I'm excited to help you with your homework!\""}],"created":1708745345,"id":"cmpl-859196db-9fdf-4cef-bdcf-53e3fa0670b5","model":"tinyllama-1.1b-chat-v1.0.Q2_K.gguf","object":"text_completion","usage":{"completion_tokens":43,"prompt_tokens":34,"total_tokens":77}}
```

**Step 24.** Using your favorite text-editor, update the `backendRefs` section of your `httproute.yaml` file so it looks like below.
```yaml
    backendRefs:
    - name: llmservice
      port: 80  
    - name: apigateway
      port: 8080    
```

**Step 25.** Apply the change you just made. FYI, I chose to make a copy of my YAML files from Task 1 and put them into a single file for Task 2. I felt like this just made things easier to think about and debug. The name of this new, all-in-one, file is `task-02.yaml`. Again, it's just an aggregation of the `gateway.yaml`, `httproute.yaml`, and `clusterissuer.yaml` files created in Task 1 ableit with the change in the previous step.
```bash
kubectl apply -f task-02.yaml
```

**Step 26.** In the `spec` section of [the provided Kubernetes file](task-02/deployment.yaml), change your KrakenD service from a `LoadBalancer` type to a `ClusterIP` type.
```yaml
spec:
  type: ClusterIP
  selector:
    application: apigateway
  ports:
    - port: 8080
      targetPort: 8080
```

**Step 27.** Verify you can access your LLM through your KrakenD service. If you get a response with a HTTP server code 404, wait a few seconds and try again. 
```bash
curl https://cyberphorwashere.zapto.org/v1/llm?message=hello
```

## Task 03
**Step 1.** Create a folder called `task-03` and change directories to it.
```bash
mkdir task-03
cd task-03/
```

**Step 2.** Create a Python virtual environment called `venv`. 
```bash
python3 -m venv venv
```

**Step 3.** Activate the Python virtual environment you just created.
```bash
source venv/bin/activate
```

**Step 4.** Upgrade the Python libraries below to their latest versions.
```bash
pip install --upgrade pip setuptools wheel
```

**Step 5.** Install the Django, a Python web app framework.
```bash
pip install Django djangorestframework djangorestframework-simplejwt[crypto]
```

**Step 6.** Create a Django project called `task3`. FYI, the `django-admin` program is used for creating projects and/or apps, managing them.
```bash
django-admin startproject task3 .
```

**Step 7.** Change directories to the `task3` folder automatically created by the Django CLI in the previous step. This folder is completely different from the one created at the beginning of this task. To explain, your path should be something like `task-03/task03` when you're done with this step.
```bash
cd task3
```

**Step 8.** Create a Django app called `login`.
```bash
django-admin startapp login
```

**Step 9.** Change directories to the parent of the `task3` folder (i.e., the `task-03` folder). It contains a file called `manage.py`.
```bash
cd ..
```

**Step 10.** Create a database file called `db.sqlite3` using the command below.
```bash
python manage.py migrate
```

**Step 11.** Create a new privileged Django user called `admin`. Whe prompted, give it the password `asdasd`. This password sucks so enter `Y` to bypass the password validation and reject everything Vic represents.
```bash
python manage.py createsuperuser --username admin --email admin@example.com
```

**Step 12.** Using the command below, run your Django app to make sure it works. If you're doing this in GitHub Codespaces, click the "Ports" tab in your terminal window. Then, in the "Forwarded Address" column, click the "Open in Browser" button on the right side of the auto-generated URL. 
```bash
python manage.py runserver
```

**Step 13.** Add `admin/login/` to the end of the URL in your browser tab. You will be redirected to a login page. Login using the credentials you specified above (username: `admin`, password: `asdasd`). Once you confirm you're able to login, stop the app. 

**Step 14.** Using your favorite text-editor, create a file called `serializers.py` in the `task3/login` folder using [the provided example](task-03/task3/login/serializers.py).
```bash
vim task3/login/serializers.py
```

**Step 15.** Using your favorite text-editor, update the file called `views.py` in the `task3/login` folder using [the provided example](task-03/task3/login/views.py).
```bash
vim task3/login/views.py
```

**Step 16.** Using your favorite text-editor, update the file called `urls.py` in the `task3/` folder using [the provided example](task-03/task3/urls.py).
```bash
vim task3/urls.py
```

**Step 17.** Using your favorite text-editor, update the file called `settings.py` in the `task3/` folder using [the provided example](task-03/task3/settings.py).
```bash
vim task3/settings.py
```

**Step 18.** Using the command below, run your Django app as a background process.  
```bash
python manage.py runserver &
```

**Step 19.** Verify the login service you created works. Don't forget the trailing `/` at the end of the URL. 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://localhost:8000/api/token/ 
```

Your output should be similar to below. Again, all of these commands and Python code allow you to include add authentication to your LLM service.
```json
{
  "refresh": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwOTAwMjYxMywiaWF0IjoxNzA4OTE2MjEzLCJqdGkiOiI5MmM0MzVkMmJkMWM0YjQ3ODdmNmNmZDQ1YjFjYzUzMSIsInVzZXJfaWQiOjF9.xmEO4qaLX9-zmiBE1-sMNU4rS2ZNJLyUzqFpsqMSimWsWh4Gpsy-9nzgiOnVpnCe05eoMjMLMSSz6yZ5cVWIh_WufqRHjPk1qnsBxrbqWMfsz77oWvzNjx5-YZG_vDdEKxzNUDtoGNjz-pH4Pa6Xx6v7muqgVgudRl9qxj41bxdXqZHNk0uPWPNUMC2WndmPi057_Cb-y_v8L5dTLR_yBF7x9-mfviTF2iStr03vGmgDSjiaDdTPFP8vlYDJjOL94zeNQBRTCDWchv9g4SaCA-TYn_a5k08fRDl-qaMI4mm5--GkBo4hfF6X5ImptQedr8Y_VI_8HfUz6zRH6bpYig",
  "access": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4OTE2NTEzLCJpYXQiOjE3MDg5MTYyMTMsImp0aSI6IjIwZDRmOTBhOWYxNjQyMDFhYjYzNzFlN2MxYTYzMTRhIiwidXNlcl9pZCI6MX0.Gtp_eYvSAxESfKYo2JFYVcxbQZBaYId5fXPvr0butzoQflIEKos0d-lk1rk-CuEqRFX0uYZzWb8XBQYfcVdjg4k0XpFEfD7LgfYJs1ywnbOs6mx8bVSYM5IIcOvdpQ-g07JaouZ6NBFfoDSH3jytS-36tZHur535w_VNgPa8dJdNlviyVR60-0wdf1dJjAbrHgbginDblfE2ua2ETHIDoIg1aeNaZo2Jxo-zb_xTmoZjf46eFmrusxgdBXYif_McWE1glKuIrrJghtw7QkJ-A-t0-lLOf2IPRFbz2p6XadNYMd1MO-zO4Dkfy8_ZwnVx_DKjjtknKd9HXvnNN26ByQ"
}
```

## Task   04
FYSA, I made a copy of all the files generated in the `task-03` folder and copied them to a `task-04/django` folder I made (to include the Python virtual environment folder called `venv`). Then, before starting this task, I changed directories to `task-04/django`.

**Step 1.** Create an private key.
```bash
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
```

**Step 2.** Create a public key.
```bash
openssl rsa -pubout -in private.pem -out public.pem
```

**Step 3.** Create an environment variable using the content of your private key as its value.
```bash
export PRIVATE_KEY=$(cat private.pem)
```

**Step 4.** Create an environment variable using the content of your public key as its value.
```bash
export PUBLIC_KEY=$(cat public.pem)
```

**Step 5.** Using your favorite text-editor, update the file called `settings.py` in the `task3/` folder using [the provided example](task-04/django/task3/settings.py). Again, I made a copy of the files generated in the `task-03` folder and copied them to a `task-04` I made. Then, before starting this task, I changed directories to `task-04`.
```bash
vim task3/settings.py
```

This is what I added for this step. `RS256` is not a typo. 
```python
SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "SIGNING_KEY": os.getenv("PRIVATE_KEY"),
    "VERIFYING_KEY": os.getenv("PUBLIC_KEY"),
}
```

**Step 6.** Reactivate your Python virtual environment. 
```bash
source venv/bin/activate
```

**Step 7.** Verify your environment variables (`PRIVATE_KEY` AND `PUBLIC_KEY`) are still set. Then, restart your Django application as a background process.
```bash
python manage.py runserver &
```

**Step 8.** Verify the login service you just updated works by first running the following command. Don't forget the trailing `/` at the end of the URL. 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://localhost:8000/api/token/ -s | jq .access
```

Your output should be a string similar to below. If you also get something like `[26/Feb/2024 02:37:49] "POST /api/token/ HTTP/1.1" 200 1081`, ignore it. It's a server log from Django and not part of your JWT. 
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4OTE1MzY5LCJpYXQiOjE3MDg5MTUwNjksImp0aSI6ImNkODIzYTc5MjAwNDQzOWFhYTMxYzdiYTk4NDViMzMzIiwidXNlcl9pZCI6MX0.hrIdW_XsWAn3mRifqgX0Liheyn6PrSSrsoebOGDFnJ9-ognsKZkWU1GlIzo_Ua53JA8L1GXA10XxKK3U6llCqdHTHwZqRRGcvdl9OMWJsS1IU7vLGATWd5HwWe_jy4DY7IOP7xGtTDTnzLx7EjY_PKn0Cxox4oxiUiQOgVxXvtB52Bp9ovABMjfrrVDU3bGEZZtgxk5_D52GHGRMJz8xh_BIHPgoyJUt-0hi8ooPE8XnNslOF98Nm2iHZjNS8F4Mzlts4z6wDUgZxX8Jo5WHgeFZADf6oOxtD2oJPxX5cCts5Bxkb7S3Iq-xa2SVO2lCqcYX0AHrNSN6LG4GyhYltw
```

Open a browser and go to [https://jwt.io/](https://jwt.io/). Copy and paste the string generated by the previous command to the "Encoded" field. Then, copy the contents of your `PUBLIC_KEY` variable to the "Public key..." field inside the "VERIFY SIGNATURE" box. Make sure you see "Signature Verified" before moving on.

**Step 9.** Create a folder called `docker` in the `task-04` folder. 
```bash
mkdir docker/
```

**Step 10.** Using your favorite text-editor and [the provided example](task-04/docker/Dockerfile), create a Dockerfile in the `docker` folder. The purpose of the next few steps is to containerize the login service you created via Django.

**Step 11.** Build and tag container image using the Dockerfile you just created.
```bash
docker image build --rm --tag loginservice:v1.0.0 -f docker/Dockerfile  . 
```

**Step 12.** Create a container using the image you just built.
```bash
docker run --name login -d -p 8000:8000 \
  -e PUBLIC_KEY="${PUBLIC_KEY}" \
  -e PRIVATE_KEY="${PRIVATE_KEY}" \
  loginservice:v1.0.0
```

**Step 13.** Test your containerized login service by entering the command below. Your output should be similar to what we've seen already.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://localhost:8000/api/token/
```

**Step 14.** Stop the container you created.
```bash
docker container stop login
```

**Step 15.** Remove the container you created.
```bash
docker container rm login
```

**Step 16.** Add another tag to your image for your Azure Container Registry (ACR). 
```bash
docker tag loginservice:v1.0.0 cyberphorwashere.azurecr.io/loginservice:v1.0.0
```

**Step 17.** Push your container image to your ACR.
```bash
docker push cyberphorwashere.azurecr.io/loginservice:v1.0.0 
```

**Step 18.** Using your favorite text-editor and [the provided example](task-04/kubernetes/loginservice.yaml), create a file called `loginservice.yaml` in the `kubernetes` folder.

**Step 19.** Create a Kubernetes secret using the command below. To explain, this command creates a single secret containing the contents of your `private.pem` and `private.pem` keys. 
```bash
kubectl create secret generic loginservice \
  --from-file=django/private.pem \
  --from-file=django/public.pem
```

**Step 20.** Apply the `loginservice.yaml` file you created to your Kubernetes cluster.
```bash
kubectl apply -f kubernetes/loginservice.yaml 
```

**Step 21.** Identify the external IP address Kubernetes gave your login service. 
```bash
kubectl get svc
```

Your output should be similar to below.
```bash
NAME           TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
apigateway     ClusterIP      10.0.245.122   <none>          8080/TCP       2d2h
kubernetes     ClusterIP      10.0.0.1       <none>          443/TCP        6d17h
llmservice     ClusterIP      10.0.250.211   <none>          80/TCP         6d13h
loginservice   LoadBalancer   10.0.209.2     52.226.154.50   80:32701/TCP   10s
```

**Step 22.** Test your containerized login service using the command below, the external IP address you just identified, and TCP port 80. Your output should be similar to what we've seen already. 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://52.226.154.50/api/token/
```

**Step 23.** Install the `jwcrypto` Python library in your Python virtual environment.
```bash
pip install jwcrypto
```

**Step 24.** Run the provided Python script that converts your public key to a format called JWKS.
```bash
python pubkey2jwk.py 
```

**Step 25.** Take the output of the previouse command and create a file called `publickey.json`. Make it look like below.
```json
{
  "keys": [
    {
      "kty":"RSA",
      "use": "sig",
      "kid":"yourcoolkid",
      "n":"3rID6InQ-Pdo922pq4AsJWnGk_11v2U7iNp4KHb-RPVDzohtzfHQmwZps8lNbXJq0uyZMFVKHVkHK3uME16zYECJHU_j0m7XP-iqTCaUSYfdnHMjpTxVxEFqVWr1P_7vFbiQ8wm_2gKhKiwlHiEfqenGT3CPv5kEi87I78YLjHPCzsWx2gU6GLqVSpj3teyrBeksZljLMVxtbfb31xeoUFKJTDMMKcGoWag7XnfLgHpd1571LxAzOuODLrfGMALb0fNDzV7cC9TQySK1zs9qbb7oEq7216oGm-j53sNNaXP5rot2dWG70DSHy6i7Gyc28Z8L8jD62kYW0wZb0a7YVQ",
      "e":"AQAB",
      "alg":"RS256",
    }
  ]
}
```

**Step 26.** Using your favorite text-editor and [the provided example](task-04/krakend/krakend.json), update your `krakend.json` configuration file. 
```bash
vim krakend.json
```

**Step 27.** Delete your old KrakenD configuration and upload your new one.
```bash
kubectl delete configmap krakend-cfg 
kubectl create configmap krakend-cfg --from-file=krakend/krakend.json
```

**Step 28.** Restart your KrakenD pod.
```bash
kubectl rollout restart deployment/krakend-deploy
```

**Step 29.** See if you can access your login service through your KrakenD pod.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://52.226.154.50/api/token/
```

**Step 30.** Create a Kubernetes secret based on the `publickey.json` file you created earlier.
```bash
kubectl create secret generic krakend-pubkey \
  --from-file=krakend/publickey.json
```

**Step 31.** Update your `httproute.yaml` so it looks like [the provided example](task-04/kubernetes/httproute.yaml).
```bash
kubectl apply -f kubernetes/httproute.yaml
```

**Step 32.** Authenticate with your login service so it returns a JWT.
```bash
curl -H 'Content-Type: application/json' -d '{"username":"admin", "password":"asdasd" }' -X POST https://cyberphorwashere.zapto.org/v1/logintoken | jq .access
```

Your output should be similar to below.
```
eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4OTMxNDAyLCJpYXQiOjE3MDg5MzExMDIsImp0aSI6IjZkMWQ0MTJlZGIzNDRiMGRhNzlhZWI5NGM4NjYyMjJlIiwidXNlcl9pZCI6MX0.PpyHEab1OFvreWTOpfSv-Wrmq6H6HL70j5E2enJPkUo7m0erDQWZEwkDdPc42z74_L5NoTFU4JT6Zvgzy_QGMF1otIHzg2bL6nwRmsPQgIOsWtZSrZoUq7y-JUt3OvHYraEeAL1-51OU-PLNBIhX7cc1-7_x4isUKL4FC2eEZZA4NeGeG1ukVcpzwwJa75yY8pfu0YQVYh1mrYeBo1ieP_pV6EBtbJOlm13XJgVqEFxpIuQhVqi381UuY1ZWAEVyaMQMsQD6tRY1bINPyswFZtWzxA3UIJXNWevtShOhD1kdcm7yfEtjFXHxAxI0z1Esv2ueWp4U9pVeaRFZfiJvkw
```

**Step 33.** Use the JWT your login service returned to query your LLM.
```bash
curl -D - -H "Authorization: BEARER eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4OTMxNDAyLCJpYXQiOjE3MDg5MzExMDIsImp0aSI6IjZkMWQ0MTJlZGIzNDRiMGRhNzlhZWI5NGM4NjYyMjJlIiwidXNlcl9pZCI6MX0.PpyHEab1OFvreWTOpfSv-Wrmq6H6HL70j5E2enJPkUo7m0erDQWZEwkDdPc42z74_L5NoTFU4JT6Zvgzy_QGMF1otIHzg2bL6nwRmsPQgIOsWtZSrZoUq7y-JUt3OvHYraEeAL1-51OU-PLNBIhX7cc1-7_x4isUKL4FC2eEZZA4NeGeG1ukVcpzwwJa75yY8pfu0YQVYh1mrYeBo1ieP_pV6EBtbJOlm13XJgVqEFxpIuQhVqi381UuY1ZWAEVyaMQMsQD6tRY1bINPyswFZtWzxA3UIJXNWevtShOhD1kdcm7yfEtjFXHxAxI0z1Esv2ueWp4U9pVeaRFZfiJvkw" https://cyberphorwashere.zapto.org/v1/llm?message=hello
```

**Misc.** The commands below helped me troubleshoot during this task.
```bash
# get pods
kubectl get pods

# print env vars of a given pod (ex: login-788bc9cb7-nrvtl)
kubectl exec login-788bc9cb7-nrvtl -- env

# enter a pod
kubectl exec -it login-788bc9cb7-lj2tr -- /bin/bash

# look at logs of a pod
kubectl logs krakend-deploy-58fcc87f9-mdp99
```