# Data Engineering: Data Processing with Spark
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)

## Setup
**Step 1.** Download the `vic-code` GitHub repository and change directories to setup folder for this week's project. These commands are meant to be ran on your personal computer or GitHub Codespace.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-04/setup
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. This command is meant to be ran on your personal computer. `-t` defines the key pair type. `-b` defines the key lengths (i.e., the number of bits). `-C` is used to include a comment. 
```bash
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. These commands are meant to be ran on your personal computer. The first command starts the SSH authentication agent while the second command adds your SSH private key to it.
```bash
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa  
```

**Step 4.** Install Ansible if you don't already have it installed. This command is meant to be ran on your personal computer.
```bash
python -m pip install ansible
```

**Step 5.** Login to the Azure CLI if you haven't already. This command is meant to be ran on your personal computer.
```bash
az login --use-device-code
```

**Step 6.** Set your subscription if you haven't already. This command is meant to be ran on your personal computer.
```bash
az account set --subscription "AI2C Subscription 3"
```

**Step 7.** Initialize the `terraform` directory for Terraform use by installing the necessary Terraform plugins and modules. This command is meant to be ran on your personal computer. 
```bash
terraform -chdir=terraform init
```

**Step 8.** Create the cloud resources needed for this week's project using the [provided Terraform configuration](setup/terraform/main.tf). This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
terraform -chdir=terraform apply -auto-approve
```

**Step 9.** Save the `username` of the virtual machine (that was created by Terraform) as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export USERNAME=$(terraform -chdir=terraform output -raw username)
```

**Step 10.** Save the `ipaddress` of the virtual machine (that was created by Terraform) as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export IPADDRESS=$(terraform -chdir=terraform output -raw ipaddress)
```

**Step 11.** Save the `DATABRICKS_HOST` determined by Terraform as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export DATABRICKS_HOST=$(terraform -chdir=terraform output -raw databricks_host)
```

**Step 12.** Save the `DATABRICKS_TOKEN` created via by Terraform as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export DATABRICKS_TOKEN=$(terraform -chdir=terraform output -raw databricks_token)
```

**Step 13.** Use Ansible and the provided [Ansible playbook](ansible/playbook.yaml) to configure the virtual machine. The [scripts](setup/ansible/scripts/) listed in the Ansible playbook install software and download this week's handouts. This command is meant to be ran on your personal computer and from the `setup` directory.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

**Step 14.** Save the environment variables you created to a file so you can use them again in the future (the example below saves them to a file called `.env` in the parent directory of `setup`). For example, if you lose your environment (e.g., reboot your personal computer), you can get your environment variables back by running `source .env` (from whatever directory you create said `.env` file). Also, the filename `.env` is not special. You could call the file where you store your environment variables whatever you want. Lastly, it would also be helpful to save your Sail() submission credentials to this file too. 
```bash
echo "export USERNAME=$USERNAME" >> ../.env &&\
echo "export IPADDRESS=$IPADDRESS" >> ../.env &&\
echo "export DATABRICKS_HOST=$DATABRICKS_HOST" >> ../.env &&\
echo "export DATABRICKS_TOKEN=$DATABRICKS_TOKEN" >> ../.env
```

**Step 15.** Login to the virtual machine.
```bash
ssh $USERNAME@$IPADDRESS
```

## Task 01
**Step 1.** Text goes here.

## Task 02
**Step 1.** Text goes here.

## Task 03
**Step 1.** Text goes here.

## Task 04