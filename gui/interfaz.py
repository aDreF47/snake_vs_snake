import pygame
import math
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


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
BOARD_OFFSET_X = 150
BOARD_OFFSET_Y = 150
CELL_SIZE = 70

# Paleta de colores moderna
COLORS = {
    "background": (32, 35, 42),  # Azul oscuro moderno
    "surface": (44, 47, 56),     # Superficie elevada
    "board": (60, 64, 75),       # Tablero
    "grid": (80, 85, 96),        # Líneas de grid
    "text": (255, 255, 255),     # Texto blanco
    "text_secondary": (180, 185, 200),  # Texto secundario
    "accent": (88, 166, 255),    # Azul accent
    "success": (82, 196, 26),    # Verde éxito
    "warning": (250, 173, 20),   # Amarillo advertencia
    "danger": (245, 108, 108),   # Rojo peligro
    
    # Colores de fichas con gradiente
    ROJO: (245, 108, 108),
    AZUL: (88, 166, 255),
    VACIO: (60, 64, 75),
    f'{ROJO}_cabeza': (255, 138, 138),
    f'{AZUL}_cabeza': (118, 196, 255),
    
    # Botones con estados
    "boton": (68, 72, 83),
    "boton_hover": (88, 92, 103),
    "boton_active": (108, 112, 123),
    "boton_disabled": (40, 43, 50),
    
    # Efectos
    "shadow": (20, 23, 30),
    "highlight": (255, 255, 255, 30),
    "glow": (88, 166, 255, 100),
}


class AnimacionManager:
    """Maneja las animaciones de la interfaz"""
    
    def __init__(self):
        self.animaciones = {}
        self.tiempo_actual = 0
    
    def actualizar(self, dt):
        self.tiempo_actual += dt
        # Limpiar animaciones completadas
        self.animaciones = {k: v for k, v in self.animaciones.items() 
                           if v.get('activa', True)}
    
    def agregar_pulsacion(self, pos, duracion=500):
        """Animación de pulsación al hacer click"""
        self.animaciones[f"pulse_{len(self.animaciones)}"] = {
            'tipo': 'pulse',
            'pos': pos,
            'inicio': self.tiempo_actual,
            'duracion': duracion,
            'activa': True
        }
    
    def dibujar_animaciones(self, pantalla):
        """Dibuja todas las animaciones activas"""
        for anim in self.animaciones.values():
            if anim['tipo'] == 'pulse':
                self.dibujar_pulsacion(pantalla, anim)
    
    def dibujar_pulsacion(self, pantalla, anim):
        """Dibuja efecto de pulsación"""
        progreso = (self.tiempo_actual - anim['inicio']) / anim['duracion']
        if progreso >= 1.0:
            anim['activa'] = False
            return
        
        radio = int(30 * progreso)
        alpha = int(100 * (1 - progreso))
        
        # Crear superficie temporal para transparencia
        temp_surface = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, (*COLORS["accent"][:3], alpha), 
                          (radio, radio), radio)
        
        pos = (anim['pos'][0] - radio, anim['pos'][1] - radio)
        pantalla.blit(temp_surface, pos)


class BotonModerno:
    """Botón moderno con efectos visuales"""
    
    def __init__(self, rect, texto, color_principal=None, icono=None):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.color_principal = color_principal or COLORS["boton"]
        self.icono = icono
        self.estado = "normal"  # normal, hover, active, disabled
        self.animacion_hover = 0
        self.sombra_offset = 4
    
    def actualizar(self, mouse_pos, mouse_pressed):
        """Actualiza el estado del botón basado en la interacción"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                self.estado = "active"
            else:
                self.estado = "hover"
            self.animacion_hover = min(1.0, self.animacion_hover + 0.15)
        else:
            self.estado = "normal"
            self.animacion_hover = max(0, self.animacion_hover - 0.15)
    
    def dibujar(self, pantalla):
        """Dibuja el botón con efectos"""
        # Colores basados en estado
        colores_estado = {
            "normal": self.color_principal,
            "hover": COLORS["boton_hover"],
            "active": COLORS["boton_active"],
            "disabled": COLORS["boton_disabled"]
        }
        
        color_actual = colores_estado[self.estado]
        
        # Sombra
        sombra_rect = self.rect.copy()
        sombra_rect.x += self.sombra_offset
        sombra_rect.y += self.sombra_offset
        pygame.draw.rect(pantalla, COLORS["shadow"], sombra_rect, border_radius=8)
        
        # Botón principal
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)
        
        # Borde de hover
        if self.animacion_hover > 0:
            alpha = int(50 * self.animacion_hover)
            temp_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, (*COLORS["accent"][:3], alpha), 
                           temp_surface.get_rect(), width=2, border_radius=8)
            pantalla.blit(temp_surface, self.rect.topleft)
        
        # Texto
        fuente = pygame.font.Font(None, 32)
        texto_surface = fuente.render(self.texto, True, COLORS["text"])
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        pantalla.blit(texto_surface, texto_rect)
    
    def fue_clickeado(self, pos):
        """Verifica si el botón fue clickeado"""
        return self.rect.collidepoint(pos) and self.estado != "disabled"


class PantallaDificultad:
    """Pantalla de selección de dificultad mejorada"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.dificultad_seleccionada: Optional[Dificultad] = None
        self.animacion_manager = AnimacionManager()

        # Configurar botones modernos
        self.botones = {
            Dificultad.PRINCIPIANTE: BotonModerno(
                (300, 250, 300, 60), "🌱 Principiante", COLORS["success"]
            ),
            Dificultad.NORMAL: BotonModerno(
                (300, 340, 300, 60), "⚡ Normal", COLORS["warning"]
            ),
            Dificultad.EXPERTO: BotonModerno(
                (300, 430, 300, 60), "🔥 Experto", COLORS["danger"]
            ),
        }

    def manejar_eventos(self, eventos) -> bool:
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.animacion_manager.agregar_pulsacion(pos)
                
                for dificultad, boton in self.botones.items():
                    if boton.fue_clickeado(pos):
                        self.dificultad_seleccionada = dificultad
                        return True
        return False

    def dibujar(self) -> None:
        # Fondo degradado
        self.dibujar_fondo_degradado()
        
        # Actualizar animaciones
        self.animacion_manager.actualizar(16.67)  # ~60 FPS
        
        # Título principal con sombra
        fuente_titulo = pygame.font.Font(None, 64)
        titulo_sombra = fuente_titulo.render("Selecciona Dificultad", True, COLORS["shadow"])
        titulo_principal = fuente_titulo.render("Selecciona Dificultad", True, COLORS["text"])
        
        titulo_rect = titulo_principal.get_rect(centerx=WINDOW_WIDTH // 2, y=120)
        self.pantalla.blit(titulo_sombra, (titulo_rect.x + 2, titulo_rect.y + 2))
        self.pantalla.blit(titulo_principal, titulo_rect)
        
        # Subtítulo
        fuente_sub = pygame.font.Font(None, 28)
        subtitulo = fuente_sub.render("Elige tu nivel de desafío", True, COLORS["text_secondary"])
        sub_rect = subtitulo.get_rect(centerx=WINDOW_WIDTH // 2, y=170)
        self.pantalla.blit(subtitulo, sub_rect)

        # Actualizar y dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for boton in self.botones.values():
            boton.actualizar(mouse_pos, mouse_pressed)
            boton.dibujar(self.pantalla)
        
        # Dibujar animaciones
        self.animacion_manager.dibujar_animaciones(self.pantalla)
        
        pygame.display.flip()
    
    def dibujar_fondo_degradado(self):
        """Dibuja un fondo con degradado"""
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            color = (
                int(COLORS["background"][0] * (1 - ratio * 0.3)),
                int(COLORS["background"][1] * (1 - ratio * 0.3)),
                int(COLORS["background"][2] * (1 - ratio * 0.3))
            )
            pygame.draw.line(self.pantalla, color, (0, y), (WINDOW_WIDTH, y))


class PantallaTurno:
    """Pantalla de selección de jugador inicial mejorada"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.jugador_inicial: Optional[str] = None
        self.animacion_manager = AnimacionManager()

        self.botones = {
            AZUL: BotonModerno((250, 350, 150, 80), "Azul", COLORS[AZUL]),
            ROJO: BotonModerno((500, 350, 150, 80), "Rojo", COLORS[ROJO]),
        }

    def manejar_eventos(self, eventos) -> bool:
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.animacion_manager.agregar_pulsacion(pos)
                
                for jugador, boton in self.botones.items():
                    if boton.fue_clickeado(pos):
                        self.jugador_inicial = jugador
                        return True
        return False

    def dibujar(self) -> None:
        self.dibujar_fondo_degradado()
        self.animacion_manager.actualizar(16.67)

        # Título
        fuente_titulo = pygame.font.Font(None, 64)
        titulo = fuente_titulo.render("¿Quién inicia?", True, COLORS["text"])
        titulo_rect = titulo.get_rect(centerx=WINDOW_WIDTH // 2, y=150)
        self.pantalla.blit(titulo, titulo_rect)
        
        # Subtítulo
        fuente_sub = pygame.font.Font(None, 28)
        subtitulo = fuente_sub.render("Selecciona el color que jugará primero", True, COLORS["text_secondary"])
        sub_rect = subtitulo.get_rect(centerx=WINDOW_WIDTH // 2, y=200)
        self.pantalla.blit(subtitulo, sub_rect)

        # Mostrar íconos de serpientes
        self.dibujar_preview_serpientes()

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for boton in self.botones.values():
            boton.actualizar(mouse_pos, mouse_pressed)
            boton.dibujar(self.pantalla)
        
        self.animacion_manager.dibujar_animaciones(self.pantalla)
        pygame.display.flip()
    
    def dibujar_preview_serpientes(self):
        """Dibuja preview de las serpientes"""
        # Serpiente azul
        for i in range(3):
            pos = (280 + i * 25, 290)
            color = COLORS[f"{AZUL}_cabeza"] if i == 2 else COLORS[AZUL]
            pygame.draw.circle(self.pantalla, color, pos, 12)
        
        # Serpiente roja
        for i in range(3):
            pos = (530 + i * 25, 290)
            color = COLORS[f"{ROJO}_cabeza"] if i == 2 else COLORS[ROJO]
            pygame.draw.circle(self.pantalla, color, pos, 12)
    
    def dibujar_fondo_degradado(self):
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            color = (
                int(COLORS["background"][0] * (1 - ratio * 0.3)),
                int(COLORS["background"][1] * (1 - ratio * 0.3)),
                int(COLORS["background"][2] * (1 - ratio * 0.3))
            )
            pygame.draw.line(self.pantalla, color, (0, y), (WINDOW_WIDTH, y))


class PantallaJuego:
    """Pantalla principal del juego mejorada"""

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.click_callback: Optional[Callable] = None
        self.animacion_manager = AnimacionManager()
        self.hover_pos = None
        self.animacion_tiempo = 0

    def establecer_callback_click(self, callback: Callable[[Posicion], None]) -> None:
        self.click_callback = callback

    def manejar_eventos(self, eventos) -> Optional[Posicion]:
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and self.click_callback:
                pos = pygame.mouse.get_pos()
                self.animacion_manager.agregar_pulsacion(pos)
                pos_tablero = self.convertir_pixel_a_casilla(pos)
                if pos_tablero:
                    self.click_callback(pos_tablero)
            
            if evento.type == pygame.MOUSEMOTION:
                self.hover_pos = self.convertir_pixel_a_casilla(pygame.mouse.get_pos())
        
        return None

    def dibujar_tablero(self, estado: EstadoJuego) -> None:
        # Actualizar animaciones
        self.animacion_manager.actualizar(16.67)
        self.animacion_tiempo += 16.67

        # Fondo degradado
        self.dibujar_fondo_degradado()
        
        # Panel de información
        self.dibujar_panel_info(estado)

        # Tablero con efectos
        self.dibujar_tablero_mejorado(estado)
        
        # Efectos de hover
        if self.hover_pos:
            self.dibujar_hover_effect(self.hover_pos)
        
        # Animaciones
        self.animacion_manager.dibujar_animaciones(self.pantalla)

    def dibujar_tablero_mejorado(self, estado: EstadoJuego):
        """Dibuja el tablero con efectos visuales mejorados"""
        # Sombra del tablero
        sombra_rect = pygame.Rect(BOARD_OFFSET_X - 10, BOARD_OFFSET_Y - 10, 
                                 TABLERO_TAMANO * CELL_SIZE + 20, 
                                 TABLERO_TAMANO * CELL_SIZE + 20)
        pygame.draw.rect(self.pantalla, COLORS["shadow"], sombra_rect, border_radius=15)
        
        # Fondo del tablero
        tablero_rect = pygame.Rect(BOARD_OFFSET_X - 5, BOARD_OFFSET_Y - 5,
                                  TABLERO_TAMANO * CELL_SIZE + 10,
                                  TABLERO_TAMANO * CELL_SIZE + 10)
        pygame.draw.rect(self.pantalla, COLORS["surface"], tablero_rect, border_radius=10)
        
        for y in range(TABLERO_TAMANO):
            for x in range(TABLERO_TAMANO):
                rect = pygame.Rect(
                    BOARD_OFFSET_X + x * CELL_SIZE,
                    BOARD_OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                # Casilla base con borde redondeado
                pygame.draw.rect(self.pantalla, COLORS["board"], rect, border_radius=8)
                pygame.draw.rect(self.pantalla, COLORS["grid"], rect, width=1, border_radius=8)

                # Coordenadas en las esquinas
                if y == 0:  # Números de columna arriba
                    fuente_coord = pygame.font.Font(None, 20)
                    coord_text = fuente_coord.render(str(x), True, COLORS["text_secondary"])
                    coord_pos = (rect.centerx - 5, rect.top - 20)
                    self.pantalla.blit(coord_text, coord_pos)
                
                if x == 0:  # Números de fila a la izquierda
                    fuente_coord = pygame.font.Font(None, 20)
                    coord_text = fuente_coord.render(str(y), True, COLORS["text_secondary"])
                    coord_pos = (rect.left - 20, rect.centery - 5)
                    self.pantalla.blit(coord_text, coord_pos)

                # Dibujar ficha si hay
                if estado.tablero[y][x] != VACIO:
                    self.dibujar_ficha_mejorada(rect, estado, Posicion(x, y))

    def dibujar_ficha_mejorada(self, rect, estado, pos):
        """Dibuja fichas con efectos visuales mejorados"""
        color = estado.tablero[pos.y][pos.x]
        
        # Determinar si es cabeza
        es_cabeza = ((pos == estado.cabeza_azul and color == AZUL) or 
                    (pos == estado.cabeza_roja and color == ROJO))

        # Color de la ficha
        if es_cabeza:
            color_ficha = COLORS[f"{color}_cabeza"]
            radio = CELL_SIZE // 2 - 8
            # Efecto de brillo en la cabeza
            self.dibujar_efecto_brillo(rect.center, radio + 5)
        else:
            color_ficha = COLORS[color]
            radio = CELL_SIZE // 2 - 12

        # Sombra de la ficha
        sombra_pos = (rect.centerx + 2, rect.centery + 2)
        pygame.draw.circle(self.pantalla, COLORS["shadow"], sombra_pos, radio)
        
        # Ficha principal
        pygame.draw.circle(self.pantalla, color_ficha, rect.center, radio)
        
        # Borde de la ficha
        pygame.draw.circle(self.pantalla, (255, 255, 255, 50), rect.center, radio, width=2)
        
        # Efecto de destello en cabezas
        if es_cabeza:
            destello_offset = int(5 * math.sin(self.animacion_tiempo * 0.005))
            destello_pos = (rect.centerx - radio//3, rect.centery - radio//3)
            pygame.draw.circle(self.pantalla, (255, 255, 255, 100), destello_pos, 4)

    def dibujar_efecto_brillo(self, pos, radio):
        """Dibuja efecto de brillo alrededor de las cabezas"""
        # Crear superficie temporal para el brillo
        brillo_surface = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        brillo_alpha = int(30 + 20 * math.sin(self.animacion_tiempo * 0.01))
        pygame.draw.circle(brillo_surface, (*COLORS["accent"][:3], brillo_alpha), 
                          (radio, radio), radio)
        
        brillo_pos = (pos[0] - radio, pos[1] - radio)
        self.pantalla.blit(brillo_surface, brillo_pos)

    def dibujar_hover_effect(self, pos):
        """Dibuja efecto de hover sobre casillas"""
        if pos:
            rect = pygame.Rect(
                BOARD_OFFSET_X + pos.x * CELL_SIZE,
                BOARD_OFFSET_Y + pos.y * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            
            # Efecto de resaltado
            highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            alpha = int(50 + 20 * math.sin(self.animacion_tiempo * 0.02))
            pygame.draw.rect(highlight_surface, (*COLORS["accent"][:3], alpha), 
                           highlight_surface.get_rect(), border_radius=8)
            self.pantalla.blit(highlight_surface, rect.topleft)

    def dibujar_panel_info(self, estado):
        """Dibuja panel lateral con información del juego"""
        panel_x = 50
        panel_y = 150
        panel_width = 80
        panel_height = 400
        
        # Fondo del panel
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.pantalla, COLORS["surface"], panel_rect, border_radius=10)
        pygame.draw.rect(self.pantalla, COLORS["grid"], panel_rect, width=2, border_radius=10)
        
        # Contador de fichas
        azul_count = sum(row.count(AZUL) for row in estado.tablero)
        rojo_count = sum(row.count(ROJO) for row in estado.tablero)
        
        fuente_info = pygame.font.Font(None, 24)
        
        # Fichas azules
        pygame.draw.circle(self.pantalla, COLORS[AZUL], (panel_x + 25, panel_y + 40), 12)
        azul_text = fuente_info.render(str(azul_count), True, COLORS["text"])
        self.pantalla.blit(azul_text, (panel_x + 45, panel_y + 32))
        
        # Fichas rojas
        pygame.draw.circle(self.pantalla, COLORS[ROJO], (panel_x + 25, panel_y + 80), 12)
        rojo_text = fuente_info.render(str(rojo_count), True, COLORS["text"])
        self.pantalla.blit(rojo_text, (panel_x + 45, panel_y + 72))

    def dibujar_info_turno(self, turno_actual: str, juego_terminado: bool, ganador: Optional[str]) -> None:
        """Dibuja información de turno mejorada"""
        # Panel de estado en la parte superior
        estado_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, 50, 400, 80)
        pygame.draw.rect(self.pantalla, COLORS["surface"], estado_rect, border_radius=12)
        pygame.draw.rect(self.pantalla, COLORS["grid"], estado_rect, width=2, border_radius=12)

        fuente_estado = pygame.font.Font(None, 42)

        if juego_terminado:
            if ganador:
                color_ganador = COLORS[ganador]
                texto = f"¡{ganador.upper()} GANA! 🎉"
                # Efecto de celebración
                self.dibujar_efecto_celebracion()
            else:
                color_ganador = COLORS["text_secondary"]
                texto = "¡EMPATE! 🤝"
        else:
            color_ganador = COLORS[turno_actual]
            texto = f"Turno: {turno_actual.upper()}"
            
            # Indicador visual del jugador actual
            indicador_pos = (WINDOW_WIDTH // 2 - 150, 75)
            pygame.draw.circle(self.pantalla, color_ganador, indicador_pos, 15)

        # Texto del estado con sombra
        texto_sombra = fuente_estado.render(texto, True, COLORS["shadow"])
        texto_principal = fuente_estado.render(texto, True, color_ganador)
        
        texto_rect = texto_principal.get_rect(center=estado_rect.center)
        self.pantalla.blit(texto_sombra, (texto_rect.x + 2, texto_rect.y + 2))
        self.pantalla.blit(texto_principal, texto_rect)

        pygame.display.flip()

    def dibujar_efecto_celebracion(self):
        """Efecto visual de celebración cuando alguien gana"""
        for i in range(10):
            x = (WINDOW_WIDTH // 2) + (i - 5) * 50
            y = 100 + int(20 * math.sin(self.animacion_tiempo * 0.01 + i))
            color = COLORS["warning"] if i % 2 == 0 else COLORS["success"]
            pygame.draw.circle(self.pantalla, color, (x, y), 8)

    def convertir_pixel_a_casilla(self, pos_pixel: Tuple[int, int]) -> Optional[Posicion]:
        x, y = pos_pixel

        if (BOARD_OFFSET_X <= x < BOARD_OFFSET_X + TABLERO_TAMANO * CELL_SIZE and 
            BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + TABLERO_TAMANO * CELL_SIZE):

            tablero_x = (x - BOARD_OFFSET_X) // CELL_SIZE
            tablero_y = (y - BOARD_OFFSET_Y) // CELL_SIZE
            return Posicion(tablero_x, tablero_y)

        return None

    def dibujar_fondo_degradado(self):
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            color = (
                int(COLORS["background"][0] * (1 - ratio * 0.2)),
                int(COLORS["background"][1] * (1 - ratio * 0.2)),
                int(COLORS["background"][2] * (1 - ratio * 0.2))
            )
            pygame.draw.line(self.pantalla, color, (0, y), (WINDOW_WIDTH, y))


class GestorInterfaz:
    """Coordina todas las pantallas con efectos mejorados"""

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake vs Snake - Estrategia Épica")
        pygame.display.set_icon(pygame.Surface((32, 32)))  # Icono personalizable
        self.reloj = pygame.time.Clock()

        # Estados de la interfaz
        self.estado_actual = "dificultad"

        # Pantallas mejoradas
        self.pantalla_dificultad = PantallaDificultad(self.pantalla)
        self.pantalla_turno = PantallaTurno(self.pantalla)
        self.pantalla_juego = PantallaJuego(self.pantalla)

        # Variables para almacenar el estado del juego
        self.estado_juego_actual = None
        self.turno_actual = None
        self.juego_terminado = False
        self.ganador_actual = None

    def ejecutar_bucle_principal(self, callback_juego_iniciado: Callable, callback_movimiento: Callable) -> None:
        ejecutando = True
        while ejecutando:
            dt = self.reloj.tick(60)  # 60 FPS para animaciones suaves
            eventos = pygame.event.get()
            
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    ejecutando = False

            if self.estado_actual == "dificultad":
                self.pantalla_dificultad.dibujar()
                if self.pantalla_dificultad.manejar_eventos(eventos):
                    self.estado_actual = "turno"

            elif self.estado_actual == "turno":
                self.pantalla_turno.dibujar()
                if self.pantalla_turno.manejar_eventos(eventos):
                    callback_juego_iniciado(
                        self.pantalla_dificultad.dificultad_seleccionada,
                        self.pantalla_turno.jugador_inicial,
                    )
                    self.pantalla_juego.establecer_callback_click(callback_movimiento)
                    self.estado_actual = "juego"

            elif self.estado_actual == "juego":
                self.pantalla_juego.manejar_eventos(eventos)
                
                # Dibujar el estado actual del juego siempre
                if self.estado_juego_actual:
                    self.pantalla_juego.dibujar_tablero(self.estado_juego_actual)
                    self.pantalla_juego.dibujar_info_turno(
                        self.turno_actual, self.juego_terminado, self.ganador_actual
                    )

            # Actualizar pantalla se hace en cada pantalla individualmente
            # para mejor control de las animaciones

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
        # Almacenar el estado para redibujarlo en el bucle principal
        self.estado_juego_actual = estado
        self.turno_actual = turno
        self.juego_terminado = juego_terminado
        self.ganador_actual = ganador

    def cambiar_cursor(self, tipo="normal"):
        """Cambia el cursor según el contexto"""
        cursores = {
            "normal": pygame.SYSTEM_CURSOR_ARROW,
            "mano": pygame.SYSTEM_CURSOR_HAND,
            "espera": pygame.SYSTEM_CURSOR_WAIT
        }
        pygame.mouse.set_cursor(cursores.get(tipo, pygame.SYSTEM_CURSOR_ARROW))

    def mostrar_transicion(self, texto="Cargando...", duracion=1000):
        """Muestra una transición suave entre pantallas"""
        inicio = pygame.time.get_ticks()
        fuente = pygame.font.Font(None, 48)
        
        while pygame.time.get_ticks() - inicio < duracion:
            # Fondo semi-transparente
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(COLORS["background"])
            self.pantalla.blit(overlay, (0, 0))
            
            # Texto de transición
            texto_surface = fuente.render(texto, True, COLORS["text"])
            texto_rect = texto_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.pantalla.blit(texto_surface, texto_rect)
            
            # Barra de progreso animada
            progreso = (pygame.time.get_ticks() - inicio) / duracion
            barra_width = 300
            barra_height = 6
            barra_x = (WINDOW_WIDTH - barra_width) // 2
            barra_y = WINDOW_HEIGHT // 2 + 50
            
            # Fondo de la barra
            pygame.draw.rect(self.pantalla, COLORS["grid"], 
                           (barra_x, barra_y, barra_width, barra_height), border_radius=3)
            
            # Progreso de la barra
            pygame.draw.rect(self.pantalla, COLORS["accent"],
                           (barra_x, barra_y, int(barra_width * progreso), barra_height), 
                           border_radius=3)
            
            pygame.display.flip()
            self.reloj.tick(60)
            
            # Procesar eventos para evitar que se cuelgue
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def reproducir_sonido(self, tipo):
        """Reproduce efectos de sonido (placeholder para futura implementación)"""
        # Aquí se pueden agregar efectos de sonido
        # pygame.mixer.Sound("assets/click.wav").play()
        pass

    def vibrar_pantalla(self, intensidad=5, duracion=100):
        """Efecto de vibración de pantalla para eventos importantes"""
        inicio = pygame.time.get_ticks()
        pos_original = (0, 0)
        
        while pygame.time.get_ticks() - inicio < duracion:
            import random
            offset_x = random.randint(-intensidad, intensidad)
            offset_y = random.randint(-intensidad, intensidad)
            
            # Esto requeriría reescribir todo en una superficie temporal
            # Por ahora es un placeholder para efectos futuros
            pygame.time.wait(16)  # ~60 FPS

    def obtener_info_rendimiento(self):
        """Obtiene información de rendimiento para debugging"""
        fps = self.reloj.get_fps()
        return {
            'fps': round(fps, 1),
            'estado': self.estado_actual,
            'resolucion': f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        }

    def mostrar_ayuda(self):
        """Muestra pantalla de ayuda con las reglas del juego"""
        mostrar_ayuda = True
        while mostrar_ayuda:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        mostrar_ayuda = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mostrar_ayuda = False

            # Fondo semi-transparente
            self.pantalla.fill(COLORS["background"])
            
            # Panel de ayuda
            panel_rect = pygame.Rect(100, 50, WINDOW_WIDTH-200, WINDOW_HEIGHT-100)
            pygame.draw.rect(self.pantalla, COLORS["surface"], panel_rect, border_radius=15)
            pygame.draw.rect(self.pantalla, COLORS["accent"], panel_rect, width=3, border_radius=15)
            
            # Título
            fuente_titulo = pygame.font.Font(None, 48)
            titulo = fuente_titulo.render("🎯 Reglas del Juego", True, COLORS["text"])
            titulo_rect = titulo.get_rect(centerx=WINDOW_WIDTH//2, y=80)
            self.pantalla.blit(titulo, titulo_rect)
            
            # Reglas
            fuente_regla = pygame.font.Font(None, 24)
            reglas = [
                "• El objetivo es bloquear al oponente sin movimientos válidos",
                "• Las fichas se colocan adyacentes a la cabeza de tu serpiente",
                "• La cabeza es siempre la última ficha colocada",
                "• No puedes chocar con serpientes existentes",
                "• El tablero tiene wraparound (bordes conectados)",
                "• Gana quien deje al oponente sin movimientos",
                "",
                "🎮 Controles:",
                "• Click en casilla vacía para colocar ficha",
                "• ESC para cerrar esta ayuda",
                "",
                "💡 Click en cualquier lugar para continuar..."
            ]
            
            y_pos = 150
            for regla in reglas:
                color = COLORS["text"] if regla.startswith("•") or regla.startswith("🎮") else COLORS["text_secondary"]
                if regla.startswith("💡"):
                    color = COLORS["accent"]
                    
                texto = fuente_regla.render(regla, True, color)
                self.pantalla.blit(texto, (130, y_pos))
                y_pos += 35
            
            pygame.display.flip()
            self.reloj.tick(60)