import pygame
import os

# Scrip dir toma la direccion del archivo que se esta ejecutando
scrip_dir = os.path.dirname(__file__)


class Area(pygame.sprite.Sprite):
    def __init__(self, rect, sprite_url, *groups) -> None:
        super().__init__(*groups)
        self.rect = rect
        self.image = pygame.image.load(os.path.join(scrip_dir, f"sprites\{sprite_url}"))
        self.image = pygame.transform.scale(self.image, (rect.width, rect.height))
