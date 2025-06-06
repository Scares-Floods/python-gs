# Sistema de Monitoramento e Prevenção de Enchentes - Global Solution 2025.1
# Disciplina: Computational Thinking Using Python
# Grupo: [Bruno Scuciato:562159 | João Paulo: 565383 | kelwin Silva: 566348]
# Data: Maio 2025

import datetime
from twilio.rest import Client

# =================== CONFIGURAÇÕES WHATSAPP ===================

# Configurações do Twilio para WhatsApp Sandbox (substitua pelos seus dados reais)
# VOCÊ PEGA ISSO NO SEU CONSOLE TWILIO, NA SEÇÃO DO WHATSAPP SANDBOX
TWILIO_ACCOUNT_SID = 'your_account_sid_here' # MESMO SID DA SUA CONTA TWILIO
TWILIO_AUTH_TOKEN = 'your_auth_token_here' # MESMO TOKEN DA SUA CONTA TWILIO
TWILIO_WHATSAPP_SANDBOX_NUMBER = 'whatsapp:+14155238886' # ESTE É O NÚMERO DO SANDBOX TWILIO (GERALMENTE FIXO)
WHATSAPP_SANDBOX_JOIN_CODE = 'join word-word-word' # CÓDIGO QUE USUÁRIOS PRECISAM ENVIAR PARA O SANDBOX

# Lista de contatos para emergência (devem ter enviado a mensagem JOIN para o Sandbox primeiro)
EMERGENCY_CONTACTS_WHATSAPP = [
    'whatsapp:+5511999999999',  # Seu WhatsApp (precisa ter enviado o código JOIN)
    'whatsapp:+5511888888888',  # WhatsApp da Defesa Civil (precisa ter enviado o código JOIN)
    # Adicione mais números conforme necessário, no formato 'whatsapp:+55DDDNUMERO'
]

def enviar_whatsapp(mensagem, numero_destino=None):
    """
    Envia mensagem via WhatsApp usando Twilio Sandbox
    Parâmetros:
        mensagem: texto da mensagem
        numero_destino: número de destino no formato 'whatsapp:+55DDDNUMERO' (opcional, usa o primeiro contato de emergência se não especificado)
    Retorna:
        bool: True se enviado com sucesso, False caso contrário
    """
    try:
        # Inicializar cliente Twilio
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Usar número padrão se não especificado
        if numero_destino is None:
            # Pegar o primeiro número da lista de contatos de emergência para o teste
            if EMERGENCY_CONTACTS_WHATSAPP:
                numero_destino = EMERGENCY_CONTACTS_WHATSAPP[0]
            else:
                print("❌ Nenhum contato de WhatsApp de emergência configurado.")
                return False
        
        # Enviar mensagem via WhatsApp
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_SANDBOX_NUMBER,
            body=mensagem,
            to=numero_destino
        )
        
        print(f"✅ Mensagem WhatsApp enviada com sucesso! ID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem WhatsApp: {str(e)}")
        print("Certifique-se de que o contato de destino enviou a mensagem de adesão ao Sandbox.")
        return False

def enviar_alerta_critico_whatsapp(registro):
    """
    Envia alerta WhatsApp para situações críticas
    Parâmetros:
        registro: objeto RegistroEnchente com situação crítica
    """
    mensagem = f"""
🚨 ALERTA CRÍTICO - ENCHENTE 🚨

📍 Região: {registro.regiao}
📅 Data: {registro.data.strftime('%d/%m/%Y %H:%M')}
💧 Nível: {registro.nivel_agua:.1f}m
🌧️ Chuva: {registro.precipitacao:.0f}mm
👥 Afetados: {registro.populacao_afetada:,}
⚠️ Risco: {registro.risco}

Ação imediata necessária!
Sistema de Monitoramento
""".strip()
    
    # Enviar para todos os contatos de emergência do WhatsApp
    for contato in EMERGENCY_CONTACTS_WHATSAPP:
        enviar_whatsapp(mensagem, contato)

def configurar_twilio_whatsapp():
    """
    Permite ao usuário configurar as credenciais do Twilio para WhatsApp
    """
    print("\n📱 CONFIGURAÇÃO DO TWILIO WHATSAPP SANDBOX")
    print("=" * 40)
    print("Para testar o envio de mensagens WhatsApp:")
    print("1. Vá para o console Twilio -> Develop -> Messaging -> Try it out -> WhatsApp Sandbox.")
    print("2. Pegue o 'WhatsApp Sandbox Number' e o 'Your Sandbox Channel' (o código 'join...').")
    print("3. Peça para os contatos de emergência enviarem este código para o número do Sandbox.")
    
    global TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_SANDBOX_NUMBER, WHATSAPP_SANDBOX_JOIN_CODE
    
    while True:
        print("\n1. Configurar credenciais Twilio (WhatsApp Sandbox)")
        print("2. Testar envio de mensagem WhatsApp")
        print("3. Voltar ao menu principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            TWILIO_ACCOUNT_SID = input("Account SID: ").strip()
            TWILIO_AUTH_TOKEN = input("Auth Token: ").strip()
            TWILIO_WHATSAPP_SANDBOX_NUMBER = input("Número WhatsApp Sandbox (ex: whatsapp:+14155238886): ").strip()
            WHATSAPP_SANDBOX_JOIN_CODE = input("Código de adesão do Sandbox (ex: join word-word-word): ").strip()
            # O ADMIN_PHONE_NUMBER agora seria parte de EMERGENCY_CONTACTS_WHATSAPP
            
            # Atualiza o primeiro contato de emergência com o número do admin para testar
            admin_whatsapp = input("Seu WhatsApp (ex: +5511999999999, para teste inicial): ").strip()
            if admin_whatsapp:
                 # Adiciona o número do admin se não estiver na lista ou atualiza o primeiro.
                if f"whatsapp:{admin_whatsapp}" not in EMERGENCY_CONTACTS_WHATSAPP:
                    EMERGENCY_CONTACTS_WHATSAPP.insert(0, f"whatsapp:{admin_whatsapp}")
                else: # Garante que o primeiro da lista é o do admin se já existir
                    EMERGENCY_CONTACTS_WHATSAPP.remove(f"whatsapp:{admin_whatsapp}")
                    EMERGENCY_CONTACTS_WHATSAPP.insert(0, f"whatsapp:{admin_whatsapp}")

            print("✅ Configurações salvas! Lembre-se de enviar o código de adesão para o Sandbox.")
            
        elif opcao == "2":
            if enviar_whatsapp("🧪 Teste do Sistema de Monitoramento de Enchentes - WhatsApp funcionando!"):
                print("✅ Mensagem WhatsApp de teste enviada com sucesso!")
                print("Lembre-se: o destinatário precisa ter enviado o código de adesão ao Sandbox.")
            else:
                print("❌ Falha no envio da mensagem WhatsApp de teste")
                
        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida!")

# =================== CLASSES E ESTRUTURAS DE DADOS (Mantidas) ===================
# ... (Resto do seu código, classes RegistroEnchente, validar_numero_float, etc.) ...
# Certifique-se de que 'registros_enchentes' e 'regioes_brasil' estão definidos.

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


# =================== VARIÁVEIS GLOBAIS (Mantidas, mas adaptando contatos de emergência) ===================

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

# Dados de emergência para contatos (mantidos, mas não usados diretamente para o envio de mensagens)
contatos_emergencia = {
    "Bombeiros": "193",
    "SAMU": "192",
    "Defesa Civil": "199",
    "Polícia": "190"
}

# =================== FUNÇÕES DE VALIDAÇÃO (Mantidas) ===================
# ... (validar_numero_float, validar_numero_int, validar_opcao_menu) ...
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

# =================== FUNÇÕES DE ENTRADA DE DADOS (Mantidas) ===================
# ... (obter_regiao, obter_dados_enchente) ...
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
        validado, nivel_agua = validar_numero_float(nivel_str, "Nível da água", 0, 10)
        if validado:
            break

    # Obter precipitação
    while True:
        precip_str = input("🌧️  Digite a precipitação (em mm): ").strip()
        validado, precipitacao = validar_numero_float(precip_str, "Precipitação", 0, 500)
        if validado:
            break

    # Obter população afetada
    while True:
        pop_str = input("👥 Digite o número de pessoas afetadas: ").strip()
        validado, populacao = validar_numero_int(pop_str, "População afetada", 0, 10000000)
        if validado:
            break

    # Criar e retornar o registro
    return RegistroEnchente(regiao, nivel_agua, precipitacao, populacao)


# =================== FUNÇÕES DE PROCESSAMENTO (Mantidas) ===================
# ... (calcular_estatisticas, filtrar_por_risco, buscar_por_regiao) ...
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


# =================== FUNÇÕES DE EXIBIÇÃO (Mantidas) ===================
# ... (exibir_cabecalho, exibir_menu_principal, exibir_registro, etc.) ...
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
    print("8. 📱 Configurar WhatsApp/Alertas")  # Opção atualizada
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
    print("5. Configure WhatsApp para receber alertas automáticos (via Sandbox)")

    print("\n🎯 NÍVEIS DE RISCO:")
    print("🔴 CRÍTICO: Nível > 3m OU Chuva > 100mm")
    print("🟠 ALTO: Nível > 2m OU Chuva > 60mm")
    print("🟡 MODERADO: Nível > 1m OU Chuva > 30mm")
    print("🟢 BAIXO: Demais situações")

    print("\n📱 ALERTAS WHATSAPP (SANDBOX):")
    print("• Configure sua conta Twilio e ative o WhatsApp Sandbox na opção 8")
    print("• Alerta automático enviado para situações críticas (apenas para contatos que aderiram ao Sandbox)")
    print("• Útil para testes e demonstrações, não para uso em produção real.")


# =================== FUNÇÕES DE MENU (Mantidas) ===================
# ... (menu_filtrar_risco, menu_buscar_regiao) ...
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
    print("📱 Configure o WhatsApp Sandbox na opção 8 para testar alertas!")

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

                # Alerta para situações críticas via WhatsApp
                if novo_registro.risco == "CRÍTICO":
                    print("\n🚨 ATENÇÃO: SITUAÇÃO CRÍTICA DETECTADA!")
                    print("📞 Recomenda-se contato imediato com autoridades!")
                    
                    # Enviar WhatsApp automático para situações críticas
                    print("\n📱 Enviando alerta WhatsApp (via Sandbox)...")
                    enviar_alerta_critico_whatsapp(novo_registro)

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

        elif opcao == "8":
            # Configurar WhatsApp - Nova opção
            configurar_twilio_whatsapp()

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