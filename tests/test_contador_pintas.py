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

    def test_contar_pintas_con_ases_mixtos(self):
        """Test conteo con Ases y pintas específicas mezcladas"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As (comodín)
            Mock(valor=5),  # Quina
            Mock(valor=1),  # As (comodín)
            Mock(valor=5),  # Quina
            Mock(valor=2),  # Tonto
        ]
        
        resultado = contador.contar_pinta(dados, 5, ases_comodines=True)  # Contar Quinas
        
        assert resultado == 4  # 2 Quinas reales + 2 Ases comodines

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

    def test_contar_sin_ases_con_comodines_activados(self):
        """Test que cuando no hay Ases, el comportamiento es igual con o sin comodines"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=2),  # Tonto
            Mock(valor=3),  # Tren
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=6),  # Sexto
        ]
        
        # Sin Ases, debería contar igual independiente del flag de comodines
        resultado_sin_comodines = contador.contar_pinta(dados, 3, ases_comodines=False)
        resultado_con_comodines = contador.contar_pinta(dados, 3, ases_comodines=True)
        
        assert resultado_sin_comodines == resultado_con_comodines == 2

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

    def test_ases_no_afectan_otras_pintas_sin_comodines(self):
        """Test que los Ases no afectan el conteo de otras pintas cuando los comodines están desactivados"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As (NO comodín)
            Mock(valor=1),  # As (NO comodín)
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
        ]
        
        resultado = contador.contar_pinta(dados, 3, ases_comodines=False)  # Contar Trenes sin comodines
        
        assert resultado == 1  # Solo 1 Tren real, Ases NO cuentan

    def test_contar_con_dados_reales_y_comodines(self):
        """Test integración con objetos Dado reales usando Ases como comodines"""
        contador = ContadorPintas()
        dados = [
            Dado(1),  # As (comodín)
            Dado(3),  # Tren
            Dado(3),  # Tren
            Dado(1),  # As (comodín)
            Dado(5),  # Quina
        ]
        
        resultado = contador.contar_pinta(dados, 3, ases_comodines=True)  # Contar Trenes con comodines
        
        assert resultado == 4  # 2 Trenes + 2 Ases comodines

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

    def test_parametro_por_defecto_ases_comodines(self):
        """Test que el parámetro ases_comodines tiene un valor por defecto apropiado"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=4),  # Cuadra
            Mock(valor=4),  # Cuadra
        ]
        
        # Sin especificar el parámetro, debería comportarse consistentemente
        resultado_default = contador.contar_pinta(dados, 4)
        resultado_explicito = contador.contar_pinta(dados, 4, ases_comodines=False)
        
        assert resultado_default == resultado_explicito == 2  # Por defecto NO usa comodines

    def test_edge_case_solo_ases_buscando_otras_pintas(self):
        """Test caso extremo: solo hay Ases y se busca otra pinta"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As
            Mock(valor=1),  # As
            Mock(valor=1),  # As
        ]
        
        # Sin comodines: no encuentra nada
        resultado_sin_comodines = contador.contar_pinta(dados, 6, ases_comodines=False)
        
        # Con comodines: todos los Ases cuentan
        resultado_con_comodines = contador.contar_pinta(dados, 6, ases_comodines=True)
        
        assert resultado_sin_comodines == 0
        assert resultado_con_comodines == 3

    def test_todas_las_pintas_con_comodines(self):
        """Test que los Ases funcionan como comodines para todas las pintas 2-6"""
        contador = ContadorPintas()
        dados = [
            Mock(valor=1),  # As (comodín)
            Mock(valor=1),  # As (comodín)
            Mock(valor=3),  # Tren
            Mock(valor=4),  # Cuadra
            Mock(valor=5),  # Quina
        ]
        
        # Para pintas 2-6, los Ases deben sumar como comodines
        for pinta in range(2, 7):
            if pinta == 3:
                assert contador.contar_pinta(dados, pinta, ases_comodines=True) == 3  # 1 real + 2 Ases
            elif pinta in [4, 5]:
                assert contador.contar_pinta(dados, pinta, ases_comodines=True) == 3  # 1 real + 2 Ases
            else:  # pinta 2 o 6
                assert contador.contar_pinta(dados, pinta, ases_comodines=True) == 2  # 0 reales + 2 Ases
        
        # Para As (pinta 1), no actúan como comodines de sí mismos
        assert contador.contar_pinta(dados, 1, ases_comodines=True) == 2  # Solo Ases reales