import pygame
from enum import Enum
import sys


class EVENTS(Enum):
    PRIMER_EVENTO = pygame.USEREVENT + 1
    SEGUNDO_EVENTO = pygame.USEREVENT + 2


# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana_ancho = 400
ventana_alto = 300
ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
pygame.display.set_caption("Temporizador en Pygame")

# Configuración de colores
blanco = (255, 255, 255)

# Configuración del temporizador
pygame.time.set_timer(
    EVENTS.PRIMER_EVENTO.value, 1000
)  # Cada 1000 milisegundos (1 segundo)
pygame.time.set_timer(
    EVENTS.SEGUNDO_EVENTO.value, 2000
)  # Cada 2000 milisegundos (2 segundo)

# Fuente para mostrar el tiempo restante
fuente = pygame.font.Font(None, 36)

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == EVENTS.PRIMER_EVENTO.value:
            print(EVENTS.PRIMER_EVENTO)
        elif evento.type == EVENTS.SEGUNDO_EVENTO.value:
            print(EVENTS.SEGUNDO_EVENTO)

    ventana.fill(blanco)

    # Mostrar el tiempo restante en la ventana
    texto = fuente.render(str("Opa"), True, (0, 0, 0))
    ventana.blit(texto, (ventana_ancho // 2 - 20, ventana_alto // 2 - 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
