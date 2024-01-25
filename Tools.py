from numba import njit
import pygame
@njit
def canView(x1, x2, y1, y2, screen_width, screen_height):
    distance_squared = (x2 - x1)**2 + (y2 - y1)**2
    return distance_squared <= (x1 + screen_width+screen_height)**1.8
def toggle_fullscreen():
    global screen
    if not pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
        pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((800, 600), pygame.RESIZABLE)