# Python: Files and Data Stores

## Solutions
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)

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

**Step 8.** Install MongoDB using the [script shared](/python/week-12/install-MongoDB.sh). 
```bash
sudo bash install-MongoDB.sh
```

**Step 9.** Verify MongoDB is listening for connections on TCP port 27017. 
```bash
sudo netstat -pant | grep 27017
```

## Task 01
**Step 1.** Create a Python script called `books_retrieval.py` using inspiration from the [source code shared](/python/week-12/ppp-p6-files-datastores/books_retrieval.py). 
```bash
touch books_retrieval.py
```

**Step 2.** Execute the Python script. 
```bash
python books_retrieval.py
```

## Task 02
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

**Step 5.** Update the script created in Task 1 (`books_retrieval.py`) using the function below. 
```python
def retrieve_long_books(user: str, password: str, host: str, db: str, table: str, csv_out: str):
    with open(csv_out, "w", encoding="UTF-8") as csv_file:
        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position;"
        cursor.execute(query)
        csv_headers = [csv_header[0] for csv_header in cursor]
        csv_headers.pop(0)
        csv_headers.insert(0, "book_id")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_headers)
        query = f"SELECT * FROM {db}.{table} WHERE num_pages > 2000;"
        cursor.execute(query)
        csv_writer.writerows(cursor)
        cursor.close()
        connection.commit()
```

**Step 6.** Execute the updated script. 
```bash
python books_retrieval.py
```

## Task 03
**Step 1.** Update the script created in Task 2 (`data_loading.py`) using the function below. Beware of any import dependencies not shown.
```python
def load_to_mongodb(db: str, coll: str, json_in: str):
    """Function for loading data from a JSON file into a NoSQL collection"""
    with open(json_in, "r", encoding="UTF-8") as json_file:
        books = json.load(json_file)
        client = MongoClient()
        client.drop_database(db)
        database = client[db]
        for book in books:
            book = fix_book_value_types(book)
            database[coll].insert_one(book)
```

**Step 2.** Execute the updated script. 
```bash
python data_loading.py
```

**Step 3.** Verify data was loaded into the NoSQL (i.e., MongoDB) collection using the [script shared](/python/week-12/ppp-p6-files-datastores/nosql-print-collection.js). 
```bash
sudo mongosh < nosql-print-collection.js
```

**Step 4.** Update the script created in Task 1 (`books_retrieval.py`) using the function below. Beware of any import dependencies not shown.
```python
def retrieve_obscure_books(db: str, coll: str, json_out: str):
  """Function for getting books in a NoSQL collection into a JSON file"""
  with open(json_out, "w", encoding="UTF-8") as json_file:
    obscure_books = {}
    client = MongoClient()
    database = client[db]
    books = database[coll].find({})
    for book in books:
      book.pop("_id")
      if book["ratings_count"] == 1:
        obscure_books.update({book["bookID"]: {
          "info": {attribute: book[attribute] for attribute in BOOK_ATTRIBUTES},
          "rating": {attribute: book[attribute] for attribute in RATING_ATTRIBUTES}
        }})
    json_file.write(json.dumps(obscure_books, indent=4))
```

**Step 5.** Execute the updated script. 
```bash
python books_retrieval.py
```