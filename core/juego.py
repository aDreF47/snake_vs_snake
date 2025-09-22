from typing import List, Optional, Tuple
from core.interfaces import AZUL, ROJO, Posicion, EstadoJuego, MovimientoResult
from core.estado import GestorEstado


class MotorJuego:
    """Controla la lógica principal del juego"""

    def __init__(self):
        self.estado_actual: Optional[EstadoJuego] = None
        self.juego_terminado: bool = False
        self.ganador: Optional[str] = None

    def inicializar_juego(self, jugador_inicial: str) -> None:
        """Inicializa un nuevo juego"""
        self.estado_actual = GestorEstado.crear_estado_inicial()
        self.estado_actual.turno = jugador_inicial
        self.juego_terminado = False
        self.ganador = None

    def obtener_movimientos_validos(self, jugador: str) -> List[Posicion]:
        """
        INTERFAZ CLAVE PARA PERSONA 2 (IA)
        Retorna lista de posiciones donde el jugador puede colocar fichas
        """
        if not self.estado_actual or jugador != self.estado_actual.turno:
            return []

        movimientos_validos = []
        cabeza = (
            self.estado_actual.cabeza_azul
            if jugador == AZUL
            else self.estado_actual.cabeza_roja
        )

        # Si no hay cabeza, cualquier casilla vacía es válida
        if not cabeza:
            for y in range(len(self.estado_actual.tablero)):
                for x in range(len(self.estado_actual.tablero[y])):
                    pos = Posicion(x, y)
                    resultado = GestorEstado.aplicar_movimiento(
                        self.estado_actual.copiar(), pos
                    )
                    if resultado.es_valido:
                        movimientos_validos.append(pos)
            return movimientos_validos

        # Si hay cabeza, solo las casillas adyacentes vacías son válidas
        adyacentes = GestorEstado.obtener_posiciones_adyacentes(cabeza)
        for pos in adyacentes:
            resultado = GestorEstado.aplicar_movimiento(
                self.estado_actual.copiar(), pos
            )
            if resultado.es_valido:
                movimientos_validos.append(pos)

        return movimientos_validos

    def realizar_movimiento(self, posicion: Posicion) -> MovimientoResult:
        """
        INTERFAZ CLAVE PARA PERSONA 3 (GUI)
        Procesa un movimiento del jugador humano
        """
        if not self.estado_actual or self.juego_terminado:
            return MovimientoResult(es_valido=False, mensaje="Juego no iniciado")

        resultado = GestorEstado.aplicar_movimiento(self.estado_actual, posicion)

        if resultado.es_valido:
            # Verificar fin de juego
            self.verificar_fin_juego()
            if not self.juego_terminado:
                self.cambiar_turno()

        return resultado

    def verificar_fin_juego(self) -> Tuple[bool, Optional[str]]:
        """
        INTERFAZ CLAVE PARA AMBOS
        Retorna (juego_terminado, ganador)
        """
        if not self.estado_actual:
            return True, None

        # Verificar si hay movimientos disponibles
        movimientos = self.obtener_movimientos_validos(self.estado_actual.turno)

        if not movimientos:
            self.juego_terminado = True
            # El ganador es el oponente (quien forzó que no haya movimientos)
            self.ganador = ROJO if self.estado_actual.turno == AZUL else AZUL

        return self.juego_terminado, self.ganador

    def obtener_estado_actual(self) -> EstadoJuego:
        """
        INTERFAZ CLAVE PARA AMBOS
        Retorna el estado actual del juego
        """
        if not self.estado_actual:
            raise RuntimeError("Juego no inicializado")
        return self.estado_actual

    def cambiar_turno(self) -> None:
        """Cambia el turno al siguiente jugador"""
        if self.estado_actual:
            self.estado_actual.turno = (
                ROJO if self.estado_actual.turno == AZUL else AZUL
            )
