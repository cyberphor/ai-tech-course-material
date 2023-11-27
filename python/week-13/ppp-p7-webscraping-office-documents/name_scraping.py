"""Module for scraping names"""
from requests import codes
from requests import session

URL = "https://www.behindthename.com/names"

def get_names_page(num: int) -> str:
    """Function to get a page"""
    with session() as browser:
        response = browser.get(url=f"{URL}/{num}")
        if codes.ok is response.status_code:
            return(response.text)

if __name__ == "__main__":
    get_names_page(num=4)