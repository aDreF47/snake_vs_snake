from typing import List
from core.interfaces import (
    TABLERO_TAMANO,
    VACIO,
    AZUL,
    Posicion,
    EstadoJuego,
    MovimientoResult,
)


class GestorEstado:
    """Maneja la representación y manipulación de estados"""

    @staticmethod
    def crear_estado_inicial() -> EstadoJuego:
        """Crea el estado inicial del juego (tablero vacío)"""
        tablero = [
            [VACIO for _ in range(TABLERO_TAMANO)] for _ in range(TABLERO_TAMANO)
        ]
        return EstadoJuego(tablero=tablero, turno=VACIO)

    @staticmethod
    def es_posicion_valida(pos: Posicion) -> bool:
        """Valida si una posición está dentro del tablero"""
        return 0 <= pos.x < TABLERO_TAMANO and 0 <= pos.y < TABLERO_TAMANO

    @staticmethod
    def obtener_posiciones_adyacentes(pos: Posicion) -> List[Posicion]:
        """Obtiene posiciones adyacentes (incluye wraparound)"""

        # Función helper para aplicar wraparound
        def mod(n: int) -> int:
            return n % TABLERO_TAMANO

        # Posiciones adyacentes con wraparound
        adyacentes = [
            Posicion(mod(pos.x - 1), pos.y),  # Izquierda
            Posicion(mod(pos.x + 1), pos.y),  # Derecha
            Posicion(x=pos.x, y=mod(pos.y - 1)),  # Arriba
            Posicion(x=pos.x, y=mod(pos.y + 1)),  # Abajo
        ]
        return adyacentes

    @staticmethod
    def aplicar_movimiento(estado: EstadoJuego, posicion: Posicion) -> MovimientoResult:
        """Aplica un movimiento y retorna el resultado"""
        # Validar que la posición esté dentro del tablero
        if not GestorEstado.es_posicion_valida(posicion):
            return MovimientoResult(
                es_valido=False, mensaje="Posición fuera del tablero"
            )
        # Validar que la casilla esté vacía
        if estado.tablero[posicion.y][posicion.x] != VACIO:
            return MovimientoResult(es_valido=False, mensaje="Casilla ocupada")
        # Si es el primer movimiento del color
        cabeza = estado.cabeza_azul if estado.turno == AZUL else estado.cabeza_roja
        if not cabeza:
            # Colocar primera ficha
            estado.tablero[posicion.y][posicion.x] = estado.turno
            estado._actualizar_cabezas()
            return MovimientoResult(es_valido=True)
        # Validar que la posición sea adyacente a la cabeza
        adyacentes = GestorEstado.obtener_posiciones_adyacentes(cabeza)
        if posicion not in adyacentes:
            return MovimientoResult(
                es_valido=False, mensaje="Posición no adyacente a la cabeza"
            )
        # Colocar ficha
        estado.tablero[posicion.y][posicion.x] = estado.turno
        estado._actualizar_cabezas()
        return MovimientoResult(es_valido=True)
