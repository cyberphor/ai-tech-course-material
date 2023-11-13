"""Module for retrieving books"""
import csv
import json

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

def retrieve_popular_books(csv_in: str, json_out: str):
  """Function for getting books from a CSV file and writing them to a JSON file"""
  with open(json_out, "w") as json_file:
    popular_books = {}
    with open(csv_in, "r", encoding="UTF-8") as csv_file:
      books = csv.DictReader(csv_file)
      for book in books:
        book["num_pages"] = int(book["num_pages"])
        book["average_rating"] = float(book["average_rating"])
        book["ratings_count"] = int(book["ratings_count"])
        book["text_reviews_count"] = int(book["text_reviews_count"])
        if book["num_pages"] > 50 and book["average_rating"] > 4.5 and book["ratings_count"] > 1000:
          popular_books[book["bookID"]] = {
            "info": {attribute: book[attribute] for attribute in BOOK_ATTRIBUTES},
            "rating": {attribute: book[attribute] for attribute in RATING_ATTRIBUTES}
          }
    json_file.write(json.dumps(popular_books, indent=4))

if __name__ == "__main__":
  retrieve_popular_books(csv_in="books_data/books_v2.csv", json_out="books_data/books_v2_head_popular.json")