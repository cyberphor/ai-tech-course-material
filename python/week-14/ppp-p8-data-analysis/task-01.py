"""Module for Task 1"""
import os
import pandas

def task1(data_source_path: str):
    data = pandas.read_csv(data_source_path)
    columns = [
        "Compulsory education, duration (years)",
        "Educational attainment, Doctoral or equivalent, population 25+, total (%) (cumulative)",
        "Educational attainment, at least completed primary, population 25+ years, total (%) (cumulative)",
        "Government expenditure on education, total (% of GDP)",
        "Literacy rate, adult total (% of people ages 15 and above)",
        "Primary education, duration (years)",
        "Primary school starting age (years)"
    ]
    education_data = pandas.DataFrame(data[columns], index=data["Country Name"])
    print(education_data.to_pickle("wdi_exports/education_data.pkl"))

if __name__ == "__main__":
    task1(data_source_path="wdi_data/worldDevInds2017-education.csv")