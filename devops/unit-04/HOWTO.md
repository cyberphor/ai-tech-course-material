# GitHub Actions

## Setup
### Setup an SSH Key  
**Step 1.** Create an SSH key pair. 
```bash
# -t: key type
# -b: key bit-length
# -C: comment
ssh-keygen -t rsa -b 4096 -C "for DevOps"
```

**Step 2.** Press "Enter" to save your private key to the default location (i.e., under `.ssh/id_rsa` within your home directory).  
  
**Step 3.** Enter a passphrase to encrypt the private key.  

**Step 4.** Open your BASH configuration file using your favorite text-editor
```bash
vim .bashrc
```

**Step 5.** Append the commands below to your BASH configuration file (they will be executed every time you login). 
```bash
eval "$(ssh-agent -s)" # start the SSH authentication agent
ssh-add ~/.ssh/id_rsa  # add my SSH private key to the SSH authentication agent
```

**Step 6.** Reload your environment (this will run the commands added to your BASH configuration file). 
```bash
source .bashrc
```

**Step 7.** Print your SSH public key to the console and copy it into memory.
```bash
cat ~/.ssh/id_rsa.pub
```

**Step 8.** Open a browser and login to GitHub.  

**Step 9.** Click your profile (top-right icon) and click "Settings."  

**Step 10.** Click "SSH and GPG keys" in the pane on the left-hand side.  

**Step 11.** Click "New SSH key."  

**Step 12.** Enter a "Title" (e.g., "for DevOps").  

**Step 13.** Click "Add SSH key" and go back to the CLI. 

### Clone a GitHub Repo Using SSH
**Step 1.** Define your environment variables. 
```bash
export GITUB_ORG="SAIL-Classroom"
export GITUB_REPO="intro-to-github-actions-cyberphor"
```

**Step 2.** Clone the GitHub repo using SSH. 
```bash
git clone git@github.com:${GITHUB_ORG}/${GITHUB_REPO}
```

### Create a GitHub Personal Access Token for the Submitter Program
**Step 1.** Login to GitHub.  
**Step 2.** Click your profile (top-right icon) and click "Settings."  
**Step 3.** Click "Developer Settings" at the bottom of the pane on the left-hand side.  
**Step 4.** Click "Personal access tokens" > "Tokens (classic)."  
**Step 5.** Click "Generate new token" > "Generate new token (classic)."  
**Step 6.** Enter a "Note" (e.g., "Submitter program").  
**Step 7.** Set the "Expiration" date (e.g., 60 days).  
**Step 8.** Select "repo" as the scope.  
**Step 9.** Click "Generate token."  

## Create a CI Pipeline Using a GitHub Actions Workflow
**Step 1.** Create two folders called `.github/` and `.github/workflows/`. 
```bash
mkdir -p .github/workflows/
```

**Step 2.** Create a file called `main.yml` under the `.github/workflow/` folder using the [provided GitHub Actions Workflow configuration file](/devops/week-11/task1.yml) as a template. 

**Step 3.** Commit the changes you made to your repository. 
```bash
git add .
git commit -m "Added a CI pipeline"
git push
```

## Create a CD Pipeline Using a GitHub Actions Workflow
**Step 1.** Create a web app using the Azure App Service. 
* Azure > App Service
  * Create > Web App
    * Basics
      * Project Details
        * Subscription: (your subscription)
          * Resource Group > Create new: `ghactions_app`
      * Instance Details
        * Name: `devopsweek11cyberphor`
        * Publish: "Code"
        * Runtime Stack: "Java 8"
        * Java web server stack: "Apache Tomcat 9.0"
        * Operating System: "Windows"
        * Region: "East US"
      * Pricing Plans
        * Windows Plan (East US): (use the value provided by default)
        * Pricing Plan: "Free F1 (Shared Infrastructure)"

**Step 2.** Create a service principal for your GitHub Actions runner to authenticate with when connecting to Azure. Copy the output to memory.
```bash
# define your environment variables
export SUBSCRIPTION_ID="17408d59-f3b6-43a5-a48c-c3667527f330"
export RESOURCE_GROUP="ghactions_app"
export SERVICE_PRINCIPAL_NAME="WebApp"
```
```bash
# create a service prinicpal
az ad sp create-for-rbac 
  --name "${SERVICE_PRINCIPAL_NAME}" \
  --role "contributor" \
  --scopes "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}" \
  --sdk-auth 
```

**Step 3.** Add the output of the previous step as a "Secret" to your Github repository (NOTE: if the name of your secret was `AZURE_CREDENTIALS`, the GitHub Actions Workflow would access it using `${{ secrets.AZURE_CREDENTIALS }}`).
* GitHub > (your repository) > Settings > Security > Secrets and variables > Actions
  * New repository secret
    * Name: `AZURE_CREDENTIALS`
    * Secret: (the output of the previous step)

**Step 4.** Create a file called `main.yml` under the `.github/workflow/` folder using the [provided GitHub Actions Workflow configuration file](/devops/week-11/task2.yml) as a template. 

**Step 5.** Commit the changes you made to your repository. 
```bash
git add .
git commit -m "Added a CD pipeline"
git push
```

## Create a CD Pipeline Using a GitHub Actions Workflow With a Matrix Strategy
**Step 1.** Create a file called `main.yml` under the `.github/workflow/` folder using the [provided GitHub Actions Workflow configuration file](/devops/week-11/task3.yml) as a template. 

**Step 5.** Commit the changes you made to your repository. 
```bash
git add .
git commit -m "Added a matrix strategy to the CD pipeline"
git push
```

## Create a CD Pipeline Using a GitHub Actions Workflow With Conditional Statements
**Step 1.** Create a file called `main.yml` under the `.github/workflow/` folder using the [provided GitHub Actions Workflow configuration file](/devops/week-11/task3.yml) as a template. 

**Step 2.** Commit the changes you made to your repository. 
```bash
git add .
git commit -m "Added conditional statements to the CD pipeline"
git push
```

**Step 3.** Create a new tag within the local instance of the repository. 
```bash
git tag v1.0
```

**Step 4.** Push the tags added to the local instance of the repository to the remote instance of the repository.
```bash
git push origin --tags
```

