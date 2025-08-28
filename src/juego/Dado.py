import random

class Dado:
    def __init__(self):
        self.valor = random.randint(1, 6)

    def lanzar(self):
        self.valor = random.randint(1, 6)
        return self.valor
