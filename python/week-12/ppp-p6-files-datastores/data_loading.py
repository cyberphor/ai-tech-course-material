"""Module for loading data into a SQL database"""
import csv
import mysql.connector

def setup_sql_table(user: str, password: str, host: str, new_db: str, new_table: str):
    """Function for creating a SQL database and table"""
    queries = [
        f'DROP DATABASE IF EXISTS {new_db};',
        f'CREATE DATABASE {new_db};',
        f'''
            CREATE TABLE {new_db}.{new_table} (
                id VARCHAR(255) PRIMARY KEY,
                title VARCHAR(1024),
                authors VARCHAR(1024),
                average_rating FLOAT(9,2),
                isbn VARCHAR(255),
                isbn13 VARCHAR(255),
                language_code VARCHAR(255),
                num_pages INT,
                ratings_count INT,
                text_reviews_count INT,
                publication_date VARCHAR(255),
                publisher VARCHAR(255)
            );
        '''
    ]
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    for query in queries:
        cursor.execute(query)  
    cursor.close()
    connection.commit()

def load_to_sql(user: str, password: str, host: str, db: str, table: str, csv_in: str):
    """Function for loading data from a CSV into a SQL table"""
    with open(csv_in, "r", encoding="UTF-8") as csv_file:
        books = csv.DictReader(csv_file)    
        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()
        for book in books:
            query_arguments = tuple(book.values())
            query_parameters = ", ".join(["%s"] * len(query_arguments))
            query = f"INSERT INTO {db}.{table} VALUES ({query_parameters});"
            cursor.execute(query, query_arguments)
        cursor.close()
        connection.commit()

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

if __name__ == "__main__":
    setup_sql_table(
        user="dbuser",
        password="dbroot",
        host="localhost",
        new_db="books",
        new_table="goodreads",        
    )
    load_to_sql(
        user="dbuser",
        password="dbroot",
        host="localhost",
        db="books",
        table="goodreads",
        csv_in="books_data/books_v2.csv"
    )
