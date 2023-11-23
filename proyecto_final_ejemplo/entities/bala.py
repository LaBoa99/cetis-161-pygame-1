import pygame

import utils as UTILS


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((6, 15))
        self.image.fill((207, 199, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]      
          
        self.velocidad = 50
        self.direction = pygame.Vector2(0, -1)
    
    def update(self, dt) -> None:
        self.rect.center += self.velocidad * self.direction * dt
        if self.rect.bottom < 0:
            self.kill()