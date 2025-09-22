from core import (
    AZUL, ROJO,
    Dificultad, Posicion,
    MotorJuego
)
from gui import GestorInterfaz
from ai import (
    EstrategiaAleatoria,
    EstrategiaPrimeroMejor,
    EstrategiaMinimax
)


class FactoriaEstrategias:
    """Crea estrategias de IA según la dificultad seleccionada"""
    
    @staticmethod
    def crear_estrategia(dificultad: Dificultad, jugador: str):
        if dificultad == Dificultad.PRINCIPIANTE:
            return EstrategiaAleatoria(jugador)
        elif dificultad == Dificultad.NORMAL:
            return EstrategiaPrimeroMejor(jugador)
        else:  # EXPERTO
            return EstrategiaMinimax(jugador, profundidad=3)


class ControladorPrincipal:
    """Orquesta toda la aplicación"""
    
    def __init__(self):
        self.motor_juego = MotorJuego()
        self.interfaz = GestorInterfaz()
        self.estrategia_ia = None
        self.jugador_humano = AZUL  # Por defecto
        self.jugador_ia = ROJO
    
    def iniciar_aplicacion(self) -> None:
        """
        MÉTODO PRINCIPAL
        Punto de entrada de la aplicación
        """
        self.interfaz.ejecutar_bucle_principal(
            callback_juego_iniciado=self.inicializar_juego,
            callback_movimiento=self.procesar_movimiento_humano
        )
    
    def inicializar_juego(self, dificultad: Dificultad, jugador_inicial: str) -> None:
        """Callback llamado cuando se selecciona configuración"""
        # Crear estrategia IA
        self.estrategia_ia = FactoriaEstrategias.crear_estrategia(
            dificultad,
            self.jugador_ia
        )
        
        # Inicializar motor
        self.motor_juego.inicializar_juego(jugador_inicial)
        
        # Si la IA empieza, hacer su movimiento
        if jugador_inicial == self.jugador_ia:
            self.procesar_turno_ia()
    
    def procesar_movimiento_humano(self, posicion: Posicion) -> None:
        """
        CALLBACK DE INTERFAZ
        Procesa movimiento del jugador humano
        """
        # Validar que sea turno del humano
        estado_actual = self.motor_juego.obtener_estado_actual()
        if estado_actual.turno != self.jugador_humano:
            return
        
        # Realizar movimiento
        resultado = self.motor_juego.realizar_movimiento(posicion)
        
        if resultado.es_valido:
            # Actualizar interfaz
            self.actualizar_interfaz()
            
            # Verificar fin de juego
            juego_terminado, ganador = self.motor_juego.verificar_fin_juego()
            if not juego_terminado:
                # Turno de la IA
                self.procesar_turno_ia()
    
    def procesar_turno_ia(self) -> None:
        """Ejecuta el turno de la IA"""
        if not self.estrategia_ia:
            return
        
        posicion = self.estrategia_ia.seleccionar_movimiento(self.motor_juego)
        
        if posicion:
            self.motor_juego.realizar_movimiento(posicion)
        
        self.actualizar_interfaz()
    
    def actualizar_interfaz(self) -> None:
        """Actualiza la interfaz con el estado actual"""
        estado = self.motor_juego.obtener_estado_actual()
        juego_terminado, ganador = self.motor_juego.verificar_fin_juego()
        
        self.interfaz.actualizar_display_juego(
            estado,
            estado.turno,
            juego_terminado,
            ganador
        )


# ===== PUNTO DE ENTRADA =====
if __name__ == "__main__":
    controlador = ControladorPrincipal()
    controlador.iniciar_aplicacion()