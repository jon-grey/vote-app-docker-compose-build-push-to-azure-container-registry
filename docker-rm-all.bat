@echo off
FOR /f "tokens=*" %%i IN ('docker ps -aq') DO docker rm -f -v %%i
@REM FOR /f "tokens=*" %%i IN ('docker images --format "{{.ID}}"') DO docker rmi -f %%i