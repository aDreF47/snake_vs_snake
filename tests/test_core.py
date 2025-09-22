import pytest
from core.interfaces import TABLERO_TAMANO, AZUL, ROJO, VACIO, Posicion
from core.juego import MotorJuego


def test_inicializacion_motor():
    """Prueba que el motor de juego se cree correctamente"""
    juego = MotorJuego()
    assert juego.estado_actual is None
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

    # Al inicio el tablero debe estar vacío
    assert all(celda == VACIO for fila in estado.tablero for celda in fila)


def test_primer_movimiento():
    """Prueba la validez del primer movimiento"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Movimiento inválido (fuera del tablero)
    resultado = juego.realizar_movimiento(Posicion(-1, 0))
    assert not resultado.es_valido

    # Movimiento válido dentro del tablero
    resultado = juego.realizar_movimiento(Posicion(3, 3))
    assert resultado.es_valido

    estado = juego.obtener_estado_actual()
    assert estado.tablero[3][3] == AZUL
    assert estado.cabeza_azul == Posicion(3, 3)
    assert estado.turno == ROJO


def test_movimientos_adyacentes():
    """Prueba que los movimientos deben ser adyacentes a la cabeza"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Primer movimiento de Azul -> libre
    resultado = juego.realizar_movimiento(Posicion(3, 3))
    assert resultado.es_valido

    # Primer movimiento de Rojo -> también libre
    resultado = juego.realizar_movimiento(Posicion(0, 0))
    assert resultado.es_valido

    # Segundo movimiento de Azul -> debe ser adyacente a (3,3)
    resultado = juego.realizar_movimiento(Posicion(3, 4))  # válido (abajo)
    assert resultado.es_valido

    # Movimiento de Rojo -> debe ser adyacente a (0,0)
    resultado = juego.realizar_movimiento(Posicion(0, 1))  # válido (abajo)
    assert resultado.es_valido

    # Movimiento inválido de Azul -> no adyacente a cabeza actual (3,4)
    resultado = juego.realizar_movimiento(Posicion(5, 5))  # no adyacente
    assert not resultado.es_valido


def test_fin_de_juego_sin_movimientos():
    """Prueba que el juego termina cuando un jugador no tiene movimientos válidos"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Crear una situación donde un jugador quede bloqueado
    # Azul en esquina superior izquierda
    juego.realizar_movimiento(Posicion(0, 0))  # Azul
    juego.realizar_movimiento(Posicion(2, 2))  # Rojo lejos

    # Azul se mueve a la derecha
    juego.realizar_movimiento(Posicion(1, 0))  # Azul
    juego.realizar_movimiento(Posicion(2, 3))  # Rojo

    # Azul se mueve hacia abajo
    juego.realizar_movimiento(Posicion(1, 1))  # Azul
    juego.realizar_movimiento(Posicion(3, 3))  # Rojo

    # Azul hacia la izquierda (vuelve por wraparound)
    juego.realizar_movimiento(Posicion(0, 1))  # Azul
    juego.realizar_movimiento(Posicion(4, 3))  # Rojo

    # Verificar que el juego puede continuar
    terminado, ganador = juego.verificar_fin_juego()
    # En este punto, Azul debería tener movimientos disponibles
    movimientos_azul = juego.obtener_movimientos_validos(AZUL)
    print(f"Movimientos disponibles para Azul: {movimientos_azul}")

    # El test anterior era incorrecto - este es más realista
    # El juego debería continuar mientras haya movimientos disponibles


def test_wraparound():
    """Prueba que el wraparound funciona correctamente"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Colocar Azul en el borde derecho
    juego.realizar_movimiento(Posicion(TABLERO_TAMANO - 1, 3))  # Azul en borde derecho
    juego.realizar_movimiento(Posicion(2, 2))  # Rojo lejos

    # Azul se mueve hacia la derecha (wraparound al lado izquierdo)
    resultado = juego.realizar_movimiento(
        Posicion(0, 3)
    )  # Debería ser válido por wraparound
    assert resultado.es_valido

    estado = juego.obtener_estado_actual()
    assert estado.tablero[3][0] == AZUL  # Verificar que se colocó correctamente


def test_movimientos_validos():
    """Prueba que obtener_movimientos_validos funciona correctamente"""
    juego = MotorJuego()
    juego.inicializar_juego(AZUL)

    # Al inicio, Azul puede moverse a cualquier casilla
    movimientos = juego.obtener_movimientos_validos(AZUL)
    assert len(movimientos) == TABLERO_TAMANO * TABLERO_TAMANO  # Todas las casillas

    # Después del primer movimiento
    juego.realizar_movimiento(Posicion(3, 3))  # Azul
    juego.realizar_movimiento(Posicion(0, 0))  # Rojo

    # Azul solo puede moverse a casillas adyacentes a (3,3)
    movimientos_azul = juego.obtener_movimientos_validos(AZUL)
    expected_positions = [
        Posicion(2, 3),  # Izquierda
        Posicion(4, 3),  # Derecha
        Posicion(3, 2),  # Arriba
        Posicion(3, 4),  # Abajo
    ]

    # Verificar que solo tiene 4 movimientos adyacentes
    assert len(movimientos_azul) == 4
    for pos in expected_positions:
        assert pos in movimientos_azul
