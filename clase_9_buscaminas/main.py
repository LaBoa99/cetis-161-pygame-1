import pygame
from pygame.sprite import AbstractGroup

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (320, 320)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

CUADRADOS = 8
CUADRADO_W = ancho // CUADRADOS

class Casilla(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((w, h))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.content_image = pygame.Surface((w - 5, h - 5))
        self.content_image.fill((200, 200, 200))
        self.content_rect = self.content_image.get_rect()
        self.content_rect.center = self.rect.center
        
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        screen.blit(self.content_image, self.content_rect)
        
casillas = pygame.sprite.Group()
for i in range(CUADRADOS):
    for j in range(CUADRADOS):
        Casilla(i * CUADRADO_W, j * CUADRADO_W, CUADRADO_W, CUADRADO_W, casillas)

while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == pygame.BUTTON_LEFT:
                for casilla in casillas.sprites():
                    if casilla.rect.collidepoint(x, y):
                        print(casilla)
                        break
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime

    # Draw
    for casilla in casillas.sprites():
        casilla.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
