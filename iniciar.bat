@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "SERVIDOR=%~1"
if "%SERVIDOR%"=="" set /p "SERVIDOR=Endereco IP do servidor: "
.venv\Scripts\python cliente.py %SERVIDOR%
pause
