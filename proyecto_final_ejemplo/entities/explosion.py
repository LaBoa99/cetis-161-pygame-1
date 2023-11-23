import pygame

from entities.animatable import Animatable
from enums.entities_enum import ENTITIES_SPRITES
from tools.image_cache import ImageCache

class Explosion(pygame.sprite.Sprite, Animatable):
    
    def __init__(self, x, y, *groups) -> None:
        super().__init__(groups)
        Animatable.__init__(self, ImageCache().get_image(ENTITIES_SPRITES.EXPLOSION), 1, False)
        self.rect.center = x, y
    
    def update(self, dt):
        self.next_frame(dt)
        if self.finish_loop:
            self.kill()