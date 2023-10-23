import pygame
import sys
import psutil

class Player:
    def __init__(self, x, y, width, height, texture=None, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = 5
        self.y_speed = 0
        self.camera_x = 0
        self.is_jumping = False

        self.texture = texture
        self.color = color
        if not self.texture and not self.color:
            self.color = (255, 0, 255)

    def move(self, keys):
        if keys[pygame.K_a]:
            if self.x>1:
                self.x -= self.x_speed
        if keys[pygame.K_d]:
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
                    if self.y_speed > 0:
                        self.y = platform.y - self.height 
                        self.is_jumping = False
                        self.y_speed = 0
                    elif -self.y_speed > (platform.y + platform.height - self.y):
                        self.y = platform.y + self.height
                        self.y_speed = 0
                    elif self.x_speed > (platform.x + self.width - self.x):
                        self.x = platform.x - self.width
                        self.x_speed = 0


    def debug_info(self):
        print(f"Player - X: {self.x}, Y: {self.y}, X Speed: {self.x_speed}, Y Speed: {self.y_speed}",end="\r")
        pass

class Block:
    def __init__(self, x, y, block_type, texture=None, color=None):
        self.x = x
        self.y = y
        self.block_type = block_type
        self.width = 50
        self.height = 50
        self.texture = texture
        self.color = color

        if not self.texture and not self.color:
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
        process = psutil.Process()
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

            if self.player.x>395:
                self.camera_x = self.player.x - self.screen_width // 2

            self.screen.fill(self.white)
            self.draw_map()
            self.draw_entities()
            pygame.display.update()

            self.player.debug_info()

            cpu_percent = process.cpu_percent()
            memory_percent = process.memory_percent()
            
            #print(f"CPU Usage: {cpu_percent}%  Memory Usage: {round(memory_percent)}% ", end="\r")

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
                    
    def draw_entities(self):
        if self.player.texture:
            player_texture = pygame.image.load(self.player.texture)
            player_texture=pygame.transform.scale(player_texture, (self.player.width, self.player.height))
            if player_texture:
                player_rect = pygame.Rect(self.player.x - self.camera_x, self.player.y, self.player.width, self.player.height)
                self.screen.blit(player_texture, player_rect)
        else:
            pygame.draw.rect(self.screen, self.player.color, (self.player.x - self.camera_x, self.player.y, self.player.width, self.player.height))
        
if __name__ == "__main__":
    game = Game()
    game.load_map("map.txt")
    game.run()
