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
        return " ".join(["X"] * len(self.dados))

    def perder_dado(self):
        if len(self.dados) > 0:
            self.dados.pop()

    def ganar_dado(self):
        if len(self.dados) < 5:
            self.dados.append(Dado())