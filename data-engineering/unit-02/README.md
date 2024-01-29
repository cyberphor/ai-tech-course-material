# Data Engineering
* [Setup](#setup)
  * [Using GitHub Codespaces](#using-github-codespaces)
  * [Not Using GitHub Codespaces](#not-using-github-codespaces)
* [Task 01](#task-01)
* [Task 02](#task-02)

## Setup
### Using GitHub Codespaces
Complete the steps below if you are using GitHub Codespaces. 

**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's project. 
```bash
# this command is meant to be ran in GitHub Codespaces
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-02/
```

**Step 2.** Run the [provided scripts](setup/ansible/scripts/). 
```bash
bash setup/ansible/scripts/Install-Unzip.sh
bash setup/ansible/scripts/Get-Handouts.sh
bash setup/ansible/scripts/Update-Python.sh
```

**Step 3.** Move the handout into the `task-01` folder. 
```bash
mv relational-databases-1 task-01/
```

**Step 4.** Change directories to `task-01`.
```bash
cd task-01/
```

### Not Using GitHub Codespaces
Complete the steps below if you are NOT using GitHub Codespaces. 

**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's project 
```bash
# this command is meant to be ran on your personal computer or Gi
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-02/setup/
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. 
```bash
# this command is meant to be ran on your personal computer 
# -t: defines the key pair type
# -b: defines the key lengths (i.e., the number of bits)
# -C: used to include a comment 
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. 
```bash
# these commands are meant to be ran on your personal computer
eval "$(ssh-agent -s)" # starts the SSH authentication agent
ssh-add ~/.ssh/id_rsa  # adds your SSH private key to the SSH authentication agent
```

**Step 4.** Install Ansible if you don't already have it installed. 
```bash
# this command is meant to be ran on your personal computer
python -m pip install ansible
```

**Step 5.** Login to the Azure CLI and set your subscription if you haven't already.
```bash
# this command is meant to be ran on your personal computer
az login --use-device-code
az account set --subscription "AI2C Subscription 3"
```

**Step 6.** Install the `Remote Development Extension Pack` VS Code Extension.

**Step 7.** Deploy a virtual machine in Azure using the [provided Terraform files](setup/terraform). 
```bash
# these commands are meant to be ran on your personal computer
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
export USERNAME=$(terraform -chdir=terraform output -raw username)
export IP_ADDRESS=$(terraform -chdir=terraform output -raw ip_address)
```

**Step 8.** Configure the virtual machine using Ansible. The [Ansible playbook](ansible/playbook.yaml) provided references multiple scripts in the [`ansible/scripts`](ansible/scripts/) folder. The scripts install software and download this week's handout.  
```bash
# this command is meant to be ran on your personal computer 
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

**Step 9.** Using your personal computer and the `Remote Development Extension Pack` VS Code extension, login to the virtual machine created above.

## Task 01
The steps below assume you've already downloaded this week's handout manually or automatically while executing the steps outlined above. 

**Step 1.** Change directories to this week's handout. 
```bash
# these commands are meant to be ran on the virtual machine created above or GitHub Codespaces
cd relational-databases-1/
```

**Step 2.** Create and invoke a Python virtual environment.
```bash
# these commands are meant to be ran on the virtual machine created above
python3 -m venv venv
source venv/bin/activate
```

**Step 3.** Install the Python requirements listed and upgrade Jupyter.
```bash
# these commands are meant to be ran on the virtual machine created above
python3 -m pip install -r requirements.txt
python3 -m pip install Jupyter --upgrade
python3 -m pip install Jupyter-core --upgrade
```

**Step 4.** Run Jupyter Notebook in the background (use the URL and token printed to the console to access your Jupyter Notebook).
```bash
jupyter notebook &
```

## Task 02
Text goes here.