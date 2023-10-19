import os
import random
from math import cos, radians, sin

import pygame

# Configuración
scrip_dir = os.path.dirname(__file__)

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (720, 480)
pantalla = pygame.display.set_mode((ancho, altura))

# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, x_end, y_end, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(scrip_dir, f"sprites\\bullet.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Rotate
        self.image, self.rect, self.angle = self.point_at(x_end, y_end, self.image, self.rect.center)
        self.direction = pygame.Vector2(x_end - x, y_end - y)
        self.direction = self.direction.normalize()
        
        #Stats
        self.damage = 20
        self.speed = 100
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom < 0 or self.rect.top > altura or self.rect.right < 0 or self.rect.left > ancho:
            self.kill()
    
    def point_at(self, x, y, originalImage, originalRectTuple, angleX=0, angleY=0):
        direction = pygame.math.Vector2(x, y) - originalRectTuple
        angle = direction.angle_to((angleX, angleY))
        image = pygame.transform.rotate(originalImage, angle)
        
        rect = image.get_rect(center=originalRectTuple)
        return image, rect, angle

class Pistol(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(scrip_dir, f"sprites\\pistol.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(scrip_dir, f"sprites\\bob.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (ancho // 2, altura // 2)

        self.right_arm = pygame.image.load(
            os.path.join(scrip_dir, f"sprites\\arm.png")
        ).convert_alpha()
        self.right_arm_rect = self.right_arm.get_rect()

        self.left_arm = pygame.transform.flip(
            self.right_arm, False, True
        ).convert_alpha()
        self.left_arm_rect = self.left_arm.get_rect()

        # Colocoar posiciones iniciales de brazos
        self.right_arm_rect.center = self.rect.center
        self.left_arm_rect.center = self.rect.center
        
        self.hands = [None, None]
        self.left_hand_weapon_rect = None
        self.right_hand_weapon_rect = None
        
        # players info
        self.direccion = pygame.Vector2(0, 0)
        self.velocidad = 9
        self.vida = 100
        
    def shoot(self, mx, my):
        bullets = []
        if self.left_hand_weapon_rect != None:
            bullets.append(self.__genBullet(mx, my, self.left_hand_weapon_rect.bottomright))
        if self.right_hand_weapon_rect != None:
            bullets.append(self.__genBullet(mx, my, self.right_hand_weapon_rect.topright))
        return bullets

    def __genBullet(self, mx, my, rect_tupple):
        x, y = rect_tupple
        return Bullet(x, y, mx, my)

    def pickup(self, pistol):
        if self.hands[0] == None:
            pistol.image = pygame.transform.flip(pistol.image, False, True).convert_alpha()
            self.hands[0] = pistol
        elif self.hands[1] == None:
            self.hands[1] = pistol

    def input(self):
        keys = pygame.key.get_pressed()
        # Horizontal
        if keys[pygame.K_a]:
            self.direccion.x = -1
        elif keys[pygame.K_d]:
            self.direccion.x = 1
        else:
            self.direccion.x = 0

        # Vertical
        if keys[pygame.K_w]:
            self.direccion.y = -1
        elif keys[pygame.K_s]:
            self.direccion.y = 1
        else:
            self.direccion.y = 0

    def update(self, dt):
        self.input()
        movement = self.direccion * self.velocidad * dt
        self.rect.center += movement
        self.left_arm_rect.center += movement
        self.right_arm_rect.center += movement

    def draw(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        mx, my = mouse_pos
        # draw bob
        body_image, body_rect, body_angle = self.point_at(
            mx, my, self.image, self.rect.center
        )

        rect = self.get_points_by_angle(-body_angle - 45, 32, 32, self.left_arm_rect)
        left_image, left_rect, a = self.point_at(
            mx, my, self.left_arm, rect.topleft
        )

        rect = self.get_points_by_angle(-body_angle - 135, -32, -32, self.right_arm_rect)
        rigth_image, rigth_rect, a = self.point_at(
            mx, my, self.right_arm, rect.topleft
        )
        
        if self.hands[0]:
            rectPistol = self.get_points_by_angle(-body_angle - 20, 56, 56, self.left_arm_rect)
            pistol_image, pistol_rect, a = self.point_at(mx, my, self.hands[0].image, rectPistol.topleft)
            self.left_hand_weapon_rect = pistol_rect
            screen.blit(pistol_image, pistol_rect)
        if self.hands[1]:
            rectPistol = self.get_points_by_angle(-body_angle - 165, -56, -56, self.right_arm_rect)
            pistol_image, pistol_rect, a = self.point_at(mx, my, self.hands[1].image, rectPistol.topleft)
            self.right_hand_weapon_rect = pistol_rect
            screen.blit(pistol_image, pistol_rect)
        
        screen.blit(left_image, left_rect)
        screen.blit(rigth_image, rigth_rect)
        screen.blit(body_image, body_rect)

    def get_points_by_angle(self, angle, dx, dy, rect):
        x, y = dx * cos(radians(angle)), dy * sin(radians(angle))
        rect = pygame.Rect(
            rect.centerx + x,
            rect.centery + y,
            rect.width,
            rect.height,
        )
        return rect

    def point_at(self, x, y, originalImage, originalRectTuple, angleX=0, angleY=0):
        direction = pygame.math.Vector2(x, y) - originalRectTuple
        angle = direction.angle_to((angleX, angleY))
        image = pygame.transform.rotate(originalImage, angle)
        
        rect = image.get_rect(center=originalRectTuple)
        return image, rect, angle

objects = pygame.sprite.Group()
pistol = Pistol(objects)
pistol2 = Pistol(objects)
pistol.rect.x = random.randint(100, ancho - 100)
pistol.rect.y = random.randint(100, altura - 100)

bullets = pygame.sprite.Group()

player = Player()
while True:
    pantalla.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            bbs = player.shoot(x, y)
            bullets.add(bbs) 
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    mouse_pos = pygame.mouse.get_pos()

    player.update(deltatime)
    bullets.update(deltatime)
    x, y = mouse_pos
    
    collisions = pygame.sprite.spritecollide(player, objects, True)
    if len(collisions):
        player.pickup(collisions[0])
    
    # Draw
    objects.draw(pantalla)
    player.draw(pantalla)
    bullets.draw(pantalla)
    pygame.draw.rect(pantalla, (255, 0, 0), [x - (32 // 2), y - (32 // 2), 32, 32])
    # Final
    pygame.display.flip()
    clock.tick(fps)
