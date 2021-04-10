
@REM ESET | Azure Active Directory -> App registrations -> New: ad-app-executor
SET APP_ID="38039648-bcde-4f5e-8179-c762c7e24dbf"
SET TENANT_ID="01f7e0e8-c680-4293-8068-d572231a88f4"
@REM ESET | Azure Active Directory -> App registrations -> ad-app-executor 
@REM -> Certificates & secrets -> new client secret -> copy value
SET PASSWORD="tN~3vAO-4uUVh58vllaUqvB_9t7HI~a-Js"

@REM Subskrypcja programu Visual Studio Professional | Access control (IAM) -> Add : ad-app-executor

az login --service-principal --username %APP_ID% --tenant %TENANT_ID% --password %PASSWORD%
az acr login --name crExecutor
docker pull hello-world
docker tag hello-world "crexecutor.azurecr.io/hello-world:v1"
docker push "crexecutor.azurecr.io/hello-world:v1"