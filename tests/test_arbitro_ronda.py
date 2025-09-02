import pytest
from unittest.mock import Mock, patch
from src.juego.contador_pintas import ContadorPintas


class TestArbitroRonda:
    
    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_duda_apuesta_correcta_jugador_que_duda_pierde(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 3
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        jugador_que_duda = Mock()
        dados = [Mock(valor=3)] * 5
        
        resultado = arbitro.determinar_resultado_duda((3, 3), dados, jugador_apostador, jugador_que_duda)
        
        assert resultado['jugador_perdedor'] == jugador_que_duda
        assert resultado['razon'] == 'apuesta_correcta'
        mock_contador.contar_pinta.assert_called_once_with(dados, 3, ases_comodines=True)

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_duda_apuesta_correcta_con_exceso_jugador_que_duda_pierde(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 5
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        jugador_que_duda = Mock()
        dados = [Mock(valor=4)] * 5
        
        resultado = arbitro.determinar_resultado_duda((2, 4), dados, jugador_apostador, jugador_que_duda)
        
        assert resultado['jugador_perdedor'] == jugador_que_duda
        assert resultado['razon'] == 'apuesta_correcta'

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_duda_apuesta_incorrecta_jugador_apostador_pierde(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 1
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        jugador_que_duda = Mock()
        dados = [Mock(valor=i) for i in range(1, 6)]
        
        resultado = arbitro.determinar_resultado_duda((4, 5), dados, jugador_apostador, jugador_que_duda)
        
        assert resultado['jugador_perdedor'] == jugador_apostador
        assert resultado['razon'] == 'apuesta_incorrecta'

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_duda_apuesta_ases_usa_comodines_false(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 2
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        dados = [Mock(valor=1), Mock(valor=1), Mock(valor=3)]
        
        arbitro.determinar_resultado_duda((2, 1), dados, Mock(), Mock())
        
        mock_contador.contar_pinta.assert_called_once_with(dados, 1, ases_comodines=False)

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_duda_modo_especial_ases_no_comodines(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 1
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        dados = [Mock(valor=3), Mock(valor=1)]
        
        resultado = arbitro.determinar_resultado_duda(
            (2, 3), dados, Mock(), Mock(), modo_especial=True
        )
        
        assert resultado['jugador_perdedor'] is not None
        mock_contador.contar_pinta.assert_called_once_with(dados, 3, ases_comodines=True, modo_especial=True)

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_duda_cero_pintas_apostador_pierde(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 0
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        dados = [Mock(valor=i) for i in range(1, 6)]
        
        resultado = arbitro.determinar_resultado_duda((1, 6), dados, jugador_apostador, Mock())
        
        assert resultado['jugador_perdedor'] == jugador_apostador
        assert resultado['razon'] == 'apuesta_incorrecta'

    def test_validacion_pinta_invalida(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        
        with pytest.raises(ValueError, match="Pinta debe estar entre 1 y 6"):
            arbitro.determinar_resultado_duda((2, 7), [Mock()], Mock(), Mock())

    def test_validacion_cantidad_invalida(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        
        with pytest.raises(ValueError, match="Cantidad debe ser mayor a 0"):
            arbitro.determinar_resultado_duda((0, 3), [Mock()], Mock(), Mock())

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_resultado_incluye_informacion_completa(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 2
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        dados = [Mock(valor=3)] * 3
        apuesta = (3, 3)
        
        resultado = arbitro.determinar_resultado_duda(apuesta, dados, jugador_apostador, Mock())
        
        assert 'jugador_perdedor' in resultado
        assert 'razon' in resultado
        assert 'pintas_encontradas' in resultado
        assert 'apuesta_original' in resultado
        assert resultado['pintas_encontradas'] == 2
        assert resultado['apuesta_original'] == apuesta