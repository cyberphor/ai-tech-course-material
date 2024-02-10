az group create \
  --location "eastus" \
  --name "SimpleLLM" &&\
az storage account create \
  --location "eastus" \
  --resource-group "SimpleLLM" \
  --name "simplellmstorageaccount" \
  --sku "Standard_LRS" &&\
az functionapp create \
  --consumption-plan-location "eastus" \
  --resource-group "SimpleLLM" \
  --name "SimpleLLM" \
  --os-type "linux" \
  --functions-version 4 \
  --runtime "python" \
  --runtime-version "3.8" \
  --storage-account "simplellmstorageaccount" &&\
echo "Waiting 30 seconds..." &&\
sleep 30 &&\
func azure functionapp publish "SimpleLLM"