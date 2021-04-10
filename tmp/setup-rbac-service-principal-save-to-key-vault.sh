#!/usr/bin/bash -euo pipefail
. .env
. .secrets.env


# Login to azure container registry
az login 
az account set --subscription ${AZ_SUBS_ID}
az account list --output table


AAD_ACR_PUSH_PRINCIPAL_NAME="${ACR_NAME}-push"
AAD_ACR_PUSH_CLIENT_ID_NAME="${ACR_NAME}-push-usr"
AAD_ACR_PUSH_SECRET_NAME="${ACR_NAME}-push-pwd"

# Create service principal, store its password in AKV (the registry *password*)
ACR_SCOPES=$(az acr show --name $ACR_NAME --query id --output tsv)
AAD_ACR_PUSH=$(az ad sp create-for-rbac --name $AAD_ACR_PUSH_PRINCIPAL_NAME --scopes $ACR_SCOPES --role acrpush)

AAD_ACR_PUSH_SECRET=$(python -c "print($AAD_ACR_PUSH['password'])")
ADD_ACR_PUSH_TENANT_ID=$(python -c "print($AAD_ACR_PUSH['tenant'])")

az keyvault secret set --vault-name $AKV_NAME --name $AAD_ACR_PUSH_SECRET_NAME --value $AAD_ACR_PUSH_SECRET

# Store service principal ID in AKV (the registry *username*)
AAD_ACR_PUSH_CLIENT_ID=$(az ad sp show --id http://$AAD_ACR_PUSH_PRINCIPAL_NAME --query appId --output tsv)

OUT_FILE=".rbac.secrets.env"

rm $OUT_FILE
touch $OUT_FILE
echo AAD_PRINCIPAL_NAME=$AAD_ACR_PUSH_PRINCIPAL_NAME >> $OUT_FILE
echo AAD_CLIENT_ID=$AAD_ACR_PUSH_CLIENT_ID >> $OUT_FILE
echo ADD_TENANT_ID=$ADD_ACR_PUSH_TENANT_ID >> $OUT_FILE
echo AAD_SECRET=$AAD_ACR_PUSH_SECRET >> $OUT_FILE
