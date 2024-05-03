# AI Practitioner: Deep Learning For Computer Vision
The purpose of this project is to describe how to build and deploy a Convolutional Neural Network (CNN) model using Azure, PyTorch, and the CIFAR-10 dataset. 
* [Notes](#notes)
* [References](#references)
* [Setup](#setup)

## Notes
If I learn anything new, I will put it here until I migrate the topic to my public [Knowledge Base](https://github.com/cyberphor/knowledge-base).

## References
If I find any helpful references, I will put them here.

## Setup
This document assumes (1) you're using a Linux-based environment (GitHub Codespaces, Azure Shell, Windows Subsystem for Linux, etc.), (2) you've installed the software required for this recipe (i.e., Terraform and the Azure CLI), (3) you've forked this repository, (4) you've downloaded this repository, and (5) you're starting in the root folder of this project folder.

**Step 1.** Define environment variables for your infrastructure. I usually save my environment variables in a file called something like `.env` and run `source .env` as needed. This makes it easy to pick up where I left off after leaving my workspace for an extended period of time. If you didn't know, the `source` command reads and executes shell commands from the file you provide it.   
```bash
export SUBSCRIPTION_ID="c60c349f-4b5c-4e39-98cb-4fc2323804c5"
```
 
**Step 2.** Login to Azure using the CLI. 
```bash
az login --use-device-code
```

**Step 3.** Set your subscription.
```bash
az account set --subscription "${SUBSCRIPTION_ID}"
```

**Step 4.** Initialize the `setup/terraform` folder for Terraform-use. 
```bash
terraform -chdir=setup/terraform init
```

**Step 5.** Create and apply a Terraform execution plan using the provided Terraform configuration.
```bash
terraform -chdir=setup/terraform apply
```

**Step 6.** Login to the Azure Portal and click-on the resource group created in the previous step. 

**Step 7.** Click the Azure Machine Learning Workspace resource.

**Step 8.** Click "Launch studio."

**Step 9.** Under "Authoring", click "Notebooks."

**Step 10.** Click "Terminal."

**Step 11.** Copy and paste the command below into your shell environment to download the provided Jupyter Notebook.
```bash
wget -qc https://aipractitioner.blob.core.windows.net/ai-practitioner-cv-model-deployment/sail2/v1/ai-practitioner-cv-model-deployment.tgz -O - | tar -xz -C .
```

**Step 12.** Copy and paste the command below into your shell environment to install the Python dependencies required for this project.
```bash
pip install -r requirements.txt
```

**Step 13.** Open the file called `model_deployment_comparison.ipynb` and authenticate if prompted.