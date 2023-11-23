import random
import math
from abc import ABC, abstractmethod

from alien_behavior import AlienBehaviors

class AlienGenerationStrategy(ABC):
    @abstractmethod
    def generate_aliens(self, aliens, w, h):
        pass


class OndaCosAlienGeneration(AlienGenerationStrategy):
    def generate_aliens(self, aliens, w, h):
        vel = random.random() + random.randint(0, 1)
        for i, alien in enumerate(aliens):
            alien.rect.center = -(alien.rect.width * 2), -(alien.rect.height * 2)
            alien.delay = 50 * i
            alien.velocity = vel
            alien.behavior = AlienBehaviors.onda_cos
        return aliens
            
class OndaSinAlienGeneration(AlienGenerationStrategy):
    def generate_aliens(self, aliens, w, h):
        vel = random.random() + random.randint(0, 1)
        for i, alien in enumerate(aliens):
            alien.rect.center = -(alien.rect.width * 2), -(alien.rect.height * 2)
            alien.delay = 50 * i
            alien.velocity = vel
            alien.behavior = AlienBehaviors.onda_sin
        return aliens

class OndaChoqueAlienGeneration(AlienGenerationStrategy):
    def generate_aliens(self, aliens, w, h):
        m1 = aliens[:len(aliens) // 2]
        m2 = aliens[len(aliens) // 2:]
        _cos = OndaCosAlienGeneration().generate_aliens(m1, w, h)
        _sin = OndaSinAlienGeneration().generate_aliens(m2, w, h)
        return _cos + _sin
            
class ToBottomAlienGeneration(AlienGenerationStrategy):
    def generate_aliens(self, aliens, w, h):
        cols = math.floor(w // aliens[0].rect.width)
        remaining_space = w - cols * aliens[0].rect.width
        gap = remaining_space / (cols - 1) if cols > 1 else 0
        w, h = aliens[0].rect.width, aliens[0].rect.height
        for i, alien in enumerate(aliens):
            row = i // cols
            col = i % cols
            alien.rect.topleft = w * col + gap * col, -(h * (row + 1))
            alien.delay = 5 * row
            alien.behavior = AlienBehaviors.to_bottom
            alien.velocity = 5 / 1000
        return aliens

class ToBottomChangeAlienGeneration(AlienGenerationStrategy):
    def generate_aliens(self, aliens, w, h):
        cols = math.floor(w // aliens[0].rect.width)
        remaining_space = w - cols * aliens[0].rect.width
        gap = remaining_space / (cols - 1) if cols > 1 else 0
        w, h = aliens[0].rect.width, aliens[0].rect.height
        for i, alien in enumerate(aliens):
            row = i // cols
            col = i % cols
            alien.rect.topleft = w * col + gap * col, -(h * (row + 1))
            alien.delay = 5 * row
            alien.behavior = AlienBehaviors.to_bottom_change
            alien.velocity = 5 / 1000
        return aliens
            
                

