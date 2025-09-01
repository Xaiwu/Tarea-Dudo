import pytest
from src.juego.gestor_partida import GestorPartida

@pytest.mark.parametrize("num_jugadores", [2, 3, 4])
def test_gestor_partida_jugadores(num_jugadores):
    gestor = GestorPartida(num_jugadores)
    assert len(gestor.jugadores) == num_jugadores