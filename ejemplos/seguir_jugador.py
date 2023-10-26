import pygame

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 100, 0))
        self.rect = self.image.get_rect()
        self.velocidad = 3
        self.direction = pygame.Vector2(0, 0)
        
    def update(self, dt, player):
        # Se obtiene por parametro la clase Jugador
        x, y = player.rect.center
        # Al restar un vector  de otro se obtiene un vector amputanod a B, es decir B - A apunta a A
        self.direction = pygame.math.Vector2(x - self.rect.centerx, y - self.rect.centery)
        if self.direction.length() > 0:
            # La normalizacion es un vector de no mayor a 1 o -1 de longitud pues con esto podemos indicar como mvoerse en X,Y
            self.direction.normalize_ip()
            self.rect.center += self.direction * self.velocidad * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.velocidad = 10
        self.direction = pygame.Vector2(0, 0)
    
    def update(self, dt):
        self.rect.center += self.direction * self.velocidad * dt
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
            
    def update(self, dt):
        self.input()
        self.rect.center += self.direction * self.velocidad * dt
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Groups
jugador = Jugador()
enemigo = Enemigo()

while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    jugador.update(deltatime)
    enemigo.update(deltatime, jugador)
    # Draw
    jugador.draw(pantalla)
    enemigo.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
