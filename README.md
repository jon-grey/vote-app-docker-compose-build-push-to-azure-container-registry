
## Setup service principal for whole subscription

### Via Azure (Portal) Shell

[Authenticate with service principal - Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-service-principal)

### Via Azure Portal

#### Go to AAD 

![](images/README/2021-04-06-22-36-51.png)

#### App Registrations 

![](images/README/2021-04-06-22-37-14.png)

#### new registration -> ...

![](images/README/2021-04-06-22-37-47.png)

#### Grab `AAD_CLIENT_ID` and `ADD_TENANT_ID`

![](images/README/2021-04-08-14-29-15.png)

#### Create `secret` and save as `ACR_PASS`

![](images/README/2021-04-06-22-38-14.png)

![](images/README/2021-04-06-22-38-31.png)

#### Assign role to subscription to controll all resources in subscription:

![](images/README/2021-04-06-22-40-18.png)

#### Or assing role to Container Registry to controll only it:

![](images/README/2021-04-06-22-49-18.png)

#### Here set service principal as `Owner`

![](images/README/2021-04-06-22-45-43.png)


# Development

Go and fill in `.env` and `.secrets.env` with data needed by next steps.

## Setup Azure Resources

First Key Vault (AKV) if not already exists. In powershell...

```ps1
powershell setup-key-vault.ps1
powershell setup-managed-identity-and-container-registry.ps1
```

Now in bash. Create RBAC ASP and save secret as key to AKV.

```sh
bash setup-rbac-service-principal-save-to-key-vault.sh
```

It will recreate .rbac.secrets.env file used when pushing.

## Build and ship steps


> Note: first follow prep steps

```sh
# build and test
docker-compose up --build
# build only
docker-compose build
# push to registry
bash push-images-to-azure-container-registry.sh
```

# Scripts in tmp

Probably not needed. 