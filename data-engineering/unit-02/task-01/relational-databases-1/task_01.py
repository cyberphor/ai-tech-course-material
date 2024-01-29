import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import re

def normalize_filename(filename):
    new_label = ''
    new_label = re.sub('-ws-', '+', filename)
    new_label = re.sub('-ws', '+', new_label)
    # === YOUR SOLUTION STARTS HERE ===
    # Do not change the code above.
    #
    # TODO 1: Following the examples above change the `new_label`
    #         variable so that "-cl" is replaced with "*" and
    #         "-u" is replaced with "=".
    new_label = re.sub('-cl', '*', new_label)
    new_label = re.sub('-u', '=', new_label)
    # Do not change the code below.
    # === YOUR SOLUTION ENDS HERE ===
    if(re.fullmatch('.*-.*', new_label)):
        new_label = re.sub('-', '.', new_label)
    elif(re.fullmatch('.*_.*', new_label)):
        new_label = re.sub('_', '-', new_label)
    return new_label.upper()

def file2df(dirname, filename, security_id):
    """ Given:
        dirname: a string representing the path to the directory containing the file with name filename
        filename: a string representing the name of a file in directory dirname
        securityID: a number representing the foreign key value assigned to this particular security
    
        This method when called with the correct arguments should return a pandas Dataframe containing the columns
        Date (of type datetime),Open, High, Low, Close, Volume, OpenInt, ID (of type int)
        populated with the data from the given file.
    """
    filepath = os.path.join(dirname, filename)
    df = pd.read_csv(filepath, sep=',')
    # === YOUR SOLUTION STARTS HERE ===
    # Do not change the code above.
    #
    # TODO 2: Add a column named ID that will have a constant
    #         value equal to the `securityID` argument.
    df["ID"] = security_id
    # TODO 3: Use pandas `to_datetime` function to parse the
    #         `Date` column to datetimes.
    df["Date"] = pd.to_datetime(df["Date"])
    # Do not change the code below.
    # === YOUR SOLUTION ENDS HERE ===
    return df

def dirname2etf(dirname):
    """ Given the path to the directory containing the information of a particular security, 
    determine the contents of the "ETF" column of its record in Table 2
    """
    # === YOUR SOLUTION STARTS HERE ===
    # Do not change the code above.
    #
    # TODO 4: Implement the function that extracts the right most subdirectory
    #         of the provided `dirname` path. If the name of the subdirectory
    #         is "ETFs" then the function returns "Y" else it returns "N".
    if dirname.split("/")[-1] == "ETFs":
        return "Y"
    else:
        return "N"
    # Do not change the code below.
    # === YOUR SOLUTION ENDS HERE ===

def filename2ticker(filename):
    """ Given the filename of the file containing the time series data on a particular security,
    determine the contents of the "Ticker" column of its record in Table 2
    """
    # === YOUR SOLUTION STARTS HERE ===
    # Do not change the code above.
    #
    # TODO 5: Implement the function that extracts the left most part of the
    #         provided filename (i.e., up till the first dot). The earlier
    #         implemented `normalize_filename` function is then used on the
    #         extracted part to create the desired result.
    # Do not change the code below.
    # === YOUR SOLUTION ENDS HERE ===

def build_security_dfs():
    """ This method should return a tuple of the form (frame_time_series 
        frame_tickers) where frame_time_series is a pandas DataFrame representing
        the data found in the text files of the dataset along with the assigned
        foreign key ID, and frame_tickers is a DataFrame representing the second
        table of our chosen representation. 
        """
    directory = os.walk('./Data/')
    data_time_series = []
    ticker_inf = {'id': [], 'ticker': [], 'ETF': []}
    id_cntr = 0
    for dirname, _, filenames in sorted(directory):
        if len(filenames) == 0:
            continue
        type_ind = dirname2etf(dirname) #"Y" or "N"
        for filename in sorted(filenames):
            if os.path.getsize(os.path.join(dirname, filename)) > 0:
                # === YOUR SOLUTION STARTS HERE ===
                # Do not change the code above.
                #
                # TODO 6: Use `dirname`, `filename`, and `id_cntr` as
                #         arguments in the `file2df` that you implemented
                #         earlier to generate a dataframe object. Append
                #         the generated dataframe to the end of
                #         `data_time_series` list.
                # TODO 7: Use `filename` as the argument in the
                #         `filename2ticker` that you implemented earlier
                #         to generate a normalized ticker. Append the
                #         `id_cntr` to the list under the `id` key of the
                #         `ticker_inf` dictionary. Append the normalized
                #         ticker to the list under the `ticker` key of the
                #         `ticker_inf` dictionary. Append the `type_ind`
                #         to the list under the `ETF` key of the
                #         `ticker_inf` dictionary.
                # TODO 8: Increment the value of `id_ctr` variable by 1.
                pass
    frame_time_series = pd.concat(data_time_series)
    frame_tickers = pd.DataFrame(data=ticker_inf)
    return (frame_time_series, frame_tickers)

if __name__ == "__main__":
    # TODO 1:
    assert normalize_filename("abcd-ws")  == "ABCD+"
    assert normalize_filename("ab-ws-z")  == "AB+Z"
    assert normalize_filename("abd-ws-u") == "ABD+U"
    assert normalize_filename("cd-cl")    == "CD*"
    assert normalize_filename("cd_a-cl")  == "CD-A*"
    assert normalize_filename("def-u")    == "DEF="
    assert normalize_filename("def-a")    == "DEF.A"
    assert normalize_filename("def_a")    == "DEF-A"

    # TODO 2 and TODO 3:
    file2df("./Data/ETFs", "schz.us.txt", 1)
    
    # TODO 4:
    assert dirname2etf("./Data/ETFs")   == "Y"
    assert dirname2etf("./Data/Stocks") == "N"

    # TODO 4:
    assert filename2ticker("inda.us.txt")   == "INDA"
    assert filename2ticker("c-ws-a.us.txt") == "C+A"
    assert filename2ticker("cof_c.us.txt")  == "COF-C"