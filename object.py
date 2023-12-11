# object.py
import pygame
from collision import check_collision

class GameObject:
    def __init__(self, x, y, width, height, color, depth):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.depth = depth
        self.image = pygame.Surface((width, height))  # Creamos una superficie para el objeto
        self.image.fill(color)  # Rellenamos la superficie con el color del objeto

    def draw(self, screen, camera_rect=None):
        if camera_rect:
            rect_to_draw = self.rect.move(-camera_rect.x, -camera_rect.y)
            screen.blit(self.image, rect_to_draw)
        else:
            screen.blit(self.image, self.rect)