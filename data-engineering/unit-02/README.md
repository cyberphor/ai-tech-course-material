# Data Engineering
* [Setup](#setup)
  * [Using GitHub Codespaces](#using-github-codespaces)
  * [Not Using GitHub Codespaces](#not-using-github-codespaces)
* [Task 01](#task-01)
* [Task 02](#task-02)

## Setup
### Using GitHub Codespaces
Complete the steps below if you are using GitHub Codespaces. 

**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's project. This command is meant to be ran in GitHub Codespaces.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-02/
```

**Step 2.** Run the [provided scripts](setup/ansible/scripts/). 
```bash
bash setup/ansible/scripts/Update-Python.sh
bash setup/ansible/scripts/Install-Unzip.sh
bash setup/ansible/scripts/Install-Mysql.sh
bash setup/ansible/scripts/Get-Handouts.sh
```

**Step 3.** Create a Python virtual environment.
```bash
cd relational-databases-1/
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install Jupyter --upgrade
python3 -m pip install Jupyter-core --upgrade
```

### Not Using GitHub Codespaces
Complete the steps below if you are NOT using GitHub Codespaces. 

**Step 1.** Download the `vic-code` GitHub repository and change directories to this week's project. These commands are meant to be ran on your personal computer.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-02/setup/
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. This command is meant to be ran on your personal computer. `-t` defines the key pair type. `-b` defines the key lengths (i.e., the number of bits). `-C` is used to include a comment. 
```bash
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. These commands are meant to be ran on your personal computer.
```bash
eval "$(ssh-agent -s)" # starts the SSH authentication agent
ssh-add ~/.ssh/id_rsa  # adds your SSH private key to the SSH authentication agent
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

**Step 6.** Install the `Remote Development Extension Pack` VS Code Extension.

**Step 7.** Deploy a virtual machine in Azure using the [provided Terraform files](setup/terraform). These commands are meant to be ran on your personal computer.
```bash
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
export USERNAME=$(terraform -chdir=terraform output -raw username)
export IP_ADDRESS=$(terraform -chdir=terraform output -raw ip_address)
```

**Step 8.** Configure the virtual machine using Ansible. The [Ansible playbook](ansible/playbook.yaml) provided references multiple scripts in the [`ansible/scripts`](ansible/scripts/) folder. The scripts install software and download this week's handout. This command is meant to be ran on your personal computer.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

**Step 9.** Using your personal computer and the `Remote Development Extension Pack` VS Code extension, login to the virtual machine created above.

**Step 10.** Create a Python virtual environment.
```bash
cd relational-databases-1/
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install Jupyter --upgrade
python3 -m pip install Jupyter-core --upgrade
```

## Task 01
The steps below assume you've already downloaded this week's handout manually or automatically while executing the steps outlined above. 

**Step 1.** Change directories to this week's handout and invoke your Python virtual environment if you haven't already. This command is meant to be ran on the virtual machine created above or GitHub Codespaces.
```bash
cd relational-databases-1/
source venv/bin/activate
```

**Step 2.** Run Jupyter Notebook in the background (use the URL and token printed to the console to access your Jupyter Notebook).
```bash
jupyter notebook &
```

**Step 4.** Edit `data_cleaning.ipynb` using the [provided example](task-01/relational-databases-1/data_cleaning.ipynb).

**Step 4.** Before submiting your work for Task 01, run the command below. 
```bash
jupyter nbconvert --to script data_cleaning.ipynb
```

## Task 02
Use an Azure virtual machine instead of GitHub Codespaces for this task. Execute the setup steps in the [Not Using GitHub Codespaces](#not-using-github-codespaces) instructions above. Then, login to the virtual machine using SSH (`ssh $USERNAME@$IP_ADDRESS`).

**Step 1.** Change directories to `relational-databases-1/`. 
```bash
cd relational-databases-1/
```

**Step 2.** Run the commands below to configure the local MySQL server.
```bash
sudo mysql -e "use mysql; CREATE USER 'clouduser'@'localhost' IDENTIFIED BY 'dbroot'; GRANT ALL PRIVILEGES ON *.* TO 'clouduser'@'localhost' WITH GRANT OPTION; CREATE USER 'clouduser'@'%' IDENTIFIED BY 'dbroot'; GRANT ALL PRIVILEGES ON *.* TO 'clouduser'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;"
sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.backup
sudo sed -i 's/^[^#]*bind-address/#&/' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo sed -i '/^\[mysqld\]/alocal_infile = 1' /etc/mysql/mysql.conf.d/mysqld.cnf
echo "[client]" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf
echo "local_infile = 1" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf
set global local-infile=1
sudo service mysql restart
sudo mysql -u clouduser -pdbroot < create_security_database.sql
```

**Step 3.** Load the `load_tickerInfo_time_series.sql` file. 
```bash
mysql -u clouduser -pdbroot < load_tickerInfo_time_series.sql
```

If you get the error `ERROR 2 (HY000) at line 7: File 'tickerInfo.csv' not found (OS errno 2 - No such file or directory)`, copy your `data_cleaning.ipynb` to your your virtual machine. Then, run the commands below one at a time. 
```bash
source venv/bin/activate
jupyter nbconvert --to script data_cleaning.ipynb
python3 data_cleaning.py
```

**Step 4.** Run the commands below one at a time to verify the previous step worked.
```bash
mysql -u clouduser -pdbroot -e "USE security_db; SELECT COUNT(*) FROM ticker_info;"
```
```bash
mysql -u clouduser -pdbroot -e "USE security_db; SELECT COUNT(*) FROM time_series;"
```

**Step 5.** Edit `q6.sql` using the [provided example](task-02/q6.sql).

**Step 6.** Edit `q7.sql` using the [provided example](task-02/q7.sql).

**Step 7.** Edit `q8.sql` using the [provided example](task-02/q8.sql).

**Step 8.** Edit `q9.sql` using the [provided example](task-02/q9.sql).

**Step 9.** Edit `q10.sql` using the [provided example](task-02/q10.sql).