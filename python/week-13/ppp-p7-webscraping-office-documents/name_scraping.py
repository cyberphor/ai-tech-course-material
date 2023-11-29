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
        usage  = [", ".join([child.text for child in parent.iter("usage")])]
        desc   = [child.text for child in parent.iter("desc")]
        worksheet.append(name + gender + usage + desc)
    workbook.save(excel_file_path)