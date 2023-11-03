import pygame
import sys
import psutil
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sound(self, sound_name, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        self.sounds[sound_name] = sound

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
            
class Animation:
    def __init__(self, frames):
        self.frames = frames
        self.frame_index = 0
        self.frame_rate = 10
        self.frame_counter = 0

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0

    def current_frame(self):
        return self.frames[self.frame_index]
class Enemy:
    def __init__(self, x, y, width, height, speed, texture=None, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed  
        self.direction = 1  
        self.on_ground = False

        self.texture = texture
        self.color = color

        if not self.texture and not self.color:
            self.color = (255, 0, 0) 

        idle_animation = Animation([pygame.image.load("textures/a.png"), pygame.image.load("textures/a.png")])
        walk_animation = Animation([pygame.image.load("textures/elweon.png"), pygame.image.load("textures/elweon.png")])

        self.animations = {
            "idle": idle_animation,
            "walk": walk_animation,
        }
        self.current_animation = "idle"

    def move(self):
        self.x += self.speed * self.direction

    def update_animation(self):
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
        
        self.texture = texture
        self.color = color
        if not self.texture and not self.color:
            self.color = (255, 0, 255)

        idle_animation = Animation([pygame.image.load("textures/idle.png"), pygame.image.load("textures/idle.png")])
        walk_animation = Animation([pygame.image.load("textures/walk1.png"), pygame.image.load("textures/walk2.png"), pygame.image.load("textures/walk3.png")])
        jump_animation = Animation([pygame.image.load("textures/jump.png")])
        self.animations = {
            "idle": idle_animation,
            "walk": walk_animation,
            "jump": jump_animation,
        }
        self.current_animation = "idle"
        self.orientation = "right"  

    def move(self, keys):
        if keys[pygame.K_a]:
            if self.x > 1:
                self.x_speed -= self.acceleration
                self.orientation = "left" 
        elif keys[pygame.K_d]:
            self.x_speed += self.acceleration
            self.orientation = "right" 
        else:
            if self.x_speed > 0:
                self.x_speed -= self.acceleration
                self.x_speed = max(self.x_speed, 0)  
            elif self.x_speed < 0:
                self.x_speed += self.acceleration
                self.x_speed = min(self.x_speed, 0)  

        max_speed = 5
        self.x_speed = max(min(self.x_speed, max_speed), -max_speed)

        self.x += self.x_speed

    def jump(self, keys):
        if not self.is_jumping:
            if keys[pygame.K_SPACE]:
                self.y_speed = -15
                self.is_jumping = True

    def update(self, screen_height):
        self.y_speed += 1
        self.y += self.y_speed

        if self.y >= screen_height - self.height:
            self.y = screen_height - self.height
            self.is_jumping = False
            self.y_speed = 0

    def check_collision(self, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        broad_rect = player_rect.inflate(5, 5)  

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
                            else:
                                self.x = platform_rect.left - self.width
                                self.x_speed = 0
                        else:
                            if dy > 0:
                                self.y = platform_rect.bottom
                                self.is_jumping = True
                                self.y_speed = 0
                            else:
                                self.y = platform_rect.top - self.height
                                self.is_jumping = False
                                self.y_speed = 0
                                

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

    def respawn(self):
        self.x=50
        self.y=500
    def debug_info(self):
        process = psutil.Process()
        cpu_percent = process.cpu_percent()
        memory_percent = process.memory_percent()
        print(f"Player - X: {round(self.x)}, Y: {round(self.y)}, X Speed: {round(self.x_speed)}, Y Speed: {round(self.y_speed)} / CPU Usage: {cpu_percent}%  Memory Usage: {round(memory_percent)}% {self.is_jumping}", end="\r")
class Block:
    def __init__(self, x, y, block_type, collidable, texture=None, color=None):
        self.x = x
        self.y = y
        self.collidable = collidable
        self.block_type = block_type
        self.width = 50
        self.height = 50
        self.texture = texture
        self.color = color

        if not self.texture and not this.color:
            self.color = (255, 0, 255)

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")

        self.player = Player((self.screen_width - 50) // 2, self.screen_height - 50, 50, 50, texture="textures/elweon.png")
        self.blocks = []

        self.camera_x = 0
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()

        self.sound = SoundManager()  
        
    def check_enemy_collision(self, player, enemy):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

        if player_rect.colliderect(enemy_rect):
            if player.x + player.width < enemy.x + enemy.width / 2:
                self.player.respawn()
            elif player.x > enemy.x + enemy.width / 2:
                self.player.respawn()
            else:
                print("b (colisión en la parte superior)")
    
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
                        collidable = True
                    else:
                        block_type = int(char)
                        collidable = False
                    block = Block(col * 50, row * 50, block_type, collidable, texture="textures/b.png", color=None)
                    self.blocks.append(block)
                    col += 1
                row += 1

    def set_background(self, background_image):
        self.background = pygame.image.load(background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def run(self):
        running = True
        self.initialize_textures()
        self.set_background("textures/a.png")

        enemy = Enemy(350, 500, 50, 50, 2)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            self.player.update(self.screen_height)
            self.player.check_collision(self.blocks)
            self.player.move(keys)
            self.player.jump(keys)

            enemy.move()
            enemy.check_collision(self.blocks)
            self.check_enemy_collision(self.player, enemy)
            enemy.update_animation()

            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.player.current_animation = "walk"
            else:
                self.player.current_animation = "idle"

            if self.player.x > 395:
                self.camera_x = self.player.x - self.screen_width // 2

            self.screen.fill(self.white)

            self.screen.blit(self.background, (0, 0))

            self.draw_map()

            self.player.update_animation()
            self.player.draw(self.screen, self.camera_x)

            enemy.draw(self.screen, self.camera_x)

            pygame.display.update()

            self.player.debug_info()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


    def draw_map(self):
        for block in self.blocks:
            if block.block_type == 1:
                block_rect = pygame.Rect(block.x - self.camera_x, block.y, block.width, block.height)

                if block.texture:
                    self.screen.blit(self.textures[block.texture], block_rect)
                else:
                    pygame.draw.rect(self.screen, block.color, block_rect)

if __name__ == "__main__":
    game = Game()
    game.load_map("sources/map.txt")
    game.run()
