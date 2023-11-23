import pygame
from tools.singleton import Singleton


class SoundManager(Singleton):
    
    _sounds = {}
    
    def __init__(self) -> None:
        super().__init__()
        pygame.mixer.init()
        self.channels =  [pygame.mixer.Channel(i) for i in range(8)]
    
    def is_busy(self, channel_number):
        return self.channels[channel_number].get_busy()
    
    def queue(self, key, channel_number):
        if 0 <= channel_number < len(self.channels):
            if key in self._sounds:
                sound = self._sounds[key]
                self.channels[channel_number].queue(sound)
    
    def play(self, key, channel_number, loop=False):
        if 0 <= channel_number < len(self.channels):
            if key in self._sounds:
                sound = self._sounds[key]
                self.channels[channel_number].play(sound, -1 if loop else 0, fade_ms=0)
    
    def load_sound(self, sound_path, key, volume=1.0):
        sound = pygame.mixer.Sound(sound_path)
        self._sounds[key] = sound
        self.set_volume(key, volume)

    def set_volume(self, key, volume):
        if key in self._sounds:
            self._sounds[key].set_volume(volume)


    def stop(self, channel_number):
        if 0 <= channel_number < len(self.channels):
            self.channels[channel_number].stop()