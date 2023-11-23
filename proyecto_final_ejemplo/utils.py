import pygame

def loadFrames(sprite, w, h, row, col, offset_x = 0, offset_y = 0):
    frames = []
    for i in range(col):
        frame = pygame.Surface((w, h), pygame.SRCALPHA)
        frame.blit(sprite, (0, 0), (offset_x + (i * w), offset_y + (row * h),  w, h))
        frames.append(frame)
    return frames 

def scale_image(surface, n = 2):
    return pygame.transform.scale(surface, (surface.get_width() * n, surface.get_height() * n))

def scale_images(surfaces, n=2):
    frames = []
    for frame in surfaces:
        frames.append(scale_image(frame, n))
    return frames

def change_color(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
    return finalImage