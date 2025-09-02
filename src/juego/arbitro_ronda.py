from src.juego.contador_pintas import ContadorPintas


class ArbitroRonda:
    def __init__(self):
        self.contador_pintas = ContadorPintas()
    
    def determinar_resultado_duda(self, apuesta, dados, jugador_apostador, jugador_que_duda, modo_especial=False):
        cantidad, pinta = apuesta
        
        if pinta < 1 or pinta > 6:
            raise ValueError("Pinta debe estar entre 1 y 6")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        
        ases_comodines = pinta != 1
        
        if modo_especial:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines, modo_especial=modo_especial
            )
        else:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines
            )
        
        if pintas_encontradas >= cantidad:
            return {
                'jugador_perdedor': jugador_que_duda,
                'razon': 'apuesta_correcta',
                'pintas_encontradas': pintas_encontradas,
                'apuesta_original': apuesta
            }
        else:
            return {
                'jugador_perdedor': jugador_apostador,
                'razon': 'apuesta_incorrecta',
                'pintas_encontradas': pintas_encontradas,
                'apuesta_original': apuesta
            }
    
    def determinar_resultado_calzar(self, apuesta, dados, jugador_calzador, modo_especial=False):
        cantidad, pinta = apuesta
        
        if pinta < 1 or pinta > 6:
            raise ValueError("Pinta debe estar entre 1 y 6")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        
        ases_comodines = pinta != 1
        
        if modo_especial:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines, modo_especial=modo_especial
            )
        else:
            pintas_encontradas = self.contador_pintas.contar_pinta(
                dados, pinta, ases_comodines=ases_comodines
            )
        
        if pintas_encontradas == cantidad:
            return {
                'jugador_ganador': jugador_calzador,
                'razon': 'calzar_exacto',
                'pintas_encontradas': pintas_encontradas
            }
        else:
            return {
                'jugador_perdedor': jugador_calzador,
                'razon': 'calzar_inexacto',
                'pintas_encontradas': pintas_encontradas
            }
    
    def validar_puede_calzar(self, dados_totales, jugador_calzador):
        dados_jugador = len(jugador_calzador.cacho.dados)
        total_dados = len(dados_totales)
        
        if dados_jugador == 1:
            return True
        
        return dados_jugador >= (total_dados / 2)
    
    def aplicar_resultado_duda(self, apuesta, dados, jugador_apostador, jugador_que_duda, modo_especial=False):
        resultado = self.determinar_resultado_duda(apuesta, dados, jugador_apostador, jugador_que_duda, modo_especial)
        
        if 'jugador_perdedor' in resultado:
            resultado['jugador_perdedor'].cacho.perder_dado()
        
        return resultado
    
    def aplicar_resultado_calzar(self, apuesta, dados, jugador_calzador, modo_especial=False):
        resultado = self.determinar_resultado_calzar(apuesta, dados, jugador_calzador, modo_especial)
        
        if 'jugador_ganador' in resultado:
            resultado['jugador_ganador'].cacho.ganar_dado()
        elif 'jugador_perdedor' in resultado:
            resultado['jugador_perdedor'].cacho.perder_dado()
        
        return resultado
    
    def determinar_siguiente_jugador(self, resultado):
        if 'jugador_perdedor' in resultado:
            return resultado['jugador_perdedor']
        elif 'jugador_ganador' in resultado:
            return resultado['jugador_ganador']
        else:
            return None
    
    def procesar_duda_completa(self, apuesta, dados, jugador_apostador, jugador_que_duda, modo_especial=False):
        resultado = self.aplicar_resultado_duda(apuesta, dados, jugador_apostador, jugador_que_duda, modo_especial)
        resultado['siguiente_jugador'] = self.determinar_siguiente_jugador(resultado)
        return resultado
    
    def procesar_calzar_completo(self, apuesta, dados, jugador_calzador, modo_especial=False):
        resultado = self.aplicar_resultado_calzar(apuesta, dados, jugador_calzador, modo_especial)
        resultado['siguiente_jugador'] = self.determinar_siguiente_jugador(resultado)
        return resultado
    
    def validar_jugador_puede_continuar(self, jugador):
        return len(jugador.cacho.dados) > 0
    
    def validar_condiciones_calzar(self, todos_los_dados, dados_jugador):
        if hasattr(dados_jugador, 'cacho'):
            cantidad_dados_jugador = len(dados_jugador.cacho.dados)
        elif isinstance(dados_jugador, list):
            cantidad_dados_jugador = len(dados_jugador)
        else:
            cantidad_dados_jugador = dados_jugador
        
        if isinstance(todos_los_dados, list):
            total_dados = len(todos_los_dados)
        else:
            total_dados = todos_los_dados
        
        if cantidad_dados_jugador == 1:
            return True
        
        mitad_dados = total_dados / 2.0
        return cantidad_dados_jugador >= mitad_dados
    
    def calzar_con_validacion(self, apuesta, todos_los_dados, jugador_calzador, modo_especial=False):
        if not self.validar_condiciones_calzar(todos_los_dados, jugador_calzador):
            raise ValueError("No se puede calzar: condiciones no cumplidas")
        
        return self.determinar_resultado_calzar(apuesta, todos_los_dados, jugador_calzador, modo_especial)
