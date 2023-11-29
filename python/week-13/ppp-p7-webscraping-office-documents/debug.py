"""Module for debugging and developing this week's solution"""
import name_scraping

name_scraping.scrape_names(
    pages=[1,2,3,4],
    output_file_path="debug.csv",
    gender=True,
    usage=True,
    desc=bool,
    output_format="csv"
)

name_scraping.scrape_names(
    pages=[1,2,3,4],
    output_file_path="debug.json",
    gender=True,
    usage=True,
    desc=bool,
    output_format="json"
)

name_scraping.scrape_names(
    pages=[1,2,3,4],
    output_file_path="debug.xml",
    gender=True,
    usage=True,
    desc=bool,
    output_format="xml"
)