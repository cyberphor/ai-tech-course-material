"""Module for loading data into a SQL database"""
import mysql.connector

def setup_sql_table(user: str, password: str, host: str, new_db: str, new_table: str):
    delete_database = f'DROP DATABASE IF EXISTS {new_db};'
    create_database = f'CREATE DATABASE {new_db};'
    create_table = f'''
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

    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute(delete_database)
    cursor.execute(create_database)    
    cursor.execute(create_table)
    cursor.close()
    connection.commit()

def load_to_sql(user: str, password: str, host: str, db: str, table: str, csv_in: str):
    connection = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    insert_statement = f'INSERT INTO {db}.{table} VALUES (%s, %s);'
    #cursor.execute(insert_statement, (val1, val2))
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