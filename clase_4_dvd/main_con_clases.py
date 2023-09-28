import pygame
import random

FPS = 60
pygame.init()
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))


# Rectangulos
class Rectangulo:
    colores = [(100, 200, 120), (50, 20, 100), (255, 20, 100), (0, 0, 255), (255, 0, 0)]

    def __init__(self, x, y, b, h, velocidad=20):
        self.x = x
        self.y = y
        self.b = b
        self.h = h
        self.velocidad = velocidad
        self.direccion = (
            pygame.Vector2(1, 1)
            if random.randint(1, 2) == 1
            else pygame.Vector2(-1, -1)
        )
        self.color = random.choice(self.colores)
        self.rect = pygame.Rect(x, y, b, h)

    def update(self, dt):
        self.rect.x += self.direccion.x * self.velocidad * dt
        self.rect.y += self.direccion.y * self.velocidad * dt
        if self.rect.x <= 0:
            self.direccion.x = 1
        if self.rect.x + self.b >= ancho:
            self.direccion.x = -1
        if self.rect.y <= 0:
            self.direccion.y = 1
        if self.rect.y + self.h >= altura:
            self.direccion.y = -1

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def change_color(self):
        current_color = self.color
        new_color = random.choice(self.colores)
        if current_color != new_color:
            self.color = new_color
        else:
            self.change_color()


NUM_RECTS = 20
rects = []
for i in range(NUM_RECTS):
    rects.append(
        Rectangulo(
            random.randint(20, ancho - 50),
            random.randint(20, altura - 50),
            30,
            30,
        )
    )
# deltatime
current_time = pygame.time.get_ticks()
previous_time = current_time
while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("Quitando un rectangulo de la lista")
                rects.pop()
            elif event.key == pygame.K_2:
                print("Cambiando color")
                for rect in rects:
                    rect.change_color()

    deltatime = (current_time - previous_time) / 1000.0
    previous_time = deltatime

    for rect in rects:
        rect.update(deltatime)

    for rect in rects:
        rect.draw(pantalla)

    pygame.display.flip()
    clock.tick(FPS)
