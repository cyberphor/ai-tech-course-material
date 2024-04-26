"""Module for Task 1"""

from os import mkdir
from os import path
import pandas as pd


def get_education_data(source_file: str = "wdi_data/worldDevInds2017-education.csv"):
    """Function to get education data"""
    education_data = pd.read_csv(
        source_file,
        usecols=[0, 14, 21, 36, 46, 56, 81, 86],
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
            "Primary school (starting age)",
        ],
    )
    return education_data


def get_health_data(source_file: str = "wdi_data/healthWorld-2017-worldBank.xlsx"):
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
                names=["Country", "Birth mortality rate (per 1,000)"],
            ),
        )
        health_data.set_index("Country", inplace=True)
        return health_data


def get_infrastructure_data(source_file: str = "wdi_data/2017infra.json"):
    """Function to get infrastructure data"""
    data = pd.read_json(source_file)  # original df
    countries = data.axes[1]  # axis 1 = column names, axis 0 = row names
    transportation = pd.json_normalize(data.iloc[0]).set_index(
        countries
    )  # create new df using 1st series in original df
    communications = pd.json_normalize(data.iloc[1]).set_index(
        countries
    )  # create new df using 2nd series in original df
    technology = pd.json_normalize(data.iloc[2]).set_index(
        countries
    )  # create new df using 3rd series in original df
    filters = [
        "Air transport, passengers carried",
        "Fixed broadband subscriptions (per 100 people)",
        "Individuals using the Internet (% of population)",
        "High-technology exports (% of manufactured exports)",
        "Research and development expenditure (% of GDP)",
        "Technicians in R&D (per million people)",
    ]
    labels = [
        "Air travel passengers",
        "Broadband subscriptions (per 100 people)",
        "Internet use (% of population)",
        "High-tech exports (%)",
        "R&D expenditure (% of GDP)",
        "Technicians in R&D (per million people)",
    ]
    infrastructure_data = transportation.join(communications).join(technology)[filters]
    infrastructure_data.rename(columns=dict(zip(filters, labels)), inplace=True)
    return infrastructure_data


def get_poverty_data(
    source_file: str = "wdi_data/World_Development_Indicators_Poverty_2017.xml",
):
    """Function to get poverty data"""
    poverty_data = (
        pd.DataFrame(
            data={
                "Country": pd.read_xml(
                    path_or_buffer=source_file,
                    xpath="/countries/country",
                    attrs_only=True,
                    parser="lxml",
                )["name"],
                "Gini index": pd.read_xml(
                    path_or_buffer=source_file,
                    xpath="/countries/country/field[@metric='Gini index (World Bank estimate)']",
                    parser="lxml",
                )["field"],
                "Income share of highest 10%": pd.read_xml(
                    path_or_buffer=source_file,
                    xpath="/countries/country/field[@metric='Income share held by highest 10%']",
                    parser="lxml",
                )["field"],
                "Daily consumption per capita (USD)": pd.read_xml(
                    path_or_buffer=source_file,
                    xpath="/countries/country/field[@metric='Survey mean consumption or income per capita, total population (2011 PPP $ per day)']",
                    parser="lxml",
                )["field"],
            }
        )
        .set_index("Country")
        .rename_axis(index=None)
    )
    return poverty_data


def store_data(destination: str, source: pd.DataFrame):
    """Function to store a pandas DataFrame"""
    folder = destination.split("/")[0]
    if not path.exists(folder):
        mkdir(folder)
    source.to_pickle(destination)


if __name__ == "__main__":
    education_data = get_education_data()
    health_data = get_health_data()
    infrastructure_data = get_infrastructure_data()
    poverty_data = get_poverty_data()
    wdi_data = (
        education_data.join(health_data)
        .join(infrastructure_data)
        .join(poverty_data)
        .rename_axis(index=None)
    )
    data = {
        "wdi_exports/education_data.pkl": education_data,
        "wdi_exports/health_data.pkl": health_data,
        "wdi_exports/infrastructure_data.pkl": infrastructure_data,
        "wdi_exports/poverty_data.pkl": poverty_data,
        "wdi_exports/wdi_data.pkl": wdi_data,
    }
    for destination, source in data.items():
        store_data(destination, source)
