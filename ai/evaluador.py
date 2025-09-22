from core.interfaces import AZUL, ROJO, EstadoJuego


class FuncionEvaluadora:
    """Implementa la función de evaluación f(e) = Ma(e) - Mr(e)"""
    
    @staticmethod
    def evaluar_estado(estado: EstadoJuego, motor_juego) -> float:
        """
        FUNCIÓN PRINCIPAL PARA ESTRATEGIAS
        Implementa: f(e) = movimientos_azul - movimientos_rojo
        
        Args:
            estado: Estado actual del juego
            motor_juego: Instancia de MotorJuego para obtener movimientos
        
        Returns:
            float: Valor de evaluación (+ favorable a azul, - favorable a rojo)
        """
        # Guardar turno actual
        turno_original = estado.turno
        
        # Contar movimientos disponibles para azul
        estado.turno = AZUL
        movimientos_azul = len(motor_juego.obtener_movimientos_validos(AZUL))
        
        # Contar movimientos disponibles para rojo
        estado.turno = ROJO
        movimientos_rojo = len(motor_juego.obtener_movimientos_validos(ROJO))
        
        # Restaurar turno original
        estado.turno = turno_original
        
        # Retornar diferencia
        return movimientos_azul - movimientos_rojo