# =====================================================================
# cliente.py  -  CLIENTE DO SISTEMA DE VENDA DE INGRESSOS (gRPC)
# =====================================================================
# Menu de texto que chama as funções REMOTAS do servidor.
# O ponto central do RPC: no código abaixo, comprar um ingresso parece
# uma chamada de função comum (stub.ComprarIngresso(...)), mas ela é
# executada em OUTRO computador. Isso é a "transparência de acesso".
#
# Como rodar:
#   python cliente.py                 -> conecta no servidor desta máquina
#   python cliente.py 192.168.0.15    -> conecta no servidor de outra máquina
# =====================================================================

import sys     # para ler o IP do servidor da linha de comando

import grpc                  # biblioteca gRPC (canal, erros de rede)
import ingressos_pb2         # GERADO: classes das mensagens (PedidoCompra, etc.)
import ingressos_pb2_grpc    # GERADO: o STUB do cliente (VendaIngressosStub)

PORTA = 50051     # precisa ser a MESMA porta em que o servidor está escutando
TIMEOUT = 5       # segundos: se o servidor não responder nesse tempo, desistimos


# ---------------------------------------------------------------------
# CHAMADA REMOTA PROTEGIDA
# ---------------------------------------------------------------------
# Numa chamada LOCAL, a função sempre está lá. Numa chamada REMOTA, a
# rede pode falhar, o servidor pode estar desligado ou travado. Essa é
# a grande diferença entre RPC e chamada local.
# Esta função faz a chamada e trata os erros de rede num lugar só.

def chamar(funcao_remota, pedido):
    try:
        # timeout = "deadline": o gRPC cancela a chamada se passar de TIMEOUT.
        return funcao_remota(pedido, timeout=TIMEOUT)
    except grpc.RpcError as erro:
        # erro.code() diz o TIPO de falha de rede (códigos de status do gRPC).
        if erro.code() == grpc.StatusCode.UNAVAILABLE:
            print("\n  [REDE] Servidor indisponível: está ligado? O IP e a porta estão certos?"
                  "\n  O firewall da máquina do servidor libera a porta 50051?")
        elif erro.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            print(f"\n  [REDE] O servidor não respondeu em {TIMEOUT} segundos.")
        else:
            print(f"\n  [REDE] Erro na chamada remota: {erro.code().name} - {erro.details()}")
        return None


# ---------------------------------------------------------------------
# FUNÇÕES DE TELA (só imprimem as respostas de forma organizada)
# ---------------------------------------------------------------------

def mostrar_ingresso(ing):
    print(f"  Ingresso nº {ing.id} | {ing.nome_evento} ({ing.data_evento}) | "
          f"assento {ing.assento} | dono: {ing.usuario} | status: {ing.status}")


def mostrar_mapa(mapa):
    """Desenha os assentos: [  ] livre, [XX] vendido."""
    print(f"\n  {mapa.nome_evento}   ([  ] livre   [XX] vendido)")
    print("     " + "".join(f"{n:>4} " for n in range(1, mapa.assentos_por_fileira + 1)))
    for f in range(mapa.fileiras):
        # Os assentos vêm em ordem: A1, A2, ..., B1, B2...; pegamos a fatia da fileira f.
        fileira = mapa.assentos[f * mapa.assentos_por_fileira:(f + 1) * mapa.assentos_por_fileira]
        letra = chr(ord("A") + f)
        print(f"  {letra}  " + "".join(" [XX]" if a.vendido else " [  ]" for a in fileira))


def ler_inteiro(texto):
    """Lê um número do teclado sem deixar o programa quebrar se digitarem letras."""
    while True:
        valor = input(texto).strip()
        if valor.isdigit():
            return int(valor)
        print("  Digite um número.")


# ---------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------

def main():
    # IP do servidor: o primeiro argumento, ou "localhost" (esta própria máquina).
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    endereco = f"{host}:{PORTA}"

    # 1) CANAL: representa a conexão com o servidor.
    #    "insecure" = sem TLS (sem criptografia), igual ao servidor.
    #    Detalhe: o gRPC só abre a conexão TCP de verdade na primeira chamada
    #    (por isso um servidor desligado só dá erro quando você escolhe uma opção).
    canal = grpc.insecure_channel(endereco)

    # 2) STUB: o "dublê" do servidor aqui no cliente. Ele tem um método para
    #    cada rpc do .proto. Ao chamar stub.ComprarIngresso(pedido), o stub:
    #    a) serializa o pedido em bytes (Protobuf)  -> marshalling
    #    b) envia por HTTP/2 dentro da conexão TCP
    #    c) espera a resposta, e converte os bytes de volta em objeto
    stub = ingressos_pb2_grpc.VendaIngressosStub(canal)

    print("=" * 60)
    print(f" Sistema de Venda de Ingressos  -  servidor {endereco}")
    print("=" * 60)
    usuario = ""
    while not usuario:
        usuario = input("Seu nome de usuário: ").strip()

    while True:
        print(f"\n--- Menu ({usuario}) ---")
        print(" 1. Listar eventos")
        print(" 2. Ver mapa de assentos")
        print(" 3. Comprar ingresso")
        print(" 4. Cancelar compra")
        print(" 5. Meus ingressos")
        print(" 6. Consultar um ingresso")
        print(" 7. Criar evento            (extra)")
        print(" 8. Transferir ingresso     (extra)")
        print(" 9. Validar entrada         (extra - portaria)")
        print("10. Relatório de vendas     (extra)")
        print("11. Trocar de usuário")
        print(" 0. Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            # ingressos_pb2.Vazio() é a mensagem vazia: a função não tem parâmetros.
            r = chamar(stub.ListarEventos, ingressos_pb2.Vazio())
            if r:
                if not r.sucesso:
                    print(f"  {r.mensagem}")
                for e in r.eventos:
                    print(f"  [{e.id}] {e.nome} | {e.data} | {e.local} | "
                          f"{e.assentos_livres}/{e.total_assentos} livres")

        elif opcao == "2":
            pedido = ingressos_pb2.PedidoEvento(id_evento=ler_inteiro("  ID do evento: "))
            r = chamar(stub.ConsultarAssentos, pedido)
            if r:
                mostrar_mapa(r) if r.sucesso else print(f"  {r.mensagem}")

        elif opcao == "3":
            # Montamos a MENSAGEM de pedido (o "formulário" definido no .proto)...
            pedido = ingressos_pb2.PedidoCompra(
                usuario=usuario,
                id_evento=ler_inteiro("  ID do evento: "),
                assento=input("  Assento (ex.: B4): "),
            )
            # ...e chamamos a função remota como se fosse local.
            r = chamar(stub.ComprarIngresso, pedido)
            if r:
                print(f"  {r.mensagem}")
                if r.sucesso:
                    mostrar_ingresso(r.ingresso)

        elif opcao == "4":
            pedido = ingressos_pb2.PedidoCancelamento(
                usuario=usuario, id_ingresso=ler_inteiro("  Nº do ingresso: "))
            r = chamar(stub.CancelarCompra, pedido)
            if r:
                print(f"  {r.mensagem}")

        elif opcao == "5":
            r = chamar(stub.ConsultarIngressosUsuario, ingressos_pb2.PedidoUsuario(usuario=usuario))
            if r:
                if not r.sucesso:
                    print(f"  {r.mensagem}")
                for ing in r.ingressos:
                    mostrar_ingresso(ing)

        elif opcao == "6":
            pedido = ingressos_pb2.PedidoIngresso(id_ingresso=ler_inteiro("  Nº do ingresso: "))
            r = chamar(stub.ConsultarIngresso, pedido)
            if r:
                mostrar_ingresso(r.ingresso) if r.sucesso else print(f"  {r.mensagem}")

        elif opcao == "7":
            pedido = ingressos_pb2.PedidoCriarEvento(
                nome=input("  Nome do evento: "),
                data=input("  Data (AAAA-MM-DD HH:MM): "),
                local=input("  Local: "),
                fileiras=ler_inteiro("  Quantas fileiras (1-26): "),
                assentos_por_fileira=ler_inteiro("  Assentos por fileira (1-50): "),
            )
            r = chamar(stub.CriarEvento, pedido)
            if r:
                print(f"  {r.mensagem}")

        elif opcao == "8":
            pedido = ingressos_pb2.PedidoTransferencia(
                usuario_origem=usuario,
                id_ingresso=ler_inteiro("  Nº do ingresso: "),
                usuario_destino=input("  Transferir para (usuário): "),
            )
            r = chamar(stub.TransferirIngresso, pedido)
            if r:
                print(f"  {r.mensagem}")

        elif opcao == "9":
            pedido = ingressos_pb2.PedidoIngresso(id_ingresso=ler_inteiro("  Nº do ingresso: "))
            r = chamar(stub.ValidarEntrada, pedido)
            if r:
                print(f"  {r.mensagem}")
                if r.ingresso.id:
                    mostrar_ingresso(r.ingresso)

        elif opcao == "10":
            pedido = ingressos_pb2.PedidoEvento(id_evento=ler_inteiro("  ID do evento: "))
            r = chamar(stub.RelatorioVendas, pedido)
            if r:
                if r.sucesso:
                    print(f"  {r.nome_evento}: {r.vendidos} vendidos de {r.total_assentos} "
                          f"({r.ocupacao:.1f}% de ocupação) | {r.livres} livres | "
                          f"{r.usados} já entraram | {r.cancelados} cancelados")
                else:
                    print(f"  {r.mensagem}")

        elif opcao == "11":
            novo = input("  Novo usuário: ").strip()
            usuario = novo or usuario

        elif opcao == "0":
            canal.close()   # fecha a conexão TCP com o servidor de forma educada
            print("Até mais!")
            break

        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    main()
