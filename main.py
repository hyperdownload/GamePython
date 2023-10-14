import pygame
import sys
def on_draw_gizmos(screen, obj, gizmo_color):
    if isinstance(obj, Player):
        pygame.draw.rect(screen, gizmo_color, (obj.x, obj.y, obj.width, obj.height), 2)
    elif isinstance(obj, Block):
        if obj.block_type == 1:
            pygame.draw.rect(screen, gizmo_color, (obj.x, obj.y, obj.width, obj.height))


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = 5
        self.y_speed = 0
        self.is_jumping = False

    def move(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.x_speed
        if keys[pygame.K_d]:
            self.x += self.x_speed

    def jump(self, keys):
        if not self.is_jumping:
            if keys[pygame.K_SPACE]:
                self.y_speed = -10
                self.is_jumping = True

    def update(self, screen_height):
        self.y_speed += 1
        self.y += self.y_speed

        if self.y >= screen_height - self.height:
            self.y = screen_height - self.height
            self.is_jumping = False

    def check_collision(self, platforms):
        for platform in platforms:
            if self.y + self.height > platform.y and self.y < platform.y + platform.height:
                if self.x + self.width > platform.x and self.x < platform.x + platform.width:
                    if platform.block_type != 0:
                        if self.y_speed > 0:
                            self.y = platform.y - self.height
                            self.is_jumping = False
                            self.y_speed = 0
                        elif self.y_speed < 0:
                            self.y = platform.y + platform.height
                            self.y_speed = 0

class Block:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type
        self.width = 50
        self.height = 50

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Juego en 2D")

        self.player = Player((self.screen_width - 50) // 2, self.screen_height - 50, 50, 50)
        self.blocks = []

        self.white = (255, 255, 255)

        self.clock = pygame.time.Clock()

    def load_map(self, filename):
        with open(filename, 'r') as file:
            row = 0
            for line in file:
                col = 0
                for char in line.strip():
                    if char == ' ':
                        block_type = 0  # Bloque de aire
                    else:
                        block_type = int(char)
                    block = Block(col * 50, row * 50, block_type)
                    self.blocks.append(block)
                    col += 1
                row += 1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            self.player.move(keys)
            self.player.jump(keys)
            self.player.update(self.screen_height)
            self.player.check_collision(self.blocks)

            self.screen.fill(self.white)
            pygame.draw.rect(self.screen, (0, 0, 255), (self.player.x, self.player.y, self.player.width, self.player.height))
            self.draw_map()
            pygame.display.update()


            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def draw_map(self):
        for block in self.blocks:
            if block.block_type == 1:
                pygame.draw.rect(self.screen, (0, 0, 0), (block.x, block.y, block.width, block.height))

if __name__ == "__main__":
    game = Game()
    game.load_map("map.txt")
    on_draw_gizmos(game.screen, game.player, (0, 255, 255))
    game.run()
