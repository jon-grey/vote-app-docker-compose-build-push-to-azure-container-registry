
SET CR="crexecutorx"

@REM Azure Active Directory -> App registrations -> New: ad-app-executorx
SET APP_ID="018d0910-78bf-47b1-af62-6ada57b9d744"
SET TENANT_ID="4e0bfea1-1425-4dbd-9173-7f9db28c3ded"
@REM ad-app-executorx -> Certificates & secrets -> new client secret -> copy value
SET PASSWORD="5~4XU7r3~ey74p.J4SMfon.O~nlJY2Aoes"

@REM Subskrypcja XYZ | Access control (IAM) -> Add : ad-app-executorx
SET SUBS="47ce52c2-1af8-4c4c-92e3-69d8ee255a8e"

@REM NOTE: UNCOMMENT BELOW TO LOGIN
@REM call az account set --subscription %SUBS%
@REM call az account list --output table
@REM call az login --service-principal ^
@REM               --username %APP_ID% ^
@REM               --tenant %TENANT_ID% ^
@REM               --password %PASSWORD% 
@REM call az acr login --name %CR%

call docker-compose build
call docker push "%CR%.azurecr.io/azure-vote-flask-mysql:v1"
call docker push "%CR%.azurecr.io/azure-vote-mysql:v1"
call docker push "%CR%.azurecr.io/azure-vote-flask-cosmosdb:v1"
