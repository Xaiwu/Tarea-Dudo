from src.juego.Cacho import Cacho

class GestorPartida:
    def __init__(self, num_jugadores):
        self.jugadores = [Cacho() for i in range(num_jugadores)]
        self.turno_actual = None

    def determinar_iniciador(self):
        while True:
            valores = [jugador.get_valores()[0] for jugador in self.jugadores]
            max_valor = max(valores)
            candidatos = [jugador for jugador, valor in zip(self.jugadores, valores) if valor == max_valor]
            if len(candidatos) == 1:
                self.turno_actual = self.jugadores.index(candidatos[0])
                return candidatos[0]
            for cacho in candidatos:
                cacho.dados[0].lanzar()

    def jugador_actual(self):
        return self.jugadores[self.turno_actual]

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)