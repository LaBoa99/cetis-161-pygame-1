import pygame
import os
from enum import Enum
# Inicializar Pygame
pygame.init()

# Configurar el número de canales
num_channels = 4  # Número de canales personalizados
pygame.mixer.set_num_channels(num_channels)

# Crear instancias de canales personalizados
# los canales nos sirven para en uno reproducir musica de fondo, sonidos de efecto, sonidos de GUI y sonidos extras o de efecto
# Puedes diferenciar mucho los canales en que tratan utilizando un enum
# Los canales maximos son 8 y un chanel puede reproducir un sonido a la vez por eso la importancia de diferenciar los canales
class CANALES_AUDIO(Enum):
    FONDO = 0,
    SFX = 1,
    GUI = 2,
    AMBIENTE = 3
"""_summary_
    channel1 = pygame.mixer.Channel(CANALES_AUDIO.FONDO.value)
    channel2 = pygame.mixer.Channel(CANALES_AUDIO.SFX.value)
    channel3 = pygame.mixer.Channel(CANALES_AUDIO.GUI.value)
    channel4 = pygame.mixer.Channel(CANALES_AUDIO.AMBIENTE.value)
"""
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)



# Cargar sonidos
sound1 = pygame.mixer.Sound(os.path.join("sonidos", "friying_pan.wav"))
sound2 = pygame.mixer.Sound(os.path.join("sonidos", "friying_pan.wav"))

# Reproducir sonidos en canales específicos
channel1.play(sound1)
channel2.play(sound2)

# Esperar a que los sonidos terminen antes de salir
while pygame.mixer.get_busy():
    pygame.time.delay(100)

# Salir de Pygame
pygame.quit()
