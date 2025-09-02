from src.juego.Cacho import Cacho

class Jugador:
    def __init__(self, valores=None):
        self.cacho = Cacho(valores)
        self.modo_obligado = False
        self.obligar_disponible = True 