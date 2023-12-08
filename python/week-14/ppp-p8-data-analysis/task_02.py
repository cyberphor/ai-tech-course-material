"""Module for Task 2"""
import pandas as pd

def get_country_centric_usability_analysis(source="wdi_exports/wdi_data.pkl", destination="wdi_exports/country-centric-assessment.xlsx"):
  wdi_data = pd.read_pickle(source)
  countries = []
  for country in wdi_data.index.to_list():
    missing_value = wdi_data.loc[country].isna().sum()
    countries.append({
      "Country": country,
      "Missing Values": missing_value,
      "Usability": ""
    })
  print(countries)
    
if __name__ == "__main__":
    get_country_centric_usability_analysis()