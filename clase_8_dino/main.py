import pygame
import os
import random
from enum import Enum

scrip_dir = os.path.dirname(__file__)
# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

# Animacion de sprites
"""_summary_
    x: 677 dinosaurio w: 45 h: 48
    
    x: 134 ave w: 45
    
    x: 331 w= 24, h= 51, y = 2
"""
spritessheet = pygame.image.load(os.path.join(scrip_dir, "sprites", "dino.png")).convert_alpha()
def loadFrames(sprite, w, h, row, col, offset_x = 0, offset_y = 0):
    frames = []
    for i in range(col):
        frame = pygame.Surface((w, h), pygame.SRCALPHA)
        frame.blit(sprite, (0, 0), (offset_x + (i * w), offset_y + (row * h),  w, h))
        frames.append(frame)
    return frames

class DinoEnum(Enum):
    IDLE = 0
    RUN_START = 2
    RUN_END = 3
    DEATH = 4
    
    CRUNCH_START = 0
    CRUNCH_END = 1
    
class Dino(pygame.sprite.Sprite):
    
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.sprites = loadFrames(spritessheet, 44, 48, 0, 4, 677, 2)
        self.current_frame: DinoEnum = DinoEnum.IDLE.value
        self.animation_speed = 0.1
        
        # Dino
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.original_y = self.rect.centery
        self.groud_level = self.rect.bottom
        
        self.is_running = True
        self.is_in_ground = False
        self.jump = 30 # vel
        self.current_jump = 0
    
    def input(self, event):
        if event.key == pygame.K_SPACE:
            if self.is_in_ground:
                print("XD")
                self.is_in_ground = False
                self.current_jump = self.jump
                
        
    def update(self, dt, v):
        # Salto
        if not self.is_in_ground:
            self.rect.centery -= self.current_jump * dt
            self.current_jump -= 4.8 * dt
        
        if self.rect.bottom >= self.groud_level:
            self.is_in_ground = True
            self.rect.bottom = self.groud_level
        # Actualiza la animación
        if not self.is_running or not self.is_in_ground:
            self.current_frame = DinoEnum.IDLE.value
        else:
            self.current_frame += self.animation_speed + v
            if self.current_frame >= len(self.sprites) or self.current_frame < 2:
                self.current_frame = DinoEnum.RUN_START.value
        self.image = self.sprites[int(self.current_frame)]

ground_w = spritessheet.get_width() // 4
ground_images = loadFrames(spritessheet, ground_w, 15, 0, 4, 2, 53)    

def genGround(groundIndex, offset=0):
    return Ground(groundIndex, groundIndex * ground_w) if offset == 0 else Ground(groundIndex, offset)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groundIndex, x, *groups) -> None:
        super().__init__(*groups)  
        self.ground_index = groundIndex
        self.image = ground_images[self.ground_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = altura - 46
    
    def update(self, dt, velocity):
        self.rect.x -= velocity * dt
        if self.rect.right <= 0:
            self.kill()
            
def genCactus(cactusIndex, offset=0):
    return Cactus(cactusIndex, cactusIndex * ground_w) if offset == 0 else Cactus(cactusIndex, offset)

cactus_images = loadFrames(spritessheet, 24, 51, 0, 2, 331, 2)
class Cactus(pygame.sprite.Sprite):
    def __init__(self, cactusIndex, x, *groups) -> None:
        super().__init__(*groups)
        self.cactus_index = cactusIndex
        self.image = cactus_images[self.cactus_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = altura - 32

    def update(self, dt, velocity):
        self.rect.x -= velocity * dt
        if self.rect.right <= 0:
            self.kill()

        
        
def scaled_sigmoid(x, lim = 1, a = 10):
    """
    Retorna un valor entre 0 y 1 basado en una función sigmoide escalada.

    Parámetros:
    - x (float o int): El valor de entrada.
    - a (float o int): El factor de escala que afecta la suavidad de la transición.

    Retorna:
    - float: Un valor entre 0 y a que representa la salida de la función sigmoide escalada.
    """
    return lim / (1 + 2.71828 ** (-x/a))


dino = Dino(50, altura - (altura // 4))
grounds = pygame.sprite.Group(
    genGround(0),
    genGround(1),
    genGround(2),
    genGround(3)
)
cactuses = pygame.sprite.Group()
player = pygame.sprite.GroupSingle(dino)

# Texto
font = pygame.font.Font(None, 24)

velocity = scaled_sigmoid(pygame.time.get_ticks() / 1000.0, 20, 10)
ground_count = 0
last_cactus_x = 0
score = 0
text = font.render(str(score), True, (0, 0, 0))
while True:
    pantalla.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            dino.input(event)
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    
    if len(grounds) != 4:
        velocity = scaled_sigmoid(pygame.time.get_ticks() / 1000.0, 20, 10)
        grounds.add(genGround(ground_count % len(ground_images), ground_w * 3))
        ground_count += 1
        score += 10
        text = font.render(str(score), True, (0, 0, 0))
        cactus = genCactus(ground_count % len(cactus_images), ancho + random.randint(last_cactus_x + 100, last_cactus_x + 150))
        last_cactus_x = cactus.rect.x
        cactuses.add(cactus)

    grounds.update(deltatime, velocity)
    cactuses.update(deltatime, velocity)
    player.update(deltatime, velocity // 100)
    # Draw
    
    grounds.draw(pantalla)
    cactuses.draw(pantalla)
    player.draw(pantalla)
    pantalla.blit(text, (ancho // 2 - (text.get_width() // 2), 32))
    # Final
    pygame.display.flip()
    clock.tick(fps)
