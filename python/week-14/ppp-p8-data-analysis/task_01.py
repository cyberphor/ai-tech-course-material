"""Module for Task 1"""
from os import mkdir
from os import path
import pandas as pd

def get_education_data(source_file: str="wdi_data/worldDevInds2017-education.csv"):
    """Function to get education data"""
    education_data = pd.read_csv(
        source_file,
        usecols=[0,14,21,36,46,56,81,86],
        header=0,
        index_col=0,
        names=[
            "Country Name",
            "Compulsory education (years)",
            "Doctoral degrees (%)",
            "Completed primary education (%)",
            "Government expenditure on education (%)",
            "Literacy rate (%)",
            "Primary education (years)",
            "Primary school (starting age)"
        ]
    )
    return education_data

def get_health_data(source_file: str="wdi_data/healthWorld-2017-worldBank.xlsx"):
    """Function to get health data"""
    with pd.ExcelFile(source_file, engine="openpyxl") as xlsx_file:
        health_data = pd.merge(
            pd.read_excel(
                xlsx_file,
                sheet_name="Life expectancy at birth,2",
                usecols=[0, 4],
                header=None,
                names=["Country", "Life expectancy (years)"],
            ),
            pd.read_excel(
                xlsx_file,
                sheet_name="Mortality rate, infant (p",
                usecols=[0, 4],
                header=None,
                names=["Country", "Birth mortality rate (per 1,000)"]
            )
        )
        health_data.set_index("Country", inplace=True)
        return health_data

def get_infrastructure_data(source_file: str="wdi_data/2017infra.json"):
    data = pd.read_json(source_file).transpose()
    transporation  = pd.json_normalize(data.iloc[:,0]).set_index(data.index)
    communications = pd.json_normalize(data.iloc[:,1]).set_index(data.index)
    technology     = pd.json_normalize(data.iloc[:,2]).set_index(data.index)
    print(transporation)
    print(communications)
    print(technology)
    #print(data.iloc[0,:].iloc[0]["Air transport, passengers carried"]) # first row, first row
    #print(data.iloc[1,:])
    #print(data.iloc[2,:])
    #data = pd.read_json(source_file).transpose()
    #print(data["Transportation"]["Air transport, passengers carried"])
    #[print(key) for key in data["Transportation"].iloc[0].keys()]
    #print(data["Transportation"])
    #"Air transport, passengers carried"
    #[print(key) for key in data["Communications"].iloc[0].keys()]
    #[print(key) for key in data["Technology"].iloc[0].keys()]
    
def get_poverty_data():
    pass

def merge_data():
    pass

def store_data(destination: str, source: pd.DataFrame):
    """Function to store a pandas DataFrame"""
    folder = destination.split("/")[0]
    if not path.exists(folder):
        mkdir(folder)
    source.to_pickle(destination)

if __name__ == "__main__":
    get_infrastructure_data()