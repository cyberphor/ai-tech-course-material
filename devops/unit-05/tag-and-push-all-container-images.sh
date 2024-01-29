export ACR_NAME="devopsweek12acrcyberphor"
export IMAGES=$(docker image ls | grep latest | grep -v azure | cut -d" " -f1)

for IMAGE in $IMAGES; do 
  docker tag ${IMAGE}:latest ${ACR_NAME}.azurecr.io/${IMAGE}:latest
  docker push ${ACR_NAME}.azurecr.io/${IMAGE}:latest
done