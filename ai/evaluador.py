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
        Cuenta movimientos válidos de forma segura sin afectar el estado original
        """
        try:
            # Método 1: Usar el motor si está disponible
            estado_original_turno = estado.turno
            estado.turno = jugador
            
            movimientos = motor_juego.obtener_movimientos_validos(jugador)
            cantidad = len(movimientos) if movimientos else 0
            
            # Restaurar turno original
            estado.turno = estado_original_turno
            
            return cantidad
            
        except Exception as e:
            print(f"[DEBUG] Error con motor_juego para {jugador}: {e}, usando conteo manual")
            # Método 2: Conteo manual como fallback
            return self._contar_movimientos_manual(estado, jugador)

    def _contar_movimientos_manual(self, estado: EstadoJuego, jugador: str) -> int:
        """
        Cuenta movimientos válidos manualmente
        """
        try:
            contador = 0
            tablero = estado.tablero
            
            for y in range(len(tablero)):
                for x in range(len(tablero[y])):
                    if tablero[y][x] == "":  # Casilla vacía
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