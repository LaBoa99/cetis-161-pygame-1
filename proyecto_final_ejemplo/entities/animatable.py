
from enums.sound_manager_enum import SOUNDS


class Animatable:
    
    def __init__(self, frames, frame_duration=10, loop=True) -> None:
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_count = len(self.frames)
        self.loop = loop
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.finish_loop = False

    
    def next_frame(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.image = self.frames[self.current_frame]  
        if not self.loop:
            self.finish_loop = self.current_frame >= (self.frame_count - 1)
                