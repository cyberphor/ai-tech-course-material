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

**Step 4.** For `TODO1`, replace `YOUR_SOLUTION_HERE` with the code below. 
```python
    for i in zip(csv_paths, table_names, index_cols):
        df_dict[i[1]] = pd.read_csv(filepath_or_buffer=i[0], index_col=i[2], dtype=)
```

**Step 5.** For `TODO2`, replace `YOUR_SOLUTION_HERE` with the code below. 
```python
    print(f"- {name} ({df.shape[0]} rows, {df.shape[1]} columns)")
```

**Step 6.** For `TODO3`, replace `YOUR_SOLUTION_HERE` with the code below. 
```python

```

**Step 7.** For `TODO4`, replace `YOUR_SOLUTION_HERE` with the code below. 
```python

```

**Step 8.** For `TODO4`, replace `YOUR_SOLUTION_HERE` with the code below. 
```python

```