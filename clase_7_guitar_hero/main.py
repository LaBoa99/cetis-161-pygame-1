import pygame
import pygame.midi

# Configuración
pygame.init()
pygame.midi.init()

#Audio
output_device = pygame.midi.Output(0)
TIC = pygame.USEREVENT + 1



fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 480)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time
"""_summary_
    do = C
    re = D
    mi + E
    fa = F
    sol = G
    la = A
    si = B
"""
OCARINA_OF_TIME = [
    "_______#____",
    "#__#__#_#___",
    "__#__#___#__",
    "_#__#_____#_",
    "___________#"
]

class Song():
    def __init__(self, track_centers: list[float], notes:list[str]) -> None:
        self.notes_data = notes
        self.current_index = -1
        self.notes = pygame.sprite.Group()
        self.track_centers = track_centers
    
    def onTic(self):
        self.current_index += 1
        
    def readLineOfNotes(self):
        for track_num, note in enumerate(self.notes_data):
            Note()
    
    def draw(self, screen):
        self.notes.draw(screen)
    
    def update(self, dt):
        self.notes.update(dt)

class Metronome:
    def __init__(self, tempo) -> None:
        self.tempo = tempo
        self.intervalo_tiempo = 60.0 / self.tempo
        self.beat = 0
        self.tiempo_ultimo_beat = 0
    
    def update(self):
        actual = pygame.time.get_ticks() / 1000.0

        if actual - self.tiempo_ultimo_beat >= self.intervalo_tiempo:
            self.beat += 1
            self.tiempo_ultimo_beat = actual
            pygame.event.post(pygame.event.Event(TIC))

class Note(pygame.sprite.Sprite):
    def __init__(self, w, h, d, t, color, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centery = -h
        self.vel = (d + (w // 2)) / t
    
    def update(self, dt):
        self.rect.centery += self.vel * dt

class Guitar():
    def __init__(self) -> None:
        self.tracks = pygame.sprite.Group()
        
        # define tracks
        self.track_colors = [(0, 255, 0), (255, 0, 0), (245, 222, 179), (0, 0, 255), (140,96,40)]
        self.track_w = (ancho // 2) // (len(self.track_colors) + 1)
        self.track_h = self.track_w

        self.track_centers = []
        
        for i, color in enumerate(self.track_colors):
            track = Track(self.track_w, self.track_h, color, self.tracks)
            track.rect.centerx = self.track_w * i + (self.track_w // 2)
            track.rect.y = altura - self.track_h - 10
        
        x = ancho // 4
        spacing = self.track_w // len(self.track_colors)
        for i, track in enumerate(self.tracks.sprites()):
            track.rect.x = x
            track.rect.x += spacing * i + self.track_w * i
            self.track_centers.append(track.rect.centerx)
    
    def draw(self, screen):
        self.tracks.draw(screen)
    
    def update(self, dt):
        self.tracks.update(dt)

class Track(pygame.sprite.Sprite):
    def __init__(self, w, h, color, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
     
guitar = Guitar()
metronome = Metronome(60)
song = Song(guitar.track_centers, OCARINA_OF_TIME)
while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == TIC:
            song.onTic()
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    
    metronome.update()
    guitar.update(deltatime)
    song.update(deltatime)
    
    # Draw
    guitar.draw(pantalla)
    song.draw(pantalla)
    
    # Final
    pygame.display.flip()
    clock.tick(fps)

pygame.midi.quit()
pygame.quit()
