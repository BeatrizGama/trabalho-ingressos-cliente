#!/bin/sh
cd "$(dirname "$0")" || exit 1
echo "Instalando o cliente de ingressos..."
if ! python3 -m venv .venv; then
  echo ""
  echo "ERRO: nao foi possivel criar o ambiente."
  echo "No Ubuntu/Debian, rode: sudo apt install python3 python3-venv"
  exit 1
fi
.venv/bin/python -m pip install -r requirements.txt || exit 1
echo ""
echo "Pronto! Agora rode: ./iniciar.sh"
