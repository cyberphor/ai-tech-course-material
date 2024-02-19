az group create \
    --name project3 \
    --location eastus &&\
az acr create \
    --resource-group project3 \
    --name $ACR_NAME \
    --sku Basic &&\
az acr login \
    --name $ACR_NAME &&\
az aks create \
    --resource-group project3 \
    --name project3cluster \
    --enable-managed-identity \
    --node-count 2 \
    --generate-ssh-keys &&\
az aks update \
    --resource-group project3 \
    --name project3cluster \
    --attach-acr $ACR_NAME &&\
az aks get-credentials \
    --resource-group project3 \
    --name project3cluster