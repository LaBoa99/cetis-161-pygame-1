
from tools.singleton import Singleton


class ImageCache(Singleton):
    
    _cache = {}
    
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def set_image(self, image, key):
        self._cache[key] = image
        
    @classmethod
    def get_image(self, key):
        sprites = self._cache.get(key)
        if type(sprites) is list:
            return list(map(lambda sprite: sprite.convert_alpha(), sprites))
        return sprites.convert_alpha()
    
    @classmethod
    def remove_image(self, key):
        self._cache.pop(key)
    
    @classmethod
    def clear_cache(self):
        self._cache.clear()