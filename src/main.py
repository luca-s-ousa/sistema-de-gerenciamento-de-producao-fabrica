import json
import uuid

divisor = "\n|=====================================|\n"


def acessar_banco_de_dados():
    with open("banco_de_dados.json", "r") as arquivo:
        bd = json.load(arquivo)
        lista_de_ordens = bd["ordens_de_producao"]
    return lista_de_ordens


def atualizar_banco_de_dados(dados):
    with open("banco_de_dados.json", "w") as arquivo:
        arquivo.write(json.dumps(dados))


def percorrer_materiais_necessarios(materiais):
    mensagem = ""
    for material in materiais:
        mensagem += material + ","
    return mensagem


def imprimir_detalhada_a_ordem_de_producao(ordem_de_producao):
    return f"|ID: {ordem_de_producao['id']}|\n|nome_do_produto: {ordem_de_producao['nome_do_produto']}|\n|quantidade: {ordem_de_producao['quantidade']}|\n|data_de_entrega: {ordem_de_producao['data_de_entrega']}|\n|materiais_necessarios: {percorrer_materiais_necessarios(ordem_de_producao['materiais_necessarios'])}|{divisor}"


def fitro_ordens_em_andamento(lista_de_ordens):
    return lista_de_ordens["status"] == "em andamento"


def fitro_ordens_concluidas(lista_de_ordens):
    return lista_de_ordens["status"] == "concluida"


def nova_ordem_de_producao(ordem_de_producao):
    lista_de_ordens = acessar_banco_de_dados()

    lista_de_ordens.append(ordem_de_producao)

    registrar_no_banco = {
        "ordens_de_producao": lista_de_ordens,
    }

    atualizar_banco_de_dados(registrar_no_banco)

    return "\n|ORDEM DE PRODUCAO CADASTRADA COM SUCESSO|\n"


def relatorio_de_producao():
    lista_de_ordens = acessar_banco_de_dados()
    mensagem_final = ""
    ordens_concluidas_personalizacao = "|==========ORDENS CONCLUIDAS==========|\n"
    ordens_em_andamento_personalizacao = "|==========ORDENS EM ANDAMENTO==========|\n"

    ordens_em_andamento = list(filter(fitro_ordens_em_andamento, lista_de_ordens))
    ordens_concluidas = list(filter(fitro_ordens_concluidas, lista_de_ordens))

    for ordem in ordens_concluidas:
        ordens_concluidas_personalizacao += imprimir_detalhada_a_ordem_de_producao(
            ordem
        )

    for ordem in ordens_em_andamento:
        ordens_em_andamento_personalizacao += imprimir_detalhada_a_ordem_de_producao(
            ordem
        )

    mensagem_final += ordens_em_andamento_personalizacao
    mensagem_final += ordens_concluidas_personalizacao

    return mensagem_final


def listar_ordens_de_producao_existentes():
    ordens_de_producao_existentes = acessar_banco_de_dados()
    for ordem in ordens_de_producao_existentes:
        print(imprimir_detalhada_a_ordem_de_producao(ordem))


def atualizar_status_de_uma_ordem_de_producao(id_ordem_de_producao, novo_status):
    lista_de_ordens_de_producao = acessar_banco_de_dados()

    for ordem in lista_de_ordens_de_producao:
        if ordem["id"] == id_ordem_de_producao:
            lista_de_ordens_de_producao.remove(ordem)
            ordem["status"] = novo_status
            lista_de_ordens_de_producao.append(ordem)
            registrar_no_banco = {"ordens_de_producao": lista_de_ordens_de_producao}
            atualizar_banco_de_dados(registrar_no_banco)
            return "|ORDEM DE PRODUCAO ATUALIZADA COM SUCESSO|"

    return "|ORDEM DE PRODUCAO NAO ENCONTRADA|"


def verificar_possibilidade_de_producao_de_uma_ordem(id_ordem_de_producao):
    contador = 0
    itens_disponiveis = 0
    lista_de_ordens_de_producao = acessar_banco_de_dados()
    print("|==========VERIFICAR PRODUTOS DISPONÍVEIS==========|")
    for ordem in lista_de_ordens_de_producao:
        if ordem["id"] == id_ordem_de_producao:
            while contador < len(ordem["materiais_necessarios"]):
                print(f"|VOCE TEM {ordem['materiais_necessarios'][contador]}?|")
                print("\n|===== 1-SIM 2-NAO =====|\n")
                resposta = int(input("Insira aqui sua resposta: "))
                if resposta == 1:
                    itens_disponiveis += 1
                    contador += 1
                elif resposta == 2:
                    return "|VOCE ESTA NAO APTO A PRODUZIR ESTE PRODUTO|"
                else:
                    print("|===== RESPOSTA INVÁLIDA =====|")
                    continue
            if itens_disponiveis == len(ordem["materiais_necessarios"]):
                return "|VOCE ESTA APTO A PRODUZIR ESTE PRODUTO|"
            else:
                return "|VOCE ESTA NAO APTO A PRODUZIR ESTE PRODUTO|"


opcao = 99

while opcao != 0:
    print("\n|========== SISTEMA DE GERENCIAMENTO DE ORDENS DE PRODUCAO ==========|\n")
    print("|========== ESCOLHA UMA OPCAO PARA PROSSEGUIR ==========|\n")
    print("| 1 - CADASTRAR NOVA ORDEM DE PRODUCAO |\n")
    print("| 2 - VER ORDENS DE PRODUCAO EXISTENTES|\n")
    print("| 3 - ATUALIZAR STATUS DE ORDEM DE PRODUCAO|\n")
    print("| 4 - VERIFICAR POSSIBILIDADE DE PRODUCAO DE UMA ORDEM|\n")
    print("| 5 - EXIBIR RELATORIO DAS ORDENS DE PRODUCAO|\n")
    print("| 0 - SAIR DO SISTEMA|\n")
    print(divisor)
    opcao = int(input("INSIRA SUA RESPOSTA AQUI: "))

    if opcao == 0:
        continue
    elif opcao == 2:
        listar_ordens_de_producao_existentes()
        continue
    elif opcao == 5:
        print(relatorio_de_producao())
        continue
    elif opcao == 3:
        id_da_ordem = input("INFORME AQUI O ID DA ORDEM DE PRODUCAO: ")
        novo_status = input("INFORME AQUI O NOVO STATUS DA ORDEM: ")
        print(atualizar_status_de_uma_ordem_de_producao(id_da_ordem, novo_status))
        continue
    elif opcao == 4:
        id_da_ordem = input("INFORME AQUI O ID DA ORDEM DE PRODUCAO: ")
        print(verificar_possibilidade_de_producao_de_uma_ordem(id_da_ordem))
        continue
    elif opcao == 1:
        opc_add_materiais = 2
        materiais_necessarios = []
        nome_do_produto = input("INFORME AQUI O NOME DO PRODUTO: ")
        quantidade = input("INFORME AQUI A QUANTIDADE DO PRODUTO: ")
        status = input("INFORME AQUI O STATUS DA ORDEM DE PRODUCAO: ")
        data_de_entrega = input("INFORME AQUI A DATA DE ENTREGA DO PRODUTO: ")

        while opc_add_materiais != 0:
            print("\n|=====MATERIAL NECESSARIO=====|\n")
            print("|0 - SAIR 1 - ADICIONAR NOVO MATERIAL|\n")
            opc_add_materiais = int(input("INSIRA AQUI SUA RESPOSTA: "))
            if opc_add_materiais == 0:
                if len(materiais_necessarios) == 0:
                    print(
                        "\n|VOCE PRECISA ADICIONAR PELO MENOS UM MATERIAL PARA A ORDEM DE PRODUCAO|\n"
                    )
                    opc_add_materiais = 2
                    continue
                opc_add_materiais = 0
                continue
            elif opc_add_materiais == 1:
                novo_material = input(
                    "\nDIGITE AQUI A QUANTIDADE E O MATERIAL PARA A FABRICACAO: "
                )
                materiais_necessarios.append(novo_material)
                continue
            else:
                print("\n|===== OPCAO INVALIDA =====|\n")
                continue

        novo_produto = {
            "id": str(uuid.uuid4()),
            "nome_do_produto": nome_do_produto,
            "quantidade": quantidade,
            "status": status,
            "data_de_entrega": data_de_entrega,
            "materiais_necessarios": materiais_necessarios,
        }

        print(nova_ordem_de_producao(novo_produto))
        continue
