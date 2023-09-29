import pygame
import random
import math

FPS = 60
pygame.init()
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))


# Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.surface.Surface((16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = ancho // 2
        self.rect.y = altura // 2
        self.vida = 100
        self.direccion = pygame.Vector2(0, 0)
        self.velocidad = 10

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direccion.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direccion.x = 1
        else:
            self.direccion.x = 0

        if keys[pygame.K_UP]:
            self.direccion.y = -1
        elif keys[pygame.K_DOWN]:
            self.direccion.y = 1
        else:
            self.direccion.y = 0

    def update(self, dt):
        # Mover el jugador multiplicando la dirección por la velocidad
        self.input()
        self.rect.center += self.direccion * self.velocidad * dt

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, (0, 0, 255), self.rect)


# Rectangulos
class Asteroide(pygame.sprite.Sprite):
    colores = [(255, 0, 0)]

    def __init__(self, x, y, b, h, direccion, velocidad=0.5, *groups):
        super().__init__(groups)
        self.x = x
        self.y = y
        self.b = b
        self.h = h
        self.velocidad = velocidad
        self.direccion = direccion
        self.color = random.choice(self.colores)
        self.rect = pygame.Rect(x, y, b, h)

    def update(self, dt):
        self.rect.x += self.direccion.x * self.velocidad * dt
        self.rect.y += self.direccion.y * self.velocidad * dt

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def round_cuadrant(self, x):
        if x == 0:
            return 0
        if x < 0:
            return -1
        return 1

    def change_color(self):
        current_color = self.color
        new_color = random.choice(self.colores)
        if current_color != new_color:
            self.color = new_color
        else:
            self.change_color()


asteroides = pygame.sprite.Group()


def escoger_direccion(x, gap):
    if x <= 0:
        return 1
    if x >= gap:
        return -1
    return 0


def crearAsteroide():
    """
    :--------+----------------+-------:
    | -1, -1 | 0, -1          | 1, -1 |
    | -1, 0  | 0,0 (pantalla) | 1, 0  |
    | -1, 1  | 0, 1           | 1, 1  |
    '--------'----------------'-------'
    """
    # cuadrantes = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    x_ranges = [(-50, ancho + 50), (-50, -20)]
    y_ranges = [(altura + 20, altura + 50), (0, altura), (-50, -20)]
    y_range = random.choice(y_ranges)
    y = random.randint(y_range[0], y_range[1])
    x = 0
    if y < 0 or y > altura:
        x = random.randint(x_ranges[0][0], x_ranges[0][1])
    else:
        x = random.randint(x_ranges[1][0], x_ranges[1][1])
    direccion = pygame.Vector2(
        escoger_direccion(x, ancho), escoger_direccion(y, altura)
    )
    Asteroide(x, y, 20, 20, direccion, 5, asteroides)


# deltatime
current_time = pygame.time.get_ticks()
previous_time = current_time
# timers
asteroide_spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(asteroide_spawn_event, 500)

jugador = Jugador()
while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == asteroide_spawn_event:
            crearAsteroide()

    deltatime = (current_time - previous_time) / 1000.0
    previous_time = deltatime

    jugador.update(deltatime)
    if len(pygame.sprite.spritecollide(jugador, asteroides, True)):
        jugador.vida -= 10
        if jugador.vida < 0:
            print("Perdiste")
            pygame.quit()
            break

    for asteroide in asteroides.sprites():
        asteroide.update(deltatime)

    jugador.draw(pantalla)
    for asteroide in asteroides.sprites():
        asteroide.draw(pantalla)

    pygame.display.flip()
    clock.tick(FPS)
