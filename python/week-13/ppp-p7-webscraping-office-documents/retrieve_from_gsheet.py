"""Module for using a web API"""
from os import mkdir
from os import path
from pygsheets import authorize
from docx import Document

def get_google_sheet():
    """Function to get a Google Sheet"""
    client = authorize(service_account_file="algebraic-ratio-338019-eb975aa8f686.json")
    workbook = client.open("Accounts") # name of Google Sheet
    return workbook.sheet1             # tab 1

def get_accounts_info(fields: list[str] = None, start: int = 0, end: int = 9):
    """Function to get records from a Google Sheet"""
    worksheet = get_google_sheet()
    accounts = []
    for record in worksheet.get_all_records()[start:(end+1)]:
        if None is fields:
            accounts.append(record)
        else:
            account = {}
            [account.update({field: record[field]}) for field in fields]
            accounts.append(account)
    return accounts

def generate_reminder(
        first_name: str = "",
        last_name: str = "",
        title: str = "Mr.",
        street: str = "",
        city: str = "",
        state: str = "",
        zip_code: str = "",
        amount_owed: float = 0.0,
        num_reminders: int = 0,
        output_dir: str = ""  
    ):
    """Function for creating a Microsoft Word document"""
    if not path.exists(output_dir):
        mkdir(output_dir)
    reminder = [
        f"{title} {first_name} {last_name}",
        f"{street}",
        f"{city}, {state} {zip_code}",
        f"Dear {title} {last_name},",
        f"Payment on your XYZ account in the amount of ${amount_owed} is due.",
        f"We have already sent you {num_reminders} reminders.",
        "Please, disregard this notice if you have already made the payment.",
        "Best Regards.",
        "John Doe",
        "Account Manager XYZ"
    ]
    document = Document()
    if num_reminders <= 0:
        reminder = reminder[0:4] + reminder[6:]
    for paragraph in reminder:
        document.add_paragraph(paragraph, style=document.styles["No Spacing"])
    document.save(f"{output_dir}/{last_name}_{first_name}_reminder_{num_reminders + 1}.docx")

def generate_reminders(start: int, end: int, output_dir: str):
    pass
