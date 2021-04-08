Set-StrictMode -Version Latest

$LOCATION="germanywestcentral"
$ARG_NAME="myResourceGroup002" 
$AKV_NAME="myKeyVault134234"

New-AzKeyVault `
  -Name ${AKV_NAME} `
  -ResourceGroupName ${ARG_NAME} `
  -Location  ${LOCATION} `
  -EnabledForDeployment `
  -EnabledForDiskEncryption `
  -EnablePurgeProtection

Get-AzKeyVault `
  -VaultName ${AKV_NAME} `
  -ResourceGroupName ${ARG_NAME} `
| Update-AzKeyVault -EnablePurgeProtection