import pygame
import random

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

# Rectangulo
colores = [(100, 200, 120), (50, 20, 100), (255, 20, 100), (0, 0, 255), (255, 0, 0)]
rectangulo_velocidad = 9
rectangulo_base = 100
rectangulo_altura = 50
rectangulo_x = ancho // 2
rectangulo_y = altura // 2
rectangulo_color = random.choice(colores)
rectangulo = pygame.Rect(rectangulo_x, rectangulo_y, rectangulo_base, rectangulo_altura)
rectangulo_direccion = pygame.Vector2(1, 1)
while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime

    # Movimiento de rectangulo
    rectangulo.x += rectangulo_velocidad * rectangulo_direccion.x * deltatime
    rectangulo.y += rectangulo_velocidad * rectangulo_direccion.y * deltatime

    if rectangulo.x <= 0:
        rectangulo_direccion.x = 1
        rectangulo_color = random.choice(colores)
    if rectangulo.x + rectangulo_base >= ancho:
        rectangulo_direccion.x = -1
        rectangulo_color = random.choice(colores)
    if rectangulo.y <= 0:
        rectangulo_direccion.y = 1
        rectangulo_color = random.choice(colores)
    if rectangulo.y + rectangulo_altura >= altura:
        rectangulo_direccion.y = -1
        rectangulo_color = random.choice(colores)

    # Draw
    pygame.draw.rect(
        pantalla,
        rectangulo_color,
        rectangulo,
    )
    # Final
    pygame.display.flip()
    clock.tick(fps)
