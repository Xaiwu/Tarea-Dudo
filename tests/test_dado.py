import pytest
from src.juego.Dado import Dado

def test_lanzamiento_dado(mocker):
    mocker.patch("random.randint", return_value=4)
    dado = Dado()
    valorDado = dado.lanzar()
    assert valorDado == 4

@pytest.mark.parametrize("valor, esperado", [(1, "As"), (2, "Tonto"), (3, "Tren"), (4, "Cuadra"), (5, "Quina"), (6, "Sexto")])
def test_denominacion(valor, esperado):
    dado = Dado(valor)
    resultado = dado.get_denominacion()
    assert resultado == esperado

def test_dado_valor_fuera_de_rango():
    with pytest.raises(ValueError):
        Dado(0)
    with pytest.raises(ValueError):
        Dado(7)
