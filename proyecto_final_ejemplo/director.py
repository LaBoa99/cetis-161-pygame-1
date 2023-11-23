import random
import math
import pygame
import alien_strategies as ALIEN_STRATEGIES
from entities.alien import Alien


class Director:
    
    def __init__(self, w, h) -> None:
        self.strategies = {
            "cos": ALIEN_STRATEGIES.OndaCosAlienGeneration(),
            "sin": ALIEN_STRATEGIES.OndaSinAlienGeneration(),
            "cos_sin": ALIEN_STRATEGIES.OndaChoqueAlienGeneration(),
            "to_bottom": ALIEN_STRATEGIES.ToBottomAlienGeneration(),
            "to_bottom_change": ALIEN_STRATEGIES.ToBottomChangeAlienGeneration(),
        }
        
        self.w = w
        self.h = h
    
    def build(self, min=1, max=2):
        behavior = random.choice(list(self.strategies.keys()))
        aliens: list[Alien] = self.gen_aliens(random.randint(min, max),self.w, self.h)
        return self.strategies[behavior].generate_aliens(aliens, self.w, self.h)
    
    def gen_aliens(self, n, w, h):
        return [Alien(0, 0, 0, w, h) for _ in range(n)]

        

