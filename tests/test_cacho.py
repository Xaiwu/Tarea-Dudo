from src.juego.Cacho import Cacho


def test_agitar_cacho():
    cacho = Cacho()
    valores = cacho.get_valores()
    cacho.agitar()
    nuevosVal = cacho.get_valores()
    assert nuevosVal != valores
