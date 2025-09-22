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
        try:
            print(f"[DEBUG] IA Minimax iniciando movimiento para jugador: {self.jugador}")
            
            # USAR EL MOTOR CORRECTAMENTE - solo movimientos desde la cabeza
            movimientos = motor_juego.obtener_movimientos_validos(self.jugador)
            if not movimientos:
                print("[DEBUG] No hay movimientos válidos disponibles")
                return None
            
            print(f"[DEBUG] Movimientos válidos desde cabeza encontrados: {len(movimientos)}")
            
            # Si solo hay un movimiento, devolverlo directamente
            if len(movimientos) == 1:
                print(f"[DEBUG] Solo un movimiento disponible: {movimientos[0]}")
                return movimientos[0]
            
            estado_actual = motor_juego.obtener_estado_actual()
            
            mejor_movimiento = None
            mejor_valor = float("-inf")
            
            print(f"[DEBUG] Evaluando {len(movimientos)} movimientos...")
            
            for i, movimiento in enumerate(movimientos):
                print(f"[DEBUG] Evaluando movimiento {i+1}/{len(movimientos)}: {movimiento}")
                
                # USAR EL MÉTODO DE SIMULACIÓN DEL MOTOR
                estado_simulado = motor_juego.simular_movimiento(estado_actual, movimiento, self.jugador)
                
                if estado_simulado is None:
                    print(f"[DEBUG] Movimiento {movimiento} no es válido según simulación")
                    continue
                
                # Llamar a minimax
                try:
                    valor, _ = self.minimax(
                        estado_simulado,
                        self.profundidad - 1,
                        False,  # Siguiente turno es del oponente (minimizar)
                        motor_juego
                    )
                    
                    print(f"[DEBUG] Movimiento {movimiento} evaluado con valor: {valor}")
                    
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_movimiento = movimiento
                        print(f"[DEBUG] Nuevo mejor movimiento: {movimiento} con valor {valor}")
                        
                except Exception as e:
                    print(f"[DEBUG] Error evaluando movimiento {movimiento}: {e}")
                    continue
            
            print(f"[DEBUG] Mejor movimiento seleccionado: {mejor_movimiento}")
            return mejor_movimiento
            
        except Exception as e:
            print(f"[ERROR] Error en seleccionar_movimiento: {e}")
            # Fallback: devolver movimiento aleatorio válido
            movimientos = motor_juego.obtener_movimientos_validos(self.jugador)
            if movimientos:
                fallback = random.choice(movimientos)
                print(f"[FALLBACK] Usando movimiento aleatorio: {fallback}")
                return fallback
            return None

    def minimax(
        self, 
        estado: EstadoJuego, 
        profundidad: int, 
        es_maximizando: bool, 
        motor_juego
    ) -> Tuple[float, Optional[Posicion]]:
        """Algoritmo minimax recursivo que respeta las reglas del Snake"""
        
        try:
            # Condición de parada por profundidad
            if profundidad <= 0:
                try:
                    valor = self.evaluador.evaluar_estado(estado, motor_juego)
                    # Ajustar evaluación según perspectiva del jugador IA
                    if self.jugador == "rojo":
                        valor = -valor
                    return valor, None
                except Exception as e:
                    print(f"[ERROR] Error en evaluación: {e}")
                    return 0.0, None

            # Determinar jugador actual según el contexto de minimax
            jugador_actual = self.jugador if es_maximizando else self.oponente

            # CRÍTICO: Obtener movimientos válidos SOLO desde la cabeza del jugador actual
            movimientos = motor_juego.obtener_movimientos_validos(jugador_actual)
            
            if not movimientos:
                # No hay movimientos - evaluar estado actual
                try:
                    valor = self.evaluador.evaluar_estado(estado, motor_juego)
                    if self.jugador == "rojo":
                        valor = -valor
                    return valor, None
                except Exception as e:
                    print(f"[ERROR] Error evaluando estado sin movimientos: {e}")
                    return 0.0, None

            mejor_movimiento = None
            
            if es_maximizando:
                mejor_valor = float("-inf")
                
                for movimiento in movimientos:
                    # USAR SIMULACIÓN CORRECTA DEL MOTOR
                    nuevo_estado = motor_juego.simular_movimiento(estado, movimiento, jugador_actual)
                    
                    if nuevo_estado is None:
                        continue  # Movimiento inválido
                    
                    # Llamada recursiva
                    valor, _ = self.minimax(
                        nuevo_estado, 
                        profundidad - 1, 
                        False,  # Cambiar a minimizar
                        motor_juego
                    )
                    
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_movimiento = movimiento
                        
            else:  # Minimizando
                mejor_valor = float("inf")
                
                for movimiento in movimientos:
                    # USAR SIMULACIÓN CORRECTA DEL MOTOR
                    nuevo_estado = motor_juego.simular_movimiento(estado, movimiento, jugador_actual)
                    
                    if nuevo_estado is None:
                        continue  # Movimiento inválido
                    
                    # Llamada recursiva
                    valor, _ = self.minimax(
                        nuevo_estado, 
                        profundidad - 1, 
                        True,  # Cambiar a maximizar
                        motor_juego
                    )
                    
                    if valor < mejor_valor:
                        mejor_valor = valor
                        mejor_movimiento = movimiento

            return mejor_valor, mejor_movimiento
            
        except Exception as e:
            print(f"[ERROR] Error en minimax: {e}")
            # Retornar evaluación simple del estado actual
            try:
                valor = self.evaluador.evaluar_estado(estado, motor_juego)
                if self.jugador == "rojo":
                    valor = -valor
                return valor, None
            except Exception as e:
                print(f"[ERROR] Error en evaluación de emergencia: {e}")
                return 0.0, None



