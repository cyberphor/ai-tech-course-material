"""Module for retrieving books"""

import csv
import json
import mysql.connector
from pymongo import MongoClient
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import indent
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import SubElement

BOOK_ATTRIBUTES = [
    "title",
    "authors",
    "isbn",
    "isbn13",
    "language_code",
    "num_pages",
    "publication_date",
    "publisher",
]

RATING_ATTRIBUTES = ["average_rating", "ratings_count", "text_reviews_count"]


def fix_book_value_types(book):
    """Function for converting string-based book properties to numbers"""
    book["num_pages"] = int(book["num_pages"])
    book["average_rating"] = float(book["average_rating"])
    book["ratings_count"] = int(book["ratings_count"])
    book["text_reviews_count"] = int(book["text_reviews_count"])
    return book


def retrieve_popular_books(csv_in: str, json_out: str):
    """Function for getting books from a CSV file and writing them to a JSON file"""
    with open(json_out, "w") as json_file:
        popular_books = {}
        with open(csv_in, "r", encoding="UTF-8") as csv_file:
            books = csv.DictReader(csv_file)
            for book in books:
                book = fix_book_value_types(book)
                if (
                    book["num_pages"] > 50
                    and book["average_rating"] > 4.5
                    and book["ratings_count"] > 1000
                ):
                    popular_books[book["bookID"]] = {
                        "info": {
                            attribute: book[attribute] for attribute in BOOK_ATTRIBUTES
                        },
                        "rating": {
                            attribute: book[attribute]
                            for attribute in RATING_ATTRIBUTES
                        },
                    }
        json_file.write(json.dumps(popular_books, indent=4, ensure_ascii=False))


def retrieve_boring_books(json_in: str, xml_out: str):
    """Function for getting books from a JSON file and writing them to an XML file"""
    boring_books = Element("books")
    with open(json_in, "r", encoding="UTF-8") as json_file:
        books = json.load(json_file)
        for book in books:
            book = fix_book_value_types(book)
            if (
                book["num_pages"] > 300
                and book["average_rating"] < 3.0
                and book["ratings_count"] > 100
            ):
                boring_book = SubElement(boring_books, "book")
                boring_book.set("id", book["bookID"])
                boring_book_info = SubElement(boring_book, "info")
                boring_book_rating = SubElement(boring_book, "rating")
                for attribute in BOOK_ATTRIBUTES:
                    SubElement(boring_book_info, attribute).text = str(book[attribute])
                for attribute in RATING_ATTRIBUTES:
                    SubElement(boring_book_rating, attribute).text = str(
                        book[attribute]
                    )
    indent(boring_books, space="\t")
    ElementTree(boring_books).write(xml_out)


def retrieve_wildly_popular_books(xml_in: str, csv_out: str):
    """Function for getting books from an XML file and writing them to a CSV file"""
    with open(csv_out, "w", encoding="UTF-8") as csv_file:
        xml_file = parse(xml_in).getroot()
        csv_headers = [csv_header.tag for csv_header in xml_file[0]]
        csv_headers.pop(0)
        csv_headers.insert(0, "book_id")
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=csv_headers, lineterminator="\n"
        )
        csv_writer.writeheader()
        for book in xml_file:
            average_rating = float(
                [average_rating.text for average_rating in book.iter("average_rating")][
                    0
                ]
            )
            rating_count = int(
                [rating_count.text for rating_count in book.iter("ratings_count")][0]
            )
            if average_rating > 4.0 and rating_count > 1000000:
                wildly_popular_book = {}
                for element in book:
                    if element.tag == "bookID":
                        element.tag = "book_id"
                    wildly_popular_book[element.tag] = element.text
                csv_writer.writerow(wildly_popular_book)


# HACK: this is used in Task 2
def retrieve_long_books(
    user: str, password: str, host: str, db: str, table: str, csv_out: str
):
    """Function for getting books from a SQL table into a CSV file"""
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
                obscure_books.update(
                    {
                        book["bookID"]: {
                            "info": {
                                attribute: book[attribute]
                                for attribute in BOOK_ATTRIBUTES
                            },
                            "rating": {
                                attribute: book[attribute]
                                for attribute in RATING_ATTRIBUTES
                            },
                        }
                    }
                )
        json_file.write(json.dumps(obscure_books, indent=4))


if __name__ == "__main__":
    retrieve_popular_books(
        csv_in="books_data/books_v2.csv", json_out="books_data/books_v2_popular.json"
    )
    retrieve_boring_books(
        json_in="books_data/books_v2.json", xml_out="books_data/books_v2_boring.xml"
    )
    retrieve_wildly_popular_books(
        xml_in="books_data/books_v2.xml", csv_out="books_data/books_v2_wild.csv"
    )
    retrieve_long_books(
        user="dbuser",
        password="dbroot",
        host="localhost",
        db="books",
        table="goodreads",
        csv_out="books_data/long_books.csv",
    )
    retrieve_obscure_books(
        db="books", coll="goodreads", json_out="books_data/obscure_books.json"
    )
