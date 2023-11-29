"""Module for debugging and developing this week's solution"""
from name_scraping import scrape_names
from name_scraping import csv_to_excel
from name_scraping import json_to_excel
from name_scraping import xml_to_excel

csv_file  = "debug.csv"
json_file = "debug.json"
xml_file  = "debug.xml"

# task 1
scrape_names(
    pages=[1,2,3,4],
    output_file_path=csv_file,
    gender=True,
    usage=True,
    desc=bool,
    output_format="csv"
)

scrape_names(
    pages=[1,2,3,4],
    output_file_path=json_file,
    gender=True,
    usage=True,
    desc=bool,
    output_format="json"
)

scrape_names(
    pages=[1,2,3,4],
    output_file_path=xml_file,
    gender=True,
    usage=True,
    desc=bool,
    output_format="xml"
)

# task 2
json_to_excel(
    json_file_path=json_file, 
    excel_file_path=f"{json_file}.xlsx"
)

csv_to_excel(
    csv_file_path=csv_file, 
    excel_file_path=f"{csv_file}.xlsx"
)

xml_to_excel(
    xml_file_path=xml_file, 
    excel_file_path=f"{xml_file}.xlsx"
)