"""Module for scraping names"""
import csv
import json
from typing import Literal
from xml.etree.ElementTree import indent
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
from bs4 import BeautifulSoup
from requests import codes
from requests import session

URL = "https://www.behindthename.com/names"

def get_names_page(num: int) -> str:
    """Function to get a HTML document"""
    try:
        with session() as browser:
            names_page = browser.get(url=f"{URL}/{num}")
            if codes.ok is names_page.status_code:
                return names_page.text
    except ConnectionError as error:
        raise(error)

def extract_page_count(page_text: str) -> int:
    """Function to get number of pages to parse"""
    page_count = BeautifulSoup(page_text, "lxml").find_all("a", class_="pgcanhide")[-1].text
    return int(page_count)

def extract_names_from_page(
        page_text: str,
        gender: bool = True,
        usage: bool = False,
        desc: bool = False
    ) -> dict:
    """Function to parse an HTML document and return a dict of data"""
    extracted_names = {}
    for div in BeautifulSoup(page_text, "lxml").find_all("div", class_="browsename"):
        listname = div.find("span", class_="listname")
        listgender = div.find("span", class_="listgender")
        listusage = div.find("span", class_="listusage")
        extracted = {listname.text: {}}
        if gender:
            extracted[listname.text]["gender"] = listgender.text
        if usage:
            extracted[listname.text]["usage"] = listusage.text
        if desc:
            tags = [
                listname, 
                listgender, 
                listusage, 
                div.find("br")
            ]
            description = [tag.text for tag in div if tag not in tags]
            extracted[listname.text]["desc"] = "".join(description).lstrip()
        extracted_names.update(extracted)
    return extracted_names

def scrape_names(
        pages: list[int],
        output_file_path: str,
        gender: bool = True,
        usage: bool = False,
        desc: bool = False,
        output_format: Literal["csv", "json", "xml"] = "csv"):
    """Function to scrape names and store them in a file"""
    with open(output_file_path, "w", encoding="UTF-8") as data_store:
        names = {}
        for i in pages:
            try:
                page_text = get_names_page(i)
            except Exception as error:
                print(error)
                exit()
            names.update(extract_names_from_page(page_text, gender, usage, desc))
        match output_format:
            case "csv":
                rows = []
                for name in names:
                    row = {"name": name}
                    for i in names[name]:
                        if i == "usage":
                            row.update({"usage": ", ".join(names[name][i])})
                        else:
                            row.update({i: names[name][i]})
                    rows.append(row)
                columns = [fieldname for fieldname in rows[0].keys()]
                writer = csv.DictWriter(data_store, columns)
                writer.writeheader()
                writer.writerows(rows)
            case "json":
                data_store.write(json.dumps(names, indent=4, ensure_ascii=False))
            case "xml":
                scraped_names = Element("names")
                for name in names:
                    scraped_name = SubElement(scraped_names, "name", {"value": name})
                    for i in names[name]:
                        if i == "usage":
                            for use in names[name][i]:
                                SubElement(scraped_name, i).text = use
                        else:
                            SubElement(scraped_name, i).text = names[name][i]
                indent(scraped_names, space="\t")
                ElementTree(scraped_names).write(output_file_path)
