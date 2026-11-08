# Ingressos — Cliente

Programa para comprar, consultar e gerenciar ingressos de eventos.
Ele se conecta ao **servidor de ingressos** pela rede.

---

## Antes de começar

Você vai precisar de:

- **Python 3.10 ou mais novo**
- O **endereço IP do servidor** (peça a quem cuida do servidor, ex.: `192.168.0.15`)
- Estar na **mesma rede** que o servidor (mesmo Wi-Fi, por exemplo)

---

## Instalação no Windows

**1. Instale o Python** (se ainda não tiver)

Baixe em https://www.python.org/downloads/ e, na primeira tela do instalador,
marque a opção **"Add Python to PATH"**.

**2. Baixe o programa**

Nesta página, clique em **Code → Download ZIP** e extraia a pasta onde preferir.

**3. Instale**

Dê dois cliques em **`instalar.bat`** e espere aparecer "Pronto!".

**4. Use**

Dê dois cliques em **`iniciar.bat`**, digite o IP do servidor e aperte Enter.

---

## Instalação no Linux

**1. Instale o Python** (se ainda não tiver)

```bash
sudo apt install python3 python3-venv git
```

**2. Baixe o programa**

```bash
git clone https://github.com/BeatrizGama/trabalho-ingressos-cliente.git
cd trabalho-ingressos-cliente
```

**3. Instale**

```bash
sh instalar.sh
```

**4. Use**

```bash
sh iniciar.sh
```

Digite o IP do servidor e aperte Enter.

> Dica: dá para passar o IP direto, sem a pergunta: `sh iniciar.sh 192.168.0.15`
> (no Windows: `iniciar.bat 192.168.0.15`).

---

## Como usar

Ao abrir, digite seu **nome de usuário**. Depois escolha uma opção do menu
digitando o número e apertando Enter:

| Opção | O que faz |
|------:|-----------|
| 1 | Lista os eventos disponíveis |
| 2 | Mostra o mapa de assentos de um evento (`[  ]` livre, `[XX]` vendido) |
| 3 | Compra um ingresso (informe o ID do evento e o assento, ex.: `B4`) |
| 4 | Cancela uma compra |
| 5 | Mostra os seus ingressos |
| 6 | Consulta um ingresso pelo número |
| 7 | Cria um novo evento |
| 8 | Transfere um ingresso seu para outra pessoa |
| 9 | Valida a entrada de um ingresso (uso na portaria) |
| 10 | Mostra o relatório de vendas de um evento |
| 11 | Troca de usuário |
| 0 | Sai do programa |

---

## Deu problema?

**"Servidor indisponível"**
- Confira se o servidor está ligado.
- Confira se o IP digitado está certo.
- Confira se você está na mesma rede que o servidor.
- O computador do servidor precisa liberar a porta **50051** no firewall.

**"python não é reconhecido" (Windows)**
- Reinstale o Python marcando **"Add Python to PATH"**.

**Erro de certificado (SSL) ao instalar**
- No Windows, o `instalar.bat` já tenta resolver sozinho. Se continuar,
  pode ser o antivírus bloqueando: tente em outra rede.
