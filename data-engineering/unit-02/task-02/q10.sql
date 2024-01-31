-- MySQL version: 5.7.11+
-- Usage:
-- mysql -h ${DB_NAME}.mysql.database.azure.com -u clouduser@${DB_NAME} -p${DB_PASSWORD} < q10.sql
use security_db;
/**
 * Task Description:
 * 
 * This question is much more open-ended than the previous ones. After executing this file:
 *  1. There should be no records that represent the information of test issue securities
 *  2. There should be one table called nasdaq_info that contains the records of securities listed on NYSE, NYSE MKT, NYSE ARCA,
 *     and NASDAQ. This table should have the following fields: id (type bigint) (primary key), symbol (type varchar(14)), 
 *     security_name (type varchar(255)), market_category (type enum('G', 'Q', 'S')), 
 *     financial_status (type enum('D', 'E', 'Q', 'N', 'G', 'H', 'J', 'K')), round_lot_size (type int), 
 *     etf (type enum('Y', 'N')), exchange (type enum('A', 'P', 'N', 'Q')) 
 *  3. The primary key constraint should be honored in the final nasdaq_info table. This implies that if you remove the primary
 *     key constraint or create a new table without one, you will not receive credit for this task.
 *  4. Securities that are not listed on NASDAQ should record their Nasdaq Integrated Platform symbol in the symbol field of
 *     the final nasdaq_info table and record a null value into any NASDAQ-specific fields
 *
 * You will likely need to write multiple queries. Be careful as the order in which you do the various data manipulation steps
 * for this task will affect the correctness of your solution. It is highly recommended that you backup your database
 * prior to this question.
 */

-- filter out test issue securities from both tables (nasdaq_info and
-- other_exchange_info)
DELETE FROM nasdaq_info WHERE test_issue='Y';
DELETE FROM other_exchange_info WHERE test_issue='Y';
 
-- drop test issue column from nasdaq_info
ALTER TABLE nasdaq_info DROP COLUMN test_issue;
ALTER TABLE other_exchange_info DROP COLUMN test_issue;

-- insert records from other_exchange_info into nasdaq_info
-- EXAMPLE:
-- #################################################
-- # insert into users (user_id, date_joined)
-- # select id,date_joined
-- # from dashboard.auth_user;
INSERT INTO nasdaq_info (symbol, security_name, market_category, financial_status, round_lot_size, etf, next_shares, exchange) 
SELECT nasdaq_symbol, security_name, null, null, round_lot_size, etf, null, exchange
FROM other_exchange_info;