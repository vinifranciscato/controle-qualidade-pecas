# ==========================================================
#  Controle de qualidade e armazenamento de peças
#  Algoritmos e Lógica de Programação - UniFECAF
#  Aluno: Vinícius Franciscato - RA 254086
# ==========================================================

import json

# --- Critérios de qualidade definidos pela empresa ---
PESO_MINIMO = 95
PESO_MAXIMO = 105
COMPRIMENTO_MINIMO = 10
COMPRIMENTO_MAXIMO = 20
CORES_ACEITAS = ["azul", "verde"]
CAPACIDADE_CAIXA = 10

# --- Faixas de alerta ---
# Valores muito longe do padrão costumam ser erro de digitação (ex.: 9.8 em vez de 98).
# São uma premissa do projeto e podem ser ajustadas.
PESO_ALERTA_MINIMO = 50
PESO_ALERTA_MAXIMO = 200
COMPRIMENTO_ALERTA_MINIMO = 5
COMPRIMENTO_ALERTA_MAXIMO = 40

ARQUIVO_DADOS = "dados_pecas.json"


# ---------------- Validações ----------------

def esta_fora_da_faixa(valor, minimo, maximo):
    """Devolve True se o valor estiver fora do intervalo informado."""
    return (valor < minimo) or (valor > maximo)


def tem_so_caracteres_de_numero(texto):
    """Devolve True se o texto tiver apenas dígitos, ponto e sinal de menos."""
    for caractere in texto:
        if not caractere.isdigit() and (caractere != ".") and (caractere != "-"):
            return False

    return True


def converter_numero(texto):
    """Converte o texto digitado em número. Devolve None se não for um número."""
    texto_ajustado = texto.strip().replace(",", ".")

    # Sem esta checagem o Python aceitaria textos como "nan" e "inf" como números
    if (texto_ajustado == "") or not tem_so_caracteres_de_numero(texto_ajustado):
        return None

    try:
        return float(texto_ajustado)
    except ValueError:
        return None


def verificar_medida(numero):
    """Devolve o problema encontrado no peso ou no comprimento, ou texto vazio se estiver certo."""
    if numero is None:
        return "não é um número"

    if numero <= 0:
        return "precisa ser maior que zero"

    return ""


def contem_numero(texto):
    """Devolve True se o texto tiver algum dígito."""
    for caractere in texto:
        if caractere.isdigit():
            return True

    return False


def verificar_cor(cor):
    """Devolve o problema encontrado na cor, ou texto vazio se estiver certa."""
    if cor == "":
        return "a cor não pode ficar em branco"

    if contem_numero(cor):
        return "a cor não pode ter números"

    return ""


def localizar_peca(pecas, id_peca):
    """Procura uma peça pelo ID. Devolve a peça ou None."""
    for peca in pecas:
        if peca["id"] == id_peca:
            return peca

    return None


def verificar_id(id_peca, pecas):
    """Devolve o problema encontrado no ID, ou texto vazio se estiver certo."""
    if id_peca == "":
        return "o ID não pode ficar em branco"

    if localizar_peca(pecas, id_peca) is not None:
        return f"já existe uma peça com o ID {id_peca}"

    return ""


# ---------------- Leitura do teclado ----------------

def confirmar(mensagem):
    """Pergunta S/N e devolve True para sim."""
    while True:
        resposta = input(f"{mensagem} (S/N): ").strip().upper()

        if resposta == "S":
            return True

        if resposta == "N":
            return False

        print("  Responda apenas S ou N.")


def ler_id(pecas):
    """Lê o ID da peça, insistindo até ser válido e não repetido."""
    while True:
        id_peca = input("ID da peça: ").strip().upper()
        erro = verificar_id(id_peca, pecas)

        if erro == "":
            return id_peca

        print(f"  ID inválido: {erro}.")


def ler_numero_positivo(mensagem):
    """Lê um número maior que zero, insistindo até o valor ser válido."""
    while True:
        numero = converter_numero(input(mensagem))
        erro = verificar_medida(numero)

        if erro == "":
            return numero

        print(f"  Valor inválido: {erro}. Exemplo de valor válido: 98.5")


def ler_peso():
    """Lê o peso da peça e confirma valores muito fora do padrão."""
    while True:
        peso = ler_numero_positivo("Peso (g): ")

        if not esta_fora_da_faixa(peso, PESO_ALERTA_MINIMO, PESO_ALERTA_MAXIMO):
            return peso

        # Não bloqueia: a peça pode estar realmente com defeito
        print(f"  Atenção: {peso} g está muito fora do padrão ({PESO_MINIMO} a {PESO_MAXIMO} g).")
        print("  Pode ser erro de digitação.")

        if confirmar("  Confirma esse valor?"):
            return peso


def ler_comprimento():
    """Lê o comprimento da peça e confirma valores muito fora do padrão."""
    while True:
        comprimento = ler_numero_positivo("Comprimento (cm): ")

        if not esta_fora_da_faixa(comprimento, COMPRIMENTO_ALERTA_MINIMO, COMPRIMENTO_ALERTA_MAXIMO):
            return comprimento

        print(f"  Atenção: {comprimento} cm está muito fora do padrão ({COMPRIMENTO_MINIMO} a {COMPRIMENTO_MAXIMO} cm).")
        print("  Pode ser erro de digitação.")

        if confirmar("  Confirma esse valor?"):
            return comprimento


def ler_cor():
    """Lê a cor da peça já normalizada em minúsculas."""
    while True:
        cor = input("Cor: ").strip().lower()
        erro = verificar_cor(cor)

        if erro == "":
            return cor

        print(f"  Cor inválida: {erro}.")


# ---------------- Regras de qualidade e caixas ----------------

def avaliar_peca(peso, cor, comprimento):
    """Devolve a lista de motivos de reprovação. Lista vazia significa peça aprovada."""
    motivos = []

    if esta_fora_da_faixa(peso, PESO_MINIMO, PESO_MAXIMO):
        motivos.append("peso fora do padrão")

    if cor not in CORES_ACEITAS:
        motivos.append("cor não aceita")

    if esta_fora_da_faixa(comprimento, COMPRIMENTO_MINIMO, COMPRIMENTO_MAXIMO):
        motivos.append("comprimento fora do padrão")

    return motivos


def montar_peca(id_peca, peso, cor, comprimento):
    """Monta a peça já avaliada, sem gravar nada."""
    motivos = avaliar_peca(peso, cor, comprimento)

    return {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "aprovada": len(motivos) == 0,
        "motivos": motivos,
        "numero_caixa": None,
    }


def obter_caixa_aberta(caixas):
    """Devolve a caixa que ainda está recebendo peças, ou None se não houver."""
    for caixa in caixas:
        if not caixa["fechada"]:
            return caixa

    return None


def guardar_na_caixa(caixas, id_peca):
    """Coloca a peça na caixa aberta, criando ou fechando caixas conforme a capacidade."""
    caixa = obter_caixa_aberta(caixas)

    if caixa is None:
        caixa = {"numero": len(caixas) + 1, "ids_pecas": [], "fechada": False}
        caixas.append(caixa)

    caixa["ids_pecas"].append(id_peca)

    if len(caixa["ids_pecas"]) == CAPACIDADE_CAIXA:
        caixa["fechada"] = True

    return caixa


def registrar_peca(pecas, caixas, peca):
    """Guarda a peça na lista e, se aprovada, também na caixa aberta."""
    if peca["aprovada"]:
        caixa = guardar_na_caixa(caixas, peca["id"])
        peca["numero_caixa"] = caixa["numero"]

    pecas.append(peca)
    return peca


def separar_por_resultado(pecas):
    """Devolve duas listas: as peças aprovadas e as reprovadas."""
    aprovadas = []
    reprovadas = []

    for peca in pecas:
        if peca["aprovada"]:
            aprovadas.append(peca)
        else:
            reprovadas.append(peca)

    return aprovadas, reprovadas


def contar_motivos(reprovadas):
    """Conta quantas vezes cada motivo de reprovação apareceu."""
    contagem = {}

    for peca in reprovadas:
        for motivo in peca["motivos"]:
            if motivo in contagem:
                contagem[motivo] += 1
            else:
                contagem[motivo] = 1

    return contagem


def contar_caixas(caixas):
    """Devolve quantas caixas estão fechadas e quantas estão em aberto."""
    fechadas = 0
    abertas = 0

    for caixa in caixas:
        if caixa["fechada"]:
            fechadas += 1
        else:
            abertas += 1

    return fechadas, abertas


# ---------------- Exibição ----------------

def mostrar_menu():
    """Exibe as opções do sistema."""
    print("\n=== CONTROLE DE QUALIDADE ===")
    print("1 - Cadastrar nova peça")
    print("2 - Listar peças aprovadas/reprovadas")
    print("3 - Remover peça cadastrada")
    print("4 - Listar caixas fechadas")
    print("5 - Gerar relatório final")
    print("6 - Importar peças de planilha CSV")
    print("7 - Salvar dados agora")
    print("0 - Salvar e sair")


def mostrar_dados_peca(peca):
    """Exibe os dados da peça em uma linha."""
    print(f"Peça {peca['id']} | Peso: {peca['peso']} g | Cor: {peca['cor']} | Comprimento: {peca['comprimento']} cm")


def mostrar_motivos(peca):
    """Exibe os motivos de reprovação da peça."""
    for motivo in peca["motivos"]:
        print(f"    - {motivo}")


def mostrar_linha_peca(peca):
    """Exibe a peça em formato de listagem, com a caixa ou os motivos."""
    if peca["aprovada"]:
        print(f"{peca['id']} | {peca['peso']} g | {peca['cor']} | {peca['comprimento']} cm | caixa {peca['numero_caixa']}")
    else:
        print(f"{peca['id']} | {peca['peso']} g | {peca['cor']} | {peca['comprimento']} cm")
        mostrar_motivos(peca)


def mostrar_resultado_cadastro(peca, caixas):
    """Informa se a peça foi aprovada e em qual caixa ela ficou."""
    if not peca["aprovada"]:
        print("Peça REPROVADA. Motivos:")
        mostrar_motivos(peca)
        return

    caixa = caixas[peca["numero_caixa"] - 1]
    print(f"Peça APROVADA. Guardada na caixa {caixa['numero']} ({len(caixa['ids_pecas'])} de {CAPACIDADE_CAIXA}).")

    if caixa["fechada"]:
        print(f"Caixa {caixa['numero']} completa e FECHADA. A próxima peça aprovada abre uma nova caixa.")


# ---------------- Arquivo de dados ----------------

def carregar_dados():
    """Lê as peças e as caixas salvas. Devolve listas vazias na primeira execução."""
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print("Nenhum dado salvo encontrado - começando do zero.")
        return [], []
    except json.JSONDecodeError:
        print("Arquivo de dados corrompido - começando do zero.")
        print(f"  Atenção: o conteúdo atual de {ARQUIVO_DADOS} será substituído quando você salvar.")
        return [], []

    pecas = dados.get("pecas", [])
    caixas = dados.get("caixas", [])
    print(f"Dados carregados de {ARQUIVO_DADOS}: {len(pecas)} peça(s) e {len(caixas)} caixa(s).")
    return pecas, caixas


def salvar_dados(pecas, caixas):
    """Grava as peças e as caixas no arquivo JSON."""
    dados = {"pecas": pecas, "caixas": caixas}

    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except Exception as erro:
        print(f"  Não foi possível salvar ({type(erro).__name__}): {erro}")
        return

    print(f"{len(pecas)} peça(s) e {len(caixas)} caixa(s) salvas em {ARQUIVO_DADOS}.")


# ---------------- Opções do menu ----------------

def cadastrar_peca(pecas, caixas):
    """Lê os dados da peça, avalia e guarda depois da confirmação."""
    print("\n--- CADASTRO DE PEÇA ---")
    id_peca = ler_id(pecas)
    peso = ler_peso()
    cor = ler_cor()
    comprimento = ler_comprimento()

    peca = montar_peca(id_peca, peso, cor, comprimento)
    print()
    mostrar_dados_peca(peca)

    if not confirmar("Confirmar cadastro?"):
        print("Cadastro cancelado. Nada foi gravado.")
        return

    registrar_peca(pecas, caixas, peca)
    mostrar_resultado_cadastro(peca, caixas)


def listar_pecas(pecas):
    """Exibe as peças separadas em aprovadas e reprovadas."""
    aprovadas, reprovadas = separar_por_resultado(pecas)

    print(f"\n--- PEÇAS APROVADAS ({len(aprovadas)}) ---")
    if len(aprovadas) == 0:
        print("Nenhuma peça aprovada.")

    for peca in aprovadas:
        mostrar_linha_peca(peca)

    print(f"\n--- PEÇAS REPROVADAS ({len(reprovadas)}) ---")
    if len(reprovadas) == 0:
        print("Nenhuma peça reprovada.")

    for peca in reprovadas:
        mostrar_linha_peca(peca)


def remover_peca(pecas, caixas):
    """Remove uma peça, desde que ela não esteja em uma caixa fechada."""
    print("\n--- REMOÇÃO DE PEÇA ---")

    if len(pecas) == 0:
        print("Nenhuma peça cadastrada.")
        return

    id_peca = input("ID da peça a remover: ").strip().upper()
    peca = localizar_peca(pecas, id_peca)

    if peca is None:
        print(f"  Não existe peça com o ID {id_peca}.")
        return

    caixa = None

    if peca["aprovada"]:
        caixa = caixas[peca["numero_caixa"] - 1]

        # Caixa fechada já foi lacrada e liberada: o registro precisa continuar igual à caixa física
        if caixa["fechada"]:
            print(f"  A peça {id_peca} está na caixa {caixa['numero']}, que já está fechada.")
            print("  Peças de caixas fechadas não podem ser removidas pelo sistema.")
            return

    mostrar_dados_peca(peca)

    if not confirmar("Confirmar remoção?"):
        print("Remoção cancelada.")
        return

    if caixa is not None:
        caixa["ids_pecas"].remove(id_peca)

        # Uma caixa aberta que ficou vazia deixa de ser contada como utilizada
        if len(caixa["ids_pecas"]) == 0:
            caixas.remove(caixa)

    pecas.remove(peca)
    print(f"Peça {id_peca} removida.")


def listar_caixas_fechadas(caixas):
    """Exibe as caixas já fechadas e as peças de cada uma."""
    print("\n--- CAIXAS FECHADAS ---")
    quantidade = 0

    for caixa in caixas:
        if caixa["fechada"]:
            quantidade += 1
            print(f"Caixa {caixa['numero']} ({len(caixa['ids_pecas'])} peças): ", end="")

            for id_peca in caixa["ids_pecas"]:
                print(id_peca, end=" ")

            print()

    if quantidade == 0:
        print(f"Nenhuma caixa fechada ainda. Uma caixa fecha ao receber {CAPACIDADE_CAIXA} peças aprovadas.")


def gerar_relatorio(pecas, caixas):
    """Exibe o relatório consolidado da produção."""
    aprovadas, reprovadas = separar_por_resultado(pecas)
    contagem_motivos = contar_motivos(reprovadas)
    fechadas, abertas = contar_caixas(caixas)

    print("\n=== RELATÓRIO FINAL ===")
    print(f"Peças cadastradas: {len(pecas)}")
    print(f"Peças aprovadas: {len(aprovadas)}")
    print(f"Peças reprovadas: {len(reprovadas)}")

    if len(reprovadas) > 0:
        print("\nReprovações por motivo:")

        for motivo, quantidade in contagem_motivos.items():
            print(f"  - {motivo}: {quantidade}")

        print("  (uma peça pode ter mais de um motivo)")
        print("\nPeças reprovadas:")

        for peca in reprovadas:
            print(f"  {peca['id']}")
            mostrar_motivos(peca)

    print(f"\nCaixas utilizadas: {fechadas + abertas} - Caixas Fechadas: {fechadas} - Caixas em aberto: {abertas}")


# ---------------- Importação de planilha ----------------

def ler_celula(linha, coluna):
    """Devolve o conteúdo da célula como texto, tratando célula vazia."""
    texto = str(linha[coluna]).strip()

    # O pandas marca célula vazia como "nan"
    if texto.lower() == "nan":
        return ""

    return texto


def verificar_linha(id_peca, texto_peso, cor, texto_comprimento, pecas):
    """Devolve o problema encontrado na linha da planilha, ou texto vazio se estiver certa."""
    erro = verificar_id(id_peca, pecas)
    if erro != "":
        return erro

    erro = verificar_medida(converter_numero(texto_peso))
    if erro != "":
        return f"peso {erro}"

    erro = verificar_cor(cor)
    if erro != "":
        return erro

    erro = verificar_medida(converter_numero(texto_comprimento))
    if erro != "":
        return f"comprimento {erro}"

    return ""


def abrir_planilha():
    """Pede o nome do arquivo CSV e devolve a planilha lida, ou None se não for possível."""
    # O pandas é carregado só aqui: sem ele instalado, as outras opções continuam funcionando
    try:
        import pandas
    except ModuleNotFoundError:
        print("  A importação precisa da biblioteca pandas, que não está instalada.")
        print("  Instale com: pip install pandas")
        return None

    nome_arquivo = input("Nome do arquivo CSV (ex.: pecas_exemplo.csv): ").strip()

    try:
        # Tudo é lido como texto para passar pelas mesmas validações do cadastro pelo teclado
        planilha = pandas.read_csv(nome_arquivo, dtype=str)
    except FileNotFoundError:
        print(f'  Arquivo "{nome_arquivo}" não encontrado.')
        print("  Verifique o nome ou abra o VS Code na pasta do projeto.")
        return None
    except Exception as erro:
        print(f"  Não foi possível ler o arquivo ({type(erro).__name__}): {erro}")
        return None

    for coluna in ["id", "peso", "cor", "comprimento"]:
        if coluna not in planilha.columns:
            print(f'  A planilha precisa ter as colunas id, peso, cor e comprimento. Falta a coluna "{coluna}".')
            return None

    return planilha


def mostrar_resumo_importacao(linhas_lidas, importadas, aprovadas, recusadas, alertas):
    """Exibe o resultado da importação da planilha."""
    print(f"\nLinhas lidas: {linhas_lidas}")
    print(f"Peças importadas: {importadas} (aprovadas: {aprovadas} - reprovadas: {importadas - aprovadas})")
    print(f"Linhas recusadas: {len(recusadas)}")

    for mensagem in recusadas:
        print(f"  - {mensagem}")

    if len(alertas) > 0:
        print("Alertas (peças importadas, mas com valor suspeito):")

        for mensagem in alertas:
            print(f"  - {mensagem}")


def importar_pecas_csv(pecas, caixas):
    """Importa as peças de uma planilha CSV, aplicando as mesmas validações do cadastro."""
    print("\n--- IMPORTAÇÃO DE PLANILHA CSV ---")
    planilha = abrir_planilha()

    if planilha is None:
        return

    importadas = 0
    aprovadas = 0
    recusadas = []
    alertas = []

    for indice, linha in planilha.iterrows():
        # +2 porque a linha 1 do arquivo é o cabeçalho e o índice começa em zero
        numero_linha = indice + 2
        id_peca = ler_celula(linha, "id").upper()
        texto_peso = ler_celula(linha, "peso")
        cor = ler_celula(linha, "cor").lower()
        texto_comprimento = ler_celula(linha, "comprimento")

        erro = verificar_linha(id_peca, texto_peso, cor, texto_comprimento, pecas)

        if erro != "":
            recusadas.append(f"linha {numero_linha}: {erro}")
            continue

        peso = converter_numero(texto_peso)
        comprimento = converter_numero(texto_comprimento)

        if esta_fora_da_faixa(peso, PESO_ALERTA_MINIMO, PESO_ALERTA_MAXIMO):
            alertas.append(f"linha {numero_linha} ({id_peca}): peso {peso} g muito fora do padrão, confira se não é erro de digitação")

        if esta_fora_da_faixa(comprimento, COMPRIMENTO_ALERTA_MINIMO, COMPRIMENTO_ALERTA_MAXIMO):
            alertas.append(f"linha {numero_linha} ({id_peca}): comprimento {comprimento} cm muito fora do padrão, confira se não é erro de digitação")

        peca = montar_peca(id_peca, peso, cor, comprimento)
        registrar_peca(pecas, caixas, peca)
        importadas += 1

        if peca["aprovada"]:
            aprovadas += 1

    mostrar_resumo_importacao(len(planilha), importadas, aprovadas, recusadas, alertas)


# --- PROGRAMA PRINCIPAL ---
print("=== SISTEMA DE CONTROLE DE QUALIDADE DE PEÇAS ===")
pecas, caixas = carregar_dados()

while True:
    mostrar_menu()
    opcao = input("Opção: ").strip()

    if opcao == "1":
        cadastrar_peca(pecas, caixas)

    elif opcao == "2":
        listar_pecas(pecas)

    elif opcao == "3":
        remover_peca(pecas, caixas)

    elif opcao == "4":
        listar_caixas_fechadas(caixas)

    elif opcao == "5":
        gerar_relatorio(pecas, caixas)

    elif opcao == "6":
        importar_pecas_csv(pecas, caixas)

    elif opcao == "7":
        salvar_dados(pecas, caixas)

    elif opcao == "0":
        salvar_dados(pecas, caixas)
        print("Sistema encerrado.")
        break

    else:
        print("  Opção inválida!")
