from typing import Iterable, Union, Any
import pygame
import random
import os
from enum import Enum
from pygame.sprite import AbstractGroup

# Configuración
scrip_dir = os.path.dirname(__file__)
pygame.init()
fps = 60
clock = pygame.time.Clock()

ANCHO, ALTURA = (480, 320)
pantalla = pygame.display.set_mode((ANCHO, ALTURA))


class EVENTOS(Enum):
    SPAWN_PIPE = pygame.USEREVENT + 1


class Area(pygame.sprite.Sprite):
    def __init__(self, rect, sprite_url, *groups) -> None:
        super().__init__(*groups)
        self.rect = rect
        self.image = pygame.image.load(os.path.join(scrip_dir, f"sprites\{sprite_url}"))
        self.image = pygame.transform.scale(self.image, (rect.width, rect.height))

    def update(self, dt):
        self.rect.x -= 10 * dt
        if self.rect.x + self.rect.width < 0:
            self.kill()


class Jugador(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(scrip_dir, "sprites\\flappy_bird.png")
        )
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = ALTURA - 32
        self.salto = -20
        self.velocidad_y = 0

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.velocidad_y = self.salto

    def update(self, dt):
        self.input()
        self.velocidad_y += 9.8 * dt
        self.rect.y += self.velocidad_y * dt
        if self.rect.y + 32 >= ALTURA:
            self.rect.y = ALTURA - 32
            self.velocidad_y = 0
        if self.rect.y < 0:
            self.rect.y = 1


class Pipe(pygame.sprite.Group):
    def __init__(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        super().__init__(*sprites)
        self.areas = self.genAreas(4)
        self.add(self.areas)

    def genAreas(self, numAreas):
        hueco = random.randint(0, numAreas - 1)
        ancho, alto = 50, ALTURA // numAreas
        areas = []
        for index in range(numAreas):
            if hueco == index:
                continue
            rect = pygame.Rect(0, index * alto, ancho, alto)
            rect.x = ANCHO + 50
            area = Area(rect, self.chooseSprite(index, hueco), self)
            areas.append(area)
        return areas

    def chooseSprite(self, index, hueco):
        if index == hueco - 1:
            return "flappy_todown.png"
        elif index == hueco + 1:
            return "flappy_totop.png"
        return "flappy_pipe.png"

    def canBeRemoved(self):
        if all(area.rect.right <= 0 for area in self.areas):
            return True
        return False


# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time
pipes_group = pygame.sprite.Group()
pipes = []
jugador = pygame.sprite.GroupSingle(Jugador())
pygame.time.set_timer(EVENTOS.SPAWN_PIPE.value, 3000)
while True:
    pantalla.fill((0, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == EVENTOS.SPAWN_PIPE.value:
            pipe = Pipe()
            pipes.append(pipe)
            pipes_group.add(pipe)
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    jugador.update(deltatime)
    pipes_group.update(deltatime)
    if pygame.sprite.spritecollide(jugador.sprite, pipes_group, False):
        pipes_group.empty()
        pipes.clear()
    for pipe in pipes:
        if pipe.canBeRemoved():
            pipes.remove(pipe)
            pipes_group.remove(pipe)
    # Draw
    jugador.draw(pantalla)
    pipes_group.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
