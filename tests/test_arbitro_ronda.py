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

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_calzar_exacto_jugador_gana_dado(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 3
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        dados = [Mock(valor=4)] * 10
        
        resultado = arbitro.determinar_resultado_calzar((3, 4), dados, jugador_calzador)
        
        assert resultado['jugador_ganador'] == jugador_calzador
        assert resultado['razon'] == 'calzar_exacto'
        assert resultado['pintas_encontradas'] == 3

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_calzar_inexacto_jugador_pierde_dado(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 2
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        dados = [Mock(valor=5)] * 8
        
        resultado = arbitro.determinar_resultado_calzar((3, 5), dados, jugador_calzador)
        
        assert resultado['jugador_perdedor'] == jugador_calzador
        assert resultado['razon'] == 'calzar_inexacto'
        assert resultado['pintas_encontradas'] == 2

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_calzar_ases_sin_comodines(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 1
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        dados = [Mock(valor=1)] * 6
        
        arbitro.determinar_resultado_calzar((1, 1), dados, Mock())
        
        mock_contador.contar_pinta.assert_called_once_with(dados, 1, ases_comodines=False)

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_calzar_modo_especial_ases_no_comodines(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 1
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        dados = [Mock(valor=3), Mock(valor=1)]
        
        arbitro.determinar_resultado_calzar((1, 3), dados, Mock(), modo_especial=True)
        
        mock_contador.contar_pinta.assert_called_once_with(dados, 3, ases_comodines=True, modo_especial=True)

    def test_calzar_permitido_con_un_dado(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()]
        dados_totales = [Mock()] * 10
        
        resultado = arbitro.validar_puede_calzar(dados_totales, jugador_calzador)
        
        assert resultado is True

    def test_calzar_permitido_con_mitad_dados(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()] * 2
        dados_totales = [Mock()] * 4
        
        resultado = arbitro.validar_puede_calzar(dados_totales, jugador_calzador)
        
        assert resultado is True

    def test_calzar_no_permitido_dados_insuficientes(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()] * 2
        dados_totales = [Mock()] * 8
        
        resultado = arbitro.validar_puede_calzar(dados_totales, jugador_calzador)
        
        assert resultado is False

    def test_calzar_validacion_pinta_invalida(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        
        with pytest.raises(ValueError, match="Pinta debe estar entre 1 y 6"):
            arbitro.determinar_resultado_calzar((2, 0), [Mock()], Mock())

    def test_calzar_validacion_cantidad_invalida(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        
        with pytest.raises(ValueError, match="Cantidad debe ser mayor a 0"):
            arbitro.determinar_resultado_calzar((-1, 3), [Mock()], Mock())

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_aplicar_resultado_duda_jugador_que_duda_pierde_dado(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 3
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        jugador_que_duda = Mock()
        jugador_que_duda.cacho.perder_dado = Mock()
        dados = [Mock(valor=3)] * 5
        
        arbitro.aplicar_resultado_duda((3, 3), dados, jugador_apostador, jugador_que_duda)
        
        jugador_que_duda.cacho.perder_dado.assert_called_once()

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_aplicar_resultado_duda_jugador_apostador_pierde_dado(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 1
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        jugador_apostador.cacho.perder_dado = Mock()
        jugador_que_duda = Mock()
        dados = [Mock(valor=5)] * 5
        
        arbitro.aplicar_resultado_duda((3, 5), dados, jugador_apostador, jugador_que_duda)
        
        jugador_apostador.cacho.perder_dado.assert_called_once()

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_aplicar_resultado_calzar_exacto_jugador_gana_dado(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 2
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.ganar_dado = Mock()
        dados = [Mock(valor=4)] * 8
        
        arbitro.aplicar_resultado_calzar((2, 4), dados, jugador_calzador)
        
        jugador_calzador.cacho.ganar_dado.assert_called_once()

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_aplicar_resultado_calzar_inexacto_jugador_pierde_dado(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 1
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.perder_dado = Mock()
        dados = [Mock(valor=6)] * 6
        
        arbitro.aplicar_resultado_calzar((3, 6), dados, jugador_calzador)
        
        jugador_calzador.cacho.perder_dado.assert_called_once()

    def test_determinar_siguiente_jugador_perdedor_inicia(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_perdedor = Mock()
        jugador_ganador = Mock()
        
        siguiente = arbitro.determinar_siguiente_jugador({'jugador_perdedor': jugador_perdedor})
        
        assert siguiente == jugador_perdedor

    def test_determinar_siguiente_jugador_ganador_inicia(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_ganador = Mock()
        
        siguiente = arbitro.determinar_siguiente_jugador({'jugador_ganador': jugador_ganador})
        
        assert siguiente == jugador_ganador

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_procesar_duda_completa_con_aplicacion(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 2
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_apostador = Mock()
        jugador_apostador.cacho.perder_dado = Mock()
        jugador_que_duda = Mock()
        dados = [Mock(valor=3)] * 5
        
        resultado = arbitro.procesar_duda_completa((3, 3), dados, jugador_apostador, jugador_que_duda)
        
        assert resultado['siguiente_jugador'] == jugador_apostador
        jugador_apostador.cacho.perder_dado.assert_called_once()

    @patch('src.juego.arbitro_ronda.ContadorPintas')
    def test_procesar_calzar_completo_con_aplicacion(self, mock_contador_class):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        mock_contador = Mock()
        mock_contador.contar_pinta.return_value = 2
        mock_contador_class.return_value = mock_contador
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.ganar_dado = Mock()
        dados = [Mock(valor=5)] * 6
        
        resultado = arbitro.procesar_calzar_completo((2, 5), dados, jugador_calzador)
        
        assert resultado['siguiente_jugador'] == jugador_calzador
        jugador_calzador.cacho.ganar_dado.assert_called_once()

    def test_validar_jugador_puede_continuar_con_dados(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador = Mock()
        jugador.cacho.dados = [Mock(), Mock()]
        
        resultado = arbitro.validar_jugador_puede_continuar(jugador)
        
        assert resultado is True

    def test_validar_jugador_no_puede_continuar_sin_dados(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador = Mock()
        jugador.cacho.dados = []
        
        resultado = arbitro.validar_jugador_puede_continuar(jugador)
        
        assert resultado is False

    def test_validar_condiciones_calzar_un_dado_permitido(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()]  # 1 dado
        todos_los_dados = [Mock()] * 15  # 15 dados totales en mesa
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, jugador_calzador)
        
        assert resultado is True

    def test_validar_condiciones_calzar_mitad_exacta_permitido(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        todos_los_dados = [Mock()] * 10  # 10 dados totales
        # Jugador tiene 5 dados (mitad exacta)
        dados_jugador = [Mock()] * 5
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, dados_jugador)
        
        assert resultado is True

    def test_validar_condiciones_calzar_mas_de_mitad_permitido(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        todos_los_dados = [Mock()] * 8  # 8 dados totales
        # Jugador tiene 5 dados (más de la mitad)
        dados_jugador = [Mock()] * 5
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, dados_jugador)
        
        assert resultado is True

    def test_validar_condiciones_calzar_menos_de_mitad_no_permitido(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        todos_los_dados = [Mock()] * 10  # 10 dados totales
        # Jugador tiene 3 dados (menos de la mitad)
        dados_jugador = [Mock()] * 3
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, dados_jugador)
        
        assert resultado is False

    def test_validar_condiciones_calzar_dos_dados_pocos_no_permitido(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        todos_los_dados = [Mock()] * 12  # 12 dados totales
        # Jugador tiene 2 dados (menos de la mitad y no es 1)
        dados_jugador = [Mock()] * 2
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, dados_jugador)
        
        assert resultado is False

    def test_validar_condiciones_calzar_caso_limite_mitad_impar(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        todos_los_dados = [Mock()] * 9  # 9 dados totales
        # Jugador tiene 5 dados (más de 4.5, que es la mitad)
        dados_jugador = [Mock()] * 5
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, dados_jugador)
        
        assert resultado is True

    def test_validar_condiciones_calzar_caso_limite_mitad_impar_insuficiente(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        todos_los_dados = [Mock()] * 9  # 9 dados totales
        # Jugador tiene 4 dados (menos de 4.5, que es la mitad)
        dados_jugador = [Mock()] * 4
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, dados_jugador)
        
        assert resultado is False

    def test_validar_condiciones_calzar_con_jugador_mock_object(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()] * 6
        todos_los_dados = [Mock()] * 10  # 10 dados totales
        
        resultado = arbitro.validar_condiciones_calzar(todos_los_dados, jugador_calzador)
        
        assert resultado is True

    def test_validar_condiciones_calzar_escenario_multijugador(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        # Escenario: 4 jugadores, cada uno con diferentes cantidades de dados
        jugador1_dados = [Mock()] * 5  # Puede calzar (más de mitad de 8)
        jugador2_dados = [Mock()] * 2  # No puede calzar (menos de mitad)
        jugador3_dados = [Mock()] * 1  # Puede calzar (regla de 1 dado)
        todos_los_dados = jugador1_dados + jugador2_dados + jugador3_dados
        
        resultado1 = arbitro.validar_condiciones_calzar(todos_los_dados, jugador1_dados)
        resultado2 = arbitro.validar_condiciones_calzar(todos_los_dados, jugador2_dados)
        resultado3 = arbitro.validar_condiciones_calzar(todos_los_dados, jugador3_dados)
        
        assert resultado1 is True   # 5 dados > mitad de 8
        assert resultado2 is False  # 2 dados < mitad de 8
        assert resultado3 is True   # 1 dado (regla especial)

    def test_intentar_calzar_sin_condiciones_lanza_excepcion(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()] * 2  # Insuficientes dados
        todos_los_dados = [Mock()] * 10
        
        with pytest.raises(ValueError, match="No se puede calzar: condiciones no cumplidas"):
            arbitro.calzar_con_validacion((2, 3), todos_los_dados, jugador_calzador)

    def test_calzar_con_validacion_exitoso_un_dado(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()]  # 1 dado
        jugador_calzador.cacho.ganar_dado = Mock()
        todos_los_dados = [Mock(valor=4)] * 8
        
        with patch.object(arbitro, 'contador_pintas') as mock_contador:
            mock_contador.contar_pinta.return_value = 2
            resultado = arbitro.calzar_con_validacion((2, 4), todos_los_dados, jugador_calzador)
        
        assert resultado['jugador_ganador'] == jugador_calzador

    def test_calzar_con_validacion_exitoso_mitad_dados(self):
        from src.juego.arbitro_ronda import ArbitroRonda
        
        arbitro = ArbitroRonda()
        jugador_calzador = Mock()
        jugador_calzador.cacho.dados = [Mock()] * 4  # 4 de 8 dados (mitad)
        jugador_calzador.cacho.ganar_dado = Mock()
        todos_los_dados = [Mock(valor=5)] * 8
        
        with patch.object(arbitro, 'contador_pintas') as mock_contador:
            mock_contador.contar_pinta.return_value = 1
            resultado = arbitro.calzar_con_validacion((1, 5), todos_los_dados, jugador_calzador)
        
        assert resultado['jugador_ganador'] == jugador_calzador