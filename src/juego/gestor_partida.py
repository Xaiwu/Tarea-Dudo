from src.juego.Cacho import Cacho

class GestorPartida:
    def __init__(self, num_jugadores):
        self.jugadores = [Cacho() for i in range(num_jugadores)]


    def determinar_iniciador(self):
        while True:
            valores = [jugador.get_valores()[0] for jugador in self.jugadores]
            max_valor = max(valores)
            candidatos = [jugador for jugador, valor in zip(self.jugadores, valores) if valor == max_valor]
            if len(candidatos) == 1:
                return candidatos[0]
            for i in candidatos:
                self.jugadores[i].dados[0].lanzar()