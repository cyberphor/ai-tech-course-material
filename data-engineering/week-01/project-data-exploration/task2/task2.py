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
        df_dict[table_name] = pd.read_csv(csv_path, index_col=index_col)
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
        if series.value_counts(dropna=False) == 1:
            print(f'The column {column} appears to have only one value.')

def generate_delays_per_airline_csv(df_dict, csv_path):
    #df_dict = df_dict['flights'][[<COLUMN_1>,<COLUMN_2>]]
    #mean = df_dict.groupby([<COLUMN>]).mean()
    columns_to_sort = [['AIRLINE', 'ARRIVAL_DELAY']]
    pd.merge(mean,
        df_dict['airlines'],
        left_index=True,
        right_index=True
    ).columns_to_sort.sort_values(
        by='ARRIVAL_DELAY', ascending=False, ignore_index=True
    ).to_csv(csv_path, index=False)

def generate_delays_per_arriving_airport_csv(df_dict, csv_path):
    # YOUR SOLUTION HERE
    pass
    # You can take this as a self challenge for self practise or upload the code. 
    # Write a one-line solution minimizing the use of variables. 

if __name__ == "__main__":
    df_dict = generate_pandas_df_dict((AIRLINES_CSV_PATH, AIRPORTS_CSV_PATH, FLIGHTS_CSV_PATH), ('airlines', 'airports', 'flights'), (0, 0, None))
    #show_tables(df_dict)
    #describe_table(df_dict['airports'])
    assess_useless_columns(df_dict['airports'])
    generate_delays_per_arriving_airport_csv(df_dict, 'out.csv')