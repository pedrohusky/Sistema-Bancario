import hashlib
import os
import pickle
from datetime import datetime


class SistemaBancario:
    def __init__(self):
        self.usuários = []
        self.contas = {}
        self.load_data()

    def print_data(self):
        print("Usuários:")
        for usuario in self.usuários:
            print('  Nome: ' + usuario['nome'])
            print('  CPF: ' + usuario['cpf'])
            print('  Data de Nascimento: ' + usuario['nascimento'])
            print('  Endereço: ' + usuario['endereço'])
            print('  Conta-correntes:')
            for conta in usuario['contas']:
                print(f"     Número da agência: {conta['agencia']}")
                print(f"     Número da conta-corrente: {conta['numero']}")
        print()

        print("Contas:")
        for numero, conta in self.contas.items():
            print(f"  Conta de: {self.procurar_usuario(conta['usuario'])['nome']}")
            print(f"    Número da conta: {numero}")
            for key, value in conta.items():
                print(f"    {key}: {value}")
            print()  # Add an empty line for separation between account

    def save_data(self):
        with open('banco_data.pkl', 'wb') as file:
            data = {
                'usuários': self.usuários,
                'contas': self.contas
            }
            pickle.dump(data, file)

    def load_data(self):
        try:
            with open('banco_data.pkl', 'rb') as file:
                data = pickle.load(file)
                self.usuários = data['usuários']
                self.contas = data['contas']
                print('Dados carregados com sucesso')
        except FileNotFoundError:
            pass

    def login(self, usuario):
        cc_lista = []
        for conta in usuario['contas']:
            cc = self.procurar_conta_corrente(conta['numero'])
            if cc is not None:
                cc_lista.append(cc)
        senha_correta = self.verificar_senha(senha)

        if senha_correta:
            return usuario, cc_lista
        else:
            print("Senha incorreta")
            return None


    def criar_conta_corrente(self, cpf):
        usuario = self.procurar_usuario(cpf)
        if usuario is None:
            print(f"Nenhum usuário encontrado com o CPF {cpf}.")
        else:
            conta = {
                'agencia': '0001',
                'numero': len(self.contas)+1,
                'usuario': cpf,
                'saldo': 0.0,
                'saques_diarios': 0,
                'saldo_diario': 0.0,
                'transacoes': [],
                'LIMITE_SAQUES': 3,
                'LIMITE_DIARIO': 500.0
            }
            self.contas[len(self.contas)+1] = conta
            usuario['contas'].append({
                'agencia': conta['agencia'],
                'numero': conta['numero']
            })
            print(f"Conta-corrente criada para o usuário '{usuario['nome']}' com sucesso! \n"
                  f"Agência: {conta['agencia']}\n"
                  f"Cc (número): {conta['numero']}")
            self.save_data()

    def verificar_senha(self, entered_password):
        # Get the stored hashed password and salt from the user dictionary
        stored_hashed_password = usuario['senha']
        salt = usuario['salt']

        # Hash the entered password with the stored salt using SHA-256
        hashed_entered_password = hashlib.sha256(entered_password.encode('utf-8') + salt).hexdigest()

        # Check if the entered password matches the stored hashed password
        if hashed_entered_password == stored_hashed_password:
            return True
        else:
            print("Senha incorreta")
            return False

    def criar_usuário(self):

        cpf = input("Digite o CPF (somente números): ")
        usuario = self.procurar_usuario(cpf)
        if usuario is not None:
            print(f"Usuário com cpf {cpf} já existe.")
            return
        nome = input("Digite o nome completo: ")
        nascimento = input("Digite a data de nascimento: ")
        logradouro = input("Digite a rua onde mora (sem número): ")
        numero = input(f"Digite o número para {logradouro}: ")
        bairro = input("Digite o bairro: ")
        cidade_estado = input("Digite o a cidade e Estado (ex: Florianópolis/SC): ")
        senha = input('Crie uma senha para o usuário: ')

        endereço = logradouro + ', ' + numero + ' - ' + bairro + ' - ' + cidade_estado

        # Check if a user with the same name already exists
        usuario = self.procurar_usuario(cpf)
        if usuario is not None:
            print(f"Usuário com o CPF {cpf} já existe no banco de dados.")


        # Generate a random salt (16 bytes)
        salt = os.urandom(16)

        # Hash the password with the salt using SHA-256
        hashed_password = hashlib.sha256(senha.encode('utf-8') + salt).hexdigest()

        # If the user with the same name is not found, create a new user
        usuário = {
            'nome': nome,
            'nascimento': nascimento,
            'cpf': cpf,
            'endereço': endereço,
            'senha': hashed_password,
            'salt': salt,
            'contas': []
        }
        self.usuários.append(usuário)
        print(f"Usuário '{nome}' criado com sucesso!")
        self.save_data()

    def procurar_usuario(self, cpf):
        usuario = None
        for u in self.usuários:
            if u['cpf'] == cpf:
                usuario = u
        return usuario

    def procurar_conta_corrente(self, numero):
        for num, cc in self.contas.items():
            if int(numero) == cc['numero']:
                conta = cc
                return conta
        return None

    def deposito(self, /, agencia, cc, valor):

        if valor <= 0:
            print("Falha na operação: O valor tem que ser maior que zero.")
            return

        conta_corrente = self.procurar_conta_corrente(cc)

        if conta_corrente is None:
            print(f"Nenhuma conta com número {cc}")
            return

        usuario = self.procurar_usuario(conta_corrente['usuario'])

        conta_corrente['saldo'] += valor
        conta_corrente['transacoes'].append(f"Depósito: + R${valor:.2f}")

        print(f'|++| Depósito de R${valor} concluído com sucesso! |++|')

        self.save_data()
        return conta_corrente['saldo'], conta_corrente['transacoes']

    def saque(self, *, agencia, cc, valor):
        conta_corrente = self.procurar_conta_corrente(cc)
        if conta_corrente['saques_diarios'] >= conta_corrente['LIMITE_SAQUES']:
            print("Falha na operação: Limite de saques diários atingido.")
            return conta_corrente['saldo'], conta_corrente['transacoes']

        if conta_corrente['saldo_diario'] + valor > conta_corrente['LIMITE_DIARIO']:
            print("Falha na operação: Limite de R$500,00 por dia atingido.")
            return conta_corrente['saldo'], conta_corrente['transacoes']

        if conta_corrente['saldo'] - valor < 0:
            print("Falha na operação: Saldo insuficiente.")
            return conta_corrente['saldo'], conta_corrente['transacoes']

        conta_corrente['saldo'] -= valor
        conta_corrente['saldo_diario'] += valor
        conta_corrente['saques_diarios'] += 1
        conta_corrente['transacoes'].append(f"Saque: - R${valor:.2f}")

        self.save_data()
        print(f'|--| Saque de R${valor} concluído com sucesso! |--|')
        return conta_corrente['saldo'], conta_corrente['transacoes']

    def extrato(self, saldo, *, extrato=None):
        if extrato is not None:
            print("\n|========= EXTRATO =========|")
            if len(extrato) > 0:
                for transacao in extrato:
                    print('|  ' +transacao)
            else:
                print('|  Sem movimentações no momento.')
            print(f"| Saldo em conta: R${saldo:.2f}")
            print('|===========******==========|\n')

    def transferencia(self, agencia, cc, agencia_destino, cc_destino, valor):
        conta_corrente = self.procurar_conta_corrente(cc)
        if conta_corrente is None:
            print(f"Nenhuma conta corrente encontrada.")
            return
        conta_corrente_destino = self.procurar_conta_corrente(cc_destino)

        if conta_corrente_destino is None:
            print(f"Nenhuma conta-corrente de destino encontrada.")
            return
        if conta_corrente['saldo'] >= valor:
            conta_corrente['saldo'] -= valor

            conta_corrente_destino['saldo'] += valor

            self.save_data()
            print(f"|-+-| Transferência de R$ {valor} realizada com sucesso! |-+-|")
        else:
            print(f"Falha na operação: Saldo insuficiente. Saldo: R$ {conta_corrente['saldo']}  | Total: R$ {valor}")





if __name__ == "__main__":
    banco = SistemaBancario()

    while True:
        menu = '===========================================================\n' \
               'Bem-vindo ao Sistema Bancário - Menu de Opções\n' \
               '===========================================================\n' \
               '[l] - Entrar na conta\n' \
               '[a] - Adicionar usuário\n' \
               '[c] - Criar conta-corrente\n' \
               '[d] - Depositar\n' \
               '[s] - Sacar\n' \
               '[t] - Transferir\n' \
               '[e] - Extrato\n' \
               '[p] - Mostrar Usuários e Contas cadastradas\n' \
               '[q] - Sair do Sistema\n' \
               '-----------------------------------------------------------\n' \
               'Escolha a opção desejada: '

        opcao = input(menu)

        if opcao == "d":
            agencia = 0
            cc = 0
            valor = 0
            try:
                agencia = int(input("Digite a AGÊNCIA para depósito: "))
                cc = int(input("Digite a CONTA-CORRENTE para depósito: "))
                conta_corrente = banco.procurar_conta_corrente(cc)

                if conta_corrente is None:
                    print(f"Nenhuma conta corrente com número {cc}")
                    continue

                usuario = banco.procurar_usuario(conta_corrente['usuario'])

                if usuario is None:
                    print(f"Nenhum usuário com CPF {conta_corrente['usuario']}")
                    continue

                print("Conta Localizada para DEPÓSITO:")
                print(f"    Titular: {usuario['nome']}\n"
                      f"    Agência: {conta_corrente['agencia']}\n"
                      f"    Conta-corrente: {conta_corrente['numero']}")

                valor = float(input("Digite o valor a depositar: "))
            except Exception as e:
                print(f"Valor errado. Precisa ser um número!")


            # Format the time as DD/MM/YY HH:MM
            formatted_time = datetime.now().strftime("%d/%m/%y %H:%M")

            # Print the saque details with the formatted time
            print(f"|  Resumo da transação:\n"
                  f"|    Titular: {usuario['nome']}\n"
                  f"|    Agência: {conta_corrente['agencia']}\n"
                  f"|    Conta-corrente: {conta_corrente['numero']}\n"
                  f"|    Valor: R$ {valor}\n"
                  f"|    Ação: DEPÓSITO\n"
                  f"|    Dia: {formatted_time}")
            continuar = input("Os dados estão corretos? (Sim / Não): ")

            if continuar == "Sim" or continuar == "sim" or continuar == "s":
                banco.deposito(agencia, cc, valor)


        elif opcao == "s":

            agencia = 0
            cc = 0
            conta_corrente = None
            usuario = None

            try:
                agencia = int(input("Digite a AGÊNCIA para saque: "))
                cc = int(input("Digite a CONTA-CORRENTE para saque: "))
                conta_corrente = banco.procurar_conta_corrente(cc)

                if conta_corrente is None:
                    print(f"Nenhuma conta corrente com número {cc}")
                    continue

                usuario = banco.procurar_usuario(conta_corrente['usuario'])

                if usuario is None:
                    print(f"Nenhum usuário com CPF {conta_corrente['usuario']}")
                    continue

                print("Conta Localizada para SAQUE:")
                print(f"    Titular: {usuario['nome']}\n"
                      f"    Agência: {conta_corrente['agencia']}\n"
                      f"    Conta-corrente: {conta_corrente['numero']}")

            except Exception as e:
                print(f"Valor errado. Precisa ser um número! {e}")
                continue

            valor = float(input("Digite o valor a sacar: "))

            # Format the time as DD/MM/YY HH:MM
            formatted_time = datetime.now().strftime("%d/%m/%y %H:%M")

            # Print the saque details with the formatted time
            print(f"|  Resumo da transação:\n"
                  f"|    Titular: {usuario['nome']}\n"
                  f"|    Agência: {conta_corrente['agencia']}\n"
                  f"|    Conta-corrente: {conta_corrente['numero']}\n"
                  f"|    Valor: R$ {valor}\n"
                  f"|    Ação: SAQUE\n"
                  f"|    Dia: {formatted_time}")
            continuar = input("Os dados estão corretos? (Sim / Não): ")

            if continuar == "Sim" or continuar == "sim" or continuar == "s":
                senha = input(f"Agora a senha do usuário(a) {usuario['nome']}: ")

                senha_correta = banco.verificar_senha(senha)

                if senha_correta:

                    banco.saque(agencia=agencia, cc=cc, valor=valor)
                else:
                    print(f"Senha incorreta para {usuario['nome']}")



        elif opcao == "a":
            banco.criar_usuário()

        elif opcao == "l":
            cpf = input('Digite o CPF (apenas números): ')
            usuario = banco.procurar_usuario(cpf)

            if usuario is None:
                print(f"Nenhum usuário com CPF {cpf}")
                continue

            senha = input(f"Agora a senha do usuário(a) {usuario['nome']}: ")

            senha_correta = banco.verificar_senha(senha)

            if senha_correta:

                usuario, contas = banco.login(usuario)

                print()
                print("|  Login feito com sucesso:")
                print()
                print(f"|  Usuário: {usuario['nome']}")
                print(f"|  Contas:")
                for conta in contas:
                    print(f"|     | Agencia: {conta['agencia']}")
                    print(f"|     | Conta-corrente: {conta['numero']}")
                    print()
            else:
                print(f"Senha incorreta para {usuario['nome']}")

        elif opcao == "e":
            agencia = input("Digite a AGÊNCIA para retirar o extrato: ")
            cc = input("Digite a CONTA-CORRENTE para retirar o extrato: ")
            conta_corrente = banco.procurar_conta_corrente(cc)
            usuario = banco.procurar_usuario(conta_corrente['usuario'])
            senha = input(f"Agora a senha do usuário(a) {usuario['nome']}: ")
            senha_correta = banco.verificar_senha(senha)

            if senha_correta:
                banco.extrato(conta_corrente['saldo'], extrato=conta_corrente['transacoes'])

        elif opcao == "c":
            cpf = input('Digite o CPF: ')
            usuario = banco.procurar_usuario(cpf)

            if usuario is None:
                print("Não existe um usuário com este CPF")
                continue
            senha = input(f"Agora a senha do usuário(a) {usuario['nome']}: ")
            senha_correta = banco.verificar_senha(senha)

            if senha_correta:
                banco.criar_conta_corrente(cpf)

        elif opcao == "p":
            banco.print_data()

        elif opcao == "t":
            agencia = 0
            cc = 0
            agencia_destino = 0
            cc_destino = 0
            valor = 0
            try:
                agencia_destino = int(input("Digite a AGÊNCIA DE DESTINO para transferência: "))
                cc_destino = int(input("Digite a CONTA-CORRENTE DE DESTINO para transferência: "))

                conta_corrente_destino = banco.procurar_conta_corrente(cc_destino)

                if conta_corrente_destino is None:
                    print(f"Nenhuma conta-corrente encontrada com número {cc_destino}")
                    continue

                usuario_destino = banco.procurar_usuario(conta_corrente_destino['usuario'])


                if usuario_destino is None:
                    print(f"Nenhum usuário com CPF {conta_corrente_destino['usuario']}")
                    continue

                print("Conta de DESTINO Localizada para TRANSFERÊNCIA:")
                print(f"    Titular: {usuario_destino['nome']}\n"
                      f"    Agência: {conta_corrente_destino['agencia']}\n"
                      f"    Conta-corrente: {conta_corrente_destino['numero']}")

                agencia = int(input("Digite a AGÊNCIA REMETENTE para transferência: "))
                cc = int(input("Digite a CONTA-CORRENTE REMETENTE para transferência: "))
                conta_corrente = banco.procurar_conta_corrente(cc)

                if conta_corrente is None:
                    print(f"Nenhuma conta-corrente encontrada com número {cc}")
                    continue

                usuario = banco.procurar_usuario(conta_corrente['usuario'])

                if usuario is None:
                    print(f"Nenhum usuário com CPF {conta_corrente['usuario']}")
                    continue

                print("Conta REMETENTE Localizada para TRANSFERÊNCIA:")
                print(f"    Titular: {usuario['nome']}\n"
                      f"    Agência: {conta_corrente['agencia']}\n"
                      f"    Conta-corrente: {conta_corrente['numero']}")

                valor = float(input("Digite o valor a transferir: "))
            except Exception as e:
                print(f"Valor errado. Precisa ser um número!")

            # Format the time as DD/MM/YY HH:MM
            formatted_time = datetime.now().strftime("%d/%m/%y %H:%M")

            # Print the saque details with the formatted time
            print(f"|  Resumo da transação:\n"
                  f"|-+---+---+---+---+---+\n"
                  f"|  DE: \n"
                  f"|    Titular: {usuario['nome']}\n"
                  f"|    Agência: {conta_corrente['agencia']}\n"
                  f"|    Conta-corrente: {conta_corrente['numero']}\n"
                  f"|  PARA:\n"
                  f"|    Titular: {usuario_destino['nome']}\n"
                  f"|    Agência: {conta_corrente_destino['agencia']}\n"
                  f"|    Conta-corrente: {conta_corrente_destino['numero']}\n"
                  f"|-+---+---+---+---+---+\n"
                  f"|    Valor: R$ {valor}\n"
                  f"|    Ação: TRANSFERÊNCIA\n"
                  f"|    Dia: {formatted_time}\n")

            continuar = input("Os dados estão corretos? (Sim / Não): ")

            if continuar == "Sim" or continuar == "sim" or continuar == "s":
                senha = input(f"Agora a senha do usuário(a) {usuario['nome']}: ")
                senha_correta = banco.verificar_senha(senha)

                if senha_correta:
                    banco.transferencia(agencia, cc, agencia_destino, cc_destino, valor)

        elif opcao == "q":

            banco.save_data()

            print("Saindo do sistema.")

            break

        else:
            print("Opção inválida. Tente novamente.")
