from src.juego.Cacho import Cacho

class GestorPartida:
    def __init__(self, num_jugadores):
        self.jugadores = [Cacho() for i in range(num_jugadores)]

        
