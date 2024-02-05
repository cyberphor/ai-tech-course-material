# Cloud Native
**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's project. These commands are meant to be ran on your personal computer.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/cloud-native/unit-02/setup/
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. This command is meant to be ran on your personal computer. `-t` defines the key pair type. `-b` defines the key lengths (i.e., the number of bits). `-C` is used to include a comment. 
```bash
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. These commands are meant to be ran on your personal computer. The first command starts the SSH authentication agent while the second command adds your SSH private key to it.
```bash
eval "$(ssh-agent -s)" 
ssh-add ~/.ssh/id_rsa  
```

**Step 4.** Install Ansible if you don't already have it installed. These commands are meant to be ran on your personal computer.
```bash
python -m pip install ansible
```

**Step 5.** Login to the Azure CLI and set your subscription if you haven't already. These commands are meant to be ran on your personal computer.
```bash
az login --use-device-code
az account set --subscription "AI2C Subscription 3"
```

**Step 6.** Deploy a virtual machine in Azure using the [provided Terraform files](setup/terraform). These commands are meant to be ran on your personal computer.
```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply -auto-approve
export USERNAME=$(terraform -chdir=terraform output -raw username)
export IP_ADDRESS=$(terraform -chdir=terraform output -raw ip_address)
```

**Step 7.** Configure the virtual machine using Ansible. The [Ansible playbook](ansible/playbook.yaml) provided references multiple scripts in the [`ansible/scripts`](ansible/scripts/) folder. The scripts install software and download this week's handout. This command is meant to be ran on your personal computer.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

## Task 1
**Step 1.** Connect to the virtual machine you just created and change directories to `llmservice-handout`. 
```bash
cd llmservice-handout/
```

**Step 2.** Invoke the Python virtual environment created by Ansible and then change directories to `worker/src`. 
```bash
source venv/bin/activate
cd worker/src
```

**Step 3.** Edit the `simplellm.py` file using the [provided example](task-01/simplellm.py).

**Step 4.** Start a local Flask server as a background process. 
```bash
flask --app simplellm run --debug &
```

**Step 5.** Query the `healthcheck` endpoint of your Flask-based application. 
```bash
curl http://127.0.0.1:5000/healthcheck
```

**Step 6.** Query the `API` endpoint of your Flask-based application. 
```bash
curl -G --data-urlencode message="what is 1 + 1?" http://localhost:5000/api
```

The output should be similar to below. If these queries worked, stop your Flask server. 
```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "\nYes, the answer to your question is 1 + 1 = 2."
    }
  ],
  "created": 1707148633,
  "id": "cmpl-85a9a50a-35bf-419f-9bf4-110372ba8122",
  "model": "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 18,
    "prompt_tokens": 35,
    "total_tokens": 53
  }
}
```

**Step 7.** Edit the `pyproject.toml` file using the [provided example](task-01/pyproject.toml).

**Step 8.** Change directories to `worker` (the parent directory of `src`, your current working directory).
```bash
cd ../
```

**Step 9.** Build your Flask-based application and save the artifact in folder called `dist/`.
```bash
python3 -m pip wheel src/ -w dist/
```

**Step 10.** Validate your artifact was built correctly by importing it using `pip` 
```bash
python3 -m pip install dist/simplellm-1.0.0-py2.py3-none-any.whl
```

**Step 11.** Change directories back to `src` and serve your imported artifact as a background process using `waitress`. 
```bash
cd src/
waitress-serve simplellm:app &
```

**Step 12.** Test your imported artifact now that it's being served by `waitress`. Pay attention to the change in port number. 
```bash
curl -G --data-urlencode message="what is 1 + 1?" http://localhost:8080/api
```

## Task 2
**Step 1.** Text goes here.

## Task 3
**Step 1.** Text goes here.

## Task 4
**Step 1.** Text goes here.