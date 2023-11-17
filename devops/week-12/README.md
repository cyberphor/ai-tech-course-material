# CI/CD Pipeline for a Containerized Microservice

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
Kubernetes is a tool for managing containers. 

**Azure Kubernetes Service**  
Azure Kubernetes Service (AKS) is used to deploy and operate Kubernetes clusters. 

## Solutions
* [Setup](/devops/week-12/HOWTO.md#setup)
* [Task 1: Build container images and push them to a container registry](/devops/week-12/HOWTO.md#task-1)
* [Task 2: Provision a Kubernetes cluster](/devops/week-12/HOWTO.md#task-2)
* [Task 3: Deploy microservices onto a Kubernetes cluster](/devops/week-12/HOWTO.md#task-3)
* [Task 4: Use GitHub Actions to create a CI/CD pipeline for a containerized microservice](/devops/week-12/HOWTO.md#task-4)
* [Task 5: Implement CD for an environment with immutable infrastructure](/devops/week-12/HOWTO.md#task-5)