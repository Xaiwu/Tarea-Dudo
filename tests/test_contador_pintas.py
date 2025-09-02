import pytest
from unittest.mock import Mock
from src.juego.contador_pintas import ContadorPintas
from src.juego.Dado import Dado


class TestContadorPintas:
    
    def test_contar_pintas_sin_dados(self):
        """Test que el contador funciona con una lista vacía de dados"""
        contador = ContadorPintas()
        dados = []
        
        resultado = contador.contar_pinta(dados, 3)
        
        assert resultado == 0

    def test_contar_pintas_basico(self):
        """Test conteo básico de apariciones de una pinta específica"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=3),  # Tren
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
            Mock(valor=6),  # Sexto
        ]
        
        resultado = contador.contar_pinta(dados, 3)  # Contar Trenes
        
        assert resultado == 2

    def test_contar_pintas_diferentes_valores(self):
        """Test conteo para diferentes valores de pintas"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=2),  # Tonto
            Mock(valor=2),  # Tonto
            Mock(valor=4),  # Cuadra
            Mock(valor=6),  # Sexto
            Mock(valor=6),  # Sexto
        ]
        
        # Contar Tontos (pinta 2)
        assert contador.contar_pinta(dados, 2) == 2
        
        # Contar Cuadras (pinta 4)
        assert contador.contar_pinta(dados, 4) == 1
        
        # Contar Sextos (pinta 6)
        assert contador.contar_pinta(dados, 6) == 2
        
        # Contar Trenes (pinta 3) - no hay ninguno
        assert contador.contar_pinta(dados, 3) == 0

    def test_pinta_invalida(self):
        """Test que se maneja correctamente una pinta inválida"""
        contador = ContadorPintas()
        dados = [Mock(valor=3), Mock(valor=4)]
        
        with pytest.raises(ValueError, match="La pinta debe estar entre 1 y 6"):
            contador.contar_pinta(dados, 0)
        
        with pytest.raises(ValueError, match="La pinta debe estar entre 1 y 6"):
            contador.contar_pinta(dados, 7)

    def test_contar_con_dados_reales(self):
        """Test integración con objetos Dado reales (con valores deterministas)"""
        contador = ContadorPintas()
        # Usar constructor con valores específicos para hacer el test determinista
        dados = [
            Dado(3),  # Tren
            Dado(3),  # Tren
            Dado(1),  # As
            Dado(5),  # Quina
        ]
        
        resultado = contador.contar_pinta(dados, 3)  # Contar Trenes
        
        assert resultado == 2

    def test_contar_dados_desde_multiples_jugadores(self):
        """Test simulando el conteo de dados de múltiples jugadores"""
        contador = ContadorPintas()
        
        # Simular dados de 3 jugadores
        dados_jugador1 = [Mock(valor=2), Mock(valor=3), Mock(valor=3)]  # Tonto, Tren, Tren
        dados_jugador2 = [Mock(valor=3), Mock(valor=4)]  # Tren, Cuadra
        dados_jugador3 = [Mock(valor=1), Mock(valor=3), Mock(valor=5), Mock(valor=6)]  # As, Tren, Quina, Sexto
        
        # Combinar todos los dados
        todos_los_dados = dados_jugador1 + dados_jugador2 + dados_jugador3
        
        resultado = contador.contar_pinta(todos_los_dados, 3)  # Contar Trenes
        
        assert resultado == 4  # 4 Trenes reales

    # Tests para Ases como comodines
    def test_contar_pintas_con_ases_comodines(self):
        """Test que los Ases (pinta 1) cuentan como comodines de la pinta buscada"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As (comodín)
            Mock(valor=1),  # As (comodín)
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
        ]
        
        resultado = contador.contar_pinta(dados, 3, ases_comodines=True)  # Contar Trenes con Ases como comodines
        
        assert resultado == 3  # 1 Tren real + 2 Ases comodines

    def test_contar_ases_directamente_con_comodines_activados(self):
        """Test contar Ases directamente cuando los comodines están activados (los Ases NO actúan como comodines de sí mismos)"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
        ]
        
        resultado = contador.contar_pinta(dados, 1, ases_comodines=True)  # Contar Ases
        
        assert resultado == 3  # Solo los Ases reales, no actúan como comodines de sí mismos

    def test_comparacion_modo_con_y_sin_comodines(self):
        """Test que compara explícitamente la diferencia entre usar Ases como comodines o no"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=4),  # Cuadra
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
        ]
        
        # Sin comodines: solo cuenta apariciones exactas
        resultado_sin_comodines = contador.contar_pinta(dados, 4, ases_comodines=False)
        
        # Con comodines: Ases suman a la pinta buscada
        resultado_con_comodines = contador.contar_pinta(dados, 4, ases_comodines=True)
        
        assert resultado_sin_comodines == 2  # Solo 2 Cuadras reales
        assert resultado_con_comodines == 4  # 2 Cuadras + 2 Ases comodines

    def test_contar_todos_ases_como_comodines(self):
        """Test cuando todos los dados son Ases y se usan como comodines"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=1),  # As
        ]
        
        # Contar Ases directamente (no actúan como comodines de sí mismos)
        assert contador.contar_pinta(dados, 1, ases_comodines=True) == 5
        
        # Contar otra pinta (todos los Ases actúan como comodines)
        assert contador.contar_pinta(dados, 4, ases_comodines=True) == 5

    def test_multiples_jugadores_con_ases_comodines(self):
        """Test simulando el conteo de dados de múltiples jugadores con Ases como comodines"""
        contador = ContadorPintas()
        
        # Simular dados de 3 jugadores
        dados_jugador1 = [Mock(valor=1), Mock(valor=2), Mock(valor=3)]  # As, Tonto, Tren
        dados_jugador2 = [Mock(valor=3), Mock(valor=4)]  # Tren, Cuadra
        dados_jugador3 = [Mock(valor=1), Mock(valor=3), Mock(valor=5), Mock(valor=6)]  # As, Tren, Quina, Sexto
        
        # Combinar todos los dados
        todos_los_dados = dados_jugador1 + dados_jugador2 + dados_jugador3
        
        resultado = contador.contar_pinta(todos_los_dados, 3, ases_comodines=True)  # Contar Trenes con comodines
        
        assert resultado == 5  # 3 Trenes reales + 2 Ases comodines