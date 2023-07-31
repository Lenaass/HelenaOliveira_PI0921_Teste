import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

limite = {
    "Levantamento_max": 500,
    "Levantamento_dia": 2500
}

class Conta:
    def __init__(self, titular: str, number: int):
        self.titular = titular
        self.number = number
        self.saldo = 0
        self.movimentos = []

    def depositar(self, valor: float):
        self.saldo += valor
        self.movimentos.append(f"Depósito de {valor}")

    def levantar(self, valor: float):
        if self.saldo >= valor:
            self.saldo -= valor
            self.movimentos.append(f"Levantamento de {valor}")
        else:
            self.movimentos.append("Saldo insuficiente")

    def transferir(self, valor: float, contadestino: int):
        if self.saldo >= valor:
            self.saldo -= valor
            self.movimentos.append(f"Transferência de {valor} para a conta {contadestino}")
        else:
            self.movimentos.append("Saldo insuficiente")

    def extrato(self):
        return {"titular": self.titular, "number": self.number, "saldo": self.saldo, "movimentos": self.movimentos}

conn.close()