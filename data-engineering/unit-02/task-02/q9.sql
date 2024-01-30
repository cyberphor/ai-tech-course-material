-- MySQL version: 5.7.11+
-- Usage:
-- mysql -h ${DB_NAME}.mysql.database.azure.com -u clouduser@${DB_NAME} -p${DB_PASSWORD} < q9.sql
use security_db;

/**
 * Task Description:
 * 
 * As an intermediate step to consolidating the nasdaq_info and other_exchange_info tables into one table for easier analysis,
 * we would like to add a column to the nasdaq_info table that matches the exchange column in the table other_exchange_info.
 * This way, when we merge the two tables, we will be able to differentiate securities that have come from different
 * exchanges correctly. Let's denote securities that are traded on NASDAQ by 'Q'.
 */

-- TODO: add a column called `exchange` to nasdaq_info with an enumerated type having options
-- 'A', 'N', 'P', 'Q'. For each record in nasdaq_info_q9, its value for `exchange` should be Q.
-- alter table nasdaq_info add column exchange enum(<FILL_IN>) default <FILL_IN>;