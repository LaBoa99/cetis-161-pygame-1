import pygame
from enums.entities_enum import ENTITIES_SPRITES
from tools.image_cache import ImageCache

import utils as UTILS

class Corazon(pygame.sprite.Sprite):
    def __init__(self, x, y, n,*groups) -> None:
        super().__init__(*groups)
        self.image = ImageCache().get_image(ENTITIES_SPRITES.HEARTH)
        self.rect = self.image.get_rect()
        self.rect.right = x - (n * self.rect.width)
        self.rect.bottom = y