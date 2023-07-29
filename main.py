import time


class SistemaBancario:
    def __init__(self):
        self.saldo = 0.0
        self.saques_diarios = 0
        self.saldo_diario = 0.0
        self.transacoes = []
        self.LIMIT_SAQUES = 3
        self.LIMITE_DIÁRIO = 500

    def deposito(self, valor):
        self.saldo += valor
        self.transacoes.append(f"Depósito: + R${valor:.2f}")

    def saque(self, valor):
        if self.saques_diarios >= self.LIMIT_SAQUES:
            print("Limite de saques diários atingido.")
            return False

        if self.saldo_diario + valor > self.limite_diario:
            print("Limite de R$500,00 por dia atingido.")
            return False

        if self.saldo - valor < 0:
            print("Saldo insuficiente.")
            return False

        self.saldo -= valor
        self.saldo_diario += valor
        self.saques_diarios += 1
        self.transacoes.append(f"Saque: - R${valor:.2f}")

        return True

    def extrato(self):
        print("Extrato:")
        for transacao in self.transacoes:
            print(transacao)
        print(f"Saldo em conta: R${self.saldo:.2f}")


if __name__ == "__main__":
    banco = SistemaBancario()

    while True:
        menu = '===========================================================\n' \
               'Bem-vindo ao Sistema Bancário - Menu de Opções\n' \
               '===========================================================\n' \
               '[d] - Depositar\n' \
               '[s] - Sacar\n' \
               '[e] - Extrato\n' \
               '[q] - Sair do Sistema\n' \
               '-----------------------------------------------------------\n' \
               'Escolha a opção desejada: '

        opcao = input(menu)

        if opcao == "d":
            try:
                valor = float(input("Digite o valor a depositar: "))

                banco.deposito(valor)

                print(f'|++| Depósito de R${valor} concluído com sucesso! |++|')
            except Exception as e:
                print(f"Valor errado. Precisa ser um número!")

        elif opcao == "s":

            try:
                valor = float(input("Digite o valor a sacar: "))

                if banco.saque(valor):
                    print(f'|--| Saque de R${valor} concluído com sucesso! |--|')

            except Exception as e:
                print(f"Valor errado. Precisa ser um número!")

        elif opcao == "e":
            banco.extrato()

        elif opcao == "q":
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")

        # É necessário para manter uma boa visualizalçao da última ação do usuário
        time.sleep(1)
