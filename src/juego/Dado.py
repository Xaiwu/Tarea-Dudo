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
    
    def get_denominacion(self):
        nombres = {
            1: "As",
            2: "Tonto",
            3: "Tren",
            4: "Cuadra",
            5: "Quina",
            6: "Sexto"
        }
        return nombres[self.valor]
