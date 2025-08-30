from src.juego.Dado import Dado

class Cacho:
    def __init__(self, valores=None):
        if valores is None:
            valores = []
        valores = list(valores) + [None] * (5 - len(valores))
        self.dados = [Dado(valor) for valor in valores]

    def agitar(self):
        for dado in self.dados:
            dado.lanzar()

    def get_valores(self):
        return [dado.valor for dado in self.dados]
