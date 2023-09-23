import sys
import os
import random
import pygame
from pygame.locals import *

"""
Toma la ubicacion del archivo para ubicar la carpeta assets
"""
scrip_dir = os.path.dirname(__file__)

"""
Aqui se define la clase gotas que hereda de la clase Sprite de Pygame
Sprite le hereda diferentes funciones a nuesta clase gota
la palabra self funciona para referirse a si mismo y se encuentra en todas
las funciones dentro de Gota
"""


class Gota(pygame.sprite.Sprite):
    """
    la funcion __init__ siempre se llama cuando se crea una gota
    es decir:

    gota = Gota((50, 50), gotas) <-- Aqui van los parametros de Init dentro del parentesis como si fuera una funcion

    self - La instancia de Gota, al momento de llamar funciones no se pone
    pos - es una tupla (una lista que no puede modificar su tamano) en done (x, y)
    *groups - groups es una lista de Grupos de Sprites el * significa que se puede desempaquetar

    es  decir
    def suma(*numeros):
        return sum(numeros)

    suma(1, 2, 3, 4, 5, 6, 9)

    si te fijas el * hace que se puedan poner N numeros de variables o parametros
    """

    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(scrip_dir, "assets/gota.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    """
    La funcion update es heredada de Sprite pero se puede sobrescribir como lo hacemos aqui
    aqui se actualiza la posicion del rectangulo en su eje Y
    Delta time es la diferencia de tiempo entre fotogramas
    kill() elimina la instancia de gota 
    """

    def update(self, dt):
        self.rect.y += 9.8 * dt
        if self.rect.y > 480:
            self.kill()


"""
Al igual que gota la clase Cubeta hereda de Sprite teniendo los mismos metodos que Gota 
pero con diferente comportamiento

entiendase que funciones de una clase son metodos

una instancia es cualquier objeto creado  es decir:
cubeta = Cubeta() esto es una instancia
lista = [] Esto es una instancia de la clase List
"""


class Cubeta(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(scrip_dir, "assets/cubeta.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


# Se inicia el motor
pygame.init()

# Se define el tiempo o la tasa de refresco
fps = 60
clock = pygame.time.Clock()

# los grupos de sprite sirven como optimizacion, es lo equivalente a una lista
gotas = pygame.sprite.Group()
jugador = pygame.sprite.Group()

# ancho por altura de nuestra pantalla
ancho = 640
altura = 800
pantalla = pygame.display.set_mode((ancho, altura))

# Deltatime
curren_time = pygame.time.get_ticks()
previous_time = curren_time


# Game loop.
def agregar_gota():
    x_pos = random.randint(
        0, ancho - 64
    )  # Ancho de la ventana menos el ancho de la gota
    Gota((x_pos, -64), gotas)


# se crea un evento mayor a USEREVENT para evitar colisiones
# Recuerda que la funcion init de cubeta pide pos, y grupos
pygame.time.set_timer(USEREVENT + 1, 2000)
cubeta = Cubeta((ancho // 2 - 32, altura - 100), jugador)
while True:
    # se llena la pantalla de un color
    pantalla.fill((138, 239, 255))

    # Se busca algun evento que haya sucedido
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == USEREVENT + 1:
            agregar_gota()

    # Capturar las pulsaciones de teclas para mover la cubeta
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        cubeta.rect.x -= 9.8
    if keys[K_RIGHT]:
        cubeta.rect.x += 9.8

    # Esta funcion de aqui MAX retorna el numero mayor entre 0  y el numero minimo entre
    # la esquina superior izquierda y la resta de ancho - la anchura de la cubeta
    # permitiendonos saber si la cubeta arrebasa o no los limites de anchura
    cubeta.rect.x = max(0, min(cubeta.rect.x, ancho - cubeta.rect.width))

    # se verifica si cubeta colisiiona con alguna instancia del grupo de Sprotes de gotas
    # el True indica si al momento de colisionar la instancia gota se tiene que eliminar
    # en este caso al tener True se llama kill() heredado de Sprite en la clase Gota
    pygame.sprite.spritecollide(cubeta, gotas, True)
    # Update.
    deltatime = (curren_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime

    gotas.update(deltatime)
    jugador.update(deltatime)
    # Draw.
    gotas.draw(pantalla)
    jugador.draw(pantalla)

    # Se limpia la pantalla
    pygame.display.flip()
    # Se ajusta nuestros FPS a lo esperado
    clock.tick(fps)
