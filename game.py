import pygame
import sys
import time
import numpy as np

from interface import *
from sound_manager import SoundManager
from animation import Animation
from enemy import Enemy
from player import Player
from block import Block
from static_enemy import *
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.start_time = pygame.time.get_ticks() 
        pygame.display.set_caption("Game")

        self.player = Player(70 , 500 , 20, 50, texture="textures/elweon.png")
        self.blocks = []
        self.enemy_list = []
        self.staticEnemy_list = []

        self.camera_x = 0
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()

        self.sound = SoundManager()  
        
        self.background_images = [
            pygame.image.load("textures/background/background_layer1.png").convert(),
            pygame.image.load("textures/background/background_layer2.png").convert()
        ]
        self.layer_speeds = [1, 2]
    def canView(self,x1,x2,y1,y2,screen_width, screen_height):
        distance = np.sqrt((np.abs(x2 - x1))**2 + (np.abs(y2 - y1))**2)
        return distance <= x1 + screen_width + screen_height
    def check_enemy_collision(self, player, enemy):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

        enemy_top_zone = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height * 0.25)

        if player_rect.colliderect(enemy_rect):
            if player.x + player.width < enemy.x + enemy.width / 2 and not self.player.y_speed>0:
                self.player.death()
                self.player.respawn(self.camera_x, self.enemy_list)
                self.camera_x = self.player.x - 50
            elif player.x > enemy.x + enemy.width / 2 and not self.player.y_speed>0:
                self.player.death()
                self.player.respawn(self.camera_x, self.enemy_list)
                self.camera_x = self.player.x - 50
            else:
                if player_rect.colliderect(enemy_top_zone):
                    self.player.y_speed = -15
                    enemy.current_animation = "death"
                    enemy.is_life = False
                    Interface.draw_text(self.screen, "+100", enemy.x - self.camera_x, enemy.y, 50, (255, 255, 255), duration=10)
                    self.player.points += 100
    
    def initialize_textures(self):
        self.textures = {}
        for block in self.blocks:
            if block.texture:
                image = pygame.image.load(block.texture)
                if image:
                    image = pygame.transform.scale(image, (block.width, block.height))
                    self.textures[block.texture] = image

    def load_map(self, filename):
        with open(filename, 'r') as file:
            row = 0
            for line in file:
                col = 0
                for char in line.strip():
                    if char == ' ':
                        block_type = 0
                        collidable = False
                    elif char == '1':
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, True, texture="textures/bricks.png", color=None, kill=False)
                        self.blocks.append(block)
                    elif char == '2':
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, True, texture=None, color=None, kill=True)
                        self.blocks.append(block)
                    elif char == '3':
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, True, texture="textures/floor.png", color=None, kill=False)
                        self.blocks.append(block)
                    else:
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, False, texture=None, color=None, kill=False)
                    col += 1
                row += 1

    def set_background(self, background_image):
        self.background = pygame.image.load(background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def run(self):
        running = True
        self.initialize_textures()
        self.set_background("textures/background/background_layer1.png")
        chat=""
        for i in (Enemy(450, 500, 50, 50, 2),Enemy(550, 500, 50, 50, 2),Enemy(1000, 500, 50, 50, 2),Enemy(1050, 500, 50, 50, 2),Enemy(1100, 500, 50, 50, 2),
                  Enemy(4000, 500, 50, 50, 2),Enemy(4050, 500, 50, 50, 2),Enemy(4100, 500, 50, 50, 2)):
            self.enemy_list.append(i)
        #for x in (Staticenemy(450, 500, 50, 50, 2, 50),Staticenemy(4100, 500, 50, 50, 2, 2)):
            #self.staticEnemy_list.append(x)
        while running:
            current_time = pygame.time.get_ticks()  
            elapsed_time = (current_time - self.start_time) / 1000 
            chat = f"Tiempo: {round(elapsed_time)} segundos, Puntaje: {self.player.points}, Vidas: {self.player.lifes},(FPS: {self.clock})"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            
            self.player.update(self.screen_height)
            if self.player.block_murder(platforms=self.blocks):
                self.player.death()
                self.player.respawn(self.camera_x, self.enemy_list)
                self.camera_x = self.player.x - 50
            self.player.move(keys)
            self.player.check_collision(self.blocks)
            self.player.jump(keys)

            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.player.current_animation = "walk"
            else:
                self.player.current_animation = "idle"

            if self.player.x > 395:
                self.camera_x = self.player.x - self.screen_width // 2
            
            self.screen.fill(self.white)

            self.screen.blit(self.background, (0, 0))
            
            Interface.draw_text(self.screen, f"{chat}", 210,25 , 30, (0, 0, 0))
            #Interface.draw_text(self.screen, f"Player - X: {round(self.player.x)}, Y: {round(self.player.y)}, X Speed: {round(self.player.x_speed)}, Y Speed: {round(self.player.y_speed)}, Camera:{self.player.camera_x}", 125, 10, 20,color=(0,0,0))
            for enemy in self.enemy_list:
                if enemy.is_life:
                    if self.canView(enemy.x,enemy.y,self.player.x, self.player.y,self.screen_width, self.screen_height):
                        enemy.move()
                        enemy.check_collision(self.blocks)
                        enemy.update_animation()
                        self.check_enemy_collision(self.player, enemy)
            for enemyStatic in self.staticEnemy_list:
                if self.canView(self.player.x, self.player.y,enemy.x,enemy.y, self.screen_width, self.screen_height):
                    enemyStatic.move()
                    enemyStatic.draw(self.screen,self.camera_x)
            self.draw_map()

            self.player.update_animation()
            self.player.draw(self.screen, self.camera_x)
            for enemy in self.enemy_list:
                if self.canView(self.player.x, self.player.y,enemy.x, enemy.y, self.screen_width,self.screen_height ):
                    enemy.draw(self.screen, self.camera_x)  
            pygame.display.update()

            self.player.debug_info()

            self.clock.tick(0)

        pygame.quit()
        sys.exit()


    def draw_map(self):
        for block in self.blocks:
            if self.canView(self.player.x, self.player.y,block.x,block.y, self.screen_width, self.screen_height):
                if block.block_type == 1:
                    block_rect = pygame.Rect(block.x - self.camera_x, block.y, block.width, block.height)
                    if block.texture:
                        self.screen.blit(self.textures[block.texture], block_rect)
                    else:
                        pygame.draw.rect(self.screen, block.color, block_rect)
                elif block.block_type == 3:
                    block_rect = pygame.Rect(block.x - self.camera_x, block.y, block.width, block.height)

                    if block.texture:
                        self.screen.blit(self.textures[block.texture], block_rect)
                    else:
                        pygame.draw.rect(self.screen, block.color, block_rect)

if __name__ == "__main__":
    game = Game()
    game.load_map("sources/map.txt")
    game.run()