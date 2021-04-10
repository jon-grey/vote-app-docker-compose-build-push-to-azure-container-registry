#!/usr/bin/bash -euo pipefail

. .env
. .secrets.env

echo "AZ_SUBS_ID=${AZ_SUBS_ID}"
echo "AAD_CLIENT_ID=${AAD_CLIENT_ID}"
echo "ADD_TENANT_ID=${ADD_TENANT_ID}"
echo "AAD_SECRET=${AAD_SECRET}"
echo "AAD_PRINCIPAL_NAME=${AAD_PRINCIPAL_NAME}"

echo "${ACR_NAME}.azurecr.io"
# NOTE: UNCOMMENT BELOW TO LOGIN
## az login # in case of error 'The subscription of xxx doesn't exist in cloud AzureCloud'

# Login to azure container registry
## with az cli
# az login 
# This option require to do Step Optional from README
az login --service-principal --username $AAD_CLIENT_ID --tenant $ADD_TENANT_ID --password $AAD_SECRET
az account set --subscription ${AZ_SUBS_ID}
az account list --output table
az acr login --name "${ACR_NAME}"

## OR with to docker providing service principal creds - REDUDANT
# docker login "${ACR_NAME}.azurecr.io" --username ${AAD_CLIENT_ID} --password "${AAD_SECRET}"

docker-compose build
docker push "${ACR_NAME}.azurecr.io/azure-vote-flask-mysql:${IMAGE_VER}"
# docker push "${ACR_NAME}.azurecr.io/azure-vote-mysql:v1"
# docker push "${ACR_NAME}.azurecr.io/azure-vote-flask-cosmosdb:v1"
