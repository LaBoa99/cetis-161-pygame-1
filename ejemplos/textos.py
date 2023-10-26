import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mostrar Texto en Pygame")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Crear una fuente
font = pygame.font.Font(os.path.join("fonts", "Minecraft.ttf"), 36)  # Fuente y tamaño

# Crear un texto
text = font.render(f"Hola, Mundo!", True, white, (100, 200, 12))

# Posición del texto
text_rect = text.get_rect()
text_rect.center = (screen_width // 2, screen_height // 2)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el fondo
    screen.fill(black)

    # Dibujar el texto
    screen.blit(text, text_rect)

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
