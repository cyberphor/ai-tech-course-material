"""Module for scraping names"""
from typing import Literal
from bs4 import BeautifulSoup
from requests import codes
from requests import session

URL = "https://www.behindthename.com/names"

def get_names_page(num: int) -> str:
    """Function to get a HTML document"""
    with session() as browser:
        names_page = browser.get(url=f"{URL}/{num}")
        if codes.ok is names_page.status_code:
            return names_page.text

def extract_page_count(page_text: str) -> int:
    """Function to get number of pages to parse"""
    return BeautifulSoup(page_text, "lxml").find_all("a", class_="pgcanhide")[-1].text

def extract_names_from_page(
        page_text: str,
        gender: bool = True,
        usage: bool = False,
        desc: bool = False
    ) -> dict:
    """Function to parse an HTML document and return a dict of data"""
    extracted_names = dict()
    for div in BeautifulSoup(page_text, "lxml").find_all("div", class_="browsename"):
        NAME      = div.find("span", class_="listname")
        GENDER    = div.find("span", class_="listgender")
        USAGE     = div.find("span", class_="listusage")
        extracted = {NAME.text: {}}
        if gender:
            extracted[NAME.text]["gender"] = GENDER.text
        if usage:
            extracted[NAME.text]["usage"] = USAGE.text.split(", ")
        if desc:
            tags = [NAME, GENDER, USAGE, div.find("br")]
            description = [tag.text for tag in div if tag not in tags]
            extracted[NAME.text]["desc"] = "".join(description).lstrip()
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
    pass

if __name__ == "__main__":
    names_page = get_names_page(num=4)
    page_count = extract_page_count(page_text=names_page)
    extracted_names = extract_names_from_page(
        page_text=names_page, 
        gender=True, 
        usage=True, 
        desc=True
    )