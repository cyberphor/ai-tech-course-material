wget https://clouddataengineer.blob.core.windows.net/large-scale-batch-processing/handout/sail2/v2/large-scale-batch-processing.zip
unzip large-scale-batch-processing.zip
cd ~/large-scale-batch-processing
chmod +x databricks-setup.sh
./databricks-setup.sh
databricks workspace import-dir ./starter-code/ /