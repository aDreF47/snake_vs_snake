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
        mejor_valor = float('-inf')
        
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
    
    def seleccionar_movimiento(self, motor_juego) -> Optional[Posicion]:
        """
        INTERFAZ PARA PERSONA 3
        Implementa minimax con la profundidad especificada
        """
        estado_actual = motor_juego.obtener_estado_actual()
        valor, mejor_movimiento = self.minimax(
            estado_actual,
            self.profundidad,
            True,  # Maximizando para el jugador actual
            motor_juego
        )
        return mejor_movimiento
    
    def minimax(
        self, estado: EstadoJuego,
        profundidad: int,
        es_maximizando: bool,
        motor_juego
    ) -> Tuple[float, Optional[Posicion]]:
        """Algoritmo minimax recursivo"""
        # Condición de parada
        if profundidad == 0:
            valor = self.evaluador.evaluar_estado(estado, motor_juego)
            return valor, None
        
        # Obtener jugador actual
        jugador_actual = self.jugador if es_maximizando else (
            'rojo' if self.jugador == 'azul' else 'azul'
        )
        
        # Obtener movimientos válidos
        movimientos = []
        for y in range(len(estado.tablero)):
            for x in range(len(estado.tablero[y])):
                pos = Posicion(x, y)
                estado_prueba = estado.copiar()
                if estado_prueba.tablero[y][x] == '':
                    estado_prueba.tablero[y][x] = jugador_actual
                    movimientos.append((pos, estado_prueba))
        
        if not movimientos:
            # Si no hay movimientos, este estado es terminal
            return float('-inf') if es_maximizando else float('inf'), None
        
        mejor_valor = float('-inf') if es_maximizando else float('inf')
        mejor_movimiento = None
        
        for movimiento, nuevo_estado in movimientos:
            valor, _ = self.minimax(
                nuevo_estado,
                profundidad - 1,
                not es_maximizando,
                motor_juego
            )
            
            if es_maximizando:
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
            else:
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
        
        return mejor_valor, mejor_movimiento