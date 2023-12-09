"""Module for Task 2"""
import pandas as pd

def get_country_centric_usability_analysis(source="wdi_exports/wdi_data.pkl", destination="wdi_exports/country-centric-assessment.xlsx"):
    wdi_data = pd.read_pickle(source)
    countries = []
    for country in wdi_data.index.to_list():
        missing_values = wdi_data.loc[country].isna().sum()
        if missing_values > 15:
          usability = "None"
        elif missing_values <= 15 and missing_values > 10:
          usability = "Marginal"
        elif missing_values <= 10 and missing_values > 6:
          usability = "Fair"
        elif missing_values <= 6 and missing_values > 3:
          usability = "Good"
        else:
          usability = "Excellent"
        countries.append({
            "Country Name": country,
            "Missing Values": missing_values,
            "Usability": usability
        })
    pd.DataFrame.from_dict(countries).to_excel(
        index=None,
        excel_writer=destination,
        sheet_name="Countries Missing Data"
    )
    
if __name__ == "__main__":
    get_country_centric_usability_analysis()