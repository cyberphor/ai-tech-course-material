"""Module for Task 1"""
import csv
import pandas

def task1(data_source_path: str):
    with open(data_source_path, "r", encoding="UTF-8") as data_source:
        data = csv.DictReader(data_source)
        for row in data:
            print(row)

if __name__ == "__main__":
    task1(data_source_path="wdi_data/worldDevInds2017-education.csv")