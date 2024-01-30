-- MySQL version: 5.7.11+
-- Usage:
-- mysql -h ${DB_NAME}.mysql.database.azure.com -u clouduser@${DB_NAME} -p${DB_PASSWORD} < q7.sql
use security_db;

/**
 * Task Description:
 * If you select the first 20 records from the table `time_series` (make sure you are comfortable with how to do this),
 * you will notice that the column `open_int`` is 0 for every record selected. In fact, you can verify that for all records
 * open_int is 0 by executing and viewing the output of the following query:
 * 
 *    SELECT MAX(open_int) as 'MaxValueOpenInt', MIN(open_int) as 'MinValueOpenInt' FROM time_series;
 * 
 * You will see that `MinValueOpenInt=MaxValueOpenInt=0`, which implies that for all records, `open_int`` is 0. Therefore, we can
 * safely delete this column without losing any important data.
 *
 * https://www.mysqltutorial.org/mysql-drop-column/
 */

-- TODO: write a SQL query that will drop the open_int column from the table time_series