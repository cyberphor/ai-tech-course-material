-- MySQL version: 5.7.11+
-- Usage:
-- mysql -h ${DB_NAME}.mysql.database.azure.com -u clouduser@${DB_NAME} -p${DB_PASSWORD} --local-infile=1 < q6.sql
use security_db;

/**
 * Task Description:
 * Load the data from the files nasdaqlistedMod.txt and otherlistedMod.txt into the tables
 * nasdaq_info and other_exchange_info, respectively.
 *
 * Hints: 
 *  1. The input data files do not use commas as field delimiters, instead using pipes (|)
 *  2. The first line of both the files is a list of the fields.  
 *  3. nasdaq_info and other_exchange_info both use the auto-incremented column id as a primary key. The data files
 *     do not contain such a column, so think carefully about how to properly load the data from these files so as to ensure
 *     primary key constraints are satisfied.
 */

load data local infile 'nasdaqlistedMod.txt'
    into table nasdaq_info
    fields terminated by '|'
    enclosed by ''
    lines terminated by '\n'
    ignore 1 rows
    (symbol, security_name, market_category, test_issue, financial_status, round_lot_size, etf, next_shares)
    set id=null;

-- TODO: load data into the other_exchange_info table
load data local infile 'otherlistedMod.txt'
    into table other_exchange_info
    fields terminated by '|'
    enclosed by ''
    lines terminated by '\n'
    ignore 1 rows
    (symbol, security_name, market_category, test_issue, financial_status, round_lot_size, etf, next_shares)
    set id=null;