import os
from datetime import datetime
import re
import pwinput  # type: ignore

funcionarios = []
lixeira = []

# pattern de cores que implementei para facilitar na hora de colocar as cores no codigo
CYAN = '\033[96m'
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função que valida o cpf
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"

# analisa de qual região é o cpf base no primeiro dígito do CPF
REGIOES_CPF = {
    '1': 'Sudeste', '2': 'Sudeste', '3': 'Sudeste',
    '4': 'Sul', '5': 'Sul',
    '6': 'Centro-Oeste', '7': 'Centro-Oeste',
    '8': 'Nordeste', '9': 'Nordeste',
    '0': 'Norte'
}

# Função para verificar se o CPF é válido e corresponde à região/estado
def verificar_cpf(cpf, estado):
    if not validar_cpf(cpf):
        return False

    primeiro_digito = cpf[0]
    regiao_cpf = REGIOES_CPF.get(primeiro_digito, 'Desconhecida')

    print(f"Região correspondente ao CPF: {regiao_cpf}")
    return True

# Função para solicitar e verificar a senha
def senhas():
    senha_correta = '123456'
    while True:
        senha = pwinput.pwinput(f'{CYAN}Digite a senha: {RESET}')
        if senha == senha_correta:
            print(f'{GREEN}Senha correta!{RESET}')
            break
        else:
            print(f'{RED}Senha incorreta. Tente novamente.{RESET}')

# Função para mostrar o menu
def menu():
    print(f'{CYAN}==== MENU ===={RESET}')
    print(f'{YELLOW}1. Cadastrar Funcionário')
    print(f'2. Listar Funcionários')
    print(f'3. Editar Funcionários')
    print(f'4. Remover Funcionário')
    print(f'5. Exibir Lixeira')
    print(f'6. Restaurar Funcionário da Lixeira')
    print(f'7. Limpar Lixeira')
    print(f'8. Sair{RESET}')
    print('='*20)
   

# Função para cadastrar funcionários
def cadastro():
    nome = input(f'{CYAN}Nome: {RESET}')
    endereco = input(f'{CYAN}Endereço: {RESET}')
    
    # Verificação se o número é válido (apenas números)
    numero = input(f'{CYAN}Número: {RESET}')
    if not numero.isdigit():
        print(f'{RED}O número deve ser composto apenas por dígitos.{RESET}')
        return
    
    bairro = input(f'{CYAN}Bairro: {RESET}')
    cidade = input(f'{CYAN}Cidade: {RESET}')
    estado = input(f'{CYAN}Estado: {RESET}')
    
    # Loop para garantir que o usuário digite um CEP válido
    while True:
        
        cep = input(f'{CYAN}CEP (8 dígitos): {RESET}')
        if len(cep) == 8 and cep.isdigit():
            break  # Se o CEP for válido, sai do loop
        print(f'{RED}CEP inválido! O CEP deve ter exatamente 8 dígitos numéricos.{RESET}')
    
    # Verificação do CPF
    cpf = input(f'{CYAN}CPF (apenas números): {RESET}')
    
    if not verificar_cpf(cpf, estado):
        print(f'{RED}CPF inválido para o estado informado.{RESET}')
        return  # Corrigido: "return" estava incompleto
    
    # Conversão dos campos numéricos após validação
    numero = int(numero)
    cep = int(cep)
    
    print(f'{GREEN}Cadastro realizado com sucesso!{RESET}')

    data_nascimento = input(f'{CYAN}Digite sua data de nascimento (XX/XX/XXXX): {RESET}')
    dia, mes, ano = map(int, data_nascimento.split('/'))
    
    idade = datetime.now().year - ano
    
    if idade < 18:
        print(f'{RED}Você é menor de idade e não pode se cadastrar.{RESET}')
        return

    dependentes = input(f'{CYAN}Dependentes (SIM/NAO): {RESET}').strip().upper()
    quantidade_dependentes = int(input(f'{CYAN}Quantidade de dependentes: {RESET}')) if dependentes == 'SIM' else 0
    
    cargo = input(f'{CYAN}Cargo: {RESET}')
    salario = float(input(f'{CYAN}Salário: {RESET}'))

    funcionario = {
        
        'Nome': nome, 'Endereço': endereco, 'Número': numero,
        'Bairro': bairro, 'Cidade': cidade, 'Estado': estado,
        'CEP': cep, 'CPF': cpf, 'Idade': idade,
        'Data de nascimento': data_nascimento, 'Dependentes': quantidade_dependentes,
        'Cargo': cargo, 'Salário': salario
    }
    
    funcionarios.append(funcionario)
    
    print(f'{GREEN}Funcionário {nome} cadastrado com sucesso!{RESET}')
    
    limpar_terminal()

# Função para listar funcionários

def listar():
    
    if funcionarios:
        print('='*40)
        print(f'{BLUE}LISTA DE FUNCIONÁRIOS CADASTRADOS:{RESET}')
        for indice, funcionario in enumerate(funcionarios, start=1):
            print(f'{indice}.\n{YELLOW}Nome: {funcionario["Nome"]}\nEndereço: {funcionario["Endereço"]}\nNúmero: {funcionario["Número"]}\nBairro: {funcionario["Bairro"]}\nCidade: {funcionario["Cidade"]}\nEstado: {funcionario["Estado"]}\nCEP: {funcionario["CEP"]}\nCPF: {funcionario["CPF"]}\nIdade: {funcionario["Idade"]}\nData de nascimento: {funcionario["Data de nascimento"]}\nDependentes: {funcionario["Dependentes"]}\nCargo: {funcionario["Cargo"]}\nSalário: {funcionario["Salário"]}{RESET}')
            print('='*40)
    
    else:
        print(f'{RED}Nenhum funcionário cadastrado{RESET}')
        print('='*40)

limpar_terminal()

# Função para remover funcionários
def remover():
    if funcionarios:
        print(f'{CYAN}Funcionários disponíveis para remoção:{RESET}')
        for indice, funcionario in enumerate(funcionarios, start=1):
            print(f'{YELLOW}{indice}. {funcionario["Nome"]}{RESET}')
       
        escolha_funcionario = input(f'{CYAN}Qual funcionário deseja remover (número): {RESET}')
       
        if escolha_funcionario.isdigit():
            escolha_funcionario = int(escolha_funcionario)
            if 1 <= escolha_funcionario <= len(funcionarios):
                funcionario_removido = funcionarios.pop(escolha_funcionario - 1)
                lixeira.append(funcionario_removido)
                print(f'{GREEN}Funcionário {funcionario_removido["Nome"]} removido com sucesso.{RESET}')
            else:
                print(f'{RED}Escolha inválida. Número fora do intervalo.{RESET}')
        else:
            print(f'{RED}Escolha inválida. Por favor, insira um número válido.{RESET}')
    else:
        print(f'{RED}Nenhum funcionário cadastrado para remover.{RESET}')

limpar_terminal()

# Função para editar funcionários

def editar():
    if funcionarios:
        print(f'{CYAN}Funcionários disponíveis para edição:{RESET}')
        for indice, funcionario in enumerate(funcionarios, start=1):
            print(f'{indice}.\n{YELLOW}Nome: {funcionario["Nome"]}\nEndereço: {funcionario["Endereço"]}\nNúmero: {funcionario["Número"]}\nBairro: {funcionario["Bairro"]}\nCidade: {funcionario["Cidade"]}\nEstado: {funcionario["Estado"]}\nCEP: {funcionario["CEP"]}\nCPF: {funcionario["CPF"]}\nIdade: {funcionario["Idade"]}\nData de nascimento: {funcionario["Data de nascimento"]}\nDependentes: {funcionario["Dependentes"]}\nCargo: {funcionario["Cargo"]}\nSalário: {funcionario["Salário"]}{RESET}')
       
        escolha_funcionario = input(f'{CYAN}Qual funcionário deseja editar (número): {RESET}')
       
        if escolha_funcionario.isdigit():
            escolha_funcionario = int(escolha_funcionario)
            if 1 <= escolha_funcionario <= len(funcionarios):
                funcionario = funcionarios[escolha_funcionario - 1]
               
                print(f'{CYAN}Editando funcionário: {funcionario["Nome"]}{RESET}')
                print(f'{YELLOW}Escolha um campo para editar:')
                print(f'1. Nome\n2. Endereço\n3. Número\n4. Bairro\n5. Cidade\n6. Estado\n7. CEP\n8. Idade\n9. Data de nascimento\n10. Dependentes\n11. Cargo\n12. Salário\n13. Voltar ao Menu{RESET}')
               
                campo = input(f'{CYAN}Campo a ser editado: {RESET}')
                if campo.isdigit() and 1 <= int(campo) <= 13:
                    campo = int(campo)
                    
                    if campo == 13:  # Verificação para voltar ao menu
                        print(f'{YELLOW}Voltando ao menu...{RESET}')
                        return  # Encerra a função e volta ao menu principal
                    
                    novo_valor = input(f'{CYAN}Novo valor: {RESET}')
                   
                    if campo == 1:
                        funcionario['Nome'] = novo_valor
                    elif campo == 2:
                        funcionario['Endereço'] = novo_valor
                    elif campo == 3:
                        funcionario['Número'] = novo_valor
                    elif campo == 4:
                        funcionario['Bairro'] = novo_valor
                    elif campo == 5:
                        funcionario['Cidade'] = novo_valor
                    elif campo == 6:
                        funcionario['Estado'] = novo_valor
                    elif campo == 7:
                        funcionario['CEP'] = novo_valor
                    elif campo == 8:
                        funcionario['Idade'] = novo_valor
                    elif campo == 9:
                        funcionario['Data de nascimento'] = novo_valor
                    elif campo == 10:
                        funcionario['Dependentes'] = novo_valor
                    elif campo == 11:
                        funcionario['Cargo'] = novo_valor
                    elif campo == 12:
                        funcionario['Salário'] = novo_valor
                        
                    print(f'{GREEN}Funcionário {funcionario["Nome"]} editado com sucesso.{RESET}')
                else:
                    print(f'{RED}Escolha inválida.{RESET}')
            else:
                print(f'{RED}Escolha inválida. Número fora do intervalo.{RESET}')
        else:
            print(f'{RED}Escolha inválida. Por favor, insira um número válido.{RESET}')
    else:
        print(f'{RED}Nenhum funcionário cadastrado para editar.{RESET}')

limpar_terminal()

# Função para exibir lixeira
def exibir_lixeira():
    if lixeira:
        print(f'{BLUE}Funcionários na lixeira:{RESET}')
        for indice, funcionario in lixeira:
            print(f'{indice}.\n{YELLOW}Nome: {funcionario["Nome"]} {RESET}')
    else:    
        print(f'{RED}A lixeira está vazia.{RESET}')
limpar_terminal()

# Função para restaurar funcionários da lixeira
def restaurar():
    if lixeira:
        print(f'{CYAN}Funcionários disponíveis na lixeira:{RESET}')
        for indice, funcionario in enumerate(lixeira, start=1):
            print(f'{indice}.\n{YELLOW}Nome: {funcionario["Nome"]}\nEndereço: {funcionario["Endereço"]}\nNúmero: {funcionario["Número"]}\nBairro: {funcionario["Bairro"]}\nCidade: {funcionario["Cidade"]}\nEstado: {funcionario["Estado"]}\nCEP: {funcionario["CEP"]}\nCPF: {funcionario["CPF"]}\nIdade: {funcionario["Idade"]}\nData de nascimento: {funcionario["Data de nascimento"]}\nDependentes: {funcionario["Dependentes"]}\nCargo: {funcionario["Cargo"]}\nSalário: {funcionario["Salário"]}{RESET}')
        
        escolha = input(f'{CYAN}Deseja restaurar um funcionário específico (1) todos (2) ou voltar ao menu (3) ? {RESET}')
        
        if escolha == '1':
            escolha_funcionario = input(f'{CYAN}Qual funcionário deseja restaurar (número): {RESET}')
            if escolha_funcionario.isdigit():
                escolha_funcionario = int(escolha_funcionario)
                if 1 <= escolha_funcionario <= len(lixeira):
                    funcionario_restaurado = lixeira.pop(escolha_funcionario - 1)
                    funcionarios.append(funcionario_restaurado)
                    print(f'{GREEN}Funcionário {funcionario_restaurado["Nome"]} restaurado com sucesso.{RESET}')
                else:
                    print(f'{RED}Escolha inválida. Número fora do intervalo.{RESET}')
            
        elif escolha == '2':
            funcionarios.extend(lixeira)
            lixeira.clear()
            print(f'{GREEN}Todos os funcionários foram restaurados com sucesso.{RESET}')
        if escolha == '3':
            print('voltando ao menu')
                
            
        else:
            print(f'{RED}Escolha inválida.{RESET}')
    else:
        print(f'{RED}A lixeira está vazia.{RESET}')        

limpar_terminal()

def limpar_lixeira():
    lixeira.clear()
    print(f'{GREEN}Lixeira limpa com sucesso.{RESET}')

limpar_terminal()

senhas()

while True:
    menu()
    opcao = input(f'{CYAN}Escolha uma opção: {RESET}')
    limpar_terminal()
    
    if opcao == '1':
        cadastro()
    elif opcao == '2':
        listar()
    elif opcao == '3':
        editar()
    elif opcao == '4':
        remover()
    elif opcao == '5':
        exibir_lixeira()
    elif opcao == '6':
        restaurar()
    elif opcao == '7':
        limpar_lixeira()
    elif opcao == '8':
        print(f'{GREEN}Saindo...{RESET}')
        break
    else:
        print(f'{RED}Opção inválida!{RESET}')
