sudo mysql -e "use mysql; CREATE USER 'clouduser'@'localhost' IDENTIFIED BY 'dbroot'; GRANT ALL PRIVILEGES ON *.* TO 'clouduser'@'localhost' WITH GRANT OPTION; CREATE USER 'clouduser'@'%' IDENTIFIED BY 'dbroot'; GRANT ALL PRIVILEGES ON *.* TO 'clouduser'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;"
sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.backup
sudo sed -i 's/^[^#]*bind-address/#&/' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo sed -i '/^\[mysqld\]/alocal_infile = 1' /etc/mysql/mysql.conf.d/mysqld.cnf
echo "[client]" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf
echo "local_infile = 1" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf
set global local-infile=1
sudo service mysql restart
cd relational-databases-1/
sudo mysql -u clouduser -pdbroot < create_security_database.sql