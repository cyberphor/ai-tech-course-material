# Data Engineering
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)

## Setup
**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's task. 
```bash
# this command is meant to be ran on your personal computer (or GitHub Codespace)
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-02/setup/
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. 
```bash
# this command is meant to be ran on your personal computer (or GitHub Codespace)
# -t: defines the key pair type
# -b: defines the key lengths (i.e., the number of bits)
# -C: used to include a comment 
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. 
```bash
# these commands are meant to be ran on your personal computer (or GitHub Codespace)
eval "$(ssh-agent -s)" # starts the SSH authentication agent
ssh-add ~/.ssh/id_rsa  # adds your SSH private key to the SSH authentication agent
```

**Step 4.** Install Ansible if you don't already have it installed. 
```bash
# this command is meant to be ran on your personal computer (or GitHub Codespace)
python -m pip install ansible
```

**Step 5.** Login to the Azure CLI and set your subscription if you haven't already.
```bash
# this command is meant to be ran on your personal computer (or GitHub Codespace)
az login --use-device-code
az account set --subscription "AI2C Subscription 3"
```

## Task 01
**Step 1.** Deploy a virtual machine in Azure using the [provided Terraform files](setup/terraform). 
```bash
# these commands are meant to be ran on your personal computer (or GitHub Codespace)
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
export USERNAME=$(terraform -chdir=terraform output -raw username)
export IP_ADDRESS=$(terraform -chdir=terraform output -raw ip_address)
```

**Step 2.** Configure the virtual machine using Ansible. The [Ansible playbook](ansible/playbook.yaml) provided references multiple scripts in the [`ansible/scripts`](ansible/scripts/) folder. The scripts install software and download this week's handout.  
```bash
# this command is meant to be ran on your personal computer (or GitHub Codespace)
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

**Step 3.** Login to the virtual machine created above. 
```bash
# this command is meant to be ran on your personal computer (or GitHub Codespace)
ssh $USERNAME@$IP_ADDRESS
```

**Step 4.** Change directories to this week's handout, install the Python requirements listed, and create a Python virtual environment. 
```bash
# these command are meant to be ran on the virtual machine created above
cd relational-databases-1/
sudo apt install python3-venv -y
python3 -m venv venv
```

## Task 02
Text goes here.