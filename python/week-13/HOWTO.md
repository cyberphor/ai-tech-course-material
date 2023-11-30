# Web Scraping

## Setup
**Step 1.** Download the provided source code. 
```bash
wget https://principlesofcomputing.blob.core.windows.net/ppp-p7-webscraping-office-documents/handout/sail2/ppp-p7-webscraping-office-documents.zip
```

**Step 2.** Open the source code. 
```bash
unzip ppp-p7-webscraping-office-documents.zip
```

**Step 3.** Activate the provided Python virtual environment. 
```bash
cd ppp-p7-webscraping-office-documents
python -m venv p7-env
source p7-env/bin/activate
```

**Step 4.** Download the provided source code's dependencies. 
```bash
python -m pip install -r requirements.txt
```

## Task 1
**Step 1.** Create a file called `name_scraping.py`. 
```bash
touch name_scraping.py
```

**Step 2.** Add the code below to it. 
```python
"""Module for scraping names"""
import csv
import json
from typing import Literal
from sys import exit
from xml.etree.ElementTree import indent
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import parse
from bs4 import BeautifulSoup
from openpyxl import Workbook
from requests import codes
from requests import session

def get_names_page(num: int) -> str:
    """Function to download a HTML document"""
    URL = "https://www.behindthename.com/names"
    with session() as browser:
        try:
            names_page = browser.get(url=f"{URL}/{num}")
            if names_page.status_code == codes.ok:
                return names_page.text
            else:
                raise Exception
        except:
            print(f"Connection failed (URL: {URL})")
            exit()

def extract_page_count(page_text: str) -> int:
    """Function to get number of pages to parse"""
    page_count = BeautifulSoup(page_text, "lxml").find_all("a", class_="pgcanhide")[-1].text
    return int(page_count)

def extract_names_from_page(page_text: str, gender: bool = True, usage: bool = False, desc: bool = False) -> dict:
    """Function to parse an HTML document"""
    extracted_names = {}
    for div in BeautifulSoup(page_text, "lxml").find_all("div", class_="browsename"):
        listname = div.find("span", class_="listname")
        listgender = div.find("span", class_="listgender")
        listusage = div.find("span", class_="listusage")
        extracted = {listname.text: {}}
        if gender:
            extracted[listname.text]["gender"] = listgender.text
        if usage:
            extracted[listname.text]["usage"] = listusage.text.split(", ")
        if desc:
            tags = [listname, listgender, listusage, div.find("br")]
            description = [tag.text for tag in div if tag not in tags]
            extracted[listname.text]["desc"] = "".join(description).lstrip()
        extracted_names.update(extracted)
    return extracted_names

def scrape_names(pages: list[int], output_file_path: str, gender: bool = True, usage: bool = False, desc: bool = False, output_format: Literal["csv", "json", "xml"] = "csv"):
    """Function to carve-out names and their metadata"""
    names = {}
    for page in pages:
        page_text = get_names_page(page)
        names.update(extract_names_from_page(page_text, gender, usage, desc))
    match output_format:
        case "csv":
            rows = []
            for name in names:
                row = {"name": name}
                for i in names[name]:
                    if i == "usage":
                        names[name]["usage"] = ", ".join(names[name]["usage"])                        
                    row.update({i: names[name][i]})
                rows.append(row)
            columns = list(rows[0].keys())
            with open(output_file_path, "w", encoding="UTF-8") as csv_file:
                writer = csv.DictWriter(csv_file, columns)
                writer.writeheader()
                writer.writerows(rows)
        case "json":
            with open(output_file_path, "w", encoding="UTF-8") as json_file:
                json_file.write(json.dumps(names, indent=4, ensure_ascii=False))
        case "xml":
            scraped_names = Element("names")
            for name in names:
                scraped_name = SubElement(scraped_names, "name", {"value": name})
                for i in names[name]:
                    if i == "usage":
                        use_cases = names[name]["usage"]
                        for use_case in use_cases:
                            SubElement(scraped_name, "usage").text = use_case
                    else:
                        SubElement(scraped_name, i).text = names[name][i]
            indent(scraped_names, space="\t")
            ElementTree(scraped_names).write(output_file_path, encoding="UTF-8")
```

## Task 2
**Step 1.** Add the code below to the file created in Task 1 (i.e., `name_scraping.py`).
```python
def json_to_excel(json_file_path: str, excel_file_path: str):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "names"
    with open(json_file_path, "r", encoding="UTF-8") as json_file:
        names = json.loads(json_file.read())
    worksheet.append(["name"] + [column for column in names[list(names)[0]].keys()])
    for name in names:
        row = [name]
        for cell in names[name]:
            if cell == "usage":
                row.append(", ".join(names[name][cell]))
            else:
                row.append(names[name][cell])
        worksheet.append(row)
    workbook.save(excel_file_path)

def csv_to_excel(csv_file_path: str, excel_file_path: str):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "names"
    with open(csv_file_path, "r", encoding="UTF-8") as csv_file:
        [worksheet.append(name) for name in csv.reader(csv_file)]
    workbook.save(excel_file_path)

def xml_to_excel(xml_file_path: str, excel_file_path: str):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "names"
    names = parse(xml_file_path).getroot()
    worksheet.append(list(dict.fromkeys(name.tag for name in names[0].iter())))
    for parent in names:
        name   = [parent.attrib["value"]] 
        gender = [child.text for child in parent.iter("gender")]
        usage  = [child.text for child in parent.iter("usage")]
        desc   = [child.text for child in parent.iter("desc")]
        if usage:
            worksheet.append(name + gender + [", ".join(usage)] + desc)
        else: 
            worksheet.append(name + gender + desc)
    workbook.save(excel_file_path)
```

## Task 3
**Step 1.** Create a file called `retrieve_from_gsheet.py`. 
```bash
touch retrieve_from_gsheet.py
```

**Step 2.** Add the code below to it. 
```python
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
```

## Task 4
**Step 1.** Add the code below to the file created in Task 3 (i.e., `retrieve_from_gsheet.py`).
```python
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
        output_dir: str = ""  
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
        "Account Manager XYZ"
    ]
    document = Document()
    match num_reminders:
        case 0:
            reminder = reminder[0:5] + reminder[6:]
        case 1:
            reminder[5] = f"We have already sent you {num_reminders} reminder.\n\n",
    for paragraph in reminder:
        document.add_paragraph(paragraph, style=document.styles["No Spacing"])
    document.save(f"{output_dir}/{last_name}_{first_name}_reminder_{num_reminders + 1}.docx")

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
            output_dir
        )
```