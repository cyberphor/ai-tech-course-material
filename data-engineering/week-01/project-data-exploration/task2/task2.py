import pandas as pd
from numpy import int64, float64

AIRLINES_CSV_PATH = 'airlines.csv'
AIRPORTS_CSV_PATH = 'airports.csv'
FLIGHTS_CSV_PATH = 'flights.csv'

def generate_pandas_df_dict(csv_paths, table_names=None, index_cols=None):
    if table_names is None:
        table_names = csv_paths
    if index_cols is None:
        index_cols = (None,) * len(csv_paths)
    df_dict = {}
    for csv_path, table_name, index_col in zip(csv_paths, table_names, index_cols):
        df_dict[table_name] = pd.read_csv(csv_path, index_col=index_col, low_memory=False)
    return df_dict

def show_tables(df_dict):
    print('=== TABLES ===')
    for name, df in sorted(df_dict.items()):
        print(f"- {name} ({df.shape[0]} rows, {df.shape[1]} columns)")
    print(f'TOTAL {len(df_dict)}')

def describe_table(df):
    print('=== COLUMNS ===')
    for column, dtype in sorted(zip(df.columns, df.dtypes)):
        series = df[column]
        if dtype == int64 or dtype == float64:
            print(f'- {column} {dtype} ({series.count()}/{series.size}) ' +
                  f'[Max: {series.max()}, Mean: {series.mean()}, Min: {series.min()}]')
        else:
            print(f'- {column} {dtype} ({series.count()}/{series.size}) ' +
                  f'[{len(series.unique())} unique]')
    print(f'TOTAL {df.shape[0]}')

def assess_useless_columns(df):
    for column in df.columns:
        series = df[column]
        if series.count() == 0:
            print(f'The column {column} appears to have no values.')
        if series.nunique(dropna=False) == 1:
            print(f'The column {column} appears to have only one value.')

def generate_delays_per_airline_csv(df_dict, csv_path):
    delays_per_airline = pd.merge(
        left=df_dict['flights'][['AIRLINE','ARRIVAL_DELAY']].groupby(['AIRLINE']).mean(),
        right=df_dict['airlines'],
        left_index=True,
        right_index=True
    )[['AIRLINE', 'ARRIVAL_DELAY']]
    delays_per_airline.sort_values(by='ARRIVAL_DELAY', ascending=False, ignore_index=True, inplace=True)
    delays_per_airline.to_csv(csv_path, index=False)

def generate_delays_per_arriving_airport_csv(df_dict, csv_path):
    delays_per_airline = pd.merge(
        left=df_dict['flights'][['DESTINATION_AIRPORT','ARRIVAL_DELAY']].groupby(['DESTINATION_AIRPORT']).mean(),
        right=df_dict['airports'],
        left_on='DESTINATION_AIRPORT',
        right_on='AIRPORT'
    )[['AIRPORT', 'ARRIVAL_DELAY']]
    delays_per_airline.sort_values(by='ARRIVAL_DELAY', ascending=False, ignore_index=True, inplace=True)
    delays_per_airline.to_csv(csv_path, index=False)

if __name__ == "__main__":
    df_dict = generate_pandas_df_dict((AIRLINES_CSV_PATH, AIRPORTS_CSV_PATH, FLIGHTS_CSV_PATH), ('airlines', 'airports', 'flights'), (0, 0, None))
    generate_delays_per_arriving_airport_csv(df_dict, 'out.csv')