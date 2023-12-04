# Infrastructure as Code

## Training Objectives
Using Terraform
* Deploy and destroy a cloud resource
* Configure multiple cloud resources
* Configure a cloud resource using provisioners
* Deploy and manage replicated copies of infrastructure
* Deploy monitoring resources
* Configure and use remotely stored state 

## Concepts
**Infrastructure as Code**  
Infrastructure as Code (IAC) enhances your organization's ability to peform change management. It also allows you to automate the scaling of infrastructure. 

**Terraform**  
Text goes here. 

**Terraform Modules**  
A Terraform module is a folder with Terraform files inside of it. Modules allow you to organize and reuse resource configurations. 
* root module: the parent directory
* child module: any module that has been imported by another module

Modules are imported using the `module` block. Below is an example.
```hcl
module "servers" {
    version = 1               # optional
    source  = "./app-cluster" # required - defines the module file path
    servers = 5               # optional - an example of an "input variable" (specific to the "app-cluster" module)
}
```

**Terraform Module Input Variables**  
Module input variables are defined in the root module's `variables.tf` file. 

**Provisioner**  
Text goes here. 

**Terraform Workspaces**  
Text goes here. 

## Solutions
* [Setup](/devops/week-14/HOWTO.md)
* [Task 1](/devops/week-14/HOWTO.md#task-1)
* [Task 2](/devops/week-14/HOWTO.md#task-2)
* [Task 3](/devops/week-14/HOWTO.md#task-3)
* [Task 4](/devops/week-14/HOWTO.md#task-4)
* [Task 5](/devops/week-14/HOWTO.md#task-5)