from requests import Session
from bs4 import BeautifulSoup


def scrape_quotes():
    quotes = "https://quotes.toscrape.com/page/"
    page_number = 1
    browser = Session()
    urls = []
    while True:
        url = f"{quotes}{page_number}"
        urls.append(url)
        response = browser.get(url)
        page = BeautifulSoup(response.text, "lxml").find_all("li", class_="next")
        if len(page) == 0:
            break
        for next_tag in page:
            for href_tag in next_tag.find_all("a"):
                page_number = int(href_tag["href"].split("/")[2])
    browser.close()
    [print(url) for url in urls]


if __name__ == "__main__":
    scrape_quotes()
