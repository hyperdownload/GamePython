import pygame
import psutil
from animation import Animation
from Tools import *

class Player:
    def __init__(self, x, y, width, height, texture=None, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = 0
        self.y_speed = 0
        self.camera_x = 0
        self.is_jumping = False
        self.acceleration = 0.3
        self.canMove_left = True
        self.canMove_right = True
        self.points = 0
        self.lifes = 3
        
        self.CollisionLeft=True
        self.CollisionRight=True
        
        self.texture = texture
        self.color = color
        if not self.texture and not self.color:
            self.color = (255, 0, 255)

        idle_animation = Animation([pygame.image.load("textures/idle.png"), pygame.image.load("textures/idle.png")])
        walk_animation = Animation([pygame.image.load("textures/walk1.png"), pygame.image.load("textures/walk2.png"), pygame.image.load("textures/walk3.png")])
        jump_animation = Animation([pygame.image.load("textures/jump.png",),pygame.image.load("textures/jump.png"),pygame.image.load("textures/jump.png")])
        death_animation = Animation([pygame.image.load("textures/death.png"), pygame.image.load("textures/death.png")])
        self.animations = {
            "idle": idle_animation,
            "walk": walk_animation,
            "jump": jump_animation,
            "death": death_animation,
        }
        self.current_animation = "idle"
        self.orientation = "right"  

    def move(self, keys):
        if keys[pygame.K_a]:
            if self.x > 1 and self.canMove_left:
                self.x_speed -= self.acceleration
                self.orientation = "left" 
        elif keys[pygame.K_d] and self.canMove_right:
            self.x_speed += self.acceleration
            self.orientation = "right" 
        else:
            if self.x_speed > 0 and self.canMove_right: 
                self.x_speed -= self.acceleration
                self.x_speed = max(self.x_speed, 0)  
            elif self.x_speed < 0 and self.canMove_left:
                self.x_speed += self.acceleration
                self.x_speed = min(self.x_speed, 0)   

        max_speed = 5
        self.x_speed = max(min(self.x_speed, max_speed), -max_speed)

        self.x += self.x_speed

    def jump(self, keys):
        if not self.is_jumping:
            if keys[pygame.K_SPACE]:
                self.canMove_left = True
                self.canMove_right = True
                self.y_speed = -15
                self.is_jumping = True
    def update(self, screen_height):
        self.y_speed += 1
        self.y += self.y_speed

    def check_collision(self, platforms, screen_width):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        broad_rect = player_rect.inflate(5, 5)
        chunk_size = 50

        start_index = max(0, int(self.camera_x / 50) - chunk_size)
        end_index = min(len(platforms), int((self.camera_x + screen_width) / 50) + chunk_size)

        for platform in platforms:
            if platform.collidable:
                platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)

                if broad_rect.colliderect(platform_rect):
                    if player_rect.colliderect(platform_rect):
                        dx = player_rect.centerx - platform_rect.centerx
                        dy = player_rect.centery - platform_rect.centery

                        if abs(dx) > abs(dy):
                            if dx > 0:
                                self.x = platform_rect.right
                                self.x_speed = 0
                                self.canMove_left = False
                            else:
                                self.x = platform_rect.left - self.width
                                self.x_speed = 0
                                self.canMove_right = False
                        else:
                            if dy > 0:
                                self.y = platform_rect.bottom
                                self.y_speed = 0
                            else:
                                self.y = platform_rect.top - self.height
                                self.is_jumping = False
                                self.y_speed = 0
            if self.x_speed > 0 and self.canMove_right:
                self.canMove_left = True
            elif self.x_speed < 0 and self.canMove_left:
                self.canMove_right = True
    def death(self):
        self.current_animation = "death"
        
    def block_murder(self, platforms, screen_width):
        chunk_size = 50

        start_index = max(0, int(self.camera_x / 50) - chunk_size)
        end_index = min(len(platforms), int((self.camera_x + screen_width) / 50) + chunk_size)

        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        broad_rect = player_rect.inflate(5, 5)

        for platform in platforms[start_index:end_index]:
            if platform.collidable and platform.morido and broad_rect.colliderect(platform.rect):
                self.camera_x = self.x - 50
                return True
        return False

    def update_animation(self):
        if self.x_speed != 0:
            self.current_animation = "walk"
        elif self.y_speed != 0:
            self.current_animation = "jump"
        else:
            self.current_animation = "idle"

        self.animations[self.current_animation].update()

    def draw(self, screen, camera_x):
        player_texture = self.animations[self.current_animation].current_frame()
        if self.orientation == "left":
            player_texture = pygame.transform.flip(player_texture, True, False)
        player_texture = pygame.transform.scale(player_texture, (self.width, self.height))
        player_rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        screen.blit(player_texture, player_rect)

    def respawn(self, camera_x, enemys):
        self.lifes-=1
        if self.lifes == 0:
            self.points=0
        self.current_animation = "death"
        self.x=50
        self.y=500
        for enemy in enemys:
            enemy.is_life=True
        camera_x=self.x
    def debug_info(self):
        pass
        #print(f"Player - X: {round(self.x)}, Y: {round(self.y)}, X Speed: {round(self.x_speed)}, Y Speed: {round(self.y_speed)} / CPU Usage: {cpu_percent}%  Memory Usage: {round(memory_percent)}% {self.is_jumping}", end="\r")