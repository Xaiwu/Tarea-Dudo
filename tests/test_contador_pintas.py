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

    def test_contar_ases_como_pinta_normal(self):
        """Test contar Ases como una pinta normal (sin funcionalidad de comodín)"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
        ]
        
        resultado = contador.contar_pinta(dados, 1)  # Contar Ases
        
        assert resultado == 3

    def test_contar_sin_coincidencias(self):
        """Test cuando no hay coincidencias de la pinta buscada"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=2),  # Tonto
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
            Mock(valor=6),  # Sexto
        ]
        
        resultado = contador.contar_pinta(dados, 1)  # Buscar Ases
        
        assert resultado == 0

    def test_pinta_invalida(self):
        """Test que se maneja correctamente una pinta inválida"""
        contador = ContadorPintas()
        dados = [Mock(valor=3), Mock(valor=4)]
        
        with pytest.raises(ValueError, match="La pinta debe estar entre 1 y 6"):
            contador.contar_pinta(dados, 0)
        
        with pytest.raises(ValueError, match="La pinta debe estar entre 1 y 6"):
            contador.contar_pinta(dados, 7)

    def test_contar_con_dados_reales(self):
        """Test integración con objetos Dado reales"""
        contador = ContadorPintas()
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

    def test_edge_case_todos_dados_misma_pinta(self):
        """Test caso extremo donde todos los dados tienen la misma pinta buscada"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=6),  # Sexto
            Mock(valor=6),  # Sexto
            Mock(valor=6),  # Sexto
            Mock(valor=6),  # Sexto
            Mock(valor=6),  # Sexto
        ]
        
        resultado = contador.contar_pinta(dados, 6)  # Contar Sextos
        
        assert resultado == 5

    def test_edge_case_un_solo_dado(self):
        """Test caso extremo con un solo dado"""
        contador = ContadorPintas()
        
        # Un As
        dados_as = [Mock(valor=1)]
        assert contador.contar_pinta(dados_as, 1) == 1  # Contar el As
        assert contador.contar_pinta(dados_as, 4) == 0  # No hay Cuadras
        
        # Un dado normal
        dados_normal = [Mock(valor=3)]
        assert contador.contar_pinta(dados_normal, 3) == 1  # Contar el Tren
        assert contador.contar_pinta(dados_normal, 4) == 0  # No hay Cuadras

    def test_todas_las_pintas(self):
        """Test que funciona correctamente para todas las pintas del 1 al 6"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=2),  # Tonto
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
            Mock(valor=6),  # Sexto
        ]
        
        # Verificar que cuenta correctamente cada pinta
        for pinta in range(1, 7):
            resultado = contador.contar_pinta(dados, pinta)
            assert resultado == 1  # Cada pinta aparece exactamente una vez