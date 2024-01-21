# Data Engineering
## Task 01
**Step 1.** Deploy a virtual machine in Azure and login to it. 
```bash
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
ssh clouduser@$VM_IP_ADDRESS
```

**Step 2.** Download, unzip, and change directories to the provided data set for Task 1. 
```bash
wget https://clouddataengineer.blob.core.windows.net/data-exploration/handout/project-data-exploration.zip
unzip project-data-exploration.zip
cd project-data-exploration/task1
```

**Step 3.** Update the `find_confidential.sh` script so it includes the command below. 
```bash
grep -i -r -l "confidential" emails
```

**Step 4.** Update the `count_confidential.sh` script so it includes the command below. 
```bash
grep -i -r -l "confidential" emails | wc -l
```

**Step 5.** Update the `find_phone_numbers.sh` script so it includes the command below. 
```bash
grep -i -r -l -P '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b' emails
```

**Step 6.** Update the `count_phone_numbers.sh` script so it includes the command below. 
```bash
grep -i -r -l -P '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b' emails | wc -l
```

**Step 7.** Update the `hide_phone_numbers.sh` script so it includes the command below. 
```bash
# -r tells sed to use extended regular expressions (so you don't have to escape everything)
# \b defines a boundary
# \W* zero or more non-word characters
# [0-9]{3} three numbers
sed -r 's/\b[0-9]{3}\W*[0-9]{3}\W*[0-9]{4}\b/<PHONE_REMOVED>/gI' anon_"$file_name"_ > anon_"$file_name"
```

**Step 8.** Update the `find_course.sh` script so it includes the command below. 
```bash
awk -F '\t' '$2 ~ /Python/ && $4 == "False" {print $2}' udemy_courses_v2.csv 
```

## Task 02
<<<<<<< HEAD
**Step 1.** Download, unzip, and move the data set for Task 2 to the "project-data-exploration" folder.  
```bash
wget https://principlesofcomputing.blob.core.windows.net/data-exploration-dataset-zip/dataset.zip
unzip dataset.zip
mv airlines.csv airports.csv flights.csv project-data-exploration/task2
```

**Step 2.** Change directories to the Task 2 folder. 
```bash
cd project-data-exploration/task2
```

**Step 3.** Open `flights_delay_explore.ipynb`. 

**Step 4.** For `TODO1`, replace the code block with the one below. 
```python
def generate_pandas_df_dict(csv_paths, table_names=None, index_cols=None):
    if table_names is None:
        table_names = csv_paths
    if index_cols is None:
        index_cols = (None,) * len(csv_paths)
    df_dict = {}
    for csv_path, table_name, index_col in zip(csv_paths, table_names, index_cols):
        df_dict[table_name] = pd.read_csv(csv_path, index_col=index_col)
    return df_dict
```

**Step 5.** For `TODO2`, replace the code block with the one below. 
```python
def show_tables(df_dict):
    print('=== TABLES ===')
    for name, df in sorted(df_dict.items()):
        print(f"- {name} ({df.shape[0]} rows, {df.shape[1]} columns)")
    print(f'TOTAL {len(df_dict)}')
```

**Step 6.** For `TODO3`, replace the code block with the one below. 
```python
def describe_table(df):
    print('=== COLUMNS ===')
    for column, dtype in sorted(zip(df.columns, df.dtypes)):
        series = df[column]
        if dtype == int64 or dtype == float64:
            print(f'- {column} {dtype} ({series.count()}/{series.size}) ' +
                  f'[Max: {series.max()}, Mean: {series.mean()}, Min: {series.min()}]')
        else:
            print(f'- {column} {dtype} ({series.count()}/{series.size}) ' +
                  f'[{len(series.unique())} unique]')
    print(f'TOTAL {df.shape[0]}')
```

**Step 7.** For `TODO4`, replace the code block with the one below. 
```python
def assess_useless_columns(df):
    for column in df.columns:
        series = df[column]
        if series.count() == 0:
            print(f'The column {column} appears to have no values.')
        if series.nunique(dropna=False) == 1:
            print(f'The column {column} appears to have only one value.')
```

Then, replace the second code block in `TODO4` with the one below. 
```python
def generate_delays_per_airline_csv(df_dict, csv_path):
    delays_per_airline = pd.merge(
        left=df_dict['flights'][['AIRLINE','ARRIVAL_DELAY']].groupby(['AIRLINE']).mean(),
        right=df_dict['airlines'],
        left_index=True,
        right_index=True
    )[['AIRLINE', 'ARRIVAL_DELAY']]
    delays_per_airline.sort_values(by='ARRIVAL_DELAY', ascending=False, ignore_index=True, inplace=True)
    delays_per_airline.to_csv(csv_path, index=False)
```

**Step 8.** For `TODO5`, replace the code block with the one below. 
```python
def generate_delays_per_arriving_airport_csv(df_dict, csv_path):
    delays_per_airline = pd.merge(
        left=df_dict['flights'][['AIRLINE','ARRIVAL_DELAY']].groupby(['AIRLINE']).mean(),
        right=df_dict['airlines'],
        left_on='DESTINATION_AIRPORT',
        right_on='IATA_CODE'
    )[['AIRLINE', 'ARRIVAL_DELAY']]
    delays_per_airline.sort_values(by='ARRIVAL_DELAY', ascending=False, ignore_index=True, inplace=True)
    delays_per_airline.to_csv(csv_path, index=False)
=======
**Step 1.** Download, unzip, and change directories to the provided data set for Task 2. 
```bash
wget https://principlesofcomputing.blob.core.windows.net/data-exploration-dataset-zip/dataset.zip
unzip dataset.zip
cd dataset
>>>>>>> e9fb3e6d81a7fd08a1e8d9adadc03501ddddb83f
```