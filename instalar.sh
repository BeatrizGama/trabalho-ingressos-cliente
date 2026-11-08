#!/bin/sh
cd "$(dirname "$0")" || exit 1
echo "Instalando o cliente de ingressos..."

OPCOES_VENV=""
if [ -n "$TERMUX_VERSION" ] || echo "$PREFIX" | grep -q "com.termux"; then
  # Android (Termux): usa o gRPC ja compilado do Termux, sem compilar nada.
  echo "Android (Termux) detectado."
  # upgrade completo: o gRPC do Termux precisa das bibliotecas (libc++) atualizadas
  pkg upgrade -y || exit 1
  pkg install -y python python-grpcio || exit 1
  OPCOES_VENV="--system-site-packages"
fi

rm -rf .venv
if ! python3 -m venv $OPCOES_VENV .venv; then
  echo ""
  echo "ERRO: nao foi possivel criar o ambiente."
  echo "No Ubuntu/Debian, rode: sudo apt install python3 python3-venv"
  exit 1
fi
.venv/bin/python -m pip install --prefer-binary -r requirements.txt || exit 1
echo ""
echo "Pronto! Agora rode: sh iniciar.sh"
