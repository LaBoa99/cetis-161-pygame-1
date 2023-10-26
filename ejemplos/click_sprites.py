import pygame

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
COLORES = [AZUL, VERDE, ROJO]

class Cuadrado(pygame.sprite.Sprite):

    
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((64, 64))
        self.color = 0
        self.image.fill(COLORES[self.color])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def change_color(self):
        self.color += 1
        if self.color >= len(COLORES):
            self.color = 0
        self.image.fill(COLORES[self.color])

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time
cuadrados = pygame.sprite.Group()

# Cuadrados
Cuadrado(ancho // 4, altura // 4, cuadrados)
Cuadrado(ancho // 4 * 3,  altura // 4, cuadrados)
Cuadrado(ancho // 4, altura // 4 * 3, cuadrados)
Cuadrado(ancho // 4 * 3, altura // 4 * 3, cuadrados)
Cuadrado(ancho // 2, altura // 2, cuadrados)

while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Se obtiene la posicion del mouse
                x, y = pygame.mouse.get_pos()
                # Iteramos sobre los cuadrados
                for cuadrado in cuadrados:
                    # llamamos a su rectangulo y vemos con collidepoint si este colisiona o n o
                    if cuadrado.rect.collidepoint(x, y):
                        # en caso de que colisione cambiamos su color y con la palabra break rompemos el for
                        cuadrado.change_color()
                        break
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime

    # Draw
    cuadrados.draw(pantalla)
    # Final
    pygame.display.flip()
    clock.tick(fps)
