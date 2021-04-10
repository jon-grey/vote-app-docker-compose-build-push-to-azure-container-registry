Set-StrictMode -Version Latest
. .env

## Step 0 - Create Managed Identity (AMI)
az identity create   --resource-group ${ARG_NAME}  --name ${AMI_NAME}
$identityID=(az identity show --resource-group ${ARG_NAME}  --name ${AMI_NAME} --query 'id' --output tsv)
$identityPrincipalID=(az identity show --resource-group ${ARG_NAME} --name ${AMI_NAME} --query 'principalId' --output tsv)


## Step 1 - Get Key Vault (AKV)
$KeyVault = Get-AzKeyVault  -Name ${AKV_NAME} -ResourceGroupName ${ARG_NAME} 

## Step 1.1 - Add full permissions for self to AKV

# Grant full permissions to KV to current user
$UserObjectId = (az ad signed-in-user show --query 'objectId' --output tsv)

az keyvault set-policy `
  --resource-group ${ARG_NAME}  `
  --name ${AKV_NAME} `
  --object-id $UserObjectId `
  --certificate-permissions backup create delete deleteissuers get getissuers import list listissuers managecontacts manageissuers purge recover restore setissuers update `
  --key-permissions backup create decrypt delete encrypt get import list purge recover restore sign unwrapKey update verify wrapKey `
  --secret-permissions backup delete get list purge recover restore set `
  --storage-permissions backup delete deletesas get getsas list listsas purge recover regeneratekey restore set setsas update 


## Step 1.2 - Add some permisssions for AMI to AKV
az keyvault set-policy `
  --resource-group ${ARG_NAME}  `
  --name ${AKV_NAME} `
  --object-id $identityPrincipalID `
  --key-permissions get unwrapKey wrapKey `
  --secret-permissions delete get list purge recover restore set


## Step 1.3 - Create key in AKV that we will use by ACR
az keyvault key create `
  --name "myKey" `
  --vault-name ${AKV_NAME} `

$keyID=(az keyvault key show `
  --name "myKey" `
  --vault-name ${AKV_NAME} `
  --query 'key.kid' --output tsv)

$keyID=(echo $keyID | sed -e "s/\/[^/]*$//")


## Step 2 - Setup Azure Container Registry (ACR) with AMI and AKV key

#################################################################################
#### Create Container Registry
#################################################################################

#                         BASIC	            STANDARD	        PREMIUM
# Price per day	          $0.167	          $0.667	          $1.667
# Included storage (GB)	  10	              100	              500
#                                                             * Premium offers 
#                                                             * enhanced throughput 
#                                                             * for docker pulls 
#                                                             * across multiple, 
#                                                             * concurrent nodes
# Total web hooks	        2	                10	              500
# Geo Replication	        Not Supported	    Not Supported	    Supported
#                                                             * $1.667 per 
#                                                             * replicated region

# https://azure.microsoft.com/en-us/pricing/details/container-registry/

# TODO only premium support encryption, do we need it?
#      --identity and --key-encryption-key must be both supplied
#      Premium is paid $1.677 per day. Maybe can spend few bucks?
az acr create `
  --resource-group ${ARG_NAME} `
  --name $ACR_NAME `
  --identity $identityID `
  --key-encryption-key $keyID `
  --sku Premium

# TODO Maybe use basic, price is 
# az acr create `
#   --resource-group ${ARG_NAME} `
#   --name $ACR_NAME `
#   --sku Basic

