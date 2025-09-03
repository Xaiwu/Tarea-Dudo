from src.juego.Jugador import Jugador

class GestorPartida:
    def __init__(self, num_jugadores):
        self.jugadores = [Jugador() for _ in range(num_jugadores)]
        self.turno_actual = None
        self.modo_especial = False
        self.apuesta_actual = None

    def determinar_iniciador(self):
        while True:
            valores = [jugador.cacho.get_valores()[0] for jugador in self.jugadores]
            max_valor = max(valores)
            candidatos = [jugador for jugador, valor in zip(self.jugadores, valores) if valor == max_valor]
            if len(candidatos) == 1:
                self.turno_actual = self.jugadores.index(candidatos[0])
                return candidatos[0]
            for jugador in candidatos:
                jugador.cacho.dados[0].lanzar()

    def jugador_actual(self):
        return self.jugadores[self.turno_actual]

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
    
    def jugadores_con_un_dado(self):
            return [jugador for jugador in self.jugadores if len(jugador.cacho.dados) == 1]

    def activar_reglas_especiales(self):
        jugadores_un_dado = self.jugadores_con_un_dado()
        if jugadores_un_dado:
            self.modo_especial = True
            for jugador in jugadores_un_dado:
                jugador.modo_obligado = True   
    
    def finalizar_ronda_especial(self):
        self.modo_especial = False
        for jugador in self.jugadores:
            jugador.modo_obligado = False
    
    def eliminar_jugadores_sin_dados(self, jugador_siguiente=None):
        self.jugadores = [j for j in self.jugadores if len(j.cacho.dados) > 0]
        if jugador_siguiente and jugador_siguiente in self.jugadores:
            self.turno_actual = self.jugadores.index(jugador_siguiente)
        else:
            if self.turno_actual is None or self.turno_actual >= len(self.jugadores):
                self.turno_actual = 0