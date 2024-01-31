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
bash setup/ansible/scripts/Set-MySqlServerConfig.sh
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
Use an Azure virtual machine instead of GitHub Codespaces for this task. Execute the setup steps in the [Not Using GitHub Codespaces](#not-using-github-codespaces) instructions above. Then, login to the virtual machine. 

**Step 1.** Change directories to `relational-databases-1/` if you're not already there.
```bash
cd relational-databases-1/
```

**Step 2.** Using the command below, load the `load_tickerInfo_time_series.sql` file. This could take up to an hour to finish. I included the `date` command to help track how much time has passed. 
```bash
date && mysql -u clouduser -pdbroot < load_tickerInfo_time_series.sql && date
```

**Step 3.** Run the command below to verify the `tickerInfo.csv` was loaded into the local SQL database.
```bash
mysql -u clouduser -pdbroot -e "SELECT COUNT(*) FROM security_db.ticker_info;"
```

**Step 4.** Run the command below to verify the `outputTimeSeries.csv` was loaded into the local SQL database.
```bash
mysql -u clouduser -pdbroot -e "SELECT COUNT(*) FROM security_db.time_series;"
```

**Step 5.** Edit `q6.sql` using the [provided example](task-02/q6.sql).

**Step 6.** Using the command below, load the `nasdaqlistedMod.txt` and `otherlistedMod.txt` files. 
```bash
mysql -u clouduser -pdbroot < q6.sql
```

**Step 7.** Run the command below to verify the previous step worked. 
```bash
mysql -u clouduser -pdbroot -e "SELECT * FROM security_db.nasdaq_info ORDER BY id LIMIT 10;"
```

**Step 8.** Edit `q7.sql` using the [provided example](task-02/q7.sql).

**Step 9.** Using the command below, drop the `open_int` column from the `time_series` table. 
```bash
mysql -u clouduser -pdbroot < q7.sql
```

**Step 10.** Run the command below to verify the previous step worked.
```bash
mysql -u clouduser -pdbroot -e "DESCRIBE security_db.time_series;"
```

**Step 11.** Edit `q8.sql` using the [provided example](task-02/q8.sql).

**Step 12.** Using the command below, delete records in the `other_exchange_info` table where the `exchange` column has `Z` (BATS Global Markets) or `V` (Investors' Exchange, LLC) in it. This mapping is documented in the [Other Exchange-Listed Securities](http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs) section on "NASDAQ Trader's" website.
```bash
mysql -u clouduser -pdbroot < q8.sql
```

**Step 13.** Run the command below to verify the previous step worked.
```bash
mysql -u clouduser -pdbroot -e "SELECT COUNT(*) FROM security_db.other_exchange_info;"
```

**Step 14.** Edit `q9.sql` using the [provided example](task-02/q9.sql).

**Step 15.** Using the command below, add a column called `exchange` to the `nasdaq_info` table. The data type for this column must be `enum`. Also the acceptable options for it `A, N, P, Q` (`Q` should be the default value).
```bash
mysql -u clouduser -pdbroot < q9.sql
```

**Step 16.** Run the command below to verify the previous step worked.
```bash
mysql -u clouduser -pdbroot -e "DESCRIBE security_db.nasdaq_info;"
```

**Step 17.** Edit `q10.sql` using the [provided example](task-02/q10.sql).

**Step 18.** Using the command below, 
```bash
mysql -u clouduser -pdbroot < q10.sql
```

**Step 19.** Run the command below verify the previous step worked.
```bash
mysql -u clouduser -pdbroot -e "SELECT COUNT(*) FROM security_db.nasdaq_info;"
```