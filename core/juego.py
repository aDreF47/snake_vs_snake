from typing import List, Optional, Tuple
from core.interfaces import (
    AZUL,
    ROJO,
    VACIO,
    Posicion,
    EstadoJuego,
    MovimientoResult,
    TABLERO_TAMANO,
)
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
        if not self.estado_actual:
            return []

        # Crear un estado temporal para el jugador específico
        estado_temp = self.estado_actual.copiar()
        estado_temp.turno = jugador

        movimientos_validos = []
        cabeza = estado_temp.cabeza_azul if jugador == AZUL else estado_temp.cabeza_roja

        # Si no hay cabeza, cualquier casilla vacía es válida
        if cabeza is None:
            for y in range(TABLERO_TAMANO):
                for x in range(TABLERO_TAMANO):
                    if estado_temp.tablero[y][x] == VACIO:
                        movimientos_validos.append(Posicion(x, y))
            return movimientos_validos

        # Si hay cabeza, solo las casillas adyacentes vacías
        adyacentes = GestorEstado.obtener_posiciones_adyacentes(cabeza)
        for pos in adyacentes:
            if estado_temp.tablero[pos.y][pos.x] == VACIO:
                movimientos_validos.append(pos)

        return movimientos_validos

    def realizar_movimiento(self, posicion: Posicion) -> MovimientoResult:
        """
        INTERFAZ CLAVE PARA PERSONA 3 (GUI)
        Procesa un movimiento del jugador
        """
        if not self.estado_actual or self.juego_terminado:
            return MovimientoResult(
                es_valido=False, mensaje="Juego no iniciado o terminado"
            )

        resultado = GestorEstado.aplicar_movimiento(self.estado_actual, posicion)

        if resultado.es_valido and resultado.nuevo_estado:
            # Actualizar el estado actual
            self.estado_actual = resultado.nuevo_estado

            # Verificar fin de juego antes de cambiar turno
            self._actualizar_estado_fin_juego()

            if not self.juego_terminado:
                self.cambiar_turno()

        return MovimientoResult(
            es_valido=resultado.es_valido,
            mensaje=resultado.mensaje,
            nuevo_estado=self.estado_actual,
        )

    def verificar_fin_juego(self) -> Tuple[bool, Optional[str]]:
        """
        INTERFAZ CLAVE PARA AMBOS
        Retorna (juego_terminado, ganador)
        """
        estado = self.obtener_estado_actual()
        if estado is None:
            return False, None

        # Caso 1: tablero lleno
        lleno = all(celda != VACIO for fila in estado.tablero for celda in fila)
        if lleno:
            self.juego_terminado = True

            # Determinar ganador por cantidad de casillas ocupadas
            azul_count = sum(c == AZUL for fila in estado.tablero for c in fila)
            rojo_count = sum(c == ROJO for fila in estado.tablero for c in fila)

            if azul_count > rojo_count:
                self.ganador = AZUL
            elif rojo_count > azul_count:
                self.ganador = ROJO
            else:
                self.ganador = None  # empate

            return True, self.ganador

        # Caso 2: próximo jugador no tiene movimientos
        proximo_jugador = ROJO if estado.turno == AZUL else AZUL
        movimientos_disponibles = self.obtener_movimientos_validos(proximo_jugador)

        if not movimientos_disponibles:
            self.juego_terminado = True
            self.ganador = estado.turno
            return True, self.ganador

        # Caso 3: el juego continúa
        self.juego_terminado = False
        self.ganador = None
        return False, None

    def _actualizar_estado_fin_juego(self) -> None:
        terminado, ganador = self.verificar_fin_juego()
        self.juego_terminado = terminado
        self.ganador = ganador

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

    # MÉTODO ADICIONAL PARA LA IA
    def simular_movimiento(
        self, estado: EstadoJuego, posicion: Posicion, jugador: str
    ) -> Optional[EstadoJuego]:
        """
        INTERFAZ PARA PERSONA 2 (IA - MINIMAX)
        Simula un movimiento sin modificar el estado actual del juego
        """
        estado_temp = estado.copiar()
        estado_temp.turno = jugador
        resultado = GestorEstado.aplicar_movimiento(estado_temp, posicion)
        return resultado.nuevo_estado if resultado.es_valido else None
