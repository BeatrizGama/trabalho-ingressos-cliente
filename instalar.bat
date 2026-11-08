@echo off
cd /d "%~dp0"
echo Instalando o cliente de ingressos...
python -m venv .venv
if errorlevel 1 (
  echo.
  echo ERRO: Python nao encontrado. Instale em https://www.python.org/downloads/
  echo e marque a opcao "Add Python to PATH".
  pause
  exit /b 1
)
.venv\Scripts\python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Tentando de novo usando os certificados do Windows...
  .venv\Scripts\python -m pip install --use-feature=truststore -r requirements.txt
)
echo.
echo Pronto! Agora de dois cliques em iniciar.bat
pause
