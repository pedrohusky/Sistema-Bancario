import hashlib
import os
import pickle
from datetime import datetime
from abc import ABC, abstractclassmethod

class SistemaBancario:
    def __init__(self):
        self.clientes = []
        self.contas = []
        self.load_data()

    def sacar(self):
        agencia = 0
        cc = 0
        conta_corrente = None
        cliente = None

        try:
            cc = int(input("Digite a CONTA-CORRENTE para saque: "))
            conta_corrente = self.procurar_conta_corrente(cc)

            if conta_corrente is None:
                print(f"Nenhuma conta corrente com número {cc}")
                return

            cliente = self.procurar_cliente(conta_corrente.cliente.cpf)

            if cliente is None:
                print(f"Nenhum usuário com CPF {conta_corrente.cliente.cpf}")
                return

            print("Conta Localizada para SAQUE:")
            print(f"    Titular: {cliente.nome}\n"
                  f"    Agência: {conta_corrente.agencia}\n"
                  f"    Conta-corrente: {conta_corrente.numero}")

        except Exception as e:
            print(f"Valor errado. Precisa ser um número! {e}")
            return

        valor = float(input("Digite o valor a sacar: "))

        # Format the time as DD/MM/YY HH:MM
        formatted_time = datetime.now().strftime("%d/%m/%y %H:%M")

        # Print the saque details with the formatted time
        print(f"|  Resumo da transação:\n"
              f"|    Titular: {cliente.nome}\n"
              f"|    Agência: {conta_corrente.agencia}\n"
              f"|    Conta-corrente: {conta_corrente.numero}\n"
              f"|    Valor: R$ {valor}\n"
              f"|    Ação: SAQUE\n"
              f"|    Dia: {formatted_time}")
        continuar = input("Os dados estão corretos? (Sim / Não): ")

        if continuar == "Sim" or continuar == "sim" or continuar == "s":
            senha = input(f"Agora a senha do usuário(a) {cliente.nome}: ")

            senha_correta = cliente.verificar_senha(senha)

            if senha_correta:

                transacao = Saque(valor)

                cliente.realizar_transacao(conta_corrente, transacao)

                self.save_data()
            else:
                print(f"Senha incorreta para {cliente.nome}")
    def logar(self):
        cpf = input('Digite o CPF (apenas números): ')
        cliente = self.procurar_cliente(cpf)

        if cliente is None:
            print(f"Nenhum usuário com CPF {cpf}")
            return

        senha = input(f"Agora a senha do usuário(a) {cliente.nome}: ")

        cliente, contas = self.login(cliente, senha)
        if cliente is not None:
            print()
            print("|  Login feito com sucesso:")
            print()
            print(f"|  Usuário: {cliente.nome}")
            print(f"|  Contas:")
            for conta in contas:
                print(f"|     | Agencia: {conta.agencia}")
                print(f"|     | Conta-corrente: {conta.numero}")
                print()
        else:
            print(f"Senha incorreta para {cliente.nome}")
    def retirar_extrato(self):
        cc = input("Digite a CONTA-CORRENTE para retirar o extrato: ")
        conta_corrente = self.procurar_conta_corrente(cc)
        cliente = self.procurar_cliente(conta_corrente.cliente.cpf)
        senha = input(f"Agora a senha do usuário(a) {cliente.nome}: ")
        senha_correta = cliente.verificar_senha(senha)

        if senha_correta:
            self.extrato(conta_corrente.saldo, extrato=conta_corrente.historico)

    def criar_conta(self):
        cpf = input('Digite o CPF: ')
        cliente = self.procurar_cliente(cpf)

        if cliente is None:
            print("Não existe um usuário com este CPF")
            return
        senha = input(f"Agora a senha do usuário(a) {cliente.nome}: ")
        senha_correta = cliente.verificar_senha(senha)

        if senha_correta:
            self.criar_conta_corrente(cpf)

    def transferir(self):
        agencia = 0
        conta_corrente = 0
        agencia_destino = 0
        conta_corrente_destino = 0
        cliente = None
        valor = 0
        try:
            cc_destino = int(input("Digite a CONTA-CORRENTE DE DESTINO para transferência: "))

            conta_corrente_destino = self.procurar_conta_corrente(cc_destino)

            if conta_corrente_destino is None:
                print(f"Nenhuma conta-corrente encontrada com número {cc_destino}")
                return


            cliente_destino = self.procurar_cliente(conta_corrente_destino.cliente.cpf)

            if cliente_destino is None:
                print(f"Nenhum usuário com CPF {conta_corrente_destino.cliente.cpf}")
                return

            print("Conta de DESTINO Localizada para TRANSFERÊNCIA:")
            print(f"    Titular: {cliente_destino.nome}\n"
                  f"    Agência: {conta_corrente_destino.agencia}\n"
                  f"    Conta-corrente: {conta_corrente_destino.numero}")

            cc = int(input("Digite a CONTA-CORRENTE REMETENTE para transferência: "))
            conta_corrente = self.procurar_conta_corrente(cc)

            if conta_corrente is None:
                print(f"Nenhuma conta-corrente encontrada com número {cc}")
                return

            cliente = self.procurar_cliente(conta_corrente.cliente.cpf)

            if cliente is None:
                print(f"Nenhum usuário com CPF {conta_corrente.cliente.cpf}")
                return

            print("Conta REMETENTE Localizada para TRANSFERÊNCIA:")
            print(f"    Titular: {cliente.nome}\n"
                  f"    Agência: {conta_corrente.agencia}\n"
                  f"    Conta-corrente: {conta_corrente.numero}")

            valor = float(input("Digite o valor a transferir: "))
        except Exception as e:
            print(f"Valor errado. Precisa ser um número!")

        # Format the time as DD/MM/YY HH:MM
        formatted_time = datetime.now().strftime("%d/%m/%y %H:%M")

        # Print the saque details with the formatted time
        print(f"|  Resumo da transação:\n"
              f"|-+---+---+---+---+---+\n"
              f"|  DE: \n"
              f"|    Titular: {cliente.nome}\n"
              f"|    Agência: {conta_corrente.agencia}\n"
              f"|    Conta-corrente: {conta_corrente.numero}\n"
              f"|  PARA:\n"
              f"|    Titular: {cliente_destino.nome}\n"
              f"|    Agência: {conta_corrente_destino.agencia}\n"
              f"|    Conta-corrente: {conta_corrente_destino.numero}\n"
              f"|-+---+---+---+---+---+\n"
              f"|    Valor: R$ {valor}\n"
              f"|    Ação: TRANSFERÊNCIA\n"
              f"|    Dia: {formatted_time}\n")

        continuar = input("Os dados estão corretos? (Sim / Não): ")

        if continuar == "Sim" or continuar == "sim" or continuar == "s":
            senha = input(f"Agora a senha do usuário(a) {cliente.nome}: ")
            senha_correta = cliente.verificar_senha(senha)

            if senha_correta:
                transacao = Transferencia(valor, conta_corrente_destino, conta_corrente)

                cliente.realizar_transacao(conta_corrente, transacao)

                self.save_data()

    def extrato(self, saldo, *, extrato=None):
        if extrato is not None:
            print("\n|========= EXTRATO =========|")
            if len(extrato.transacoes) > 0:
                for transacao in extrato.transacoes:
                    dados = ''
                    if transacao['dados_adicionais'] != '':
                        dados = f"{transacao['dados_adicionais']}\n"
                    print(f"|  Tipo: {transacao['tipo']}"
                          + dados)
                    if transacao['dados_adicionais'] == '':
                        print(f"    |  Valor: R$ {transacao['valor']}")
                    print()

            else:
                print('|  Sem movimentações no momento.')
            print(f"| Saldo em conta: R${saldo:.2f}")
            print('|===========******==========|\n')
    def depositar(self):
        agencia = 0
        cc = 0
        valor = 0
        try:
            cc = int(input("Digite a CONTA-CORRENTE (ou CPF) para depósito: "))
            conta_corrente = self.procurar_conta_corrente(cc)

            if conta_corrente is None:
                print(f"Nenhuma conta corrente com número {cc}")
                return

            cliente = self.procurar_cliente(conta_corrente.cliente.cpf)

            if cliente is None:
                print(f"Nenhum usuário com CPF {conta_corrente.cliente.cpf}")
                return

            print("Conta Localizada para DEPÓSITO:")
            print(f"    Titular: {cliente.nome}\n"
                  f"    Agência: {conta_corrente.agencia}\n"
                  f"    Conta-corrente: {conta_corrente.numero}")

            valor = float(input("Digite o valor a depositar: "))
        except Exception as e:
            print(f"Valor errado. Precisa ser um número! {e}")

        # Format the time as DD/MM/YY HH:MM
        formatted_time = datetime.now().strftime("%d/%m/%y %H:%M")

        # Print the saque details with the formatted time
        print(f"|  Resumo da transação:\n"
              f"|    Titular: {cliente.nome}\n"
              f"|    Agência: {conta_corrente.agencia}\n"
              f"|    Conta-corrente: {conta_corrente.numero}\n"
              f"|    Valor: R$ {valor}\n"
              f"|    Ação: DEPÓSITO\n"
              f"|    Dia: {formatted_time}")
        continuar = input("Os dados estão corretos? (Sim / Não): ")

        if continuar == "Sim" or continuar == "sim" or continuar == "s":
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta_corrente, transacao)
            self.save_data()


    def print_data(self):
        print("Clientes:")
        for cliente in self.clientes:
            print('  Nome: ' + cliente.nome)
            print('  CPF: ' + cliente.cpf)
            print('  Data de Nascimento: ' + cliente.nascimento)
            print('  Endereço: ' + cliente.endereco)
            print('  Conta-correntes:')
            for conta in cliente.contas:
                print(f"     Número da agência: {conta.agencia}")
                print(f"     Número da conta-corrente: {conta.numero}")
            print()

        print("Contas:")
        for conta in self.contas:
            print(str(conta))
            print()  # Add an empty line for separation between account

    def save_data(self):
        with open('banco_data.pkl', 'wb') as file:
            data = {
                'usuários': self.clientes,
                'contas': self.contas
            }
            pickle.dump(data, file)

    def load_data(self):
        try:
            with open('banco_data.pkl', 'rb') as file:
                data = pickle.load(file)
                self.clientes = data['usuários']
                self.contas = data['contas']
                print('Dados carregados com sucesso')
        except FileNotFoundError:
            pass

    def login(self, cliente, senha):
        cc_lista = []
        for conta in cliente.contas:
            cc = self.procurar_conta_corrente(conta.numero)
            if cc is not None:
                cc_lista.append(cc)
        senha_correta = cliente.verificar_senha(senha)

        if senha_correta:
            return cliente, cc_lista
        else:
            print("Senha incorreta")
            return None

    def criar_conta_corrente(self, cpf):
        cliente = self.procurar_cliente(cpf)
        if cliente is None:
            print(f"Nenhum usuário encontrado com o CPF {cpf}.")
        else:
            conta = ContaCorrente.nova_conta(cliente=cliente, numero=len(self.contas) + 1)
            self.contas.append(conta)
            cliente.contas.append(conta)
            self.save_data()
            print(f"Conta-corrente criada para o usuário '{cliente.nome}' com sucesso! \n"
                  f"Agência: {conta.agencia}\n"
                  f"Cc (número): {conta.numero}")

    def criar_usuário(self):

        cpf = input("Digite o CPF (somente números): ")
        cliente = self.procurar_cliente(cpf)
        if cliente is not None:
            print(f"Usuário com cpf {cpf} já existe.")
            return
        nome = input("Digite o nome completo: ")
        nascimento = input("Digite a data de nascimento (dd/mm/aa): ")
        logradouro = input("Digite a rua onde mora (sem número): ")
        numero = input(f"Digite o número para {logradouro}: ")
        bairro = input("Digite o bairro: ")
        cidade_estado = input("Digite o a cidade e Estado (ex: Florianópolis/SC): ")
        senha = input('Crie uma senha para o usuário: ')

        endereço = logradouro + ', ' + numero + ' - ' + bairro + ' - ' + cidade_estado

        # Generate a random salt (16 bytes)
        salt = os.urandom(16)

        # Hash the password with the salt using SHA-256
        hashed_password = hashlib.sha256(senha.encode('utf-8') + salt).hexdigest()
        cliente = PessoaFisica(nome=nome, cpf=cpf, nascimento=nascimento, endereco=endereço, senha=hashed_password, salt=salt)
        self.clientes.append(cliente)
        print(f"Cliente '{nome}' criado com sucesso!")
        self.save_data()

    def procurar_cliente(self, cpf):
        cliente_recuperado = None
        for c in self.clientes:
            if c.cpf == cpf:
                cliente_recuperado = c
        return cliente_recuperado

    def procurar_conta_corrente(self, numero):
        for cc in self.contas:
            if int(numero) == cc.numero or str(numero) == cc.cliente.cpf:
                conta = cc
                return conta
        return None


class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def numero(self):
        return self.numero

    def agencia(self):
        return self.agencia

    def historico(self):
        return self.historico

    def transferir(self, cc_destino, cc, valor):
        if cc.saldo >= valor > 0:
            cc.saldo -= valor

            cc_destino.saldo += valor

            print(f"|-+-| Transferência de R$ {valor} realizada com sucesso! |-+-|")

            dados = f"\n    |  Resumo da transação:\n"\
              f"    |-+---+---+---+---+---+\n"\
              f"    |  DE: \n"\
              f"    |    Titular: {cc.cliente.nome}\n"\
              f"    |    Agência: {cc.agencia}\n"\
              f"    |    Conta-corrente: {cc.numero}\n"\
              f"    |  PARA:\n"\
              f"    |    Titular: {cc_destino.cliente.nome}\n"\
              f"    |    Agência: {cc_destino.agencia}\n"\
              f"    |    Conta-corrente: {cc_destino.numero}\n"\
              f"    |-+---+---+---+---+---+\n"\
              f"    |  Valor: R$ {valor:.2f}"

            return True, dados
        else:
            return False, ''

    def sacar(self, valor):
        saldo = self.saldo

        if saldo < valor:
            print(f"Operação Falhou: Você não tem Saldo suficiente.")
            return False
        elif saldo >= valor:
            self.saldo -= valor
            print(f"Operação bem-sucedida: Saque realizado com sucesso!")
            return True
        else:
            print(f"Operação Falhou: Valor informado é inválido.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f"Operação bem-sucedida: Depósito de R$ {valor} realizado com sucesso!")
            return True
        elif valor <= 0:
            print(f"Operação Falhou: Valor tem que ser maior que zero.")
            return False
        else:
            print(f"Operação Falhou: Valor informado é inválido.")
            return False

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def __str__(self):
        return f"    Agência: {self.agencia}\n" \
               f"    Número: {self.numero}\n" \
               f"    Cliente: {self.cliente}\n" \
               f"    Saldo: R${self.saldo:.2f}\n" \
               f"    Transações:\n" \
               f"    {', '.join(self.historico) if self.historico else 'Nenhuma transação realizada.'}\n"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        # Additional attributes specific to ContaCorrente can be added here

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f"Operação Falhou: Limite de {self.limite} excedido")
        elif excedeu_saques:
            print(f"Operação Falhou: Limite de saques ({self.limite_saques}) excedido")
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""
    Agência: {self.agencia}
    Conta-corrente: {self.numero}
    Saldo: R$ {self.saldo}
    Titular: {self.cliente.nome}"""


class Cliente:
    def __init__(self, endereco, senha, salt):
        self.endereco = endereco
        self.contas = []
        self.senha = senha
        self.salt = salt

    def adicionar_conta(self, conta):
        conta_existe = None
        for c in self.contas:
            if c.cpf == conta.cpf:
                conta_existe = c

        if conta_existe is None:
            self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def verificar_senha(self, entered_password):
        # Hash the entered password with the stored salt using SHA-256
        hashed_entered_password = hashlib.sha256(entered_password.encode('utf-8') + self.salt).hexdigest()

        # Check if the entered password matches the stored hashed password
        if hashed_entered_password == self.senha:
            return True
        else:
            print("Senha incorreta")
            return False


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, nascimento, endereco, senha, salt):
        super().__init__(endereco, senha, salt)
        self.cpf = cpf
        self.nome = nome
        self.nascimento = nascimento


class Historico:
    def __init__(self):
        self.transacoes = []

    def transacoes(self):
        return self.transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'dados_adicionais': transacao.dados,
            'data': datetime.now().strftime("%d/%m/%y %H:%M"),
        })


class Transacao(ABC):
    @property
    @abstractclassmethod
    def valor(self):
        pass

    @property
    @abstractclassmethod
    def dados(self):
        pass

    @abstractclassmethod
    def registrar(self, conta: Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._dados = ''

    @property
    def valor(self):
        return self._valor

    @property
    def dados(self):
        return self._dados

    def registrar(self, conta: Conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._dados = ''

    @property
    def valor(self):
        return self._valor

    @property
    def dados(self):
        return self._dados

    def registrar(self, conta: Conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Transferencia(Transacao):
    def __init__(self, valor, cc_destino, cc):
        self._valor = valor
        self._dados = ''
        self.cc_destino = cc_destino
        self.cc = cc

    @property
    def valor(self):
        return self._valor

    @property
    def dados(self):
        return self._dados

    def registrar(self, conta: Conta):
        sucesso_transacao, dados = conta.transferir(self.cc_destino, self.cc,
                                                    self.valor)

        if sucesso_transacao:
            self._dados = dados
            conta.historico.adicionar_transacao(self)
            if conta != self.cc_destino:
                self.cc_destino.historico.adicionar_transacao(self)
