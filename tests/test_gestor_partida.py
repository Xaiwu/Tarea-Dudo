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