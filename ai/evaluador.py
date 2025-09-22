from core.interfaces import AZUL, ROJO, EstadoJuego


class FuncionEvaluadora:
    """Evaluador de estados del juego optimizado para Minimax."""

    def evaluar_estado(self, estado: EstadoJuego, motor_juego) -> float:
        """
        FUNCIÓN PRINCIPAL PARA ESTRATEGIAS
        Implementa: f(e) = movimientos_azul - movimientos_rojo

        Args:
            estado: Estado actual del juego
            motor_juego: Instancia de MotorJuego para obtener movimientos

        Returns:
            float: Valor de evaluación (+ favorable a azul, - favorable a rojo)
        """
        try:
            # Crear una copia del estado para no modificar el original
            estado_temp = estado.copiar()
            
            # Contar movimientos disponibles para azul
            movimientos_azul = self._contar_movimientos_seguros(estado_temp, AZUL, motor_juego)
            
            # Contar movimientos disponibles para rojo  
            movimientos_rojo = self._contar_movimientos_seguros(estado_temp, ROJO, motor_juego)
            
            # Retornar diferencia
            resultado = movimientos_azul - movimientos_rojo
            
            return float(resultado)
            
        except Exception as e:
            # Fallback: evaluación simple basada en ocupación del tablero
            print(f"[ERROR] Error en evaluar_estado: {e}, usando evaluación fallback")
            return self._evaluacion_fallback(estado)

    def _contar_movimientos_seguros(self, estado: EstadoJuego, jugador: str, motor_juego) -> int:
        """
        Cuenta movimientos válidos usando el motor - SOLO desde la cabeza
        """
        try:
            # Crear motor temporal para evaluar este estado específico
            motor_temp = type(motor_juego)()
            motor_temp.estado_actual = estado.copiar()
            
            # Usar el método del motor que ya maneja correctamente las cabezas
            movimientos = motor_temp.obtener_movimientos_validos(jugador)
            cantidad = len(movimientos) if movimientos else 0
            
            return cantidad
            
        except Exception as e:
            print(f"[DEBUG] Error con motor_juego para {jugador}: {e}, usando conteo manual")
            # Fallback: usar el motor original directamente
            try:
                turno_original = estado.turno
                estado.turno = jugador
                movimientos = motor_juego.obtener_movimientos_validos(jugador)
                estado.turno = turno_original
                return len(movimientos) if movimientos else 0
            except Exception as e2:
                print(f"[DEBUG] Error con motor original: {e2}")
                return 0

    def _contar_movimientos_manual(self, estado: EstadoJuego, jugador: str) -> int:
        """
        Fallback: cuenta movimientos manualmente desde las cabezas
        """
        try:
            # Obtener la cabeza del jugador desde el estado
            cabeza = estado.cabeza_azul if jugador == "azul" else estado.cabeza_roja
            
            # Si no hay cabeza, no hay movimientos (o el juego no ha empezado)
            if cabeza is None:
                # Si no hay cabeza, cualquier casilla vacía es válida (inicio de juego)
                contador = 0
                for y in range(len(estado.tablero)):
                    for x in range(len(estado.tablero[y])):
                        if estado.tablero[y][x] == "":
                            contador += 1
                return contador
            
            # Contar casillas vacías adyacentes a la cabeza
            contador = 0
            direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for dx, dy in direcciones:
                nueva_x = cabeza.x + dx
                nueva_y = cabeza.y + dy
                
                # Verificar límites y si la casilla está vacía
                if (0 <= nueva_x < len(estado.tablero[0]) and 
                    0 <= nueva_y < len(estado.tablero) and
                    estado.tablero[nueva_y][nueva_x] == ""):
                    contador += 1
                        
            return contador
            
        except Exception as e:
            print(f"[ERROR] Error en conteo manual: {e}")
            return 0

    def _evaluacion_fallback(self, estado: EstadoJuego) -> float:
        """
        Evaluación de emergencia basada en control del tablero
        """
        try:
            tablero = estado.tablero
            fichas_azul = 0
            fichas_rojo = 0
            casillas_vacias = 0
            
            for fila in tablero:
                for casilla in fila:
                    if casilla == AZUL:
                        fichas_azul += 1
                    elif casilla == ROJO:
                        fichas_rojo += 1
                    elif casilla == "":
                        casillas_vacias += 1
            
            # Si hay casillas vacías, usar diferencia de fichas ponderada
            if casillas_vacias > 0:
                return (fichas_azul - fichas_rojo) + (casillas_vacias * 0.1)
            else:
                # Tablero lleno - solo diferencia de fichas
                return fichas_azul - fichas_rojo
                
        except Exception as e:
            print(f"[ERROR] Error crítico en evaluación fallback: {e}")
            return 0.0

    @staticmethod
    def evaluar_estado_estatico(estado: EstadoJuego, motor_juego) -> float:
        """
        Método estático para compatibilidad con código existente
        """
        evaluador = FuncionEvaluadora()
        return evaluador.evaluar_estado(estado, motor_juego)