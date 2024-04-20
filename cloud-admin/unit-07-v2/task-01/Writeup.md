## Task 01: Deploy a SQL Service in Azure
Before we get started with securing a SQL service, we need deploy one in Azure. Let's do this using the Azure Cloud Shell and Terraform. 

**Step 1.** Login to the Azure Portal and open the Azure Cloud Shell. 

**Step 2.** Create a folder called `terraform` and change your location in the file system to it. The sole purpose of this step is to keep your workspace tidy. As a cloud administrator, you will find yourself working on various tasks at the same time. Therefore, it's best practice to separate organize related files together using folders. For example, a common pattern you will see is a folder for source code, a folder for Docker, a folder for Terraform, a folder for Kubernetes, and so on.  
```bash
mkdir terraform
cd terraform
```

**Step 2.** Create and open a file called `main.tf` in the `terraform` directory.  