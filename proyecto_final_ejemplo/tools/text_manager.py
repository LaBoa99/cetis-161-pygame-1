import pygame

from tools.singleton import Singleton

class TextManager():
    
    def __init__(self, font_path, size) -> None:
        super(TextManager, self).__init__()
        self.font = pygame.font.Font(font_path, size)
        self.texts = []
        
        self.current_time = 0
    
    def add_text(self, msg, color, pos, duration=100):
        """
        Agrega texto a la pantalla para ser mostrado temporalmente.

        Parameters:
            - msg (str): El mensaje de texto que se mostrará.
            - color (tuple): Una tupla de tres valores que representa el color del texto en formato (R, G, B).
            - pos (tuple): Una tupla de cuatro valores que define el rectángulo donde se mostrará el texto en formato (x, y).
            - duration (int): La duración en segundos durante la cual el texto será visible en la pantalla. Si se establece en -1, el texto será permanente y no desaparecerá automáticamente.

        Description:
            Esta función se utiliza para agregar texto a la pantalla de juego. Puedes especificar el mensaje de texto, el color del texto y la ubicación (rect) donde se mostrará el texto en la pantalla. Además, puedes controlar la duración durante la cual el texto se mantendrá visible. Si `duration` se establece en -1, el texto será permanente y no desaparecerá automáticamente. Si se especifica una duración en milisegundos, el texto desaparecerá después de ese período.

        Example:
            Para agregar un mensaje "Puntuación: 100" en la esquina superior izquierda con color blanco y hacerlo permanente:
            add_text("Puntuación: 100", (255, 255, 255), (10, 10, 200, 30), duration=-1)
        """
        text = self.font.render(msg, True, color)
        text_rect = text.get_rect()
        
        text_rect.center = pos
        self.texts.append([text, text_rect, duration if duration < 0 else duration + self.current_time])
    
    def update(self, dt):
        self.current_time += dt
        for text in self.texts:
            if text[2] > 0 and text[2] < self.current_time:
                self.texts.remove(text)
    
    def draw(self, screen):
        for text in self.texts:
            surface, rect, _ = text
            screen.blit(surface, rect)
            
    
        