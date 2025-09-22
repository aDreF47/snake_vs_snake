import pytest
from core.interfaces import TABLERO_TAMANO, AZUL, ROJO, VACIO, Posicion
from core.juego import MotorJuego


def test_inicializacion_motor():
    """Prueba la creación del motor de juego"""
    juego = MotorJuego()
    assert not juego.estado_actual
    assert not juego.juego_terminado
    assert not juego.ganador


def test_inicializacion_juego():
    """Prueba la inicialización del juego"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)
    estado = juego.obtener_estado_actual()

    # Verificar estado inicial
    assert estado is not None
    assert estado.turno == AZUL
    assert len(estado.tablero) == TABLERO_TAMANO
    assert all(len(fila) == TABLERO_TAMANO for fila in estado.tablero)

    # Verificar que el tablero esté vacío
    assert all(
        estado.tablero[y][x] == VACIO
        for y in range(TABLERO_TAMANO)
        for x in range(TABLERO_TAMANO)
    )


def test_primer_movimiento():
    """Prueba la validez del primer movimiento"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Intento de movimiento inválido (fuera del tablero)
    resultado = juego.realizar_movimiento(Posicion(-1, 0))
    assert not resultado.es_valido

    # Movimiento válido
    resultado = juego.realizar_movimiento(Posicion(3, 3))
    assert resultado.es_valido

    estado = juego.obtener_estado_actual()
    assert estado.tablero[3][3] == AZUL
    assert estado.cabeza_azul == Posicion(3, 3)
    assert estado.turno == ROJO


def test_movimientos_adyacentes():
    """Prueba que los movimientos sean adyacentes a la cabeza"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Primer movimiento
    juego.realizar_movimiento(Posicion(3, 3))

    # Intento de movimiento no adyacente
    resultado = juego.realizar_movimiento(Posicion(0, 0))
    assert not resultado.es_valido

    # Movimiento adyacente válido
    resultado = juego.realizar_movimiento(Posicion(3, 4))
    assert resultado.es_valido


def test_fin_de_juego():
    """Prueba la detección del fin del juego"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Llenar el tablero excepto una casilla
    for y in range(TABLERO_TAMANO):
        for x in range(TABLERO_TAMANO):
            if y == TABLERO_TAMANO - 1 and x == TABLERO_TAMANO - 1:
                continue
            juego.realizar_movimiento(Posicion(x, y))

    # Verificar que el juego no ha terminado aún
    terminado, ganador = juego.verificar_fin_juego()
    assert not terminado
    assert not ganador

    # Último movimiento
    juego.realizar_movimiento(Posicion(TABLERO_TAMANO - 1, TABLERO_TAMANO - 1))

    # Verificar que el juego ha terminado
    terminado, ganador = juego.verificar_fin_juego()
    assert terminado
    assert ganador  # El último en mover gana
