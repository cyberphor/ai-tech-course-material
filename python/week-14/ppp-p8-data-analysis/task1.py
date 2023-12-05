"""Module for Task 1"""
import csv
import pandas

def task1(data_source_path: str):
    df = pandas.read_csv(data_source_path)
    columns = [
        "Country",
        "Compulsory education (years)",
        "Doctoral degrees (%)",
        "Completed primary education (%)",
        "Government expenditure on education (%)",
        "Literacy rate (%)",
        "Primary education (years)",
        "Primary school (starting age)"
    ]
    print(df[columns])

if __name__ == "__main__":
    task1(data_source_path="wdi_data/worldDevInds2017-education.csv")