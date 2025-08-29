class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta_actual, nueva_apuesta):
        # Lógica básica de validación
        if apuesta_actual is None:
            return True
            
        cantidad_actual, pinta_actual = apuesta_actual
        cantidad_nueva, pinta_nueva = nueva_apuesta
        
        if cantidad_nueva > cantidad_actual:
            return True
        if cantidad_nueva == cantidad_actual and pinta_nueva > pinta_actual:
            return True
            
        return False