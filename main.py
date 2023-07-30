from sistema_bancario import SistemaBancario

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
            banco.depositar()

        elif opcao == "s":
            banco.sacar()

        elif opcao == "a":
            banco.criar_usuário()

        elif opcao == "l":
            banco.logar()

        elif opcao == "e":
            banco.retirar_extrato()

        elif opcao == "c":
            banco.criar_conta()

        elif opcao == "p":
            banco.print_data()

        elif opcao == "t":
            banco.transferir()

        elif opcao == "q":

            banco.save_data()

            print("Saindo do sistema.")

            break

        else:
            print("Opção inválida. Tente novamente.")
