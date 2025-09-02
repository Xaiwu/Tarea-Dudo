import random

class Dado:

    def __init__(self,valor=None):
        if valor is not None:
            if valor < 1 or valor > 6:
                raise ValueError("El valor del dado debe estar entre 1 y 6")
            self.valor = valor
        else:
            self.valor = random.randint(1, 6)
        self.NOMBRES = {
            1: "As",
            2: "Tonto",
            3: "Tren",
            4: "Cuadra",
            5: "Quina",
            6: "Sexto"
            }

    def lanzar(self):
        self.valor = random.randint(1, 6)
        return self.valor
    
    def get_denominacion(self):
        return self.NOMBRES[self.valor]
