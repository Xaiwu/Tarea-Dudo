from src.juego.contador_pintas import ContadorPintas


class ArbitroRonda:
    """
    Árbitro que determina el resultado cuando un jugador duda una apuesta.
    """
    
    def __init__(self):
        self.contador_pintas = ContadorPintas()
    
    def determinar_resultado_duda(self, apuesta, todos_los_dados, jugador_apostador, jugador_que_duda, modo_especial=False):
        """
        Determina quién pierde un dado cuando se duda una apuesta.
        
        Args:
            apuesta: Tupla (cantidad, pinta) de la apuesta dudada
            todos_los_dados: Lista de todos los dados en juego
            jugador_apostador: Jugador que hizo la apuesta
            jugador_que_duda: Jugador que dudó la apuesta
            modo_especial: Si es True, los ases no actúan como comodines
            
        Returns:
            Dict con información del resultado
            
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        cantidad, pinta = apuesta
        
        # Validaciones
        if pinta < 1 or pinta > 6:
            raise ValueError("Pinta debe estar entre 1 y 6")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        
        # Determinar si usar ases como comodines
        # Los ases no se usan como comodines cuando se apuesta por ases
        ases_comodines = pinta != 1
        
        # Contar pintas reales
        if modo_especial:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                todos_los_dados, 
                pinta, 
                ases_comodines=ases_comodines,
                modo_especial=modo_especial
            )
        else:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                todos_los_dados, 
                pinta, 
                ases_comodines=ases_comodines
            )
        
        # Determinar ganador/perdedor
        if pintas_encontradas >= cantidad:
            # La apuesta era correcta, pierde quien dudó
            jugador_perdedor = jugador_que_duda
            razon = 'apuesta_correcta'
        else:
            # La apuesta era incorrecta, pierde quien apostó
            jugador_perdedor = jugador_apostador
            razon = 'apuesta_incorrecta'
        
        return {
            'jugador_perdedor': jugador_perdedor,
            'razon': razon,
            'pintas_encontradas': pintas_encontradas,
            'apuesta_original': apuesta
        }