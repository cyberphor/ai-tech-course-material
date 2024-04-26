"""Module for using a web API"""

from os import mkdir
from os import path
from pygsheets import authorize
from docx import Document


def get_google_sheet():
    """Function to get a Google Sheet"""
    client = authorize(service_account_file="algebraic-ratio-338019-eb975aa8f686.json")
    workbook = client.open("Accounts")  # name of Google Sheet
    return workbook.sheet1  # tab 1


def get_accounts_info(fields: list[str] = None, start: int = 0, end: int = 9):
    """Function to get records from a Google Sheet"""
    worksheet = get_google_sheet()
    accounts = []
    for record in worksheet.get_all_records()[start : (end + 1)]:
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
    amount_owed: float = 0,
    num_reminders: int = 0,
    output_dir: str = "",
):
    """Function for creating a Microsoft Word document"""
    if not path.exists(output_dir):
        mkdir(output_dir)
    reminder = [
        f"{title} {first_name} {last_name}",
        f"{street}",
        f"{city}, {state} {zip_code}\n\n\n\n\n\n\n",
        f"Dear {title} {last_name},\n\n",
        f"Payment on your XYZ account in the amount of ${amount_owed:.2f} is due.\n\n",
        f"We have already sent you {num_reminders} reminders.\n\n",
        "Please, disregard this notice if you have already made the payment.\n\n\n\n\n\n\n",
        "Best Regards.\n\n",
        "John Doe",
        "Account Manager XYZ",
    ]
    document = Document()
    match num_reminders:
        case 0:
            reminder = reminder[0:5] + reminder[6:]
        case 1:
            reminder[5] = (f"We have already sent you {num_reminders} reminder.\n\n",)
    for paragraph in reminder:
        document.add_paragraph(paragraph, style=document.styles["No Spacing"])
    document.save(
        f"{output_dir}/{last_name}_{first_name}_reminder_{num_reminders + 1}.docx"
    )


def generate_reminders(start: int, end: int, output_dir: str):
    """Function to create multiple Microsoft Word documents"""
    accounts = get_accounts_info(start=start, end=end)
    for account in accounts:
        generate_reminder(
            account["First Name"],
            account["Last Name"],
            account["Title"],
            account["Street"],
            account["City"],
            account["State"],
            account["ZIP"],
            account["Amount Owed"],
            account["Number of Reminders"],
            output_dir,
        )
