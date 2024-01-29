use mysql;
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbroot';
GRANT ALL PRIVILEGES ON *.* TO 'dbuser'@'localhost' WITH GRANT OPTION;