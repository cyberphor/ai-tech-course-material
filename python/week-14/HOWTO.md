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

## How to Print All Columns in a pandas DataFrame
```python
import pandas

data = pandas.read_csv("wdi_data/worldDevInds2017-education.csv")
columns = pandas.DataFrame(data.head())
for column in columns:
    print(column)
```

## How to Print All Sheet Names in a XLSX File Using Pandas
```python
import pandas

workbook = pandas.ExcelFile("wdi_data/healthWorld-2017-worldBank.xlsx")
for name in sorted(workbook.sheet_names):
    print(name)
```

## Task 1
**Step 1.** Run [the provided script](/python/week-14/ppp-p8-data-analysis/task_01.py).

## Task 2
**Step 1.** Run [the provided script](/python/week-14/ppp-p8-data-analysis/task_02.py).

## Task 3
**Step 1.** Run [the provided script](/python/week-14/ppp-p8-data-analysis/task_03.py).
