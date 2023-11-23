import pygame
from entities.animatable import Animatable
from enums.entities_enum import ENTITIES_SPRITES
from tools.image_cache import ImageCache

import random
import math

class Alien(pygame.sprite.Sprite, Animatable):
    def __init__(self, x, y, delay, w, h, *groups):
        super().__init__(*groups)
        Animatable.__init__(self, ImageCache().get_image(ENTITIES_SPRITES.ALIEN_A if random.randint(1, 2) == 1 else ENTITIES_SPRITES.ALIEN_B), 8)
        self.rect.center = x, y
        self.velocity = 5
        self.direction = pygame.Vector2(0, 1)
        # Config
        self.initial_y = y
        self.initial_x = x
        self.delay = delay
        self.creation_time = pygame.time.get_ticks()
        self.behavior = self.default_behavior
        
        # screen
        self.w = w
        self.h = h
        
    def default_behavior(self, alien, dt, w, h):
        self.rect.centery += round(self.velocity * dt)
        
    def update(self, dt):
        self.next_frame(dt)
        
        # Apply delay
        if self.delay > 0:
            self.delay -= dt
            self.creation_time = pygame.time.get_ticks()
            return  # Don't update the position until the delay is over

        # Calculate position based on time and delay
        self.behavior(self, dt, self.w, self.h)


        # Remove the alien if it goes off the screen
        if self.rect.top >= self.h:
            self.kill()
