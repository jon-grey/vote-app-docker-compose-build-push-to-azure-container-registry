Set-StrictMode -Version Latest

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