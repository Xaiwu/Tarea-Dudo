import math

class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta_actual, nueva_apuesta, dados_jugador=5):
        # Lógica básica de validación
        if apuesta_actual is None:
            # Primera apuesta: verificar regla especial de Ases
            return self._validar_primera_apuesta(nueva_apuesta, dados_jugador)
            
        cantidad_actual, pinta_actual = apuesta_actual
        cantidad_nueva, pinta_nueva = nueva_apuesta
        
        # Reglas especiales para Ases (pinta 1)
        if self._es_cambio_a_ases(pinta_actual, pinta_nueva):
            return self._validar_cambio_a_ases(cantidad_actual, cantidad_nueva)
        
        if self._es_cambio_de_ases(pinta_actual, pinta_nueva):
            return self._validar_cambio_de_ases(cantidad_actual, cantidad_nueva)
        
        # Reglas básicas: mayor cantidad o misma cantidad con mayor pinta
        if cantidad_nueva > cantidad_actual:
            return True
        if cantidad_nueva == cantidad_actual and pinta_nueva > pinta_actual:
            return True
            
        return False
    
    def _validar_primera_apuesta(self, nueva_apuesta, dados_jugador):
        """
        Valida la primera apuesta de la partida.
        No se puede partir con Ases (pinta 1) excepto cuando se tiene un solo dado.
        """
        cantidad_nueva, pinta_nueva = nueva_apuesta
        
        # Si la primera apuesta es con Ases (pinta 1)
        if pinta_nueva == 1:
            # Solo es válida si el jugador tiene exactamente 1 dado
            return dados_jugador == 1
        
        # Cualquier otra pinta es válida en la primera apuesta
        return True
    
    def _es_cambio_a_ases(self, pinta_actual, pinta_nueva):
        """Verifica si se está cambiando a Ases (pinta 1)"""
        return pinta_actual != 1 and pinta_nueva == 1
    
    def _es_cambio_de_ases(self, pinta_actual, pinta_nueva):
        """Verifica si se está cambiando desde Ases (pinta 1)"""
        return pinta_actual == 1 and pinta_nueva != 1
    
    def _validar_cambio_a_ases(self, cantidad_actual, cantidad_nueva):
        """
        Valida cambio a Ases: dividir cantidad actual por 2
        - Si es par: dividir por 2 y sumar 1
        - Si es impar: dividir por 2 y redondear arriba
        """
        if cantidad_actual % 2 == 0:  # Cantidad par
            cantidad_requerida = (cantidad_actual // 2) + 1
        else:  # Cantidad impar
            cantidad_requerida = math.ceil(cantidad_actual / 2)
        
        return cantidad_nueva == cantidad_requerida
    
    def _validar_cambio_de_ases(self, cantidad_actual, cantidad_nueva):
        """
        Valida cambio de Ases: multiplicar por 2 y sumar 1
        """
        cantidad_minima_requerida = (cantidad_actual * 2) + 1
        return cantidad_nueva >= cantidad_minima_requerida