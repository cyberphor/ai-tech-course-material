# Data Stores

## Setup
**Step 1.** Download the provided source code. 
```bash
wget https://principlesofcomputing.blob.core.windows.net/ppp-p6-files-datastores/handout/sail2/ppp-p6-files-datastores.zip
```

Use the command below if you're using PowerShell
```powershell
Invoke-WebRequest -URI https://principlesofcomputing.blob.core.windows.net/ppp-p6-files-datastores/handout/sail2/ppp-p6-files-datastores.zip -oOutfile ppp-p6-files-datastores.zip
```

**Step 2.** Open the source code. 
```bash
unzip ppp-p6-files-datastores.zip
```

Use the command below if you're using PowerShell.
```powershell
Expand-Archive ppp-p6-files-datastores.zip -DestinationPath .
```

**Step 3.** Activate the provided Python virtual environment. 
```bash
cd ppp-p6-files-datastores/
python -m venv p6-env
source p6-env/bin/activate
```

Use the commands below if you're using PowerShell. 
```powershell
cd ppp-p6-files-datastores/
python -m venv p6-env
./p6-env/Scripts/Activate.ps1
```

**Step 4.** Download the provided source code's dependencies. 
```bash
python -m pip install wheel
python -m pip install -r requirements.txt
python -m pip install mysql-connector-python
```

**Step 5.** Install MySQL server. 
```bash
sudo apt update
sudo apt install -y mysql-server
```

**Step 6.** Create a new privileged user for the MySQL server. 
```bash
vim create-priv-user.sql
```
```sql
use mysql;
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbroot';
GRANT ALL PRIVILEGES ON *.* TO 'dbuser'@'localhost' WITH GRANT OPTION;
```
```bash
sudo mysql < create-priv-user.sql
```

**Step 7.** Verify you can login using the new credentials. 
```bash
# password is "dbroot"
mysql -u dbuser -p
```

## Task 1
**Step 1.** Create a Python script called `books_retrieval.py` using inspiration from the [source code shared](/python/week-12/ppp-p6-files-datastores/books_retrieval.py). 
```bash
touch books_retrieval.py
```

**Step 2.** Execute the Python script. 
```bash
python books_retrieval.py
```

## Task 2
**Step 1.** Create a file called `data_loading.py` using inspiration from the [source code shared](/python/week-12/ppp-p6-files-datastores/data_loading.py). 
```bash
touch data_loading.py
```

**Step 2.** Execute the Python script. 
```bash
python data_loading.py
```

**Step 3.** Verify the database and table were required created. 
```bash
sudo mysql < sql-print-database-schema.sql
```

**Step 4.** Verify the table was loaded with data. 
```bash
sudo mysql < sql-print-table.sql
```

## Task 3