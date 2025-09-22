from typing import List, Optional, NamedTuple
from enum import Enum, auto

# Constantes del juego
TABLERO_TAMAÑO = 7
AZUL = "azul"
ROJO = "rojo"
VACIO = ""


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


class EstadoJuego:
    """Representa el estado completo del juego"""
    def __init__(self, tablero: List[List[str]], turno: str):
        self.tablero = tablero
        self.turno = turno
        self.cabeza_azul: Optional[Posicion] = None
        self.cabeza_roja: Optional[Posicion] = None
        self._actualizar_cabezas()
    
    def _actualizar_cabezas(self) -> None:
        """Busca y actualiza la posición de las cabezas de las serpientes"""
        for y in range(TABLERO_TAMAÑO):
            for x in range(TABLERO_TAMAÑO):
                if self.tablero[y][x] == AZUL:
                    if not self._tiene_segmento_adyacente(x, y, AZUL):
                        self.cabeza_azul = Posicion(x, y)
                elif self.tablero[y][x] == ROJO:
                    if not self._tiene_segmento_adyacente(x, y, ROJO):
                        self.cabeza_roja = Posicion(x, y)
    
    def _tiene_segmento_adyacente(self, x: int, y: int, color: str) -> bool:
        """
        Verifica si una posición tiene un segmento adyacente del mismo color
        """
        # Considerando wraparound
        def mod(n: int) -> int:
            return n % TABLERO_TAMAÑO
        
        posiciones = [
            (mod(x-1), y),  # Izquierda
            (mod(x+1), y),  # Derecha
            (x, mod(y-1)),  # Arriba
            (x, mod(y+1))   # Abajo
        ]
        
        return any(self.tablero[py][px] == color for px, py in posiciones)
    
    def copiar(self) -> 'EstadoJuego':
        """Crea una copia profunda del estado actual"""
        nuevo_tablero = [fila[:] for fila in self.tablero]
        nuevo_estado = EstadoJuego(nuevo_tablero, self.turno)
        nuevo_estado.cabeza_azul = self.cabeza_azul
        nuevo_estado.cabeza_roja = self.cabeza_roja
        return nuevo_estado
