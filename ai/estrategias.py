from typing import List, Optional, Tuple
import random
from core.interfaces import Posicion, EstadoJuego
from ai.evaluador import FuncionEvaluadora


class EstrategiaIA:
    """Clase base para estrategias de IA"""

    def __init__(self, jugador: str):
        self.jugador = jugador
        self.evaluador = FuncionEvaluadora()

    def seleccionar_movimiento(self, motor_juego) -> Optional[Posicion]:
        """Método abstracto - debe ser implementado por subclases"""
        raise NotImplementedError


class EstrategiaAleatoria(EstrategiaIA):
    """Nivel Principiante - Selección aleatoria"""

    def seleccionar_movimiento(self, motor_juego) -> Optional[Posicion]:
        """
        INTERFAZ PARA PERSONA 3
        Retorna movimiento aleatorio válido o None si no hay movimientos
        """
        movimientos = motor_juego.obtener_movimientos_validos(self.jugador)
        return random.choice(movimientos) if movimientos else None


class EstrategiaPrimeroMejor(EstrategiaIA):
    """Nivel Normal - Primero el mejor (greedy)"""

    def seleccionar_movimiento(self, motor_juego) -> Optional[Posicion]:
        """
        INTERFAZ PARA PERSONA 3
        Evalúa todos los movimientos y retorna el mejor según función evaluadora
        """
        movimientos = motor_juego.obtener_movimientos_validos(self.jugador)
        if not movimientos:
            return None

        # Evaluar cada movimiento posible
        mejor_movimiento = None
        mejor_valor = float("-inf")

        for movimiento in movimientos:
            # Simular movimiento
            estado_prueba = motor_juego.obtener_estado_actual().copiar()
            estado_prueba.tablero[movimiento.y][movimiento.x] = self.jugador

            # Evaluar estado resultante
            valor = self.evaluador.evaluar_estado(estado_prueba, motor_juego)

            # Actualizar mejor movimiento
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

        return mejor_movimiento


class EstrategiaMinimax(EstrategiaIA):
    """Nivel Experto - Algoritmo Minimax"""

    def __init__(self, jugador: str, profundidad: int = 3):
        super().__init__(jugador)
        self.profundidad = profundidad
        self.oponente = "rojo" if jugador == "azul" else "azul"

    def seleccionar_movimiento(self, motor_juego) -> Optional[Posicion]:
        """
        INTERFAZ PARA PERSONA 3
        Implementa minimax con la profundidad especificada
        """
        estado_actual = motor_juego.obtener_estado_actual()
        
        # Verificar que es nuestro turno
        if estado_actual.turno != self.jugador:
            return None
            
        _, mejor_movimiento = self.minimax(
            estado_actual,
            self.profundidad,
            True,  # Maximizando para la IA
            motor_juego,
            float("-inf"),
            float("inf")
        )
        return mejor_movimiento

    def minimax(
        self, 
        estado: EstadoJuego, 
        profundidad: int, 
        es_maximizando: bool, 
        motor_juego,
        alpha: float = float("-inf"),
        beta: float = float("inf")
    ) -> Tuple[float, Optional[Posicion]]:
        """Algoritmo minimax recursivo con poda alfa-beta"""
        
        # Verificar si el juego terminó en este estado
        ganador = self._verificar_ganador(estado, motor_juego)
        if ganador is not None:
            if ganador == self.jugador:
                return 1000 + profundidad, None  # Victoria para IA
            elif ganador == self.oponente:
                return -1000 - profundidad, None  # Victoria para humano
            else:
                return 0, None  # Empate
        
        # Condición de parada por profundidad
        if profundidad == 0:
            valor = self.evaluador.evaluar_estado(estado, motor_juego)
            # Ajustar evaluación según perspectiva
            if self.jugador == "rojo":
                valor = -valor  # Invertir si somos rojos
            return valor, None

        # Determinar jugador actual
        jugador_actual = self.jugador if es_maximizando else self.oponente

        # Obtener movimientos válidos para el jugador actual
        movimientos = self._obtener_movimientos_validos(estado, jugador_actual)
        
        if not movimientos:
            # No hay movimientos disponibles - estado terminal
            return 0, None

        mejor_movimiento = None
        
        if es_maximizando:
            mejor_valor = float("-inf")
            
            for movimiento in movimientos:
                # Crear nuevo estado con el movimiento
                nuevo_estado = self._aplicar_movimiento(estado, movimiento, jugador_actual)
                
                # Llamada recursiva
                valor, _ = self.minimax(
                    nuevo_estado, 
                    profundidad - 1, 
                    False, 
                    motor_juego,
                    alpha,
                    beta
                )
                
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
                
                # Poda alfa-beta
                alpha = max(alpha, valor)
                if beta <= alpha:
                    break
                    
        else:  # Minimizando
            mejor_valor = float("inf")
            
            for movimiento in movimientos:
                # Crear nuevo estado con el movimiento
                nuevo_estado = self._aplicar_movimiento(estado, movimiento, jugador_actual)
                
                # Llamada recursiva
                valor, _ = self.minimax(
                    nuevo_estado, 
                    profundidad - 1, 
                    True, 
                    motor_juego,
                    alpha,
                    beta
                )
                
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
                
                # Poda alfa-beta
                beta = min(beta, valor)
                if beta <= alpha:
                    break

        return mejor_valor, mejor_movimiento

    def _obtener_movimientos_validos(self, estado: EstadoJuego, jugador: str) -> List[Posicion]:
        """Obtiene todos los movimientos válidos para un jugador en un estado dado"""
        movimientos = []
        for y in range(len(estado.tablero)):
            for x in range(len(estado.tablero[y])):
                if estado.tablero[y][x] == "":  # Casilla vacía
                    movimientos.append(Posicion(x, y))
        return movimientos

    def _aplicar_movimiento(self, estado: EstadoJuego, posicion: Posicion, jugador: str) -> EstadoJuego:
        """Crea un nuevo estado aplicando un movimiento"""
        nuevo_estado = estado.copiar()
        nuevo_estado.tablero[posicion.y][posicion.x] = jugador
        
        # Cambiar turno
        nuevo_estado.turno = self.oponente if jugador == self.jugador else self.jugador
        
        return nuevo_estado

    def _verificar_ganador(self, estado: EstadoJuego, motor_juego) -> Optional[str]:
        """Verifica si hay un ganador en el estado actual"""
        try:
            # Crear un motor temporal para verificar el estado
            motor_temp = type(motor_juego)()
            motor_temp.estado = estado
            
            juego_terminado, ganador = motor_temp.verificar_fin_juego()
            if juego_terminado:
                return ganador
            return None
        except:
            # Si hay error, evaluar manualmente
            return self._verificar_ganador_manual(estado)
    
    def _verificar_ganador_manual(self, estado: EstadoJuego) -> Optional[str]:
        """Verificación manual de ganador (fallback)"""
        tablero = estado.tablero
        filas = len(tablero)
        cols = len(tablero[0]) if filas > 0 else 0
        
        # Verificar filas, columnas y diagonales
        for jugador in [self.jugador, self.oponente]:
            # Filas
            for y in range(filas):
                if all(tablero[y][x] == jugador for x in range(cols)):
                    return jugador
            
            # Columnas  
            for x in range(cols):
                if all(tablero[y][x] == jugador for y in range(filas)):
                    return jugador
                    
            # Diagonales (si es tablero cuadrado)
            if filas == cols:
                if all(tablero[i][i] == jugador for i in range(filas)):
                    return jugador
                if all(tablero[i][cols-1-i] == jugador for i in range(filas)):
                    return jugador
        
        # Verificar empate (tablero lleno)
        if all(tablero[y][x] != "" for y in range(filas) for x in range(cols)):
            return "empate"
            
        return None