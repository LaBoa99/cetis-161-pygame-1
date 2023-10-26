import pygame
import os

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

def loadFrames(sprite, w, h, row, col, offset_x = 0, offset_y = 0):
    frames = []
    for i in range(col):
        frame = pygame.Surface((w, h), pygame.SRCALPHA)
        frame.blit(sprite, (0, 0), (offset_x + (i * w), offset_y + (row * h),  w, h))
        frames.append(frame)
    return frames 

NUMEROS = pygame.image.load(os.path.join("sprites", "numeros.png")) 
class Numero(pygame.sprite.Sprite):
    
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.frames = loadFrames(NUMEROS, 8, 8, 0, 5)
        
        # Configuracion de frames
        self.current_frame = 0
        self.frame_duration = 10 # es una duracion aproximada cada N frames del Juego
        self.frame_timer = 0
        self.frame_count = len(self.frames)
        
        
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (ancho // 2, altura // 2)
        
    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.image = self.frames[self.current_frame]
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

numeros = Numero()
while True:
    pantalla.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime

    numeros.update(deltatime)
    # Draw
    numeros.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
