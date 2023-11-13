"""Module for retrieving books"""
import csv
import json
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import indent
from xml.etree.ElementTree import SubElement

BOOK_ATTRIBUTES = [
  "title",
  "authors", 
  "isbn", 
  "isbn13", 
  "language_code", 
  "num_pages",
  "publication_date",
  "publisher"
] 

RATING_ATTRIBUTES = [
  "average_rating",
  "ratings_count",
  "text_reviews_count"
]

def fix_book_value_types(book):
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
        if book["num_pages"] > 50 and book["average_rating"] > 4.5 and book["ratings_count"] > 1000:
          popular_books[book["bookID"]] = {
            "info": {attribute: book[attribute] for attribute in BOOK_ATTRIBUTES},
            "rating": {attribute: book[attribute] for attribute in RATING_ATTRIBUTES}
          }
    json_file.write(json.dumps(popular_books, indent=4))

def retrieve_boring_books(json_in: str, xml_out: str):
  boring_books = Element("books") 
  with open(json_in, "r", encoding="UTF-8") as json_file:
    books = json.load(json_file)
    for book in books:
      book = fix_book_value_types(book)
      if book["num_pages"] > 300 and book["average_rating"] < 3.0 and book["ratings_count"] > 100:
        boring_book = SubElement(boring_books, "book")
        boring_book.set("id", book["bookID"])
        boring_book_info = SubElement(boring_book, "info")
        boring_book_rating = SubElement(boring_book, "rating")
        for attribute in BOOK_ATTRIBUTES:
          SubElement(boring_book_info, attribute).text = str(book[attribute])
        for attribute in RATING_ATTRIBUTES:
          SubElement(boring_book_rating, attribute).text = str(book[attribute])
  indent(boring_books, space="\t")
  ElementTree(boring_books).write(xml_out)

def retrieve_wildly_popular_books():
  pass

if __name__ == "__main__":
  retrieve_popular_books(csv_in="books_data/books_v2.csv", json_out="books_data/books_v2_head_popular.json")
  retrieve_boring_books(json_in="books_data/books_v2.json", xml_out="books_data/books_v2_head_boring.xml")
  retrieve_wildly_popular_books()