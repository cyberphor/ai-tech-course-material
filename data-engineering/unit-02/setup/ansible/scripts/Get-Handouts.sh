wget https://clouddataengineer.blob.core.windows.net/relational-databases-1/relational-databases-1.tgz
tar -xvzf relational-databases-1.tgz
mkdir relational-databases-1
chmod 777 relational-databases-1
tar -xvzf pdatabase.tgz
rm *.tgz
mv *.deb *.ipynb *.sh *.sql *.txt runner submitter relational-databases-1
chmod -R 777 relational-databases-1/
cd relational-databases-1/

wget https://principlesofcomputing.blob.core.windows.net/relational-databases-1/handout/security.zip -O security.zip
unzip security.zip
rm security.zip