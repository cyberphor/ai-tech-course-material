# Incident Response

## Setup
**Step 1.** Login to the Azure Cloud Shell. 

**Step 2.** Using [the instructions provided](/SETUP.md#how-to-create-ssh-keys), create an SSH key pair and then add your SSH public key to your GitHub profile.

**Step 3.** Clone the GitHub repository provided. 
```bash
git clone git@github.com:sail-classroom/continuous-monitoring-cyberphor
```

## Task 1
In this task, you're going to use Terraform to provision the following:
* Azure App Service Plan
* Azure Linux Web App Service
* Azure Application Insights

**Step 1.** Initialize your Terraform configuration using the [provided Terraform configuration file](/devops/week-15/task-01/main.tf) after updating line 57. 
```bash
cd terraform/
terraform init
```

**Step 2.** Generate a Terraform execution plan.  
```bash
terraform plan
```

**Step 3.** Apply your Terraform execution plan.
```bash
terraform apply
cd ../
```

**Step 4.** Verify your web app was deployed. 
```bash
export WEB_APP_NAME="devopsweek15cyberphor"
curl "https://${WEB_APP_NAME}.azurewebsites.net"
```

## Task 2
In this task, you're going to do the following:
* Update a provided GitHub Actions workflow configuration file

**Step 1.** Login to Azure and download your web app's publish profile. 

**Step 2.** Login to GitHub and create a "repository secret" called `AZURE_WEBAPP_PUBLISH_PROFILE`. For the "Secret" field, copy/paste the contents of your web app's publish profile. 
* Settings
  * Secrets and variables > Actions
    * New repository secret

**Step 3.** Replace the default GitHub Actions workflow configuration file with [the one provided](/devops/week-15/task-02/main.yml). 

**Step 4.** Commit the changes made so far. 
```bash
git add .
git commit -m "Task 2"
git push
```

**Step 5.** Verify the web app is working as expected. 
```bash
export WEB_APP_NAME="devopsweek15cyberphor"
curl "https://${WEB_APP_NAME}.azurewebsites.net/todos"
curl "https://${WEB_APP_NAME}.azurewebsites.net/todos/2"
```

## Task 3
In this task, you're going to do the following:
* Text goes here

**Step 1.** Text goes here.