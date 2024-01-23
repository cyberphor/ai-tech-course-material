---
tags: ["azure", "terraform", "kubernetes"]
---

## Cloud-Native
## Setup
**Step 1.** Install Ansible. 
```bash
sudo python -m pip install ansible
```

## Task 01
**Step 1.** Deploy a virtual machine in Azure using Terraform.
```bash
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
export USERNAME=$(terraform -chdir=terraform output -raw username)
```

**Step 2.** Configure to the virtual machine using Ansible.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

## Task 02
**Step 1.** Text goes here.

## Task 03
**Step 1.** Text goes here.

## Task 04
**Step 1.** Text goes here.