from src.juego.contador_pintas import ContadorPintas


class ArbitroRonda:
    def __init__(self):
        self.contador_pintas = ContadorPintas()
    
    def determinar_resultado_duda(self, apuesta, dados, jugador_apostador, jugador_que_duda, modo_especial=False):
        """
        Determina el resultado cuando un jugador duda una apuesta.
        
        Returns:
            dict: Resultado con jugador_perdedor, razon, pintas_encontradas, apuesta_original
        """
        cantidad, pinta = apuesta
        
        # Validaciones
        if pinta < 1 or pinta > 6:
            raise ValueError("Pinta debe estar entre 1 y 6")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        
        # Determinar si usar ases como comodines
        ases_comodines = pinta != 1  # No usar comodines cuando se apuesta por ases
        
        # Contar pintas
        if modo_especial:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines, modo_especial=modo_especial
            )
        else:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines
            )
        
        # Determinar resultado
        if pintas_encontradas >= cantidad:
            # Apuesta correcta - quien dudó pierde
            return {
                'jugador_perdedor': jugador_que_duda,
                'razon': 'apuesta_correcta',
                'pintas_encontradas': pintas_encontradas,
                'apuesta_original': apuesta
            }
        else:
            # Apuesta incorrecta - quien apostó pierde
            return {
                'jugador_perdedor': jugador_apostador,
                'razon': 'apuesta_incorrecta',
                'pintas_encontradas': pintas_encontradas,
                'apuesta_original': apuesta
            }
    
    def determinar_resultado_calzar(self, apuesta, dados, jugador_calzador, modo_especial=False):
        """
        Determina el resultado cuando un jugador calza una apuesta.
        
        Returns:
            dict: Resultado con jugador_ganador/jugador_perdedor, razon, pintas_encontradas
        """
        cantidad, pinta = apuesta
        
        # Validaciones
        if pinta < 1 or pinta > 6:
            raise ValueError("Pinta debe estar entre 1 y 6")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        
        # Determinar si usar ases como comodines
        ases_comodines = pinta != 1  # No usar comodines cuando se calza por ases
        
        # Contar pintas
        if modo_especial:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines, modo_especial=modo_especial
            )
        else:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines
            )
        
        # Determinar resultado (debe ser exacto)
        if pintas_encontradas == cantidad:
            # Calzar exacto - jugador gana un dado
            return {
                'jugador_ganador': jugador_calzador,
                'razon': 'calzar_exacto',
                'pintas_encontradas': pintas_encontradas
            }
        else:
            # Calzar inexacto - jugador pierde un dado
            return {
                'jugador_perdedor': jugador_calzador,
                'razon': 'calzar_inexacto',
                'pintas_encontradas': pintas_encontradas
            }
    
    def validar_puede_calzar(self, dados_totales, jugador_calzador):
        """
        Valida si un jugador puede calzar según las reglas del juego.
        
        Reglas:
        - Puede calzar si tiene un solo dado
        - Puede calzar si hay mitad o más de los dados en juego
        
        Returns:
            bool: True si puede calzar, False en caso contrario
        """
        dados_jugador = len(jugador_calzador.cacho.dados)
        total_dados = len(dados_totales)
        
        # Puede calzar si tiene un solo dado
        if dados_jugador == 1:
            return True
        
        # Puede calzar si hay mitad o más dados en juego
        # (dados del jugador representan al menos la mitad del total)
        return dados_jugador >= (total_dados / 2)
