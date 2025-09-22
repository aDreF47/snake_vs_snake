import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración del tablero
FILAS, COLUMNAS = 7, 7
ANCHO, ALTO = 560, 560
CELDA = ANCHO // COLUMNAS
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake vs Snake GUI Test")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Tablero vacío
tablero = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Posiciones iniciales de las serpientes
cabeza_azul = (0, 0)
cabeza_rojo = (6, 6)
tablero[cabeza_azul[1]][cabeza_azul[0]] = 'AZUL'
tablero[cabeza_rojo[1]][cabeza_rojo[0]] = 'ROJO'

# Reloj para FPS
clock = pygame.time.Clock()

def dibujar_tablero():
    screen.fill(BLANCO)
    # Dibujar rejilla
    for x in range(COLUMNAS):
        for y in range(FILAS):
            rect = pygame.Rect(x*CELDA, y*CELDA, CELDA, CELDA)
            pygame.draw.rect(screen, NEGRO, rect, 1)  # borde
            if tablero[y][x] == 'AZUL':
                pygame.draw.rect(screen, AZUL, rect.inflate(-4, -4))
            elif tablero[y][x] == 'ROJO':
                pygame.draw.rect(screen, ROJO, rect.inflate(-4, -4))
    pygame.display.flip()

def obtener_celda_click(pos_mouse):
    x, y = pos_mouse
    col = x // CELDA
    fila = y // CELDA
    return col, fila

# Bucle principal
running = True
turno = 'AZUL'  # turno inicial
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            col, fila = obtener_celda_click(event.pos)
            # Solo coloca ficha si la celda está vacía
            if tablero[fila][col] is None:
                tablero[fila][col] = turno
                print(f"{turno} colocó ficha en ({col}, {fila})")
                # Alternar turno
                turno = 'ROJO' if turno == 'AZUL' else 'AZUL'

    dibujar_tablero()
    clock.tick(30)

pygame.quit()
sys.exit()
