from src.juego.Dado import Dado

class Cacho:
    def __init__(self, valores=None):
        if valores is None:
            valores = []
        valores = list(valores) + [None] * (5 - len(valores))
        self.dados = [Dado(valor) for valor in valores]
        self.visibilidad = False

    def agitar(self):
        for dado in self.dados:
            dado.lanzar()

    def get_valores(self):
        return [dado.valor for dado in self.dados]

    def revelar(self):
        self.visibilidad = True

    def mostrar(self):
        if self.visibilidad:
            return " ".join(str(dado.valor) for dado in self.dados)
        msj = ""
        msj = "X " * (len(self.dados) - 1)
        return msj + "X"
