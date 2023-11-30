"""Module for debugging and developing this week"s solution"""
from name_scraping import csv_to_excel
from name_scraping import json_to_excel
from name_scraping import scrape_names
from name_scraping import xml_to_excel
from retrieve_from_gsheet import generate_reminder
from retrieve_from_gsheet import generate_reminders
from retrieve_from_gsheet import get_google_sheet
from retrieve_from_gsheet import get_accounts_info

csv_file  = "debug.csv"
json_file = "debug.json"
xml_file  = "debug.xml"

# task 1
def task_1():
    scrape_names(
        pages=[1,2,3,4],
        output_file_path=csv_file,
        gender=True,
        usage=True,
        desc=True,
        output_format="csv"
    )
    scrape_names(
        pages=[1,2,3,4],
        output_file_path=json_file,
        gender=True,
        usage=True,
        desc=True,
        output_format="json"
    )
    scrape_names(
        pages=[1,2,3,4],
        output_file_path=xml_file,
        gender=False,
        usage=False,
        desc=False,
        output_format="xml"
    )

# task 2
def task_2():
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

# task 3
def task_3():
    accounts = get_accounts_info(fields=None, start=0, end=10)
    print(
        f"Number of accounts: {len(accounts)}\n{accounts}\n"
    )
    accounts = get_accounts_info(fields=["First Name", "Last Name"], start=5, end=9)
    print(
        f"Number of accounts: {len(accounts)}\n{accounts}\n"
    )

# task 4
def task_4():
    generate_reminder(
        first_name="Rocco",
        last_name="Hupp",
        title="Mr.",
        street="9733 Nancy Wall",
        city="South Christopherville",
        state="AL",
        zip_code="23514",
        amount_owed=376.6,
        num_reminders=1,
        output_dir="reminders"
    )
    generate_reminder(
        first_name="Hang",
        last_name="Hupp",
        title="Mrs.",
        street="9733 Nancy Wall",
        city="South Christopherville",
        state="AL",
        zip_code="23514",
        amount_owed=376.6,
        num_reminders=0,
        output_dir="reminders"
    )
    generate_reminders(
        start=5,
        end=10,
        output_dir="reminders"
    )

if __name__ == "__main__":
    task_4()