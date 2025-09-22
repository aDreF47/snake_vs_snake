import pygame
from typing import Optional, Callable, Tuple
import sys
from core.interfaces import (
    TABLERO_TAMANO,
    AZUL,
    ROJO,
    VACIO,
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
    ROJO: (255, 100, 100),
    AZUL: (100, 100, 255),
    VACIO: (255, 255, 255),
    f'{ROJO}_cabeza': (255, 150, 150),
    f'{AZUL}_cabeza': (150, 150, 255),
    "boton": (180, 180, 180),
    "boton_hover": (150, 150, 150),
}


class PantallaDificultad:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.dificultad_seleccionada: Optional[Dificultad] = None
        self.botones = {
            Dificultad.PRINCIPIANTE: pygame.Rect(300, 200, 200, 50),
            Dificultad.NORMAL: pygame.Rect(300, 300, 200, 50),
            Dificultad.EXPERTO: pygame.Rect(300, 400, 200, 50),
        }

    def manejar_eventos(self, eventos) -> bool:
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
        self.pantalla.fill(COLORS["background"])
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("Selecciona la Dificultad", True, COLORS["text"])
        self.pantalla.blit(texto, (250, 100))
        fuente_boton = pygame.font.Font(None, 36)
        nombres = {
            Dificultad.PRINCIPIANTE: "Principiante",
            Dificultad.NORMAL: "Normal",
            Dificultad.EXPERTO: "Experto",
        }
        for dificultad, rect in self.botones.items():
            color = COLORS["boton_hover"] if rect.collidepoint(pygame.mouse.get_pos()) else COLORS["boton"]
            pygame.draw.rect(self.pantalla, color, rect)
            texto_boton = fuente_boton.render(nombres[dificultad], True, COLORS["text"])
            pos_texto = texto_boton.get_rect(center=rect.center)
            self.pantalla.blit(texto_boton, pos_texto)


class PantallaTurno:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.jugador_inicial: Optional[str] = None
        self.botones = {
            AZUL: pygame.Rect(200, 300, 150, 50),
            ROJO: pygame.Rect(450, 300, 150, 50),
        }

    def manejar_eventos(self, eventos) -> bool:
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
        self.pantalla.fill(COLORS["background"])
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("¿Quién inicia?", True, COLORS["text"])
        self.pantalla.blit(texto, (300, 100))
        fuente_boton = pygame.font.Font(None, 36)
        nombres = {AZUL: "Azul", ROJO: "Rojo"}
        for jugador, rect in self.botones.items():
            color = COLORS["boton_hover"] if rect.collidepoint(pygame.mouse.get_pos()) else COLORS[jugador]
            pygame.draw.rect(self.pantalla, color, rect)
            texto_boton = fuente_boton.render(nombres[jugador], True, COLORS["text"])
            pos_texto = texto_boton.get_rect(center=rect.center)
            self.pantalla.blit(texto_boton, pos_texto)


class PantallaJuego:
    """Pantalla principal del juego"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.click_callback: Optional[Callable] = None
        self.tiempo_inicio = None  # Para controlar el tiempo transcurrido

        # Configurar botones
        self.boton_reiniciar = pygame.Rect(
            BOARD_OFFSET_X + TABLERO_TAMANO * CELL_SIZE + 50,  # a la derecha del tablero
            BOARD_OFFSET_Y,
            120,
            50,
        )
        self.boton_salir = pygame.Rect(
            BOARD_OFFSET_X + TABLERO_TAMANO * CELL_SIZE + 50,
            BOARD_OFFSET_Y + 70,
            120,
            50,
        )

    def establecer_callback_click(self, callback: Callable[[Posicion], None]) -> None:
        """Establece función para manejar clicks en el tablero"""
        self.click_callback = callback

    def manejar_eventos(self, eventos) -> Optional[str]:
        """
        Procesa eventos de pygame
        Retorna:
            - Posición del tablero si se clickeó allí
            - "reiniciar" si se clickeó el botón reiniciar
            - None en otros casos
        """
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Revisar si se clickeó el tablero
                pos_tablero = self.convertir_pixel_a_casilla(pos)
                if pos_tablero and self.click_callback:
                    self.click_callback(pos_tablero)

                # Revisar botones
                if self.boton_reiniciar.collidepoint(pos):
                    return "reiniciar"
                if self.boton_salir.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        return None

    def dibujar_tablero(self, estado: EstadoJuego) -> None:
        """Dibuja el tablero y las fichas"""
        self.pantalla.fill(COLORS["background"])

        # Dibujar tablero y fichas
        for y in range(TABLERO_TAMANO):
            for x in range(TABLERO_TAMANO):
                rect = pygame.Rect(
                    BOARD_OFFSET_X + x * CELL_SIZE,
                    BOARD_OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pygame.draw.rect(self.pantalla, COLORS["board"], rect)
                pygame.draw.rect(self.pantalla, COLORS["grid"], rect, 1)

                color = estado.tablero[y][x]
                if color != VACIO:
                    pos = Posicion(x, y)
                    es_cabeza = (pos == estado.cabeza_azul and color == AZUL) or (
                        pos == estado.cabeza_roja and color == ROJO
                    )
                    color_ficha = COLORS[color]
                    centro = rect.center
                    radio = CELL_SIZE // 2 - 5
                    pygame.draw.circle(self.pantalla, color_ficha, centro, radio)
                    if es_cabeza:
                        # Dibujar borde negro para la cabeza
                        pygame.draw.circle(self.pantalla, (0, 0, 0), centro, radio, 3)

        # Dibujar botones
        fuente = pygame.font.Font(None, 30)

        # Botón reiniciar
        color_reiniciar = COLORS["boton_hover"] if self.boton_reiniciar.collidepoint(pygame.mouse.get_pos()) else COLORS["boton"]
        pygame.draw.rect(self.pantalla, color_reiniciar, self.boton_reiniciar)
        texto_reiniciar = fuente.render("Reiniciar", True, COLORS["text"])
        self.pantalla.blit(texto_reiniciar, texto_reiniciar.get_rect(center=self.boton_reiniciar.center))

        # Botón salir
        color_salir = COLORS["boton_hover"] if self.boton_salir.collidepoint(pygame.mouse.get_pos()) else COLORS["boton"]
        pygame.draw.rect(self.pantalla, color_salir, self.boton_salir)
        texto_salir = fuente.render("Salir", True, COLORS["text"])
        self.pantalla.blit(texto_salir, texto_salir.get_rect(center=self.boton_salir.center))

    def dibujar_info_turno(
        self, turno_actual: str, juego_terminado: bool, ganador: Optional[str]
    ) -> None:
        """Dibuja información de turno, estado del juego y tiempo transcurrido"""
        fuente = pygame.font.Font(None, 36)

        # Texto de turno o ganador
        if juego_terminado:
            texto = f"¡{ganador.capitalize()} gana!" if ganador else "¡Empate!"
        else:
            texto = f"Turno: {turno_actual.capitalize()}"

        # Renderizar texto principal (centro arriba)
        superficie = fuente.render(texto, True, COLORS["text"])
        pos = superficie.get_rect(centerx=WINDOW_WIDTH // 2, y=BOARD_OFFSET_Y // 2)
        self.pantalla.blit(superficie, pos)

        # Calcular tiempo transcurrido en segundos
        if self.tiempo_inicio:
            tiempo_transcurrido = int(pygame.time.get_ticks() / 1000 - self.tiempo_inicio)
        else:
            tiempo_transcurrido = 0

        # Mostrar tiempo en la esquina superior derecha
        texto_tiempo = f"Tiempo: {tiempo_transcurrido}s"
        superficie_tiempo = fuente.render(texto_tiempo, True, COLORS["text"])
        pos_tiempo = superficie_tiempo.get_rect(topright=(WINDOW_WIDTH - 20, 20))
        self.pantalla.blit(superficie_tiempo, pos_tiempo)

    def convertir_pixel_a_casilla(
        self, pos_pixel: Tuple[int, int]
    ) -> Optional[Posicion]:
        """Convierte coordenadas de pixel a coordenadas de tablero"""
        x, y = pos_pixel
        if (
            BOARD_OFFSET_X <= x < BOARD_OFFSET_X + TABLERO_TAMANO * CELL_SIZE
            and BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + TABLERO_TAMANO * CELL_SIZE
        ):
            tablero_x = (x - BOARD_OFFSET_X) // CELL_SIZE
            tablero_y = (y - BOARD_OFFSET_Y) // CELL_SIZE
            return Posicion(tablero_x, tablero_y)
        return None



class GestorInterfaz:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake vs Snake")
        self.reloj = pygame.time.Clock()
        self.estado_actual = "dificultad"
        self.pantalla_dificultad = PantallaDificultad(self.pantalla)
        self.pantalla_turno = PantallaTurno(self.pantalla)
        self.pantalla_juego = PantallaJuego(self.pantalla)

    def ejecutar_bucle_principal(
        self, callback_juego_iniciado: Callable, callback_movimiento: Callable
    ) -> None:
        """
        Bucle principal de Pygame.
        Maneja selección de dificultad, turno y el juego.
        Permite reiniciar o salir, y muestra tiempo de partida.
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
                self.pantalla_dificultad.manejar_eventos(eventos)
                if self.pantalla_dificultad.dificultad_seleccionada is not None:
                    self.estado_actual = "turno"

            elif self.estado_actual == "turno":
                # Mostrar pantalla de selección de turno
                self.pantalla_turno.dibujar()
                self.pantalla_turno.manejar_eventos(eventos)
                if self.pantalla_turno.jugador_inicial is not None:
                    # Iniciar juego
                    callback_juego_iniciado(
                        self.pantalla_dificultad.dificultad_seleccionada,
                        self.pantalla_turno.jugador_inicial,
                    )
                    self.pantalla_juego.establecer_callback_click(callback_movimiento)
                    # Iniciar contador de tiempo
                    self.pantalla_juego.tiempo_inicio = pygame.time.get_ticks() / 1000
                    self.estado_actual = "juego"

            elif self.estado_actual == "juego":
                # Procesar clicks en tablero
                resultado = self.pantalla_juego.manejar_eventos(eventos)

                # Botones de Reiniciar y Cerrar
                mouse_pos = pygame.mouse.get_pos()
                boton_reiniciar = pygame.Rect(WINDOW_WIDTH - 180, 100, 160, 50)
                boton_cerrar = pygame.Rect(WINDOW_WIDTH - 180, 180, 160, 50)
                for evento in eventos:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if boton_reiniciar.collidepoint(mouse_pos):
                            # Reiniciar juego
                            self.estado_actual = "dificultad"
                            self.pantalla_dificultad.dificultad_seleccionada = None
                            self.pantalla_turno.jugador_inicial = None
                        elif boton_cerrar.collidepoint(mouse_pos):
                            ejecutando = False

                # Dibujar botones
                pygame.draw.rect(self.pantalla, COLORS["boton"], boton_reiniciar)
                pygame.draw.rect(self.pantalla, COLORS["boton"], boton_cerrar)
                fuente_boton = pygame.font.Font(None, 28)
                self.pantalla.blit(fuente_boton.render("Reiniciar", True, COLORS["text"]),
                                   boton_reiniciar.move(10, 10))
                self.pantalla.blit(fuente_boton.render("Cerrar juego", True, COLORS["text"]),
                                   boton_cerrar.move(10, 10))

                # Dibujar tablero y info
                estado_actual = callback_movimiento.__self__.motor_juego.obtener_estado_actual()
                juego_terminado, ganador = callback_movimiento.__self__.motor_juego.verificar_fin_juego()
                self.pantalla_juego.dibujar_tablero(estado_actual)
                self.pantalla_juego.dibujar_info_turno(
                    estado_actual.turno, juego_terminado, ganador
                )

            # Actualizar pantalla y controlar FPS
            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()

    def actualizar_display_juego(self, estado: EstadoJuego, turno: str, juego_terminado: bool, ganador: Optional[str]) -> None:
        if self.estado_actual == "juego":
            self.pantalla_juego.dibujar_tablero(estado)
            self.pantalla_juego.dibujar_info_turno(turno, juego_terminado, ganador)
