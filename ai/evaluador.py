from core.interfaces import AZUL, ROJO, EstadoJuego


class FuncionEvaluadora:
    """Módulo evaluador para el juego Snake vs Snake."""


from core.interfaces import AZUL, ROJO, EstadoJuego


class FuncionEvaluadora:
    """Evaluador de estados del juego."""

    @staticmethod
    def evaluar_estado(estado: EstadoJuego, motor_juego) -> float:
        """
        Calcula el valor de un estado del juego.

        La función de evaluación es f(e) = Ma(e) - Mr(e) donde:
        - Ma(e) es la cantidad de movimientos disponibles para AZUL
        - Mr(e) es la cantidad de movimientos disponibles para ROJO

        Args:
            estado: Estado actual del juego
            motor_juego: Motor del juego para calcular movimientos válidos

        Returns:
            float: Positivo si favorece a AZUL, negativo si favorece a ROJO
        """
        turno_original = estado.turno

        estado.turno = AZUL
        movimientos_azul = len(motor_juego.obtener_movimientos_validos(AZUL))

        estado.turno = ROJO
        movimientos_rojo = len(motor_juego.obtener_movimientos_validos(ROJO))

        estado.turno = turno_original

        return movimientos_azul - movimientos_rojo

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
