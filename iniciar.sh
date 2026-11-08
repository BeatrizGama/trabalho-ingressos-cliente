#!/bin/sh
cd "$(dirname "$0")" || exit 1
SERVIDOR="$1"
if [ -z "$SERVIDOR" ]; then
  printf "Endereco IP do servidor: "
  read -r SERVIDOR
fi
.venv/bin/python cliente.py "$SERVIDOR"
