from contas import Conta

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
contas = []

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



class Banco:
    def __init__(self):
        self.contas = []

    def criar_conta(self, id, saldo=0):
        conta = Conta(id, saldo)
        self.contas.append(conta)
        return conta

    def get_conta(self, id):
        for conta in self.contas:
            if conta.id == id:
                return conta
        return None

banco = Banco()

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")

@app.route("/criarconta/", methods=["POST"])
def criarconta():
    data = request.form
    id = int(data["numero"])
    saldo = float(data.get("saldo", 0.0))
    conta = banco.criar_conta(id, saldo)

@app.route("/acessarconta/", methods=["GET"])
def acessarconta():
    id = int(request.args.get("numero"))
    conta = banco.get_conta(id)