import pygame
from enums.entities_enum import ENTITIES_SPRITES
from tools.image_cache import ImageCache

import utils as UTILS

class Cage(pygame.sprite.Sprite):
    def __init__(self, x, *groups) -> None:
        super().__init__(*groups)
        self.image = ImageCache().get_image(ENTITIES_SPRITES.CAGE)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, -self.rect.width)
        
        self.direction = pygame.Vector2(0, 1)
        self.vel = 5
    
    def update(self, dt, max_altura):
        self.rect.center += self.direction * self.vel * dt
        if self.rect.top > max_altura:
            self.kill()