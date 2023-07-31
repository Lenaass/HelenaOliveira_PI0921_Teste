from fastapi import FastAPI
from banco import Conta

app = FastAPI()
dbfilename = "database.db"
Continha = None


@app.get("/")
async def root():
    return {"Bem Vindo"}


@app.get("/criarconta")
async def criarconta(titular: str, number: int):
    global Continha
    Continha = Conta(titular, number)
    Continha.movimentos.append("A conta foi criada")


@app.get("/depositar")
async def depositar(valorF: float):
    Continha.depositar(valorF)


@app.get("/levantar")
async def levantar(valorF: float):
    Continha.levantar(valorF)


@app.get("/transferir")
async def transferir(valorF: float, contadestino: int):
    Continha.transferir(valorF, contadestino)


@app.get("/extrato")
async def extrato():
    if Continha:
        return Continha.extrato()
    else:
        return {"message": "Conta não criada ainda"}