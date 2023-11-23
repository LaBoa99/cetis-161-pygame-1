import os
from enum import Enum

import pygame
import random
from director import Director
from entities.alien import Alien
from entities.explosion import Explosion
from tools.text_manager import TextManager

import utils as UTILS
from entities.bala import Bala
from entities.cage import Cage
from entities.corazon import Corazon
from enums.entities_enum import ENTITIES_SPRITES
from enums.sound_manager_enum import SOUNDS
from entities.jugador import Jugador
from tools.grid import Grid
from tools.image_cache import ImageCache
from tools.singleton import Singleton
from tools.sound_manager import SoundManager
from tools.spritesheet import Spritesheet


# ENUMS
class EVENTS(Enum):
    SPAWN_ALIENS = pygame.USEREVENT + 1
    SPAWN_CAGES = pygame.USEREVENT + 2

class COLORS(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GOLD = (255, 242, 61)


class Game(Singleton):
    def __init__(self) -> None:
        super().__init__()
        # Config
        self.fps = 60
        self.size = (480, 480)
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.src_path = os.path.join(os.path.dirname(__file__))
        
        # Deltatime 
        self.current_time = pygame.time.get_ticks()
        self.previous_time = self.current_time
        
        # Spritesheet configuration
        self.scale_factor = 4
        
        self.grid = Grid(11, 8)
        self.spritesheet = Spritesheet(os.path.join(self.src_path, "sprites", "space_sprites.png"))
        
        self.explosion_grid = Grid(16, 16)
        self.explosion_spritesheet = Spritesheet(os.path.join(self.src_path, "sprites", "explosion.png"))
        
        # Images cache 
        self.images_cache = ImageCache()
        self.load_sprites()
        
        #GROUPS
        self.jugador = Jugador((self.size[0] // 2, self.size[1] - 40))
        self.corazones = pygame.sprite.Group()
        self.jugador_balas = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.cages = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
            
        # Soound
        self.sound = SoundManager()
        self.load_sounds()
        
        # Timers
        pygame.time.set_timer(EVENTS.SPAWN_CAGES.value, 10000)
        
        # Text
        self.text = TextManager(os.path.join(self.src_path, "fonts", "Pixellari.ttf"), 16)
        
        #Director
        self.director = Director(self.size[0], self.size[1])
        a =  self.director.build(40, 41)
        self.aliens.add(a)
        for _ in range(self.jugador.vida):
            self.__appendHeart()

        
    def load_sprites(self):
        self.background = pygame.image.load(os.path.join(self.src_path, "sprites", "background.png"))
        
        # Explosion
        explosion_frames = self.explosion_spritesheet.images_at(self.explosion_grid.rects_at_row(0, 0, 8))
        explosion_frames = UTILS.scale_images(explosion_frames, self.scale_factor)
        self.images_cache.set_image(explosion_frames, ENTITIES_SPRITES.EXPLOSION)
        
        # Alines
        alien_frames = self.spritesheet.images_at(self.grid.rects_at_row(0, 0, 2))
        alien_frames = UTILS.scale_images(alien_frames, self.scale_factor)
        self.images_cache.set_image(alien_frames, ENTITIES_SPRITES.ALIEN_A)
        
        alien_frames = self.spritesheet.images_at(self.grid.rects_at_row(1, 0, 2))
        alien_frames = UTILS.scale_images(alien_frames, self.scale_factor)
        self.images_cache.set_image(alien_frames, ENTITIES_SPRITES.ALIEN_B)
        # Space
        self.images_cache.set_image(
            UTILS.scale_image(self.spritesheet.image_at(self.grid.rect_at(2, 0)), self.scale_factor), 
            ENTITIES_SPRITES.PLAYER
        )
        self.images_cache.set_image(
            UTILS.scale_image(self.spritesheet.image_at(self.grid.rect_at(3, 1))),
            ENTITIES_SPRITES.HEARTH
        )
        self.images_cache.set_image(
            UTILS.scale_image(self.spritesheet.image_at(self.grid.rect_at(3, 0)), self.scale_factor),
            ENTITIES_SPRITES.CAGE
        )
    
    def load_sounds(self):
        self.sound_path = os.path.join(self.src_path, "sounds")
        self.sound.load_sound(os.path.join(self.sound_path, "music.wav"), SOUNDS.MAIN_MUSIC, 0.4)
        self.sound.load_sound(os.path.join(self.sound_path, "laser.wav"), SOUNDS.LASER)
        self.sound.load_sound(os.path.join(self.sound_path, "explosion.wav"), SOUNDS.EXPLOSION, 0.3)
        self.sound.load_sound(os.path.join(self.sound_path, "pickup.wav"), SOUNDS.PICKUP, 0.3)
        self.sound.load_sound(os.path.join(self.sound_path, "running.wav"), SOUNDS.RUNNING)
        
    def deltatime(self):
        deltatime = (self.current_time - self.previous_time) / 1000.0  # Tiempo en segundos
        self.previous_time = deltatime
        return deltatime
    
    def update(self):
        dt = self.deltatime()
        self.jugador.update(dt)
        self.jugador_balas.update(dt)
        self.aliens.update(dt)
        self.cages.update(dt, self.size[1])
        self.explosions.update(dt)
        self.text.update(dt)
        
        sprites = pygame.sprite.groupcollide(self.jugador_balas, self.cages, True, True)
        if sprites:
            for _, aliens in sprites.items():
                for alien in aliens:
                    Explosion(alien.rect.centerx, alien.rect.centery, self.explosions)
                    self.sound.play(SOUNDS.EXPLOSION, 5)
        
        sprites = pygame.sprite.groupcollide(self.jugador_balas, self.aliens, True, True)
        if sprites:
            for _, aliens in sprites.items():
                for alien in aliens:
                    Explosion(alien.rect.centerx, alien.rect.centery, self.explosions)
                    self.text.add_text("200", COLORS.GOLD.value, alien.rect.center, 30)
                    self.sound.play(SOUNDS.EXPLOSION, 5)
        if pygame.sprite.spritecollide(self.jugador, self.cages, True):
            self.__appendHeart()
    
    def __appendHeart(self):
        Corazon(self.size[0], self.size[1], len(self.corazones), self.corazones)
        self.jugador.add_corazon()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.mixer.quit()
                os._exit(0)
            if event.type == EVENTS.SPAWN_CAGES.value:
                if random.randint(1, 10) == 1:
                    Cage(random.randint(100, 400), self.cages)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    x, y = self.jugador.disparar()
                    if x != -1 and y != -1:
                        Bala(x, y, self.jugador_balas)
                
    def draw(self):
        #self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, self.background.get_rect())
        self.corazones.draw(self.screen)
        self.jugador_balas.draw(self.screen)
        self.jugador.draw(self.screen)
        self.aliens.draw(self.screen)
        self.cages.draw(self.screen)
        self.explosions.draw(self.screen)
        self.text.draw(self.screen)
    
    def play(self):
        self.sound.play(SOUNDS.MAIN_MUSIC, 0, True)
        while self.is_running:
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
        
pygame.init()
game = Game()
game.play()