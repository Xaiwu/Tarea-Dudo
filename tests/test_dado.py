import pytest
from src.juego.Dado import Dado

def test_lanzamiento_dado():
    dado = Dado()

    valorDado = dado.lanzar()

    assert 1 <= valorDado <= 6

@pytest.mark.parametrize("valor, esperado", [(1, "As"), (2, "Tonto"), (3, "Tren"), (4, "Cuadra"), (5, "Quina"), (6, "Sexto")])
def test_denominacion(valor, esperado):
    dado = Dado(valor)
    resultado = dado.get_denominacion()
    assert resultado == esperado
