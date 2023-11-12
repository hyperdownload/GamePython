import pygame

class Interface:
    @staticmethod
    def draw_text(screen, text, x, y, font_size, color, duration=None):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

        if duration is not None and not hasattr(Interface, 'start_time'):
            Interface.start_time = pygame.time.get_ticks()

        if duration is not None:
            current_time = pygame.time.get_ticks()
            if current_time - Interface.start_time > duration * 1000:
                delattr(Interface, 'start_time')