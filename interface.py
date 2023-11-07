import pygame

class Interface:
    def draw_text(screen, text, x, y, font_size, color):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
