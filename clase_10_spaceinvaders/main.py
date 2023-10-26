import os
import random
from enum import Enum

import pygame
import utils as UTILS

# Configuración
scrip_dir = os.path.dirname(__file__)
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 480)
pantalla = pygame.display.set_mode((ancho, altura))
SPRITESHEET = pygame.image.load(os.path.join(scrip_dir, "space_sprites.png")).convert_alpha()
FRAME_W = 11
FRAME_H = 8
SCALE_FACTOR = 4
# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

# ENUMS
class EVENTS(Enum):
    SPAWN_ALIENS = pygame.USEREVENT + 1
    SPAWN_CAGES = pygame.USEREVENT + 2


# CLASES
class Alien(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.images = UTILS.loadFrames(SPRITESHEET, FRAME_W, FRAME_H, 0, 2)
        for i in range(len(self.images)):
            self.images[i] = UTILS.scale_image(self.images[i], SCALE_FACTOR)
        self.current_frame = 0
        
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        
        self.frame_timer = 0 # contador
        self.frame_delay = 10 # delay 
        
    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.current_frame = 0
            self.image = self.images[self.current_frame]
            self.frame_timer = 0
        

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, v=-1, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((2 * SCALE_FACTOR, 3 * SCALE_FACTOR))
        self.image.fill((100, 200, 10))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]      
          
        self.velocidad = 20
        self.direction = pygame.Vector2(0, v)
    
    def update(self, dt) -> None:
        self.rect.center += self.velocidad * self.direction * dt
        if self.rect.bottom < 0:
            self.kill()
        
class Corazon(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.image = UTILS.loadFrames(SPRITESHEET, FRAME_W, FRAME_H, 3, 1, FRAME_W).pop()
        self.image = UTILS.scale_image(self.image, SCALE_FACTOR - 2)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

class Cage(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = UTILS.loadFrames(SPRITESHEET, FRAME_W, FRAME_H, 3, 1).pop()
        self.image = UTILS.scale_image(self.image, SCALE_FACTOR)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(0, ancho - self.rect.width), -self.rect.width)
        
        self.direction = pygame.Vector2(0, 1)
        self.vel = 10
    
    def update(self, dt):
        self.rect.center += self.direction * self.vel * dt
        if self.rect.top > altura:
            self.kill()
        
class Jugador(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = UTILS.loadFrames(SPRITESHEET, FRAME_W, FRAME_H, 2, 1).pop()
        self.image = UTILS.scale_image(self.image, SCALE_FACTOR)
        self.rect = self.image.get_rect()
        
        # posicion inicial del jugador
        self.rect.centerx = ancho // 2
        self.rect.bottom = altura - 25
        
        # movimiento
        self.velocidad = 10
        self.direction = pygame.Vector2(0, 0)
        
        self.vida = 0
        self.corazones = pygame.sprite.Group()
        for _ in range(5):
            self.add_corazon()
    
    def add_corazon(self):
        self.vida += 1
        Corazon(ancho - ((FRAME_W * (SCALE_FACTOR - 2)) * self.vida) - (2 * self.vida), altura - FRAME_H, self.corazones)
    
    def remove_corazon(self):
        self.vida -= 1
        self.corazones.remove(self.corazones.sprites().pop())
        
    def disparar(self):
        return self.rect.center
        
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
    def update(self, dt):
        self.input()
        self.rect.center += self.direction * self.velocidad * dt

    def draw(self, screen):
        self.corazones.draw(screen)
        screen.blit(self.image, self.rect)

#GROUPS
jugador = Jugador()
jugador_balas = pygame.sprite.Group()
aliens = pygame.sprite.Group()
cages = pygame.sprite.Group()

# temporizadores
pygame.time.set_timer(
    EVENTS.SPAWN_CAGES.value, 1000
)

while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                x, y = jugador.disparar()
                bala = Bala(x, y)
                jugador_balas.add(bala)
        if event.type == EVENTS.SPAWN_CAGES.value:
            Cage(cages)
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    
    jugador.update(deltatime)
    jugador_balas.update(deltatime)
    aliens.update(deltatime)
    cages.update(deltatime)
    
    if pygame.sprite.spritecollide(jugador, cages, True):
        jugador.add_corazon()
    # Draw
    jugador_balas.draw(pantalla)
    jugador.draw(pantalla)
    aliens.draw(pantalla)
    cages.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
