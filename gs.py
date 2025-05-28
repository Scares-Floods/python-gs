# Sistema de Monitoramento e Prevenção de Enchentes - Global Solution 2025.1
# Disciplina: Computational Thinking Using Python
# Grupo: [INCLUA AQUI OS NOMES E RMs DOS INTEGRANTES]
# Data: Maio 2025

import datetime


# =================== CLASSES E ESTRUTURAS DE DADOS ===================

class RegistroEnchente:
    """Classe para representar um registro de enchente"""

    def __init__(self, regiao, nivel_agua, precipitacao, populacao_afetada, data=None):
        self.regiao = regiao
        self.nivel_agua = nivel_agua  # em metros
        self.precipitacao = precipitacao  # em mm
        self.populacao_afetada = populacao_afetada
        self.data = data if data else datetime.datetime.now()
        self.risco = self.calcular_risco()

    def calcular_risco(self):
        """Calcula o nível de risco baseado nos parâmetros"""
        if self.nivel_agua > 3.0 or self.precipitacao > 100:
            return "CRÍTICO"
        elif self.nivel_agua > 2.0 or self.precipitacao > 60:
            return "ALTO"
        elif self.nivel_agua > 1.0 or self.precipitacao > 30:
            return "MODERADO"
        else:
            return "BAIXO"


# =================== VARIÁVEIS GLOBAIS ===================

# Lista para armazenar todos os registros de enchentes
registros_enchentes = []

# Dicionário com regiões pré-cadastradas do Brasil
regioes_brasil = {
    "1": "São Paulo - SP",
    "2": "Rio de Janeiro - RJ",
    "3": "Recife - PE",
    "4": "Salvador - BA",
    "5": "Belo Horizonte - MG",
    "6": "Curitiba - PR",
    "7": "Porto Alegre - RS",
    "8": "Manaus - AM",
    "9": "Belém - PA",
    "10": "Goiânia - GO"
}

# Dados de emergência para contatos
contatos_emergencia = {
    "Bombeiros": "193",
    "SAMU": "192",
    "Defesa Civil": "199",
    "Polícia": "190"
}


# =================== FUNÇÕES DE VALIDAÇÃO ===================

def validar_numero_float(valor_str, nome_campo, minimo=0, maximo=None):
    """
    Valida se uma string pode ser convertida para float dentro de um intervalo
    Parâmetros:
        valor_str: string a ser validada
        nome_campo: nome do campo para exibição de erro
        minimo: valor mínimo permitido
        maximo: valor máximo permitido (opcional)
    Retorna:
        tuple (bool, float): (é_válido, valor_convertido)
    """
    try:
        valor = float(valor_str)
        if valor < minimo:
            print(f"❌ Erro: {nome_campo} deve ser maior ou igual a {minimo}")
            return False, 0
        if maximo is not None and valor > maximo:
            print(f"❌ Erro: {nome_campo} deve ser menor ou igual a {maximo}")
            return False, 0
        return True, valor
    except ValueError:
        print(f"❌ Erro: {nome_campo} deve ser um número válido")
        return False, 0


def validar_numero_int(valor_str, nome_campo, minimo=0, maximo=None):
    """
    Valida se uma string pode ser convertida para int dentro de um intervalo
    Parâmetros:
        valor_str: string a ser validada
        nome_campo: nome do campo para exibição de erro
        minimo: valor mínimo permitido
        maximo: valor máximo permitido (opcional)
    Retorna:
        tuple (bool, int): (é_válido, valor_convertido)
    """
    try:
        valor = int(valor_str)
        if valor < minimo:
            print(f"❌ Erro: {nome_campo} deve ser maior ou igual a {minimo}")
            return False, 0
        if maximo is not None and valor > maximo:
            print(f"❌ Erro: {nome_campo} deve ser menor ou igual a {maximo}")
            return False, 0
        return True, valor
    except ValueError:
        print(f"❌ Erro: {nome_campo} deve ser um número inteiro válido")
        return False, 0


def validar_opcao_menu(opcao_str, opcoes_validas):
    """
    Valida se a opção escolhida está entre as opções válidas
    Parâmetros:
        opcao_str: string da opção escolhida
        opcoes_validas: lista de opções válidas
    Retorna:
        bool: True se válida, False caso contrário
    """
    return opcao_str.strip() in opcoes_validas


# =================== FUNÇÕES DE ENTRADA DE DADOS ===================

def obter_regiao():
    """
    Solicita ao usuário a seleção de uma região
    Retorna:
        str: nome da região selecionada
    """
    while True:
        print("\n🌎 Selecione a região:")
        print("=" * 40)
        for codigo, regiao in regioes_brasil.items():
            print(f"{codigo}. {regiao}")
        print("11. Outra região (digitar manualmente)")

        escolha = input("\nDigite o número da opção: ").strip()

        # Validação da opção
        if validar_opcao_menu(escolha, list(regioes_brasil.keys()) + ["11"]):
            if escolha == "11":
                regiao_custom = input("Digite o nome da região: ").strip()
                if len(regiao_custom) > 0:
                    return regiao_custom
                else:
                    print("❌ Nome da região não pode estar vazio!")
            else:
                return regioes_brasil[escolha]
        else:
            print("❌ Opção inválida! Tente novamente.")


def obter_dados_enchente():
    """
    Coleta todos os dados necessários para registrar uma enchente
    Retorna:
        RegistroEnchente: objeto com os dados coletados ou None se cancelado
    """
    print("\n📊 CADASTRO DE NOVA OCORRÊNCIA DE ENCHENTE")
    print("=" * 50)

    # Obter região
    regiao = obter_regiao()

    # Obter nível da água
    while True:
        nivel_str = input("\n💧 Digite o nível da água (em metros): ").strip()
        valido, nivel_agua = validar_numero_float(nivel_str, "Nível da água", 0, 10)
        if valido:
            break

    # Obter precipitação
    while True:
        precip_str = input("🌧️  Digite a precipitação (em mm): ").strip()
        valido, precipitacao = validar_numero_float(precip_str, "Precipitação", 0, 500)
        if valido:
            break

    # Obter população afetada
    while True:
        pop_str = input("👥 Digite o número de pessoas afetadas: ").strip()
        valido, populacao = validar_numero_int(pop_str, "População afetada", 0, 10000000)
        if valido:
            break

    # Criar e retornar o registro
    return RegistroEnchente(regiao, nivel_agua, precipitacao, populacao)


# =================== FUNÇÕES DE PROCESSAMENTO ===================

def calcular_estatisticas():
    """
    Calcula estatísticas gerais dos registros de enchentes
    Retorna:
        dict: dicionário com as estatísticas calculadas
    """
    if not registros_enchentes:
        return None

    # Contadores por nível de risco
    criticos = sum(1 for r in registros_enchentes if r.risco == "CRÍTICO")
    altos = sum(1 for r in registros_enchentes if r.risco == "ALTO")
    moderados = sum(1 for r in registros_enchentes if r.risco == "MODERADO")
    baixos = sum(1 for r in registros_enchentes if r.risco == "BAIXO")

    # Médias
    nivel_medio = sum(r.nivel_agua for r in registros_enchentes) / len(registros_enchentes)
    precip_media = sum(r.precipitacao for r in registros_enchentes) / len(registros_enchentes)
    pop_total = sum(r.populacao_afetada for r in registros_enchentes)

    # Máximos
    maior_nivel = max(r.nivel_agua for r in registros_enchentes)
    maior_precip = max(r.precipitacao for r in registros_enchentes)

    return {
        "total_registros": len(registros_enchentes),
        "criticos": criticos,
        "altos": altos,
        "moderados": moderados,
        "baixos": baixos,
        "nivel_medio": nivel_medio,
        "precip_media": precip_media,
        "pop_total": pop_total,
        "maior_nivel": maior_nivel,
        "maior_precip": maior_precip
    }


def filtrar_por_risco(nivel_risco):
    """
    Filtra registros por nível de risco específico
    Parâmetros:
        nivel_risco: string com o nível de risco desejado
    Retorna:
        list: lista de registros filtrados
    """
    return [r for r in registros_enchentes if r.risco == nivel_risco]


def buscar_por_regiao(nome_regiao):
    """
    Busca registros por região (busca parcial, case-insensitive)
    Parâmetros:
        nome_regiao: string com o nome ou parte do nome da região
    Retorna:
        list: lista de registros encontrados
    """
    nome_regiao_lower = nome_regiao.lower()
    return [r for r in registros_enchentes if nome_regiao_lower in r.regiao.lower()]


# =================== FUNÇÕES DE EXIBIÇÃO ===================

def exibir_cabecalho():
    """Exibe o cabeçalho do sistema"""
    print("\n" + "=" * 60)
    print("🌊 SISTEMA DE MONITORAMENTO DE ENCHENTES - BRASIL 🌊")
    print("=" * 60)
    print("Global Solution 2025.1 - Prevenção e Resposta a Enchentes")
    print("=" * 60)


def exibir_menu_principal():
    """Exibe o menu principal do sistema"""
    print("\n📋 MENU PRINCIPAL:")
    print("-" * 30)
    print("1. 📝 Registrar nova enchente")
    print("2. 📊 Visualizar todos os registros")
    print("3. 🔍 Filtrar por nível de risco")
    print("4. 🗺️  Buscar por região")
    print("5. 📈 Ver estatísticas gerais")
    print("6. 🚨 Informações de emergência")
    print("7. ❓ Ajuda e orientações")
    print("0. 🚪 Sair do sistema")


def exibir_registro(registro, indice=None):
    """
    Exibe um registro de enchente formatado
    Parâmetros:
        registro: objeto RegistroEnchente
        indice: número do registro (opcional)
    """
    if indice is not None:
        print(f"\n📋 REGISTRO #{indice + 1}")
    else:
        print(f"\n📋 REGISTRO DE ENCHENTE")

    print("-" * 40)
    print(f"🌎 Região: {registro.regiao}")
    print(f"📅 Data: {registro.data.strftime('%d/%m/%Y %H:%M')}")
    print(f"💧 Nível da água: {registro.nivel_agua:.2f} metros")
    print(f"🌧️  Precipitação: {registro.precipitacao:.1f} mm")
    print(f"👥 População afetada: {registro.populacao_afetada:,} pessoas")

    # Colorir o nível de risco
    cor_risco = {
        "CRÍTICO": "🔴",
        "ALTO": "🟠",
        "MODERADO": "🟡",
        "BAIXO": "🟢"
    }
    print(f"⚠️  Nível de risco: {cor_risco.get(registro.risco, '⚪')} {registro.risco}")


def exibir_todos_registros():
    """Exibe todos os registros cadastrados"""
    if not registros_enchentes:
        print("\n📭 Nenhum registro encontrado!")
        print("💡 Use a opção 1 para cadastrar uma nova ocorrência.")
        return

    print(f"\n📊 TODOS OS REGISTROS ({len(registros_enchentes)} total)")
    print("=" * 50)

    for i, registro in enumerate(registros_enchentes):
        exibir_registro(registro, i)


def exibir_estatisticas():
    """Exibe as estatísticas gerais do sistema"""
    stats = calcular_estatisticas()

    if not stats:
        print("\n📭 Nenhum dado disponível para estatísticas!")
        return

    print("\n📈 ESTATÍSTICAS GERAIS")
    print("=" * 40)
    print(f"📊 Total de registros: {stats['total_registros']}")
    print(f"🔴 Situações críticas: {stats['criticos']}")
    print(f"🟠 Risco alto: {stats['altos']}")
    print(f"🟡 Risco moderado: {stats['moderados']}")
    print(f"🟢 Risco baixo: {stats['baixos']}")
    print("-" * 40)
    print(f"💧 Nível médio da água: {stats['nivel_medio']:.2f} metros")
    print(f"🌧️  Precipitação média: {stats['precip_media']:.1f} mm")
    print(f"👥 População total afetada: {stats['pop_total']:,} pessoas")
    print("-" * 40)
    print(f"📊 Maior nível registrado: {stats['maior_nivel']:.2f} metros")
    print(f"🌧️  Maior precipitação: {stats['maior_precip']:.1f} mm")


def exibir_emergencia():
    """Exibe informações de emergência"""
    print("\n🚨 INFORMAÇÕES DE EMERGÊNCIA")
    print("=" * 40)
    print("📞 CONTATOS IMPORTANTES:")
    for servico, telefone in contatos_emergencia.items():
        print(f"   {servico}: {telefone}")

    print("\n🆘 EM CASO DE ENCHENTE:")
    print("• Desligue a energia elétrica da sua casa")
    print("• Não ande ou dirija em áreas alagadas")
    print("• Procure locais mais altos")
    print("• Mantenha-se informado pelas autoridades")
    print("• Tenha um kit de emergência preparado")

    print("\n🎒 KIT DE EMERGÊNCIA:")
    print("• Água potável (3 litros por pessoa/dia)")
    print("• Alimentos não perecíveis")
    print("• Medicamentos essenciais")
    print("• Lanterna e pilhas")
    print("• Documentos em saco plástico")


def exibir_ajuda():
    """Exibe informações de ajuda do sistema"""
    print("\n❓ AJUDA E ORIENTAÇÕES")
    print("=" * 40)
    print("🎯 SOBRE O SISTEMA:")
    print("Este sistema permite monitorar e registrar ocorrências")
    print("de enchentes em diferentes regiões do Brasil, ajudando")
    print("na prevenção e resposta a emergências.")

    print("\n📝 COMO USAR:")
    print("1. Registre enchentes com dados precisos")
    print("2. Consulte histórico e estatísticas")
    print("3. Filtre informações por risco ou região")
    print("4. Acesse informações de emergência quando necessário")

    print("\n🎯 NÍVEIS DE RISCO:")
    print("🔴 CRÍTICO: Nível > 3m OU Chuva > 100mm")
    print("🟠 ALTO: Nível > 2m OU Chuva > 60mm")
    print("🟡 MODERADO: Nível > 1m OU Chuva > 30mm")
    print("🟢 BAIXO: Demais situações")


# =================== FUNÇÕES DE MENU ===================

def menu_filtrar_risco():
    """Menu para filtrar registros por nível de risco"""
    print("\n🔍 FILTRAR POR NÍVEL DE RISCO")
    print("-" * 30)
    print("1. 🔴 Crítico")
    print("2. 🟠 Alto")
    print("3. 🟡 Moderado")
    print("4. 🟢 Baixo")

    opcao = input("\nEscolha o nível de risco: ").strip()

    niveis = {"1": "CRÍTICO", "2": "ALTO", "3": "MODERADO", "4": "BAIXO"}

    if opcao in niveis:
        nivel_escolhido = niveis[opcao]
        registros_filtrados = filtrar_por_risco(nivel_escolhido)

        if registros_filtrados:
            print(f"\n📊 REGISTROS COM RISCO {nivel_escolhido} ({len(registros_filtrados)} encontrados)")
            print("=" * 50)
            for i, registro in enumerate(registros_filtrados):
                exibir_registro(registro, i)
        else:
            print(f"\n📭 Nenhum registro encontrado com risco {nivel_escolhido}")
    else:
        print("❌ Opção inválida!")


def menu_buscar_regiao():
    """Menu para buscar registros por região"""
    regiao = input("\n🗺️  Digite o nome da região para buscar: ").strip()

    if len(regiao) == 0:
        print("❌ Nome da região não pode estar vazio!")
        return

    registros_encontrados = buscar_por_regiao(regiao)

    if registros_encontrados:
        print(f"\n📊 REGISTROS PARA '{regiao}' ({len(registros_encontrados)} encontrados)")
        print("=" * 50)
        for i, registro in enumerate(registros_encontrados):
            exibir_registro(registro, i)
    else:
        print(f"\n📭 Nenhum registro encontrado para '{regiao}'")


# =================== FUNÇÃO PRINCIPAL ===================

def main():
    """Função principal do sistema"""
    # Adicionar alguns dados de exemplo para demonstração
    registros_enchentes.append(RegistroEnchente("São Paulo - SP", 2.5, 80, 15000))
    registros_enchentes.append(RegistroEnchente("Rio de Janeiro - RJ", 3.2, 120, 25000))
    registros_enchentes.append(RegistroEnchente("Recife - PE", 1.8, 45, 8000))

    exibir_cabecalho()
    print("💡 Sistema iniciado com dados de exemplo para demonstração.")

    # Loop principal do sistema
    while True:
        exibir_menu_principal()
        opcao = input("\n🎯 Digite sua opção: ").strip()

        # Estruturas de decisão para processar a opção escolhida
        if opcao == "1":
            # Cadastrar nova enchente
            novo_registro = obter_dados_enchente()
            if novo_registro:
                registros_enchentes.append(novo_registro)
                print(f"\n✅ Enchente registrada com sucesso!")
                print(f"⚠️  Nível de risco calculado: {novo_registro.risco}")

                # Alerta para situações críticas
                if novo_registro.risco == "CRÍTICO":
                    print("\n🚨 ATENÇÃO: SITUAÇÃO CRÍTICA DETECTADA!")
                    print("📞 Recomenda-se contato imediato com autoridades!")

        elif opcao == "2":
            # Visualizar todos os registros
            exibir_todos_registros()

        elif opcao == "3":
            # Filtrar por risco
            menu_filtrar_risco()

        elif opcao == "4":
            # Buscar por região
            menu_buscar_regiao()

        elif opcao == "5":
            # Estatísticas
            exibir_estatisticas()

        elif opcao == "6":
            # Informações de emergência
            exibir_emergencia()

        elif opcao == "7":
            # Ajuda
            exibir_ajuda()

        elif opcao == "0":
            # Sair do sistema
            print("\n👋 Encerrando o sistema...")
            print("🌊 Obrigado por usar o Sistema de Monitoramento de Enchentes!")
            break

        else:
            print("❌ Opção inválida! Tente novamente.")

        # Pausa para o usuário ler as informações
        input("\n⏸️  Pressione ENTER para continuar...")


# =================== EXECUÇÃO DO PROGRAMA ===================

if __name__ == "__main__":
    main()