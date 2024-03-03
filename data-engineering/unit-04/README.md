# Data Engineering: Data Processing with Spark
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)

## Setup
**Step 1.** Download the `vic-code` GitHub repository and change directories to setup folder for this week's project. These commands are meant to be ran on your personal computer or GitHub Codespace.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-04/setup
```

**Step 2.** Create an SSH key pair if you don't already have one. It's best practice to encrypt your SSH private key with a password, but this is optional. This command is meant to be ran on your personal computer. `-t` defines the key pair type. `-b` defines the key lengths (i.e., the number of bits). `-C` is used to include a comment. 
```bash
ssh-keygen -t rsa -b 4096 -C "These are SSH keys for my personal computer"
```

**Step 3.** Start an SSH authentication agent and add your SSH private key to it. As long as an SSH authentication agent is running, you don't need to enter the password for your SSH private key every time you want to authenticate with a remote machine. These commands are meant to be ran on your personal computer. The first command starts the SSH authentication agent while the second command adds your SSH private key to it.
```bash
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa  
```

**Step 4.** Install Ansible if you don't already have it installed. This command is meant to be ran on your personal computer.
```bash
python -m pip install ansible
```

**Step 5.** Login to the Azure CLI if you haven't already. This command is meant to be ran on your personal computer.
```bash
az login --use-device-code
```

**Step 6.** Set your subscription if you haven't already. This command is meant to be ran on your personal computer.
```bash
az account set --subscription "AI2C Subscription 3"
```

**Step 7.** Initialize the `terraform` directory for Terraform use by installing the necessary Terraform plugins and modules. This command is meant to be ran on your personal computer. 
```bash
terraform -chdir=terraform init
```

**Step 8.** Create the cloud resources needed for this week's project using the [provided Terraform configuration](setup/terraform/main.tf). This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
terraform -chdir=terraform apply -auto-approve
```

**Step 9.** Save the `username` of the virtual machine (that was created by Terraform) as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export USERNAME=$(terraform -chdir=terraform output -raw username)
```

**Step 10.** Save the `ipaddress` of the virtual machine (that was created by Terraform) as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export IPADDRESS=$(terraform -chdir=terraform output -raw ipaddress)
```

**Step 11.** Save the `DATABRICKS_HOST` determined by Terraform as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export DATABRICKS_HOST=$(terraform -chdir=terraform output -raw databricks_host)
```

**Step 12.** Save the `DATABRICKS_TOKEN` created via by Terraform as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export DATABRICKS_TOKEN=$(terraform -chdir=terraform output -raw databricks_token)
```

**Step 13.** Use Ansible and the provided [Ansible playbook](ansible/playbook.yaml) to configure the virtual machine. The [scripts](setup/ansible/scripts/) listed in the Ansible playbook install software and download this week's handouts. This command is meant to be ran on your personal computer and from the `setup` directory.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

**Step 14.** Save the environment variables you created to a file so you can use them again in the future (the example below saves them to a file called `.env` in the parent directory of `setup`). For example, if you lose your environment (e.g., reboot your personal computer), you can get your environment variables back by running `source .env` (from whatever directory you create said `.env` file). Also, the filename `.env` is not special. You could call the file where you store your environment variables whatever you want. Lastly, it would also be helpful to save your Sail() submission credentials to this file too. 
```bash
echo "export USERNAME=$USERNAME" >> ../.env &&\
echo "export IPADDRESS=$IPADDRESS" >> ../.env &&\
echo "export DATABRICKS_HOST=$DATABRICKS_HOST" >> ../.env &&\
echo "export DATABRICKS_TOKEN=$DATABRICKS_TOKEN" >> ../.env
```

**Step 15.** Login to the virtual machine.
```bash
ssh $USERNAME@$IPADDRESS
```

## Task 01
**Step 1.** Login to the Azure Portal, search for "databricks," and click "Azure Databricks."

**Step 2.** Click your Azure Databricks resource. Then, click "Launch Workspace."

**Step 3.** Click "Workspace > Workspace > task1."

**Step 4.** Run cell 2. This step is necessary to define, in the current notebook, where the dataset can be found.

**Step 5.** Run cell 4. This step is necessary to create a Resilient Distributed Dataset (RDD) Python object using the provided dataset. 

**Step 6.** Edit and run cell 6 using the code below. 
```python
# TODO: Create a tuple of (author, ups_count) for a single raw_line in the dataset. In the function below, replace <author> & <ups> with appropriate code to extract author and ups count from a column in the dataset.
# NOTE: Convert ups to integer using int().

def get_author_and_ups(raw_line):
    cols = raw_line.split('\t')
    
    #TODO
    return (cols[14], int(cols[1]))
```

**Step 7.** Edit and run cell 7 using the code below. 
```python
# TODO: Apply the above implmented get_author_and_ups method on each row of the dataset

parsed_data = raw_data.map(get_author_and_ups)
```

**Step 8.** Edit and run cell 8 using the code below. 
```python
# TODO: Implement reduceByKey on the parsed_data and store it in reduced_ups
# Hint: https://sparkbyexamples.com/pyspark/pyspark-reducebykey-usage-with-examples/

reduced_ups = parsed_data.reduceByKey(lambda a, b: a + b)
```

**Step 9.** Edit and run cell 10 using the code below. 
```python
# TODO: Replace the <NUM> argument so that top 100 users are returned in descending order.
# Reference: https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.top.html

top100 = reduced_ups.top(100, key=lambda x: x[1])
```

**Step 10.** Edit and run cell 11 using the code below. 
```python
top = sc.parallelize(top100).map(lambda x: x[0] + '\t' + str(x[1]))
```

**Step 11.** Edit and run cell 12 using the code below. 
```python
output_path = 'dbfs:/task1-output'
top.saveAsTextFile(output_path)
```

## Task 02
**Step 1.** Run cell 2. This step is necessary to define, in the current notebook, where the dataset can be found.

**Step 2.** Run cell 4. This step is necessary to define the schema for the provided dataset.

**Step 3.** Run cell 6. This step is necessary to create a RDD Python object using the provided dataset. 

**Step 4.** Edit and run cell 8 using the code below. 
```python
# TODO: Find the right operation to add up all the 'ups' per author and provide it with an appropriate argument.
# Replace <FUNCTION> and <COLUMN>.
# Reference: https://sparkbyexamples.com/spark/spark-sql-aggregate-functions/#sum

reduced_df = raw_df.groupBy("author").sum("ups")
```

**Step 5.** Edit and run cell 10 using the code below.
```python
from pyspark.sql.functions import col

# TODO: Sort the column "sum(ups)" of reduced_df dataframe in descending order using appropriate function
sorted_desc = reduced_df.sort(f.col("sum(ups)").desc())
```

**Step 6.** Edit and run cell 11 using the code below.
```python
# TODO: Select top 100 rows from the sorted_desc dataframe
top100 = sorted_desc.limit(100)
result = top100.select(col("author"), col("sum(ups)").alias("count"))
```

**Step 7.** Run cell 12 using the code below.
```python
# You can refer to https://spark.apache.org/docs/latest/sql-data-sources-parquet.html to learn how to save the dataframe file in parquet format.

output_path = 'dbfs:/task2-output'
result.write.save(output_path, format="parquet")
```

## Task 03
**Step 1.** Run cell 2. This step is necessary to define, in the current notebook, where the dataset can be found.

**Step 2.** Run cell 4. This step is necessary to define some helper functions.

**Step 3.** Run cell 6. This step is necessary to create a RDD Python object using the provided dataset. 

**Step 4.** Edit and run cell 7 using the code below. 
```python
raw_data = sc.textFile(files_path)
```

**Step 5.** Edit and run cell 9 using the code below. 
```python
# TODO: Complete the function as per the instructions. 
# Split raw_line by '\t' and extract body field. 
# Look up the dataset in writeup to locate the boly field. We will then apply the utility methods to the content of the body to extract words.

def split_and_flatten(raw_line):
    body = raw_line.split('\t')[17]
    filtered = preprocess(body)
    return split_body(filtered)
```

**Step 6.** Edit and run cell 10 using the code below. 
```python
# TODO: We just created the method `split_and_flatten` above. Implement this method on all the elements of dataset.
# Review the Primer to understand the purpose of flatmap and its difference from map

split_data = raw_data.flatMap(split_and_flatten)
```

**Step 7.** Edit and run cell 11 using the code below.
```python
# The output of split_data will consist of a list of words. We need to map each word to a tuple with count = 1, such that word -> (word, 1)
# You can write a utility method or use lambda like we have used before.

words = split_data.map(lambda word: (word, 1)).partitionBy(20)
```

**Step 8.** Edit and run cell 12 using the code below. 
```python
# TODO: Implement reduceByKey on `words` to get the aggregate count of word occurences. 

word_count = words.reduceByKey(lambda a, b: a + b)
```

**Step 9.** Edit and run cell 14 using the code below. 
```python
# TODO: From word_count, select top 100 words with highest count by sorting by count in descending order.
# We have done this before...

top100 = word_count.takeOrdered(100, key=lambda x: -x[1])
```

**Step 10.** Edit and run cell 15 using the code below. 
```python
# TODO: Display the words in the format <word>\t<count> -> Hello 10

top = sc.parallelize(top100).map(lambda x: f"{x[0]}\t{x[1]}")
```

**Step 11.** Edit and run cell 16 using the code below. 
```python
output_path = 'dbfs:/task3-output'

# TODO: Save the output in the output_path using the saveAsTextFile method.
top.saveAsTextFile(output_path)
```

## Task 04
**Step 1.** Run cell 2. This step is necessary to define, in the current notebook, where the dataset can be found.

**Step 2.** Run cell 4 and 5. These steps are necessary to define some helper functions.

**Step 3.** Edit and run cell 7 using the code below. This step is necessary to create a RDD Python object using the provided dataset. 
```python
# TODO: Read the text file refered to by filepath variable into a single RDD
#       named `raw_data`.

raw_data = sc.textFile(filepath)
```

**Step 4.** Edit and run cell 9 using the code below. 
```python
# TODO: 
# 1. Parse raw data and store all rows as a tuple of (author, ups_count) by using map function as we did in task1.
#    Remove rows containing author `[delete]`
# 2. Implement reduceByKey on parsed_data to calculate aggregate ups_count of users
# 3. Select top 100 users sorted in descending order of their ups_count

parsed_data = raw_data.map(lambda line: (line.split('\t')[14], int(line.split('\t')[1]))).filter(lambda x: x[0] != '[deleted]')
reduced_ups = parsed_data.partitionBy(20).reduceByKey(lambda a, b: a + b) 
top = reduced_ups.takeOrdered(100, key=lambda x: -x[1])
names = []
for pair in top:
    names.append(pair[0])
```

**Step 5.** Run cells 11, 13, and 14.

**Step 6.** Edit and run cell 15 using the code below. 
```python
top.saveAsTextFile(path_checkpoint1)
```

**Step 7.** Run cells 17, 19, 20, 22, 24, 25, 26, 28, 30, and 31.

**Step 8.** Edit and run cell 32.
```python
# TODO: Save the output as a text file to the location defined by the `output_path`.

output.saveAsTextFile(output_path)
```