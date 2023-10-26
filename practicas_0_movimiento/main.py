import pygame

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

# Movimiento uno
class Cuadrado(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 200, 20))
        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.direction = pygame.Vector2(1, 0)
        self.last_x = 1
        self.count_y = 0
        self.h_y = 30
        
    def update(self, dt, velocidad):
        print(self.rect.top, self.count_y, self.count_y * self.h_y)
        # detecta cuando se toca un borde
        if self.rect.right > ancho or self.rect.left < 0:
            self.last_x = self.direction.x
            self.direction.x = 0
            self.direction.y = 1
        self.rect.center += self.direction * dt * velocidad
        
cuadrado = pygame.sprite.GroupSingle(Cuadrado())
while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    cuadrado.update(deltatime, 10)
    # Draw
    cuadrado.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
