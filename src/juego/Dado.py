import random

class Dado:
    def __init__(self,valor=None):
        if valor is not None:
            self.valor = valor
        else:
            self.valor = random.randint(1, 6)

    def lanzar(self):
        self.valor = random.randint(1, 6)
        return self.valor