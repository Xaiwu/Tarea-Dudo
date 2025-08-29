import pytest
from src.juego.validador_apuesta import ValidadorApuesta

def test_apuesta_valida_mayor_cantidad():
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 3), (3, 3)) == True

def test_apuesta_valida_mayor_pinta():
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 2), (2, 3)) == True