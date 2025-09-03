import pytest
from src.juego.gestor_partida import GestorPartida
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.arbitro_ronda import ArbitroRonda

@pytest.mark.parametrize("num_jugadores,id_jugador", [(2, 1), (3, 2)])
def test_gestor_partida_jugadores(num_jugadores,id_jugador):
    gestor = GestorPartida(num_jugadores)
    assert len(gestor.jugadores) == num_jugadores

    gestor.jugadores[id_jugador].cacho.perder_dado()
    assert len(gestor.jugadores[id_jugador].cacho.dados) == 4

    gestor.jugadores[id_jugador].cacho.ganar_dado()
    assert len(gestor.jugadores[id_jugador].cacho.dados) == 5


def test_gestor_partida_iniciador():
    gestor = GestorPartida(3)
   
    valores = [3, 6, 2]
    for jugador, valor in zip(gestor.jugadores, valores):
        jugador.cacho.dados[0].valor = valor

    assert gestor.determinar_iniciador() == gestor.jugadores[1]

def test_gestor_partida_iniciador_con_empate(mocker):
    gestor = GestorPartida(5)
    for jugador in gestor.jugadores:
        jugador.cacho.dados[0].valor = 5

    mocker.patch("random.randint", side_effect=[6, 2, 1, 2, 4])
    assert gestor.determinar_iniciador() == gestor.jugadores[0]


def test_gestor_partida_flujo_turnos(mocker):
    mocker.patch("random.randint", side_effect=[1, 4, 2, 1, 4, 6, 1, 4, 2, 1, 4, 2, 1, 4, 2])
    gestor = GestorPartida(3)

    gestor.determinar_iniciador()
    assert gestor.jugador_actual() == gestor.jugadores[1]

    
    gestor.siguiente_turno()
    assert gestor.jugador_actual() == gestor.jugadores[2]

    
    gestor.siguiente_turno()
    assert gestor.jugador_actual() == gestor.jugadores[0]

    
    gestor.siguiente_turno()
    assert gestor.jugador_actual() == gestor.jugadores[1]

def test_gestor_partida_jugador_un_dado():
    gestor = GestorPartida(3)

    while len(gestor.jugadores[1].cacho.dados) > 1:
        gestor.jugadores[1].cacho.perder_dado()
    jugadores_un_dado = gestor.jugadores_con_un_dado()
    assert jugadores_un_dado == [gestor.jugadores[1]]


def test_gestor_partida_activa_reglas_especiales():
    gestor = GestorPartida(3)

    while len(gestor.jugadores[1].cacho.dados) > 1:
        gestor.jugadores[1].cacho.perder_dado()

    gestor.activar_reglas_especiales()
    
    assert gestor.modo_especial is True
    assert gestor.jugadores[1].modo_obligado is True


def test_activar_y_finalizar_ronda_especial():
    gestor = GestorPartida(2)
    # Simula que el jugador 0 queda con un solo dado y activa modo obligado
    while len(gestor.jugadores[0].cacho.dados) > 1:
        gestor.jugadores[0].cacho.perder_dado()
    gestor.jugadores[0].modo_obligado = True
    gestor.modo_especial = True

    # Verifica que el modo especial está activo
    assert gestor.modo_especial is True
    assert gestor.jugadores[0].modo_obligado is True

    # Finaliza la ronda especial
    gestor.finalizar_ronda_especial()

    # Verifica que el modo especial y el modo obligado se desactivan
    assert gestor.modo_especial is False
    assert gestor.jugadores[0].modo_obligado is False
    assert gestor.jugadores[1].modo_obligado is False

def test_eliminar_jugadores_sin_dados_al_finalizar_ronda():
    gestor = GestorPartida(6)
    gestor.determinar_iniciador()
    
    gestor.jugadores[3].cacho.dados = []

    gestor.eliminar_jugadores_sin_dados()
    
    assert len(gestor.jugadores) == 5
    assert 0 <= gestor.turno_actual < len(gestor.jugadores)

    turno_inicial = gestor.turno_actual
    gestor.siguiente_turno()
    turno_final = gestor.turno_actual
    assert turno_final != turno_inicial

    gestor.eliminar_jugadores_sin_dados()
    assert len(gestor.jugadores) == 5


def test_simulacion_partida(mocker):
    # Mock para dados iniciales: 3 jugadores x 2 dados + extras
    mocker.patch("random.randint", side_effect=[
        1, 2, 5, 4, 3,   # Jugador 0
        6, 6, 6, 6, 6,   # Jugador 1
        2, 3, 3, 4, 3,   # Jugador 2
        4, 5, 6          # Extras para relanzar/ganar dado
    ])
    gestor = GestorPartida(3)
    for jugador in gestor.jugadores:
        jugador.cacho.dados = jugador.cacho.dados[:2]

    validador = ValidadorApuesta()
    arbitro = ArbitroRonda()

    # Primera ronda 
    iniciador = gestor.determinar_iniciador()
    assert iniciador == gestor.jugadores[1]
    assert gestor.turno_actual == 1

    apuesta_actual = (1, 2)
    assert validador.es_apuesta_valida(None, apuesta_actual, len(gestor.jugador_actual().cacho.dados))
    gestor.apuesta_actual = apuesta_actual
    gestor.siguiente_turno()

    nueva_apuesta = (2, 2)
    assert validador.es_apuesta_valida(apuesta_actual, nueva_apuesta, len(gestor.jugador_actual().cacho.dados))
    gestor.apuesta_actual = nueva_apuesta
    gestor.siguiente_turno()
    assert gestor.turno_actual == 0

    todos_los_dados = []
    for jugador in gestor.jugadores:
        todos_los_dados.extend(jugador.cacho.dados)
    resultado = arbitro.determinar_resultado_duda(
        gestor.apuesta_actual,
        todos_los_dados,
        gestor.jugadores[2],
        gestor.jugadores[0],
        modo_especial=gestor.modo_especial
    )
    perdedor = resultado['jugador_perdedor']
    perdedor.cacho.perder_dado()
    gestor.apuesta_actual = None

    # Elimina jugadores sin dados y asigna el turno al perdedor
    gestor.eliminar_jugadores_sin_dados(perdedor)
    assert len(gestor.jugadores) == 3
    if perdedor in gestor.jugadores:
        assert gestor.jugadores[gestor.turno_actual] == perdedor
    else:
        assert gestor.turno_actual == 0

    # Segunda ronda - Simulo directamente que perdió nuevamente
    perdedor.cacho.perder_dado()
    assert len(perdedor.cacho.dados) == 0

    gestor.eliminar_jugadores_sin_dados(perdedor)
    assert len(gestor.jugadores) == 2


    # El turno continúa con los jugadores restantes
    turno_inicial = gestor.turno_actual
    gestor.siguiente_turno()
    turno_final = gestor.turno_actual
    assert turno_final != turno_inicial

    # Verifica que el juego detecta ganador cuando solo queda uno
    gestor.jugadores[0].cacho.dados = []
    gestor.eliminar_jugadores_sin_dados()
    assert len(gestor.jugadores) == 1