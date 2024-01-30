-- MySQL version: 5.7.11+
-- Usage:
-- mysql -h ${DB_NAME}.mysql.database.azure.com -u clouduser@${DB_NAME} -p${DB_PASSWORD} < q8.sql
use security_db;

/**
 * Task Description:
 * 
 * Reading the NasdaqTrader's documentation (http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs) for their datasets, you will notice that the file otherlistedMod.txt 
 * contains records on securities that are traded on the following exchanges: NYSE, NYSE MKT, NYSE ARCA, BATS Global Markets (BATS),
 * and on the Investor's Exchange, LLC (IEXG). However, also observe that we only need to have the time series data for the securities that are 
 * traded on NYSE or NASDAQ. For q8(), your task is to filter out the records in the table other_exchange_info_q8 for securities 
 * that are listed on BATS and IEXG.
 */

-- TODO: Delete the records in other_exchange_info that correspond to securities listed on BATS and IEXG