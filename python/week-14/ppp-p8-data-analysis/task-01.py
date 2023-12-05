"""Module for Task 1"""
import os
import pandas

def get_education_data(source_file: str = "wdi_data/worldDevInds2017-education.csv"):
  """Function to get education data"""
  filters = [
    "Compulsory education, duration (years)",
    "Educational attainment, Doctoral or equivalent, population 25+, total (%) (cumulative)",
    "Educational attainment, at least completed primary, population 25+ years, total (%) (cumulative)",
    "Government expenditure on education, total (% of GDP)",
    "Literacy rate, adult total (% of people ages 15 and above)",
    "Primary education, duration (years)",
    "Primary school starting age (years)"
  ]
  labels = [
    "Compulsory education (years)",
    "Doctoral degrees (%)",
    "Completed primary education (%)",
    "Government expenditure on education (%)",
    "Literacy rate (%)",
    "Primary education (years)",
    "Primary school (starting age)"
  ]
  data = pandas.read_csv(source_file)
  return pandas.DataFrame(data, columns=filters).rename(index=data["Country Name"], columns=dict(zip(filters, labels)))

def store_dataframe(dataframe: pandas.DataFrame, destination_folder: str, destination_file: str):
  """Function to store a pandas DataFrame"""
  if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
  dataframe.to_pickle(f"{destination_folder}/{destination_file}")

if __name__ == "__main__":
  education_data = get_education_data()
  store_dataframe(education_data, destination_folder="wdi_exports", destination_file="education_data.pkl")
  print(education_data)