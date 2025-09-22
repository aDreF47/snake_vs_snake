from typing import List
from core.interfaces import (
    TABLERO_TAMANO,
    VACIO,
    AZUL,
    ROJO,
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
        # Azul inicia por defecto
        return EstadoJuego(tablero=tablero, turno=AZUL)

    @staticmethod
    def es_posicion_valida(pos: Posicion) -> bool:
        """Valida si una posición está dentro del tablero"""
        return 0 <= pos.x < TABLERO_TAMANO and 0 <= pos.y < TABLERO_TAMANO

    @staticmethod
    def obtener_posiciones_adyacentes(pos: Posicion) -> List[Posicion]:
        """Obtiene posiciones adyacentes (incluye wraparound)"""

        def wraparound(coord: int) -> int:
            return coord % TABLERO_TAMANO

        adyacentes = [
            Posicion(wraparound(pos.x - 1), pos.y),  # Izquierda
            Posicion(wraparound(pos.x + 1), pos.y),  # Derecha
            Posicion(pos.x, wraparound(pos.y - 1)),  # Arriba
            Posicion(pos.x, wraparound(pos.y + 1)),  # Abajo
        ]
        return adyacentes

    @staticmethod
    def aplicar_movimiento(estado: EstadoJuego, posicion: Posicion) -> MovimientoResult:
        """Aplica un movimiento y retorna el resultado"""
        # Crear copia para no modificar el estado original
        nuevo_estado = estado.copiar()

        # Validar que la posición esté dentro del tablero
        if not GestorEstado.es_posicion_valida(posicion):
            return MovimientoResult(
                es_valido=False, mensaje="Posición fuera del tablero"
            )

        # Validar que la casilla esté vacía
        if nuevo_estado.tablero[posicion.y][posicion.x] != VACIO:
            return MovimientoResult(es_valido=False, mensaje="Casilla ocupada")

        # Obtener cabeza del jugador actual
        cabeza_actual = (
            nuevo_estado.cabeza_azul
            if nuevo_estado.turno == AZUL
            else nuevo_estado.cabeza_roja
        )

        # Si es el primer movimiento del jugador
        if cabeza_actual is None:
            # Cualquier casilla vacía es válida
            nuevo_estado.tablero[posicion.y][posicion.x] = nuevo_estado.turno
            nuevo_estado.agregar_movimiento(posicion, nuevo_estado.turno)
            return MovimientoResult(
                es_valido=True,
                mensaje="Primera ficha colocada",
                nuevo_estado=nuevo_estado,
            )

        # Validar que la posición sea adyacente a la cabeza actual
        adyacentes = GestorEstado.obtener_posiciones_adyacentes(cabeza_actual)
        if posicion not in adyacentes:
            return MovimientoResult(
                es_valido=False, mensaje="Posición no adyacente a la cabeza"
            )

        # Colocar la ficha
        nuevo_estado.tablero[posicion.y][posicion.x] = nuevo_estado.turno
        nuevo_estado.agregar_movimiento(posicion, nuevo_estado.turno)

        return MovimientoResult(
            es_valido=True, mensaje="Movimiento válido", nuevo_estado=nuevo_estado
        )

    @staticmethod
    def contar_movimientos_disponibles(estado: EstadoJuego, jugador: str) -> int:
        """
        INTERFAZ PARA PERSONA 2 (IA)
        Cuenta movimientos disponibles para la función evaluadora
        """
        if jugador != estado.turno:
            # No es el turno del jugador, retornar 0
            return 0

        cabeza = estado.cabeza_azul if jugador == AZUL else estado.cabeza_roja

        # Si no tiene cabeza, puede colocar en cualquier casilla vacía
        if cabeza is None:
            contador = 0
            for y in range(TABLERO_TAMANO):
                for x in range(TABLERO_TAMANO):
                    if estado.tablero[y][x] == VACIO:
                        contador += 1
            return contador

        # Si tiene cabeza, solo casillas adyacentes vacías
        contador = 0
        adyacentes = GestorEstado.obtener_posiciones_adyacentes(cabeza)
        for pos in adyacentes:
            if estado.tablero[pos.y][pos.x] == VACIO:
                contador += 1

        return contador
