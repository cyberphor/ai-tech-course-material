export LINUX_AGENT_DOWNLOAD_URL="https://vstsagentpackage.azureedge.net/agent/3.227.2/vsts-agent-linux-x64-3.227.2.tar.gz"
export DEPLOYMENT_GROUP="QA"
export PROJECT_ORG="victorfernandeziii"
export PROJECT_NAME="week09"
export PAT="hhs3jcpiz4wjd7saa72elzd3wku5x4brmuap4q7q7xqx3fk4lbxa" # good luck :)
export DEPLOYMENT_GROUP_TAG="ci-cd-pipeline-for-vm-hosted-webservices"

mkdir azagent
cd azagent
curl -fkSL -o vstsagent.tar.gz "{$LINUX_AGENT_DOWNLOAD_URL}"
tar -zxvf vstsagent.tar.gz
if [ -x "$(command -v systemctl)" ]; 
  then ./config.sh \
    --deploymentgroup \
    --deploymentgroupname "${DEPLOYMENT_GROUP}" \
    --acceptteeeula \
    --agent $HOSTNAME \
    --url "https://dev.azure.com/${PROJECT_ORG}" \
    --work _work \
    --projectname "${PROJECT_NAME}" \
    --auth PAT \
    --token "${PAT}" \
    --deploymentgrouptags "${DEPLOYMENT_GROUP_TAG}" \
    --runasservice 
    sudo ./svc.sh install
    sudo ./svc.sh start
else ./config.sh \
  --deploymentgroup \
  --deploymentgroupname "${DEPLOYMENT_GROUP}" \
  --acceptteeeula \
  --agent $HOSTNAME \
  --url "https://dev.azure.com/${PROJECT_ORG}" \
  --work _work \
  --projectname "${PROJECT_NAME}" \
  --auth PAT \
  --token "${PAT}" \
  --deploymentgrouptags "${DEPLOYMENT_GROUP_TAG}" \
  --unattended
  ./run.sh
fi