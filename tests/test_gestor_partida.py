import pytest
from src.juego.gestor_partida import GestorPartida

@pytest.mark.parametrize("num_jugadores,id_jugador", [(2, 1), (3, 2)])
def test_gestor_partida_jugadores(num_jugadores,id_jugador):
    gestor = GestorPartida(num_jugadores)
    assert len(gestor.jugadores) == num_jugadores

    gestor.jugadores[id_jugador].perder_dado()
    assert len(gestor.jugadores[id_jugador].dados) == 4

    gestor.jugadores[id_jugador].ganar_dado()
    assert len(gestor.jugadores[id_jugador].dados) == 5


def test_gestor_partida_iniciador():
    gestor = GestorPartida(3)
   
    valores = [3, 6, 2]
    for jugador, valor in zip(gestor.jugadores, valores):
        jugador.dados[0].valor = valor
    
    assert gestor.determinar_iniciador() == gestor.jugadores[1]

def test_gestor_partida_iniciador_con_empate(mocker):
    gestor = GestorPartida(5)
    for jugador in gestor.jugadores:
        jugador.dados[0].valor = 5 

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