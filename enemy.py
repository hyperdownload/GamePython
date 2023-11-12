import pygame
from animation import Animation
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

    def draw(self, screen, camera_x):
        enemy_texture = self.animations[self.current_animation].current_frame()
        enemy_texture = pygame.transform.scale(enemy_texture, (self.width, self.height))
        enemy_rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        screen.blit(enemy_texture, enemy_rect)

    def check_collision(self, platforms):
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for platform in platforms:
            if platform.collidable:
                platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
                if enemy_rect.colliderect(platform_rect):
                    self.direction *= -1  
                    break  