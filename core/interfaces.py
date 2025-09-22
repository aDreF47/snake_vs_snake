from typing import List, Optional, NamedTuple
from enum import Enum, auto

# Constantes del juego
TABLERO_TAMANO = 7
AZUL = "A"  # Cambiar a "A" para compatibilidad con documentos
ROJO = "R"  # Cambiar a "R" para compatibilidad con documentos
VACIO = "V"  # Cambiar a "V" para compatibilidad con documentos


class Dificultad(Enum):
    """Niveles de dificultad de la IA"""

    PRINCIPIANTE = auto()
    NORMAL = auto()
    EXPERTO = auto()


class Posicion(NamedTuple):
    """Representa una posición en el tablero"""

    x: int
    y: int


class MovimientoResult(NamedTuple):
    """Resultado de intentar realizar un movimiento"""

    es_valido: bool
    mensaje: str = ""
    nuevo_estado: Optional["EstadoJuego"] = None


class EstadoJuego:
    """Representa el estado completo del juego"""

    def __init__(self, tablero: List[List[str]], turno: str):
        self.tablero = tablero
        self.turno = turno
        self.cabeza_azul: Optional[Posicion] = None
        self.cabeza_roja: Optional[Posicion] = None
        # Historial para tracking de cabezas (última colocada)
        self.historial_azul: List[Posicion] = []
        self.historial_rojo: List[Posicion] = []
        self._actualizar_cabezas_desde_historial()

    def _actualizar_cabezas_desde_historial(self) -> None:
        """Actualiza cabezas basándose en el historial de movimientos"""
        if self.historial_azul:
            self.cabeza_azul = self.historial_azul[-1]
        if self.historial_rojo:
            self.cabeza_roja = self.historial_rojo[-1]

    def agregar_movimiento(self, posicion: Posicion, color: str) -> None:
        """Agrega un movimiento al historial correspondiente"""
        if color == AZUL:
            self.historial_azul.append(posicion)
            self.cabeza_azul = posicion
        elif color == ROJO:
            self.historial_rojo.append(posicion)
            self.cabeza_roja = posicion

    def copiar(self) -> "EstadoJuego":
        """Crea una copia profunda del estado actual"""
        nuevo_tablero = [fila[:] for fila in self.tablero]
        nuevo_estado = EstadoJuego(nuevo_tablero, self.turno)
        nuevo_estado.cabeza_azul = self.cabeza_azul
        nuevo_estado.cabeza_roja = self.cabeza_roja
        nuevo_estado.historial_azul = self.historial_azul[:]
        nuevo_estado.historial_rojo = self.historial_rojo[:]
        return nuevo_estado
