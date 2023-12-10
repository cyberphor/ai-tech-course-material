"""Module for Task 2"""
import pandas as pd

def get_country_centric_usability(source="wdi_exports/wdi_data.pkl", destination="wdi_exports/country-centric-assessment.xlsx"):
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

def get_statistic_centric_usability(source="wdi_exports/wdi_data.pkl", destination="wdi_exports/statistic-centric-assessment.xlsx"):
    wdi_data = pd.read_pickle(source)
    statistics = []
    for column in range(len(wdi_data.iloc[0,:])):
        missing_values = wdi_data.iloc[:,column].isna().sum()
        if missing_values > 180:
          usability = "None"
        elif missing_values <= 180 and missing_values > 100:
          usability = "Marginal"
        elif missing_values <= 100 and missing_values > 60:
          usability = "Fair"
        elif missing_values <= 60 and missing_values > 30:
          usability = "Good"
        else:
          usability = "Excellent"
        statistics.append({
            "Statistic Name": wdi_data.iloc[:,column].name,
            "Missing Values": missing_values,
            "Usability": usability
        })
    pd.DataFrame.from_dict(statistics).to_excel(
        index=None,
        excel_writer=destination,
        sheet_name="Statistics Missing Data"
    )

def get_descriptive_statistics(source="wdi_exports/wdi_data.pkl", destination="wdi_exports/wdi_summary.xlsx"):
    wdi_data = pd.read_pickle(source)
    descriptive_statistics = []
    for column in range(len(wdi_data.iloc[0,:])):
        statistic =  wdi_data.iloc[:,column]
        statistic_name = statistic.name[:31]
        descriptive_statistics.append([
            pd.DataFrame({
                "Summary": {
                    "Max": statistic.max(),
                    "Mean": statistic.mean(),
                    "Min": statistic.min(),
                }
              },
            ),
            pd.DataFrame({"Top 10": statistic.sort_values(ascending=False)[:10].sort_index().sort_values(ascending=False)}),
            pd.DataFrame({"Bottom 10": statistic.sort_values(ascending=True)[0:10].sort_index().sort_values(ascending=True)})
        ])
    for statistic in descriptive_statistics[0]:
      print(statistic)

if __name__ == "__main__":
    #get_country_centric_usability()
    #get_statistic_centric_usability()
    get_descriptive_statistics()