import pygame
from typing import Optional, Callable, Tuple
import sys
from core.interfaces import (
    TABLERO_TAMANO,
    AZUL,
    ROJO,
    Dificultad,
    Posicion,
    EstadoJuego,
)


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 100
CELL_SIZE = 60

COLORS = {
    "background": (240, 240, 240),
    "board": (200, 200, 200),
    "grid": (150, 150, 150),
    "text": (50, 50, 50),
    "azul": (100, 100, 255),
    "rojo": (255, 100, 100),
    "azul_cabeza": (150, 150, 255),
    "rojo_cabeza": (255, 150, 150),
    "boton": (180, 180, 180),
    "boton_hover": (150, 150, 150),
}


class PantallaDificultad:
    """Pantalla de selección de dificultad"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.dificultad_seleccionada: Optional[Dificultad] = None

        # Configurar botones
        self.botones = {
            Dificultad.PRINCIPIANTE: pygame.Rect(300, 200, 200, 50),
            Dificultad.NORMAL: pygame.Rect(300, 300, 200, 50),
            Dificultad.EXPERTO: pygame.Rect(300, 400, 200, 50),
        }

    def manejar_eventos(self, eventos) -> bool:
        """
        Procesa eventos de pygame
        Returns: True si se seleccionó dificultad, False si continúa
        """
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for dificultad, rect in self.botones.items():
                    if rect.collidepoint(pos):
                        self.dificultad_seleccionada = dificultad
                        return True
        return False

    def dibujar(self) -> None:
        """Dibuja la pantalla de selección de dificultad"""
        # Fondo
        self.pantalla.fill(COLORS["background"])

        # Título
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("Selecciona la Dificultad", True, COLORS["text"])
        self.pantalla.blit(texto, (250, 100))

        # Botones
        fuente_boton = pygame.font.Font(None, 36)
        nombres = {
            Dificultad.PRINCIPIANTE: "Principiante",
            Dificultad.NORMAL: "Normal",
            Dificultad.EXPERTO: "Experto",
        }

        for dificultad, rect in self.botones.items():
            # Dibujar botón
            color = (
                COLORS["boton_hover"]
                if rect.collidepoint(pygame.mouse.get_pos())
                else COLORS["boton"]
            )
            pygame.draw.rect(self.pantalla, color, rect)

            # Texto del botón
            texto = fuente_boton.render(nombres[dificultad], True, COLORS["text"])
            pos_texto = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, pos_texto)

        pygame.display.flip()


class PantallaTurno:
    """Pantalla de selección de quién inicia"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.jugador_inicial: Optional[str] = None

        # Configurar botones
        self.botones = {
            AZUL: pygame.Rect(200, 300, 150, 50),
            ROJO: pygame.Rect(450, 300, 150, 50),
        }

    def manejar_eventos(self, eventos) -> bool:
        """Returns: True si se seleccionó jugador inicial"""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for jugador, rect in self.botones.items():
                    if rect.collidepoint(pos):
                        self.jugador_inicial = jugador
                        return True
        return False

    def dibujar(self) -> None:
        """Dibuja la pantalla de selección de turno"""
        # Fondo
        self.pantalla.fill(COLORS["background"])

        # Título
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("¿Quién inicia?", True, COLORS["text"])
        self.pantalla.blit(texto, (300, 100))

        # Botones
        fuente_boton = pygame.font.Font(None, 36)
        nombres = {AZUL: "Azul", ROJO: "Rojo"}

        for jugador, rect in self.botones.items():
            # Dibujar botón
            color = (
                COLORS["boton_hover"]
                if rect.collidepoint(pygame.mouse.get_pos())
                else COLORS[jugador]
            )
            pygame.draw.rect(self.pantalla, color, rect)

            # Texto del botón
            texto = fuente_boton.render(nombres[jugador], True, COLORS["text"])
            pos_texto = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, pos_texto)

        pygame.display.flip()


class PantallaJuego:
    """Pantalla principal del juego"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.click_callback: Optional[Callable] = None

    def establecer_callback_click(self, callback: Callable[[Posicion], None]) -> None:
        """Establece función para manejar clicks en el tablero"""
        self.click_callback = callback

    def manejar_eventos(self, eventos) -> Optional[Posicion]:
        """
        INTERFAZ CON MOTOR DE JUEGO
        Returns: Posición clickeada o None
        """
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and self.click_callback:
                pos = pygame.mouse.get_pos()
                pos_tablero = self.convertir_pixel_a_casilla(pos)
                if pos_tablero:
                    self.click_callback(pos_tablero)
        return None

    def dibujar_tablero(self, estado: EstadoJuego) -> None:
        """
        INTERFAZ CON MOTOR DE JUEGO
        Dibuja el estado actual del tablero
        """
        # Fondo
        self.pantalla.fill(COLORS["background"])

        # Tablero
        for y in range(TABLERO_TAMANO):
            for x in range(TABLERO_TAMANO):
                rect = pygame.Rect(
                    BOARD_OFFSET_X + x * CELL_SIZE,
                    BOARD_OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                # Dibujar casilla
                pygame.draw.rect(self.pantalla, COLORS["board"], rect)
                pygame.draw.rect(self.pantalla, COLORS["grid"], rect, 1)

                # Dibujar ficha si hay
                if estado.tablero[y][x]:
                    color = estado.tablero[y][x]
                    pos = Posicion(x, y)

                    # Determinar si es cabeza
                    es_cabeza = (pos == estado.cabeza_azul and color == AZUL) or (
                        pos == estado.cabeza_roja and color == ROJO
                    )

                    color_ficha = (
                        COLORS[f"{color}_cabeza"] if es_cabeza else COLORS[color]
                    )

                    # Dibujar círculo
                    centro = rect.center
                    radio = CELL_SIZE // 2 - 5
                    pygame.draw.circle(self.pantalla, color_ficha, centro, radio)

    def dibujar_info_turno(
        self, turno_actual: str, juego_terminado: bool, ganador: Optional[str]
    ) -> None:
        """Dibuja información de turno y estado del juego"""
        fuente = pygame.font.Font(None, 36)

        if juego_terminado:
            if ganador:
                texto = f"¡{ganador.capitalize()} gana!"
            else:
                texto = "¡Empate!"
        else:
            texto = f"Turno: {turno_actual.capitalize()}"

        superficie = fuente.render(texto, True, COLORS["text"])
        pos = superficie.get_rect(centerx=WINDOW_WIDTH // 2, y=BOARD_OFFSET_Y // 2)
        self.pantalla.blit(superficie, pos)

        pygame.display.flip()

    def convertir_pixel_a_casilla(
        self, pos_pixel: Tuple[int, int]
    ) -> Optional[Posicion]:
        """Convierte coordenadas de pixel a coordenadas de tablero"""
        x, y = pos_pixel

        # Verificar si está dentro del tablero
        if (
            BOARD_OFFSET_X <= x < BOARD_OFFSET_X + TABLERO_TAMANO * CELL_SIZE
            and BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + TABLERO_TAMANO * CELL_SIZE
        ):

            # Convertir a coordenadas de tablero
            tablero_x = (x - BOARD_OFFSET_X) // CELL_SIZE
            tablero_y = (y - BOARD_OFFSET_Y) // CELL_SIZE
            return Posicion(tablero_x, tablero_y)

        return None


class GestorInterfaz:
    """Coordina todas las pantallas"""

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake vs Snake")
        self.reloj = pygame.time.Clock()

        # Estados de la interfaz
        self.estado_actual = "dificultad"  # "dificultad", "turno", "juego"

        # Pantallas
        self.pantalla_dificultad = PantallaDificultad(self.pantalla)
        self.pantalla_turno = PantallaTurno(self.pantalla)
        self.pantalla_juego = PantallaJuego(self.pantalla)

    def ejecutar_bucle_principal(
        self, callback_juego_iniciado: Callable, callback_movimiento: Callable
    ) -> None:
        """
        MÉTODO PRINCIPAL PARA main.py
        Ejecuta el bucle principal de pygame
        """
        ejecutando = True
        while ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    ejecutando = False

            # Limpiar pantalla
            self.pantalla.fill(COLORS["background"])

            if self.estado_actual == "dificultad":
                # Mostrar pantalla de dificultad
                self.pantalla_dificultad.dibujar()
                if self.pantalla_dificultad.manejar_eventos(eventos):
                    self.estado_actual = "turno"

            elif self.estado_actual == "turno":
                # Mostrar pantalla de selección de turno
                self.pantalla_turno.dibujar()
                if self.pantalla_turno.manejar_eventos(eventos):
                    # Iniciar juego
                    callback_juego_iniciado(
                        self.pantalla_dificultad.dificultad_seleccionada,
                        self.pantalla_turno.jugador_inicial,
                    )
                    self.pantalla_juego.establecer_callback_click(callback_movimiento)
                    self.estado_actual = "juego"

            elif self.estado_actual == "juego":
                # Procesar eventos del juego
                self.pantalla_juego.manejar_eventos(eventos)

            # Actualizar pantalla
            pygame.display.flip()

            # Controlar FPS
            self.reloj.tick(60)

        pygame.quit()

    def actualizar_display_juego(
        self,
        estado: EstadoJuego,
        turno: str,
        juego_terminado: bool,
        ganador: Optional[str],
    ) -> None:
        """
        INTERFAZ PARA CONTROLADOR PRINCIPAL
        Actualiza la pantalla con el estado actual
        """
        if self.estado_actual == "juego":
            self.pantalla_juego.dibujar_tablero(estado)
            self.pantalla_juego.dibujar_info_turno(turno, juego_terminado, ganador)
