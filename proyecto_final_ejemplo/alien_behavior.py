import pygame
import math

from entities.alien import Alien



class AlienBehaviors:
    
    @staticmethod
    def onda_cos(alien: Alien, dt: float, w, h):
        elapsed_time = (pygame.time.get_ticks() - alien.creation_time) / 1000
        x = ((w / 2) * math.cos(elapsed_time * 0.5 - (math.pi))) + (h / 2)
        alien.rect.centerx = x
        alien.initial_y += alien.velocity * dt
        alien.rect.y = round(alien.initial_y)
    
    @staticmethod
    def onda_sin(alien: Alien, dt: float, w, h):
        elapsed_time = (pygame.time.get_ticks() - alien.creation_time) / 1000
        x = ((w / 2) * math.sin(elapsed_time * 0.5 - (math.pi/4))) + (h / 2)
        alien.rect.centerx = w - x
        alien.initial_y += alien.velocity * dt
        alien.rect.y = round(alien.initial_y)
        
    @staticmethod
    def to_bottom(alien: Alien, dt: float, w, h):
        alien.initial_y += alien.velocity * dt
        alien.rect.y += round(alien.initial_y)
    
    @staticmethod
    def to_bottom_change(alien: Alien, dt: float, w, h):
        alien.initial_y += alien.velocity * dt
        alien.rect.y += round(alien.initial_y)
        if alien.rect.centery > h // 2:
            alien.velocity = 1