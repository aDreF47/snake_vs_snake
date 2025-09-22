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
            
            # Primero intentar con movimientos válidos del motor
            movimientos = motor_juego.obtener_movimientos_validos(self.jugador)
            if not movimientos:
                print("[DEBUG] No hay movimientos válidos disponibles")
                return None
            
            print(f"[DEBUG] Movimientos válidos encontrados: {len(movimientos)}")
            
            # Si solo hay un movimiento, devolverlo directamente
            if len(movimientos) == 1:
                print(f"[DEBUG] Solo un movimiento disponible: {movimientos[0]}")
                return movimientos[0]
            
            estado_actual = motor_juego.obtener_estado_actual()
            
            # Implementación simplificada para debugging
            mejor_movimiento = None
            mejor_valor = float("-inf")
            
            print(f"[DEBUG] Evaluando {len(movimientos)} movimientos...")
            
            for i, movimiento in enumerate(movimientos):
                print(f"[DEBUG] Evaluando movimiento {i+1}/{len(movimientos)}: {movimiento}")
                
                # Simular el movimiento
                estado_prueba = estado_actual.copiar()
                estado_prueba.tablero[movimiento.y][movimiento.x] = self.jugador
                
                # Llamar a minimax con profundidad reducida inicialmente
                try:
                    valor, _ = self.minimax(
                        estado_prueba,
                        min(2, self.profundidad - 1),  # Reducir profundidad inicialmente
                        False,  # Siguiente turno es del oponente
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
            # Fallback: devolver movimiento aleatorio
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
        """Algoritmo minimax recursivo simplificado"""
        
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

            # Determinar jugador actual
            jugador_actual = self.jugador if es_maximizando else self.oponente

            # Obtener movimientos válidos
            movimientos = self._obtener_movimientos_validos(estado)
            
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
                    # Crear nuevo estado
                    nuevo_estado = self._aplicar_movimiento(estado, movimiento, jugador_actual)
                    
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
                    # Crear nuevo estado
                    nuevo_estado = self._aplicar_movimiento(estado, movimiento, jugador_actual)
                    
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

    def _obtener_movimientos_validos(self, estado: EstadoJuego) -> List[Posicion]:
        """Obtiene todos los movimientos válidos en un estado dado"""
        movimientos = []
        try:
            for y in range(len(estado.tablero)):
                for x in range(len(estado.tablero[y])):
                    if estado.tablero[y][x] == "":  # Casilla vacía
                        movimientos.append(Posicion(x, y))
        except Exception as e:
            print(f"[ERROR] Error obteniendo movimientos válidos: {e}")
        return movimientos

    def _aplicar_movimiento(self, estado: EstadoJuego, posicion: Posicion, jugador: str) -> EstadoJuego:
        """Crea un nuevo estado aplicando un movimiento"""
        try:
            nuevo_estado = estado.copiar()
            nuevo_estado.tablero[posicion.y][posicion.x] = jugador
            # No modificar el turno aquí - lo maneja el algoritmo minimax
            return nuevo_estado
        except Exception as e:
            print(f"[ERROR] Error aplicando movimiento: {e}")
            return estado  # Retornar estado original si hay error