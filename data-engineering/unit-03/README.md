# Data Engineering
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)

## Setup
**Step 1.** Download the `vic-code` GitHub repository and change directories to setup folder for this week's project. These commands are meant to be ran on your personal computer or GitHub Codespace.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/data-engineering/unit-03/setup
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

**Step 10.** Save the `ip_address` of the virtual machine (that was created by Terraform) as an environment variable. It will be used by Ansible near the end of this task. This command is meant to be ran on your personal computer and from the `setup` directory. 
```bash
export IP_ADDRESS=$(terraform -chdir=terraform output -raw ip_address)
```

**Step 11.** Use Ansible and the provided [Ansible playbook](ansible/playbook.yaml) to configure the virtual machine. The [scripts](setup/ansible/scripts/) listed in the Ansible playbook install software and download this week's handouts. This command is meant to be ran on your personal computer and from the `setup` directory.
```bash
ansible-playbook ansible/playbook.yaml -u $USERNAME -i ansible/inventory.yaml --ssh-common-args='-o StrictHostKeyChecking=no'
```

**Step 12.** Save the environment variables you created to a file so you can use them again in the future (the example below saves them to a file called `.env` in the parent directory of `setup`). For example, if you lose your environment (e.g., reboot your personal computer), you can get your environment variables back by running `source .env` (from whatever directory you create said `.env` file). Also, the filename `.env` is not special. You could call the file where you store your environment variables whatever you want. Lastly, it would also be helpful to save your Sail() submission credentials to this file too. 
```bash
echo "export USERNAME=$USERNAME" >> ../.env && echo "export IP_ADDRESS=$IP_ADDRESS" >> ../.env
```

**Step 13.** Login to the virtual machine.
```bash
ssh $USERNAME@$IP_ADDRESS
```

## Task 01
**Step 1.** Login to the Azure Portal and search for "Azure Cosmos DB."

**Step 2.** Click "Create Azure Cosmos DB account."

**Step 3.** In the "Azure Cosmos DB for MongoDB" card, click "Create."

**Step 4.** In the "Request unit (RU) database account" card, click "Create."

**Step 5.** Use the following settings to configure your "Azure Cosmos DB Account."
| Setting                        | Value 
| ------------------------------ | -----
| Subscription                   | your subscription
| Resource Group                 | `multi-model-databases`
| Account Name                   | Something globally unique (e.g., `cyberphordataengineeringunit02`)
| Availability Zones             | Disable
| Location                       | `eastus`
| Capacity Mode                  | Provisioned throughput
| Apply Free Tier Discount       | Apply
| Limit total account throughput | Uncheck
| Version                        | `4.0`

**Step 6.** Click "Review + Create." Then, "Create" and wait for the deployment to finish.

**Step 7.** Click "Go to resource."

**Step 8.** Click the "Quick start" blade. Then, click the "Others" tab and save "HOST", "PORT", "USERNAME", and "PRIMARY PASSWORD" as environment variables in *your virtual machine.* 
```bash
export HOST="cyberphordataengineeringunit02.mongo.cosmos.azure.com"
export PORT="10255"
export USERNAME="cyberphordataengineeringunit02"
export PASSWORD="rRcL9iTOc5XSPS0ySLRROJRUzcAe8IKQinrgazcI6bUCRg8jqBrwvIr2WU4gzvbIH3GpHNF6sshEACDbrMcYcw=="
```

You will also need to save "PRIMARY CONNECTION STRING" as an environmnent variable. It can be found in the "Connection strings" blade. 
```bash
export CONNECTION_STRING="mongodb://cyberphordataengineeringunit02:rRcL9iTOc5XSPS0ySLRROJRUzcAe8IKQinrgazcI6bUCRg8jqBrwvIr2WU4gzvbIH3GpHNF6sshEACDbrMcYcw==@cyberphordataengineeringunit02.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cyberphordataengineeringunit02@"
```

**Step 9.** (Optional) Save the environment variables you created to a file so you can use them again in the future (the example below saves them to a file called `.env` in your home directory).
```bash
echo "export HOST=$HOST" >> ~/.env &&\
echo "export PORT=$PORT" >> ~/.env &&\
echo "export USERNAME=$USERNAME" >> ~/.env &&\
echo "export PASSWORD=$PASSWORD" >> ~/.env &&\
echo "export CONNECTION_STRING=$CONNECTION_STRING" >> ~/.env 
```

**Step 10.** Click the "Overview" blade. Then, click "Data Explorer."

**Step 11.** Click "New Collection."

**Step 12.** Use the following settings to configure your "Collection." The acronym `asin` stands for Amazon Standard Identification Number.
| Setting                    | Value 
| -------------------------- | -------------------
| Database name (Create new) | `Customer_reviews`
| Database throughput        | Manual
| Database Required RU/s     | `8000`
| Collection id              | `movie_reviews`
| Indexing                   | Automatic
| Sharding                   | Sharded
| Shared key                 | `asin` 

**Step 13.** Login to your virtual machine if you haven't already. 
```bash
ssh $USERNAME@$IP_ADDRESS
```

**Step 14.** Change directories to `~/multi-model-databases/`. 
```bash
cd ~/multi-model-databases/
```

**Step 15.** Import the `movieReview.json` file to your Azure Cosmos DB collection using `mongoimport`.
```bash
mongoimport \
  -h $HOST:$PORT \
  -d Customer_reviews \
  -c movie_reviews \
  -u $USERNAME \
  -p $PASSWORD \
  --ssl \
  --type json \
  --writeConcern="{w:0}" \
  --file movieReview.json \
  --batchSize 10
```

**Step 16.** Connec to your Azure Cosmos DB collection.
```bash
mongosh -u $USERNAME -p $PASSWORD --tls $HOST:$PORT/Customer_reviews
```

**Step 17.** Validate the `movieReview.json` dataset was imported. 
```bash
db.movie_reviews.count()
```

**Step 18.** Count the number of records that have a field called `reviewTime`.
```javascript 
db.movie_reviews.find({reviewTime: {$exists: true}}).count()
```

**Step 19.** Remove the `reviewTime` field from the records that have it. If your connection times out, repeat the previous step and try again.
```javascript
db.movie_reviews.updateMany({reviewTime: {$exists: true}}, {$unset: {reviewTime: ""}})
```

Your output should be similar to below.
```javascript
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 0,
  modifiedCount: 0,
  upsertedCount: 0
}
```

**Step 20.** Count the number of records where the `overall` field is less than 3.
```javascript 
db.movie_reviews.find({overall: {$lt: 3}}).count()
```

Your output should be similar to below.
```bash
4796
```

**Step 21.** Delete the records with values less than 3 in the `overall` field.
```javascript 
db.movie_reviews.deleteMany({overall: {$lt: 3}})
```

Your output should be similar to below.
```javascript
{ acknowledged: true, deletedCount: 4796 }
```

**Step 22.** Count the number of records in your collection. 
```javascript
db.movie_reviews.countDocuments()
```

If your output is similar to below, you're ready to submit your work for points.
```javascript
45204
```

## Task 02
For reference, the records in your Azure Cosmos DB collection look like the object below.
```javascript
{
  "_id": ObjectId("65ca3f19377cad047dd771c1"),
  "reviewerID": "A33EWPXESP9GQH",
  "asin": "0005019281",
  "reviewerName": "Buckaroo \"Dead Dog\"",
  "helpful": [ 0, 0 ],
  "reviewText": "Even though i don't care for Henry Winklers  acting i liked this movie it fit him real good ThanksDale", 
  "overall": 5, 
  "summary": "Good Version",
  "unixReviewTime": 1390780800
}
```

**Step 1.** Add the Python-based "Primary Connection String" for your Azure Cosmos DB collection to `~/multi-model-databases/task2.py` on your virtual machine. This value can be found in the Azure portal under the "Quick start" blade and "Python" tab.

**Step 2.** Update the `task2.py` file using the [provided example](task-02/task2.py).

**Step 3.** Submit your work (remember to set your BASH environment variables and invoke your Python virtual environment). 
