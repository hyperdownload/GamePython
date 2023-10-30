import pygame
import sys
import psutil

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
        self.acceleration = 0.2
        
        self.texture = texture
        self.color = color
        if not self.texture and not self.color:
            self.color = (255, 0, 255)

        idle_animation = Animation([pygame.image.load("a.png"), pygame.image.load("a.png")])
        walk_animation = Animation([pygame.image.load("elweon.png"), pygame.image.load("elweon.png")])

        self.animations = {
            "idle": idle_animation,
            "walk": walk_animation,
        }
        self.current_animation = "idle"
        self.orientation = "right"  # Inicialmente, el jugador mira a la derecha

    def move(self, keys):
        if keys[pygame.K_a]:
            if self.x > 1:
                self.x_speed -= self.acceleration
                self.orientation = "left"  # Cambiar la orientación a "left"
        elif keys[pygame.K_d]:
            self.x_speed += self.acceleration
            self.orientation = "right"  # Cambiar la orientación a "right"
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

    def check_collision(self, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if platform.block_type != 0:
                platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
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
                            self.is_jumping = False
                            self.y_speed = 0
                        else:
                            self.y = platform_rect.top - self.height
                            self.is_jumping = False
                            self.y_speed = 0

    def update_animation(self):
        if self.x_speed != 0:
            self.current_animation = "walk"
        else:
            self.current_animation = "idle"

        # Actualiza la animación
        self.animations[self.current_animation].update()

    def draw(self, screen, camera_x):
        player_texture = self.animations[self.current_animation].current_frame()
        if self.orientation == "left":
            # Voltear la imagen si la orientación es "left"
            player_texture = pygame.transform.flip(player_texture, True, False)
        player_texture = pygame.transform.scale(player_texture, (self.width, self.height))
        player_rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        screen.blit(player_texture, player_rect)

    def debug_info(self):
        process = psutil.Process()
        cpu_percent = process.cpu_percent()
        memory_percent = process.memory_percent()
        print(f"Player - X: {round(self.x)}, Y: {round(self.y)}, X Speed: {round(self.x_speed)}, Y Speed: {round(self.y_speed)} / CPU Usage: {cpu_percent}%  Memory Usage: {round(memory_percent)}% {self.is_jumping}", end="\r")

class Block:
    def __init__(self, x, y, block_type, texture=None, color=None):
        self.x = x
        self.y = y
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

        self.player = Player((self.screen_width - 50) // 2, self.screen_height - 50, 50, 50, texture="elweon.png")
        self.blocks = []

        self.camera_x = 0
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()

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
                    else:
                        block_type = int(char)
                    block = Block(col * 50, row * 50, block_type, texture="b.png", color=None)
                    self.blocks.append(block)
                    col += 1
                row += 1

    def run(self):
        running = True
        self.initialize_textures()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            self.player.move(keys)
            self.player.jump(keys)
            self.player.check_collision(self.blocks)
            self.player.update(self.screen_height)

            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.player.current_animation = "walk"
            else:
                self.player.current_animation = "idle"

            if self.player.x > 395:
                self.camera_x = self.player.x - self.screen_width // 2

            self.screen.fill(self.white)
            self.draw_map()

            self.player.update_animation()

            self.player.draw(self.screen, self.camera_x)

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
    game.load_map("map.txt")
    game.run()
