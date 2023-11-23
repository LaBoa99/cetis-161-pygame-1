import pygame
from entities.corazon import Corazon

from enums.entities_enum import ENTITIES_SPRITES
from enums.sound_manager_enum import SOUNDS
from tools.image_cache import ImageCache
from tools.sound_manager import SoundManager


class Jugador(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = ImageCache().get_image(ENTITIES_SPRITES.PLAYER)
        self.sound = SoundManager()
        self.rect = self.image.get_rect()
        
        # posicion inicial del jugador
        self.rect.center = pos
        
        # movimiento
        self.velocidad = 10
        self.direction = pygame.Vector2(0, 0)
        self.running = 1
        self.vida = 5
    
    def add_corazon(self):
        self.vida += 1
        self.sound.play(SOUNDS.PICKUP, 4)
        
    def disparar(self):
        if self.running > 1:
            return -1, -1
        self.sound.play(SOUNDS.LASER, 1)
        return self.rect.center
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.running = 2 if keys[pygame.K_LSHIFT] else 1
        
        if self.running >= 2:
            if not self.sound.is_busy(3):
                self.sound.play(SOUNDS.RUNNING, 3, True)
        elif self.sound.is_busy(3):
            self.sound.stop(3)
        
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
    def update(self, dt):
        self.input()
        self.rect.center += self.direction * self.velocidad * self.running  * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)