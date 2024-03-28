# Cloud-Native: Data Tier Architecture and Distributed Queries
The purpose of this project is to explore tradeoffs between consistency and availability when deploying a stateful system. It's also a tutorial in improving the throughput and reliability of a login service. 

* [References](#references)
* [Notes](#notes)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)

## References
If I find any helpful references, I will put them here. 
* [Storage options for applications in Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/concepts-storage)
* [How To Deploy MySQL Using Persistent Volume](https://blog.knoldus.com/k8s-how-to-deploy-mysql-using-persistent-volume/)
* [Retrieve the full name of a service in Kubernetes](https://stackoverflow.com/questions/59559438/retrieve-the-full-name-of-a-service-in-kubernetes)
* [Kubernetes: Opaque Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#opaque-secrets)
* [Kubernetes: Run a Replicated Stateful Application - Create the StatefulSet](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#statefulset)
* [Django: Automatic database routing](https://docs.djangoproject.com/en/5.0/topics/db/multi-db/)

## Notes
**Kubernetes PersistentVolumeClaim Resource**  
A Persistent Volume Claim is a request for storage from our Cloud Provider. It provides an interface for allocating storage and connecting it to a pod.

**How to Get Logs From a Container on a Kubernetes Pod**  
```bash
kubectl logs login-666 --container login-init
```

**Misc Docker Commands**  
FYI, if you try to add a .dockerignore file to exclude files from a new version of your image, they will still be in the layers that didn't change. If you need to exclude files, do it from the first version of your image. 
```bash
docker exec -it login
docker container rm login -f
docker image rm login:v2.0.0
docker image prune -f
```

## Setup
The following steps assume (1) you're already working within a Linux environment (Windows Subsystem for Linux, Azure Shell, GitHub Codespaces, a VirtualBox-based Linux virtual machine, etc.), (2) you've installed the usual software (i.e., Python, Azure CLI, Docker, and Kubernetes), (3) you've forked this repository, and (4) you are running these setup commands from the `vic-code/cloud-native/unit-05/setup` directory.

**Step 1.** Install MySQL client software packages.
```bash
sudo apt-get install pkg-config build-essential libmysqlclient-dev
```

**Step 2.** Define your environment variables. 
```bash
export LOCATION="eastus"
export RESOURCE_GROUP_NAME="project5"
export ACR_NAME="project5cyberphorwashere"
export ACR_SKU="Basic"
export AKS_CLUSTER_NAME="project5cluster"
export AKS_NODE_COUNT=2
```

**Step 3.** Login to Azure using the CLI. 
```bash
az login --use-device-code
```

**Step 4.** Create a resource group.
```bash
az group create --name "${RESOURCE_GROUP_NAME}" --location eastus
```

**Step 5.** Create an container registry. 
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

**Step 8.** Attach your Azure Container Registry to your Kubernetes cluster. Don't skip this step. Otherwise, you'll get `ErrImagePull`, `Failed to pull image`, and `401 Unauthorized` errors.
```bash
az aks update --resource-group "${RESOURCE_GROUP_NAME}" --name "${AKS_CLUSTER_NAME}" --attach-acr "${ACR_NAME}"
```

**Step 9.** Download credentials from your Kubernetes cluster for Kubectl to use.
```bash
az aks get-credentials --resource-group "${RESOURCE_GROUP_NAME}" --name "${AKS_CLUSTER_NAME}"
```

**Step 10.** Change directories to `src/`, create a new privileged user called `admin` and change directories back to `setup/`. When prompted, enter `asdasd` as a password. Then, enter `Y` to bypass the password validation check.
```bash
cd src/
poetry run python manage.py createsuperuser --username admin --email admin@example.com
cd ../
```

**Step 11.** Create an private key and add it to an environment variable. 
```bash
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
export PRIVATE_KEY=$(cat private.pem)
```

**Step 12.** Create a public key and add it to an environment variable.
```bash
openssl rsa -pubout -in private.pem -out public.pem
export PUBLIC_KEY=$(cat public.pem)
```

**Step 13.** Build a `login` container image using the provided [Dockerfile example](setup/docker/Dockerfile) and [entrypoint script example](setup/docker/entrypoint.sh) as well as a tag for your *local* container registry. 
```bash
docker build --no-cache -t login:v1.0.0 -f docker/Dockerfile .
```

**Step 14.** Create a container using the image you just built.
```bash
docker run --name login -p 80:8080 -e "PRIVATE_KEY=$(cat private.pem)" -e "PUBLIC_KEY=$(cat public.pem)" login:v1.0.0
```

**Step 15.** Test the container using `curl`. 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://localhost/api/token/ 
```

**Step 15.** Stop and remove the container if it works.
```bash
docker container stop login
docker container remove login
```

**Step 16.** Add a tag to the image for your Azure Container Registry.
```bash
docker tag login:v1.0.0 "${ACR_NAME}.azurecr.io/login:v1.0.0"
```

**Step 17.** Push the tested and tagged image to your Azure Container Registry. 
```bash
docker push "${ACR_NAME}.azurecr.io/login:v1.0.0"
```

**Step 18.** Change directories to the parent folder of `setup` (i.e., `vic-code/cloud-native/unit-05/`).
```bash
cd ../
```

## Task 01
The purpose of this task is to modify a containerized service so it can handle faults at the pod-level. It involves adding a "PersistentVolumeClaim" resource to a Kubernetes cluster and scaling a MySQL database. 

### Subtask 01 and 02
**Step 1.** Change directories to `task-01`.
```bash
cd task-01/
```

**Step 2.** Using your favorite text-editor create a file called `mysql.yaml` using the [provided example](task-01/kubernetes/mysql.yaml) as inspiration.
```bash
vim kubernetes/mysql.yaml
```

**Step 2.** Apply the Kubernetes configuration you just created to deploy a `mysql` image as a container on a pod in your Kubernetes cluster.
```bash
kubectl apply -f kubernetes/mysql.yaml
```

**Step 3.** Run the command below to check if the "PersistentVolumeClaim" defined in the `mysql.yaml` file is in a `Bound` status. 
```bash
kubectl get pvc
```

**Step 4.** Wait a minute or two. Then, run the command below to check if the pod you just created is in a `Running` status. 
```bash
kubectl get pods
```

**Step 5.** Run the command below to confirm the `mysql` container is working as expected.
```bash
kubectl run mysql-client --image=mysql:5.7 -it --rm --restart=Never -- mysql -h mysql -uroot -ppassword -e 'SHOW databases;'
```

Your output should be similar to below.
```
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
pod "mysql-client" deleted
```

### Subtask 03
**Step 1.** Make sure you're still in the `task-01` directory. Then, build a *new* `login` container image using the provided [Dockerfile example](task-01/docker/Dockerfile) and [entrypoint script example](task-01/docker/entrypoint.sh) as well as a *new* tag for your local container registry. 
```bash
docker build --no-cache -t login:v2.0.0 -f docker/Dockerfile .
```

**Step 2.** Add a *new* tag to the image for your Azure Container Registry too.
```bash
docker tag login:v2.0.0 "${ACR_NAME}.azurecr.io/login:v2.0.0"
```

**Step 3.** Push the *new* image to your Azure Container Registry. 
```bash
docker push "${ACR_NAME}.azurecr.io/login:v2.0.0"
```

**Step 4.** Create an opaque Secret resource using the `private.pem` and `public.pem` files generated in the [Setup](#setup) section. 
```bash
kubectl create secret generic keys --from-file=../setup/private.pem --from-file=../setup/public.pem
```

**Step 5.** Using your favorite text-editor create a file called `login.yaml` using the [provided example](task-01/kubernetes/login.yaml) as inspiration. Make sure to use the same the ACR name you declared in the [Setup](#setup) section.
```bash
vim kubernetes/login.yaml
```

**Step 6.** Apply the Kubernetes configuration you just created to deploy your `login` image as a container on a pod in your Kubernetes cluster.
```bash
kubectl apply -f kubernetes/login.yaml
```

**Step 7.** Run the command below to check if the pod you just created is in a `Running` status. 
```bash
kubectl get pods
```

**Step 8.** Run the command below to confirm the `login` container is working as expected (make sure to use the right pod name, yours will obviously be different).
```bash
kubectl logs login-85dc6cbf74-nhbx2 | tail -n1
```

Your output should be similar to below.
```
django.db.utils.OperationalError: (1049, "Unknown database 'login'")
```

### Subtask 04
**Step 1.** Make sure you're still in the `task-01` directory. Then, delete all of your MySQL resources from your Kubernetes cluster. 
```bash
kubectl delete pvc/mysql
kubectl delete pod/mysql
kubectl delete svc/mysql
```

**Step 2.** Using your favorite text-editor create a file called `subtask-04.yaml` using the [provided example](task-01/kubernetes/subtask-04.yaml) as inspiration.
```bash
vim kubernetes/subtask-04.yaml
```

**Step 3.** Apply the *new* Kubernetes configuration you just created to deploy a `mysql` image as a container on a pod in your Kubernetes cluster.
```bash
kubectl apply -f kubernetes/subtask-04.yaml
```

**Step 4.** Wait a minute or two. Then, run the command below to check if the pod you just created is in a `Running` status. 
```bash
kubectl get pods
```

**Step 5.** Run the command below to confirm the `mysql` container is working as expected.
```bash
kubectl run mysql-client --image=mysql:5.7 -it --rm --restart=Never -- mysql -h mysql -uroot -ppassword -e 'SHOW databases;'
```

Your output should be similar to below. 
```
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| login              |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
pod "mysql-client" deleted
```

### Subtask 05
**Step 1.** Make sure you're still in the `task-01` directory. Then, delete all of your `login` resources from your Kubernetes cluster. If you find yourself repeating this step multiple times, make sure your "PersistentVolumeClaim" resource has been recreated. Otherwise, it and therefore your MySQL database will have old data. 
```bash
kubectl delete svc/login
kubectl delete deployment/login
```

**Step 2.** Using your favorite text-editor create a file called `subtask-05.yaml` using the [provided example](task-01/kubernetes/subtask-05.yaml) as inspiration.
```bash
vim kubernetes/subtask-05.yaml
```

**Step 3.** Apply the *new* Kubernetes configuration you just created to deploy your `login` image as a container and an init container on a pod in your Kubernetes cluster.
```bash
kubectl apply -f kubernetes/subtask-05.yaml
```

**Step 4.** Identify the IP address of the new LoadBalancer resource you defined in [`subtask-05.yaml`](task-01/kubernetes/subtask-05.yaml). 
```bash
kubectl get svc
```

Your output should be similar to below.
```
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)        AGE
kubernetes   ClusterIP      10.0.0.1       <none>         443/TCP        60m
login        LoadBalancer   10.0.91.2      172.171.38.132 80:32760/TCP   3m42s
mysql        ClusterIP      10.0.167.147   <none>         3306/TCP       29m
```

**Step 5.** Test your `login` container using `curl` and the IP address of your LoadBalancer resource. 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://172.171.38.132/api/token/ 
```

Your output should be similar to below. 
```json
{"refresh": "eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTY2NDExNywiaWF0IjoxNzExNTc3NzE3LCJqdGkiOiJlMzIzOTFhOTExNzI0NTU5YmQ3YTQwM2U5NTgwMTM4OCIsInVzZXJfaWQiOjEsImlzcyI6ImxsbWxvZ2luIiwic3ViIjoiY2xpZW50In0.KMpX91U1TKtL_9s6c-L5j25SYfaMEUFi2SlFAikFcUeCrnpMUGVJoGYst_ngCZeGXMTxO0CtPol7uIYVKdFiBXZ3BHlnLbFrw_Pena8ptJVmYqP3UNXKmxmZ-OEqeAoXq3x8ruisv0Ne3ETyYeNzzTSoTP23v9vMDjwgbQsk9dIzua9XP-INR-mCeiUijO5pr1cU7MXIJMuYO_olopnq5A7msUhhW_jK7KKl4i8YCAddjOp6YTLkgvTQunYjJyu3PiERro4XQ8xAdWAFB29ehvCoICdArE9gHA2_Re8aTb90DizB1kK6DFYq0DllAHnqv7rT7vcn6peGm1CMiwtKrw","access": "eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExNTc4MDE3LCJpYXQiOjE3MTE1Nzc3MTcsImp0aSI6IjIyN2M1MDdhNmYxODQ0MDY5ZjAxYzE1NDQ0NGZkMzEzIiwidXNlcl9pZCI6MSwiaXNzIjoibGxtbG9naW4iLCJzdWIiOiJjbGllbnQifQ.FFn6Mt54yZd775cS4MypCze6E0httMILBnQWCgxlpg64jhIAvx4TatOAjoD8FKtEIO1MJEAfBK3ObMIInsyliK29Wqd2wLn5hpL3_boeXI7U0I5UHmmqacCwubg8RG4-C7peLOEIXo9GpbNTTIHzDqZpxjlLdyHvXvo8rw4Mhn572M-xe23iwDyOLXcrfPi0s4F0YqiZwEmN7bmjfLjutDB9NWTfpU7C8dRjgMmoLuIu3DPD1BHnMtaVW8WqAk5aL3bnFE5-whDqPSuE8NfaBT8jqboU1bpR7hzmBw0naajHVswTZFWnujgWWoqHCvaMHXMsmkb9KjLQr2ttdu3Vfw"}
```

**Step 6.** Run the command below to make sure your cluster is working as expected. 
```bash
kubectl exec deploy/login -it -- python manage.py shell -c "from django.db import connection; cm = connection.cursor(); cursor = cm.__enter__(); cursor.execute('SHOW TABLES;'); print(cursor.fetchone()); cursor.close()"
```

If your output is similar to below, you're ready to submit.
```
Defaulted container "login" out of: login, login-init (init)
('auth_group',)
```

## Task 02
The purpose of this task is to TEXT GOES HERE.

### Subtask 01
**Step 1.** Change your working directory from `task-01` to `task-02`. 
```bash
cd ../task-02/
```

**Step 2.** Create a new Python project using Poetry.
```bash
poetry new t2-locust
```

**Step 3.** Change directories to `t2-locust`.
```bash
cd t2-locust/
```

**Step 4.** Using your favorite text-editor, create and open a file called `poetry.toml`. 
```bash
vim poetry.toml
```

**Step 5.** Add the content below to it.
```toml
[virtualenvs]
in-project = true
path = ".venv"
```

**Step 6.** Add the Python package `locust` to your Python project using Poetry.
```bash
poetry add locust
```

**Step 7.** Using your favorite text-editor, create a file called `locustfile.py` using the [provided example](task-02/t2-locust/locustfile.py) as inspiration. 

**Step 8.** Identify the IP address of the new LoadBalancer resource you previously defined in Task 01 for your `login` service.
```bash
kubectl get svc
```

Your output should be similar to below.
```
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)        AGE
kubernetes   ClusterIP      10.0.0.1       <none>         443/TCP        60m
login        LoadBalancer   10.0.91.2      172.171.38.132 80:32760/TCP   3m42s
mysql        ClusterIP      10.0.167.147   <none>         3306/TCP       29m
```

**Step 9.** Run Locust against your `login` service's LoadBalancer. Let it run for a few minutes and then, kill it. *The purpose of this step is to highlight the need to scale your MySQL service.* It specifically underscores how the latency of your `login` service is about 5 seconds right now (regardless if you had more `login` pods). 
```bash
poetry run locust -f t2_locust/locustfile.py --headless -u 10 -r 10 --host http://172.171.38.132
```

**Step 10.** Change directories back to `task-02`. 
```bash
cd ../
```

**Step 11.** Delete all of your `login` and `mysql` Kubernetes objects except for your Secret (this was defined using the CLI earlier, not a YAML file). Wait for your the deletion of your "PersistentVolumeClaim" to finish before moving on (run `kubectl get pvc` to check - if need be, use the Azure Portal: Kubernetes service > Storage > Persistent volume claims). The purpose of this step is to reduce confusion and re-baseline your cluster for Task 02.  
```bash
kubectl delete configmap/mysql
kubectl delete pvc/mysql
kubectl delete pod/mysql
kubectl delete svc/mysql
kubectl delete deployment/login
```

**Step 12.** Using your favorite text-editor, create a file called `subtask-01.yaml` using the [provided example](task-02/kubernetes/subtask-01.yaml) as inspiration.
```bash
vim kubernetes/subtask-01.yaml
```

**Step 13.** Apply the *new* Kubernetes configuration you just created. It does a few things: 
* Creates a PersistentVolumeClaim object to request storage from the resource provider (i.e., Cloud Service Provider) and host the cluster's MySQL database
* Creates a StatefulSet object (in lieu of a Deployment object) to deploy and track the identity and state of all pods 
* Creates a MySQL Service object to route *read* requests to pods with MySQL servers that can read from the MySQL database
* Creates a MySQL Service object to route *write* requests to pods with MySQL servers that can write to the MySQL database
* Creates a ConfigMap object with two files
    * `primary.cnf`: used only by the the primary MySQL server within a pod
    * `replica.cnf`: used only by for all MySQL server replicas within a pod
```bash
kubectl apply -f kubernetes/subtask-01.yaml
```

**Step 14.** Wait a few minutes and then, run the command below.  
```bash
kubectl get pods
```

Your output should be similar to below before moving on.
```
NAME      READY   STATUS    RESTARTS   AGE
mysql-0   2/2     Running   0          2m41s
mysql-1   2/2     Running   0          2m6s
mysql-2   2/2     Running   0          71s
```

**Step 15.** Run the command below to confirm your MySQL system is working as expected.
```bash
kubectl run mysql-client --image=mysql:8.0 -it --rm --restart=Never -- mysql -h mysql-0.mysql -uroot -e 'SHOW databases;'
```

Your output should be similar to below. 
```
+------------------------+
| Database               |
+------------------------+
| information_schema     |
| mysql                  |
| performance_schema     |
| sys                    |
| xtrabackup_backupfiles |
+------------------------+
pod "mysql-client" deleted
```

### Subtask 02
**Step 1.** Make sure you're still in the `task-02` directory. Then, using your favorite text-editor, create a file called `subtask-02.yaml` using the [provided example](task-02/kubernetes/subtask-02.yaml) as inspiration
```bash
vim kubernetes/subtask-02.yaml
```

**Step 2.** Apply the *new* Kubernetes configuration you just created. It creates a Job object that uses a MySQL container to create a MySQL database called `login`.  
```bash
kubectl apply -f kubernetes/subtask-02.yaml
```

**Step 3.** Run the command below to confirm your MySQL system now has a database called `login`.
```bash
kubectl run mysql-client --image=mysql:8.0 -it --rm --restart=Never -- mysql -h mysql-0.mysql -uroot -e 'SHOW databases;'
```

Your output should be similar to below. 
```
+------------------------+
| Database               |
+------------------------+
| information_schema     |
| mysql                  |
| performance_schema     |
| sys                    |
| xtrabackup_backupfiles |
+------------------------+
pod "mysql-client" deleted
```

**Step 4.** Delete the Job object you made. 
```bash
kubectl delete jobs/mysql
```

### Subtask 03
**Step 1.** Make sure you're still in the `task-02` directory. Then, build a *new* `login` container image using the provided [Dockerfile example](docker/Dockerfile) and [entrypoint script example](docker/entrypoint.sh) as well as a *new* tag for your *local* container registry. The `settings.py` file has been updated to use a new file called `routers.py`. Together, they define which `login` MySQL server to use for reading and which one to use for writing. Specifically, `settings.py` uses a dictionary called `DATABASES` and list called `DATABASE_ROUTERS` (`DATABASE_ROUTERS` points to `routers.py`).
```bash
docker build --no-cache -t login:v3.0.0 -f docker/Dockerfile .
```

**Step 2.** Add a *new* tag to the image for your Azure Container Registry.
```bash
docker tag login:v3.0.0 "${ACR_NAME}.azurecr.io/login:v3.0.0"
```

**Step 3.** Push the updated and tagged image to your Azure Container Registry. 
```bash
docker push "${ACR_NAME}.azurecr.io/login:v3.0.0"
```

**Step 5.** Using your favorite text-editor, create a file called `subtask-03.yaml` using the [provided example](task-02/kubernetes/subtask-03.yaml) as inspiration.
```bash
vim kubernetes/subtask-03.yaml
```

**Step 3.** Apply the *new* Kubernetes configuration you just created to deploy your *updated* `login` image as a container as well as an init container on a pod in your Kubernetes cluster.
```bash
kubectl apply -f kubernetes/subtask-03.yaml
```

**Step 4.** Identify the IP address of the new LoadBalancer resource you defined previously. 
```bash
kubectl get svc
```

Your output should be similar to below.
```
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP      10.0.0.1       <none>        443/TCP        26h
login        LoadBalancer   10.0.247.191   4.255.92.5    80:31745/TCP   38s
mysql        ClusterIP      None           <none>        3306/TCP       71s
mysql-read   ClusterIP      10.0.94.146    <none>        3306/TCP       3h42m
```

**Step 5.** Test your *new* `login` container using `curl` and the IP address of your LoadBalancer resource. 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"asdasd"}' http://4.255.92.5/api/token/ 
```

Your output should be similar to below. 
```json
{"refresh":"eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTc0NzYwNSwiaWF0IjoxNzExNjYxMjA1LCJqdGkiOiI0YTQ0OTVjNWE0ZjA0NjgzYTFhMjg3OWQzNjZjYmYwMiIsInVzZXJfaWQiOjEsImlzcyI6ImxsbWxvZ2luIiwic3ViIjoiY2xpZW50In0.pJManSxsdzf6qM9HTgJnQclEbT3IDyZZh4ZvUA-zyoChU9IYn3yKRqgahWxGbnO9z5ldbESEuMe2d0GOC2WfWX9BIw_lPFuYjYJ6p-_PiG8KIAGqNw_SmBc10_mvV_iZZXwFqjZszFVTADhks3pchQMfvgF3SADs8Jgt8JE1U7jdQ_A9x23XaUYUQX20ZgiXTa9EKJi5TWCkc6n5PRX0-gp--GKWuALLsP3XlsSbqrq3JDRMptjOsQazHhLXs2tcR3HI-JqfRxP52EIlmV0mpLdrf8SOEgLDNIyXwmkBSPKhqWApWYjhWo6n14RU17hv-DZvVnbB4a1uhgevH7484Q","access":"eyJhbGciOiJSUzI1NiIsImtpZCI6InlvdXJjb29sa2lkIiwidHlwIjoiSldUIn0.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExNjYxNTA1LCJpYXQiOjE3MTE2NjEyMDUsImp0aSI6IjhjNGNiZDQxOWQ3OTRmZThiYzEyNmM5OWNmNGM3ODliIiwidXNlcl9pZCI6MSwiaXNzIjoibGxtbG9naW4iLCJzdWIiOiJjbGllbnQifQ.HewlfEjdKIyax_Fnsq2o1tZtGOgUus2eJ615xRd63oY5bmq0a78F0lVuJgqsERBuF9T1Zxo21ncgF9zNdBxZGdg13YotDgipzvyR1OxfhCcvjLUxR7WPz-CZ7B5xrFqC7r7Xx5AA20k8auUCAEZbKZhWB1IkWQGZZbV2UIn9s512vPOpeBb5575UuCY61o5O5TAW_dJjeSRE5rWgKv6gW-0YY6YT9-h9dlR06sThj2ltBuAO-PSqXkHm_SzVnVREx1iXzPGEmyTs35l5r0tiXQUo_FAUcy54hSSUyeHa4CEG71N2mCEbbMgppkjwLDgPlhKnnrzXciNQ_8hhbZ3H4Q"}
```

## Task 03
**Step 1.** Text goes here.

## Task 04
**Step 1.** Text goes here.