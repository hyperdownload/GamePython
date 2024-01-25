import pygame
import sys
from Tools import *
from interface import *
from sound_manager import SoundManager
from animation import Animation
from enemy import Enemy
from player import Player
from block import Block
from static_enemy import *
from particle import *
from emitter import *
from basics import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.width = self.screen_width
        self.height = self.screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.start_time = pygame.time.get_ticks()
        pygame.display.set_caption("Game")
        self.refresh_rate = 60
        self.pause = False
        
        self.player = Player(70, 500, 20, 50, texture="textures/elweon.png")
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
        
        self.textures = {}
        self.initialize_textures()
        
        
        self.camera = Camera(self.screen_width, self.screen_height)
        self.free_camera = FreeCamera(self.screen_width, self.screen_height)
        self.current_camera = self.camera
        self.free_camera_mode = False

        #global
        self.show_menu = False
        self.show_fps = False
        self.variable1 = False
        self.variable2 = False
        self.font = pygame.font.Font(None, 36)
        self.fullscreen = False
        #colors
        self.BLACK = (0,0,0)
        #asd
        self.text_input = TextInput(
            text="Initial Text",
            position=(50, 50),
            font_size=20,
            width=200,
            height=40,
            color=(255, 255, 255),
            background_color=(0, 0, 0),
            element_id="text_input_1",  # Un identificador único para este elemento
            json_file="positions.json"  # El archivo JSON donde se guardarán las posiciones
        )
        #
        self.enemy_preload = {Enemy(450, 500, 50, 50, 2), Enemy(550, 500, 50, 50, 2), Enemy(1000, 500, 50, 50, 2),
                Enemy(1050, 500, 50, 50, 2), Enemy(1100, 500, 50, 50, 2),
                Enemy(4000, 500, 50, 50, 2), Enemy(4050, 500, 50, 50, 2), Enemy(4100, 500, 50, 50, 2)}
    def on_toggle_f3(self):
        self.free_camera_mode = not self.free_camera_mode
        if self.free_camera_mode:
            print("Modo de cámara libre habilitado. Usa las flechas del teclado para mover la cámara.")
            self.current_camera = self.free_camera
        else:
            print("Modo de cámara libre deshabilitado. La cámara seguirá al jugador.")
            self.current_camera = self.camera
            self.current_camera.set_target(self.player)
            
    def handle_menu_click(self, evt):
        if self.show_menu:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.width - 150 <= mouse_x <= self.width and 0 <= mouse_y <= 120:
                self.variable1 = not self.variable1
            elif self.width - 150 <= mouse_x <= self.width and 150 <= mouse_y <= 270:
                self.variable2 = not self.variable2
            elif self.width - 150 <= mouse_x <= self.width and 300 <= mouse_y <= 420:
                self.show_fps = not self.show_fps
                
    def initialize_textures(self):
        for block in self.blocks:
            if block.texture and block.texture not in self.textures:
                image = pygame.image.load(block.texture)
                if image:
                    image = pygame.transform.scale(image, (block.width, block.height))
                    self.textures[block.texture] = image

    def can_view(self, x, y, object_width, object_height):
        object_left = x - self.camera_x
        object_right = x + object_width - self.camera_x
        object_top = y - 0  
        object_bottom = y + object_height - 0  

        return (object_right > 0 and object_left < self.screen_width and
                object_bottom > 0 and object_top < self.screen_height)

    def toggle_free_camera(self):
        if isinstance(self.current_camera, FreeCamera):
            self.current_camera = self.camera
            self.current_camera.set_target(self.player)
        else:
            self.current_camera = self.free_camera
            self.current_camera.set_target(None)


    def check_enemy_collision(self, player, enemy):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        enemy_top_zone = enemy_rect.copy()
        enemy_top_zone.height *= 0.25

        if player_rect.colliderect(enemy_rect):
            if (player.x + player.width < enemy.x + enemy.width / 2 or
                    player.x > enemy.x + enemy.width / 2) and not self.player.y_speed > 0:
                self.player.death()
                self.player.respawn(self.camera_x, self.enemy_list)
                self.enemy_list.clear()
                self.enemy_list.extend(self.enemy_preload)
                self.camera_x = self.player.x - 50
            elif player_rect.colliderect(enemy_top_zone):
                self.enemy_list.remove(enemy)
                self.player.y_speed = -15
                enemy.current_animation = "death"
                Interface.draw_text(self.screen, "+100", enemy.x - self.camera_x, enemy.y, 50, (255, 255, 255),
                                     duration=10)
                self.player.points += 100

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
                        block = Block(col * 50, row * 50, block_type, True, texture="textures/bricks.png", color=None,
                                      kill=False)
                        self.blocks.append(block)
                    elif char == '2':
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, True, texture=None, color=None, kill=True)
                        self.blocks.append(block)
                    elif char == '3':
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, True, texture="textures/floor.png", color=None,
                                      kill=False)
                        self.blocks.append(block)
                    else:
                        block_type = int(char)
                        block = Block(col * 50, row * 50, block_type, False, texture=None, color=None, kill=False)
                    col += 1
                row += 1

    def set_background(self, background_image):
        self.background_images = [
            pygame.image.load("textures/background/background_layer1.png").convert(),
            pygame.image.load("textures/background/background_layer2.png").convert()
        ]
        self.background = pygame.transform.scale(self.background_images[0], (self.screen_width, self.screen_height))

    def run(self):
        running = True
        self.initialize_textures()
        self.set_background("textures/background/background_layer1.png")
        chat = ""
        self.enemy_list.extend(self.enemy_preload)
        print(len(self.blocks))
        while running:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    # Obtener la nueva resolución de la ventana
                    width, height = event.w, event.h
                    # Reescalar la ventana manteniendo la resolución original
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        toggle_fullscreen()
                if event.type == pygame.QUIT:running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:self.on_toggle_f3()  
                    elif event.key == pygame.K_F4:self.show_menu = not self.show_menu
                    elif event.key == pygame.K_ESCAPE:self.pause = not self.pause
                elif event.type == pygame.MOUSEBUTTONDOWN:self.handle_menu_click(event)
                elif self.free_camera_mode:self.current_camera.handle_event(event)
                if self.show_menu:self.text_input.handle_event(event)

            keys = pygame.key.get_pressed()
            
            if not self.pause:

                self.update(keys, event)

                if keys[pygame.K_a] or keys[pygame.K_d]:
                    self.player.current_animation = "walk"
                else:
                    self.player.current_animation = "idle"

                if self.player.x > 395:
                    self.camera_x = self.player.x - self.screen_width // 2
                    if not self.free_camera_mode:
                        self.current_camera.set_target(self.player)
                        
                for enemy in self.enemy_list:
                    if canView(self.player.x,enemy.x,self.player.y, enemy.y, self.screen_width, self.screen_height):
                        enemy.move()
                        enemy.check_collision(self.blocks)
                        enemy.update_animation()
                        self.check_enemy_collision(self.player, enemy)

            self.render()
            self.clock.tick(self.refresh_rate)

        pygame.quit()
        sys.exit()
    #as
    def draw_map(self):
        chunk_size = 40

        start_index = max(0, int(self.current_camera.x / 50) - chunk_size)
        end_index = min(len(self.blocks), int((self.current_camera.x + self.screen_width) / 50) + chunk_size)

        for block in self.blocks[start_index:end_index]:
            if self.can_view(block.x, block.y, block.width, block.height):
                block_rect = self.current_camera.apply(pygame.Rect(block.x, block.y, block.width, block.height))
                texture = self.textures.get(block.texture)
                if texture:
                    self.screen.blit(texture, block_rect)
                else:
                    pygame.draw.rect(self.screen, block.color, block_rect)

    def update_visuals(self):
        self.draw_map()

        self.player.update_animation()
        self.player.draw(self.screen, self.current_camera)

        for enemy in self.enemy_list:
            enemy.draw(self.screen, self.current_camera)

        if self.show_menu:
            pygame.draw.rect(self.screen, (200, 200, 200), (self.width - 150, 0, 150, self.height))

            checkbox1_rect = pygame.Rect(self.width - 140, 20, 20, 20)
            pygame.draw.rect(self.screen, self.BLACK, checkbox1_rect, 2)
            if self.variable1:
                pygame.draw.rect(self.screen, self.BLACK, checkbox1_rect)

            checkbox2_rect = pygame.Rect(self.width - 140, 170, 20, 20)
            pygame.draw.rect(self.screen, self.BLACK, checkbox2_rect, 2)
            if self.variable2:
                pygame.draw.rect(self.screen, self.BLACK, checkbox2_rect)

            checkbox_fps_rect = pygame.Rect(self.width - 140, 320, 20, 20)
            pygame.draw.rect(self.screen, self.BLACK, checkbox_fps_rect, 2)
            if self.show_fps:
                pygame.draw.rect(self.screen, self.BLACK, checkbox_fps_rect)

            # Render FPS text
            fps_text = self.font.render("Show FPS", True, self.BLACK)
            self.screen.blit(fps_text, (self.width - 140, 290))
            
            self.text_input.render(self.screen)

        # Display FPS if enabled
        if self.show_fps:
            greeting_text = TextBlock(
                x=20,
                y=20,
                width=200,
                height=50,
                text=f"{self.clock.get_fps()}",
                font_size=24,
                font_color=(0, 0, 0),
                draw_background=False,
                element_id="greeting_text",  
                json_file="positions.json" 
            )
            greeting_text.draw(self.screen)
        
        pygame.display.update()


    def update(self, keys, event):
        self.player.update(self.screen_height)
        if self.player.block_murder(platforms=self.blocks, screen_width=self.screen_width):
            self.player.death()
            self.player.respawn(self.camera_x, self.enemy_list)
            self.camera_x = self.player.x - 50
        self.player.move(keys)
        self.player.check_collision(self.blocks, self.screen_width)
        self.player.jump(keys)
        
        self.current_camera.update()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.update_visuals()
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.load_map("sources/map.txt")
    game.run()
