from src.juego.Dado import Dado

def test_lanzamiento_dado():
    dado = Dado()

    valorDado = dado.lanzar()

    assert 1 <= valorDado <= 6