# Sistema-Bancario
Sistema bancário criado como exercício para a DIO

sistema bancário em python com funções:



- depósito, saque, extrato, Adicionar usuário, criar conta-corrente, transferir, mostrar usuários e contas cadastradas, login.



- no depósito, necessita apenas ser armazenado em uma variável, sem necessitar de agência e conta pois apenas funciona com um usuário. A variável precisa ser acessada da função extrato.



- no saque, no máximo três saques diários com limite de R$500,00. Caso não haja dinheiro em conta, uma mensagem informando o usuário deverá aparecer. Saques devem ser armazenados em uma variável e ser acessível da função extrato.



- no extrato, deve listar todos os depósitos e saques realizados na conta, no fim da listagem, exibir o valor total em conta no formato R$ XXXX.XX (1500.45 = R$1500,45)


- em trasnferir, recebe duas agencias e duas Cc's (destino e remetente), então, busca no banco de dados se a conta remetente possui o valor, se sim, pede a senha da pessoa remetente



Comandos:

- [l] - Entrar na conta
- [a] - Adicionar usuário
- [c] - Criar conta-corrente
- [d] - Depositar
- [s] - Sacar
- [t] - Transferir
- [e] - Extrato
- [p] - Mostrar Usuários e Contas cadastradas
- [q] - Sair do Sistema
