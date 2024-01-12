import pygame
from animation import Animation
from numba import njit
import numpy as np
@njit
def check_collision_numba(x, y, width, height, direction, platforms_x, platforms_y, platforms_width, platforms_height):
    enemy_left = x
    enemy_right = x + width
    enemy_top = y
    enemy_bottom = y + height

    for i in range(len(platforms_x)):
        platform_left = platforms_x[i]
        platform_right = platforms_x[i] + platforms_width[i]
        platform_top = platforms_y[i]
        platform_bottom = platforms_y[i] + platforms_height[i]

        if enemy_right > platform_left and enemy_left < platform_right and enemy_bottom > platform_top and enemy_top < platform_bottom:
            direction *= -1
            break

    return direction
class Enemy:
    def __init__(self, x, y, width, height, speed, texture=None, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed  
        self.direction = 1  
        self.on_ground = False
        self.is_life = True
        self.texture = texture
        self.color = color

        if not self.texture and not self.color:
            self.color = (255, 0, 0) 
        death_animation = Animation([pygame.image.load("textures/enemy_die.png"), pygame.image.load("textures/enemy_die.png")])
        idle_animation = Animation([pygame.image.load("textures/a.png"), pygame.image.load("textures/a.png")])
        walk_animation = Animation([pygame.image.load("textures/enemy_1.png"), pygame.image.load("textures/enemy_2.png")])

        self.animations = {
            "idle": idle_animation,
            "walk": walk_animation,
            "death": death_animation,
        }
        self.current_animation = "idle"

    def move(self):
        self.x += self.speed * self.direction

    def update_animation(self):
        if not self.is_life:
            self.current_animation = "death"
        if self.speed != 0:
            self.current_animation = "walk"
        else:
            self.current_animation = "idle"

        self.animations[self.current_animation].update()

    def draw(self, screen, camera):
        enemy_texture = self.animations[self.current_animation].current_frame()
        enemy_texture = pygame.transform.scale(enemy_texture, (self.width, self.height))

        # Utiliza el método apply de la cámara para obtener la posición ajustada
        enemy_rect = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
        
        screen.blit(enemy_texture, enemy_rect)


    def check_collision(self, platforms):
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        platforms_x = np.array([platform.x for platform in platforms if platform.collidable])
        platforms_y = np.array([platform.y for platform in platforms if platform.collidable])
        platforms_width = np.array([platform.width for platform in platforms if platform.collidable])
        platforms_height = np.array([platform.height for platform in platforms if platform.collidable])

        self.direction = check_collision_numba(
            self.x, self.y, self.width, self.height, self.direction,
            platforms_x, platforms_y, platforms_width, platforms_height
        ) 