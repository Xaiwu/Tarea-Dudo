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

# Tests para reglas especiales de Ases (pinta 1)
def test_cambio_a_ases_cantidad_par():
    """Test cambio a Ases con cantidad par: dividir por 2 y sumar 1"""
    validador = ValidadorApuesta()
    # 4 trenes -> 3 ases (4/2 = 2, par entonces +1 = 3)
    assert validador.es_apuesta_valida((4, 3), (3, 1)) == True
    # 6 cuadras -> 4 ases (6/2 = 3, par entonces +1 = 4)
    assert validador.es_apuesta_valida((6, 4), (4, 1)) == True
    # 8 sextos -> 5 ases (8/2 = 4, par entonces +1 = 5)
    assert validador.es_apuesta_valida((8, 6), (5, 1)) == True

def test_cambio_a_ases_cantidad_impar():
    """Test cambio a Ases con cantidad impar: dividir por 2 y redondear arriba"""
    validador = ValidadorApuesta()
    # 3 trenes -> 2 ases (3/2 = 1.5, redondear arriba = 2)
    assert validador.es_apuesta_valida((3, 3), (2, 1)) == True
    # 5 cuadras -> 3 ases (5/2 = 2.5, redondear arriba = 3)
    assert validador.es_apuesta_valida((5, 4), (3, 1)) == True
    # 7 sextos -> 4 ases (7/2 = 3.5, redondear arriba = 4)
    assert validador.es_apuesta_valida((7, 6), (4, 1)) == True

def test_cambio_a_ases_cantidad_invalida():
    """Test que no se puede cambiar a Ases con cantidad incorrecta"""
    validador = ValidadorApuesta()
    # 4 trenes -> 2 ases (debería ser 3, no 2)
    assert validador.es_apuesta_valida((4, 3), (2, 1)) == False
    # 4 trenes -> 4 ases (debería ser 3, no 4)
    assert validador.es_apuesta_valida((4, 3), (4, 1)) == False
    # 5 cuadras -> 2 ases (debería ser 3, no 2)
    assert validador.es_apuesta_valida((5, 4), (2, 1)) == False

def test_cambio_de_ases_multiplicar_por_2_mas_1():
    """Test cambio de Ases a otra pinta: multiplicar por 2 y sumar 1"""
    validador = ValidadorApuesta()
    # 2 ases -> 5 trenes (2*2+1 = 5)
    assert validador.es_apuesta_valida((2, 1), (5, 3)) == True
    # 3 ases -> 7 cuadras (3*2+1 = 7)
    assert validador.es_apuesta_valida((3, 1), (7, 4)) == True
    # 4 ases -> 9 sextos (4*2+1 = 9)
    assert validador.es_apuesta_valida((4, 1), (9, 6)) == True

def test_cambio_de_ases_cantidad_minima_requerida():
    """Test que se requiere cantidad mínima al cambiar de Ases"""
    validador = ValidadorApuesta()
    # 2 ases -> 4 trenes (debería ser mínimo 5, no 4)
    assert validador.es_apuesta_valida((2, 1), (4, 3)) == False
    # 3 ases -> 6 cuadras (debería ser mínimo 7, no 6)
    assert validador.es_apuesta_valida((3, 1), (6, 4)) == False
    # 4 ases -> 8 sextos (debería ser mínimo 9, no 8)
    assert validador.es_apuesta_valida((4, 1), (8, 6)) == False

def test_cambio_de_ases_cantidad_mayor_valida():
    """Test que se puede apostar más de la cantidad mínima al cambiar de Ases"""
    validador = ValidadorApuesta()
    # 2 ases -> 6 trenes (mínimo 5, pero 6 también es válido)
    assert validador.es_apuesta_valida((2, 1), (6, 3)) == True
    # 3 ases -> 8 cuadras (mínimo 7, pero 8 también es válido)
    assert validador.es_apuesta_valida((3, 1), (8, 4)) == True

def test_ases_casos_borde():
    """Test casos borde con las reglas especiales de Ases"""
    validador = ValidadorApuesta()
    # Cantidad mínima: 1 as
    # 2 trenes -> 1 as (2/2 = 1, par entonces +1 = 2, pero mínimo es 1)
    assert validador.es_apuesta_valida((2, 3), (1, 1)) == True
    # 1 as -> 3 trenes (1*2+1 = 3)
    assert validador.es_apuesta_valida((1, 1), (3, 3)) == True