# Containers

## Training Objectives
* Describe Docker
* Describe Kubernetes
* Describe how a developer uses Docker and Kubernetes to implement Microservice Architectures (MSA) 
* Describe the development and deployment lifecycle of a MSA
* Build container images
* Push container images into an Azure Container Registry
* Provision, configure, and manage a Kubernetes cluster
* Deploy microservices onto a Kubernetes cluster
* Use GitHub Actions to create a CI/CD pipeline for a containerized microservice
* Implement CD for an environment with immutable infrastructure

**Container**  
A container is an instance of a container image. Specifically, it's a collection of processes. Containers provide the most value in service-based architectures because they are small. The smaller your codebase, the easier and faster it is to build, test, and deploy it. 

**Container Image**  
A container image is a compiled program. 

**Dockerfile**  
A Dockerfile contains the instructions for building a specific container image. 

**Docker Engine**  
The Docker Engine builds container images using Dockerfiles. 

**Azure Container Registry**  
An Azure Container Registry is a resource for storing container images. 

**Kubernetes**  
Kubernetes is a tool for managing containers. Using Kubernetes is a two-step process. 
1. Users define requirements for their service-based architecture (i.e., container cluster) using declarative syntax in a YAML format
2. Kubernetes deploys and manages the containers needed to meet the user's requirements (i.e, the *desired state* of their app)

**Kubernetes Objects**  
Kubernetes represents requirements as objects. 

**Kubernetes Object Types**   
Below is a list of common types of Kubernetes object.  

*Node*  
A node is a physical or virtual machine within the cluster. 

*Pod*  
A pod is one or more containers. 

*Service*  
A service is one or more pods. 

*Deployment*  
A deployment is a running instance of a service (i.e., one or more running containers)

**Kubernetes Object Fields**  
Every object definition must include the fields described below. 

*apiVersion*  
The `apiVersion` field defines which version of the Kubernetes API to use. 

*kind*  
The `kind` field defines the type of object Kubernetes must create and manage. 

*metadata*  
The `metadata` field defines unique identifiers for the object. 

*spec*  
The `spec` field defines the object's characteristics (e.g., fault-tolerance).

**Azure Kubernetes Service**  
Azure Kubernetes Service (AKS) is used to deploy and operate Kubernetes clusters. 

**Mutable Infrastructure**  
Mutable infrastructure is infrastructure that changes. Changes are bolted-on and implemented manually. 

**Immutable Infrastructure**  
Immutable infrastructure is infrastructure that cannot change. Changes are baked-in using automation and redeployments. Containers faciliate immutable infrastructure. 

## Solutions
* [Setup](/devops/week-12/HOWTO.md#setup)
* [Task 1: Build container images and push them to a container registry](/devops/week-12/HOWTO.md#task-1)
* [Task 2: Provision a Kubernetes cluster](/devops/week-12/HOWTO.md#task-2)
* [Task 3: Deploy microservices onto a Kubernetes cluster](/devops/week-12/HOWTO.md#task-3)
* [Task 4: Use GitHub Actions to create a CI/CD pipeline for a containerized app](/devops/week-12/HOWTO.md#task-4)
* [Task 5: Demonstrate CD for an environment with immutable infrastructure](/devops/week-12/HOWTO.md#task-5)