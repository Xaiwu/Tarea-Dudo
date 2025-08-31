from src.juego.Cacho import Cacho


def test_agitar_cacho():
    cacho = Cacho()
    valores = cacho.get_valores()
    cacho.agitar()
    nuevosVal = cacho.get_valores()
    assert nuevosVal != valores

def test_oculto_mostrar_cacho():
    cacho = Cacho([1,2,3,4,5])
    assert cacho.mostrar() == "X X X X X"
    cacho.revelar()
    assert cacho.mostrar() == "1 2 3 4 5"