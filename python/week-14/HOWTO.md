# Data Analysis

## Setup
**Step 1.** Download the provided content. 
```bash
wget https://principlesofcomputing.blob.core.windows.net/ppp-p8-data-analysis/handout/sail2/v2/ppp-p8-data-analysis.zip
```

**Step 2.** Open the content. 
```bash
unzip ppp-p8-data-analysis.zip
```

**Step 3.** Activate the Python virtual environment. 
```bash
cd ppp-p8-data-analysis
python -m venv p8-env
source p8-env/bin/activate
```

**Step 4.** Download the provided source code's dependencies. 
```bash
python -m pip install -r requirements.txt --user
```

**Step 5.** Install the Jupyter VS Code extension. Configure it to use the virtual environment you activated previously. 

## Task 1
In this task, you're going to do the following:
* Load data from the file types listed below into `.pkl` (Pickle) files
  * CSV
  * XLSX
  * JSON
  * XML
* Merge multiple pandas DataFrames together
* Store the new DataFrames created into `.pkl` files

### How to Print All Columns in a pandas DataFrame
```python
import pandas

data = pandas.read_csv("wdi_data/worldDevInds2017-education.csv")
columns = pandas.DataFrame(data.head())
for column in columns:
    print(column)
```

### How to Print All Sheet Names in a XLSX File Using Pandas
```python
import pandas

workbook = pandas.ExcelFile("wdi_data/healthWorld-2017-worldBank.xlsx")
for name in sorted(workbook.sheet_names):
    print(name)
```

## Task 2

## Task 3