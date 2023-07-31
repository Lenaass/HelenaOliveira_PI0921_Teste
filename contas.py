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

conn.close()