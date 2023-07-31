import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

limite = {
    "Levantamento_max": 500,
    "Levantamento_dia": 2500
}

class Conta:
    def __init__(self, number, titular, saldo=0):
        self.number = number
        self.saldo = saldo
        self.titular = titular
        self.extrato = []

    def depositar(self, valorF):
        self.saldo += valorF
        self.extrato.append(f"Depósito: {valorF}")

    def levantar(self, valorF):
        if valorF > limite["Levantamento_max"]:
            print("Excedeu o limite por operação.")
            return
        elif self.saldo < valorF:
            print("Saldo insuficiente.")
            return
        self.saldo -= valorF
        self.extrato.append(f"Levantamento: {valorF}")

    def transferir(self, conta_destino, valorF):
        if conta_destino is None:
            print("Conta destino não encontrada")
        else:
            if valorF > self.saldo:
                print("Saldo insuficiente para transferência.")
            else:
                self.saldo -= valorF
                conta_destino.saldo += valorF
                self.extrato.append(f"Transferência para {conta_destino.number}: {valorF}")
                conta_destino.extrato.append(f"Transferência de {self.number}: {valorF}")

    def print_extrato(self):
        print("Extrato da conta %s \n" % self.number)
        for info in self.extrato:
            print(info)

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contas (
            number TEXT PRIMARY KEY,
            titular TEXT NOT NULL,
            saldo REAL NOT NULL
        )
    ''')
    conn.commit()

def insertconta(conta):
    cursor.execute("INSERT INTO contas VALUES (?, ?, ?)", (conta.number, conta.titular, conta.saldo))
    conn.commit()

def procurar_conta(number):
    cursor.execute("SELECT * FROM contas WHERE number = ?", (number,))
    result = cursor.fetchone()
    if result:
        return Conta(result[0], result[1], result[2])
    else:
        print("Conta inexistente.")
        return None

def criarconta():
    number = input("Número de conta: ")
    titular = input("Titular da conta: ")
    conta = Conta(number, titular)
    try:
        insertconta(conta)
    except sqlite3.IntegrityError:
        print("Já existe uma conta com essa informação.")
        return

    print("Conta criada.")

def menu():
    print("1. Criar Conta")
    print("2. Acessar Conta")
    print("3. Sair")

    opcao = int(input("Escolha: "))
    return opcao

# Create the table if it doesn't exist
create_table()

while True:
    opcao = menu()

    if opcao == 1:
        criarconta()

    elif opcao == 2:
        number = input("Número da conta: ")
        conta = procurar_conta(number)
        if conta:
            while True:
                print("1. Depositar")
                print("2. Levantar")
                print("3. Transferir")
                print("4. Extrato")
                print("5. Sair")

                opcao = int(input("Escolha uma opção: "))

                if opcao == 1:
                    valorF = float(input("Valor do depósito: "))
                    conta.depositar(valorF)
                elif opcao == 2:
                    valorF = float(input("Valor do levantamento: "))
                    conta.levantar(valorF)
                elif opcao == 3:
                    conta_destino = input("Digite o número da conta destino: ")
                    conta_dest = procurar_conta(conta_destino)
                    if conta_dest:
                        valorF = float(input("Valor da transferência: "))
                        conta.transferir(conta_dest, valorF)
                elif opcao == 4:
                    conta.print_extrato()
                elif opcao == 5:
                    break
                else:
                    print("Opção inválida.")

    elif opcao == 3:
        break

    else:
        print("Opção inválida.")

conn.close()