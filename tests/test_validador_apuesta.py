import pytest
from src.juego.validador_apuesta import ValidadorApuesta

def test_apuesta_valida_mayor_cantidad():
    """Test que una apuesta con mayor cantidad es válida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 3), (3, 3)) == True

def test_apuesta_valida_mayor_pinta():
    """Test que una apuesta con misma cantidad pero mayor pinta es válida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 2), (2, 3)) == True

def test_apuesta_invalida_menor_cantidad():
    """Test que una apuesta con menor cantidad es inválida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((3, 4), (2, 4)) == False

def test_apuesta_invalida_menor_pinta():
    """Test que una apuesta con misma cantidad pero menor pinta es inválida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 4), (2, 3)) == False

def test_apuesta_invalida_menor_cantidad_y_pinta():
    """Test que una apuesta con menor cantidad y menor pinta es inválida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((3, 5), (2, 4)) == False

def test_apuesta_invalida_igual_cantidad_y_pinta():
    """Test que una apuesta igual es inválida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 3), (2, 3)) == False

def test_primera_apuesta_siempre_valida():
    """Test que la primera apuesta (sin apuesta previa) siempre es válida"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida(None, (1, 1)) == True
    assert validador.es_apuesta_valida(None, (5, 6)) == True

def test_apuesta_valida_incremento_cantidad_pinta_menor():
    """Test que se puede incrementar cantidad aunque la pinta sea menor"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 6), (3, 1)) == True

def test_apuesta_valida_incremento_pinta_maxima():
    """Test validación con pintas en los extremos del rango"""
    validador = ValidadorApuesta()
    # De pinta 1 (As) a pinta 6 (Sexto) con misma cantidad
    assert validador.es_apuesta_valida((2, 1), (2, 6)) == True
    # De pinta 5 a pinta 6 con misma cantidad
    assert validador.es_apuesta_valida((2, 5), (2, 6)) == True

def test_apuesta_invalida_pinta_maxima_a_minima():
    """Test que no se puede bajar de pinta máxima a mínima con misma cantidad"""
    validador = ValidadorApuesta()
    assert validador.es_apuesta_valida((2, 6), (2, 1)) == False

def test_apuesta_valida_casos_borde():
    """Test casos borde con cantidades y pintas límite"""
    validador = ValidadorApuesta()
    # Cantidad mínima
    assert validador.es_apuesta_valida((1, 1), (1, 2)) == True
    assert validador.es_apuesta_valida((1, 1), (2, 1)) == True
    # Incrementos mínimos válidos
    assert validador.es_apuesta_valida((1, 1), (1, 2)) == True
    assert validador.es_apuesta_valida((1, 6), (2, 1)) == True