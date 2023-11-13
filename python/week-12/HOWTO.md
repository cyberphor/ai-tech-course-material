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
```

## Task 1
**Step 1.** Create a file called `books_retrieval.py`. 
```bash
touch books_retrieval.py
```

Use the command below if you're using PowerShell. 
```powershell
New-Item -Type File books_retrieval.py
```

## Task 2

## Task 3