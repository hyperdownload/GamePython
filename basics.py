#basics.py
import pygame
from particle import Particle
from object import GameObject
import time
import functools
class Debug:
    @staticmethod
    def draw_debug_rect(screen, obj, color=(255, 255, 255), thickness=1):
        if isinstance(obj, GameObject):
            pygame.draw.rect(screen, color, obj.rect, thickness)
        elif isinstance(obj, Particle):
            Debug.draw_debug_circle(screen, obj, color=color, thickness=thickness)

    @staticmethod
    def draw_debug_circle(screen, particle, color=(255, 255, 255), thickness=1):
        pygame.draw.circle(screen, color, (int(particle.x), int(particle.y)), particle.radius, thickness)

    # Diccionario para almacenar los tiempos de ejecución de las funciones
    execution_times = {}

    def timeit(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"{func.__name__} took {elapsed_time:.6f} seconds to execute.")

            return result

        return wrapper

    # Esta función imprimirá las estadísticas al presionar F3
    def show_statistics():
        if execution_times:
            print("Estadísticas de tiempo de ejecución:")
            for func_name, elapsed_time in execution_times.items():
                print(f"{func_name}: {elapsed_time:.6f} segundos")
        else:
            print("No hay funciones registradas.")

    # Función para resetear las estadísticas
    def reset_statistics():
        global execution_times
        execution_times = {}
        print("Estadísticas reseteadas.")

    # Presiona F3 para mostrar las estadísticas
    def on_f3_press():
        show_statistics()
class UIElement:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pass

class TextBlock(UIElement):
    def __init__(self, x, y, width, height, text="", font_size=20, font_color=(255, 255, 255), max_chars=None, draw_background=True):
        super().__init__(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.max_chars = max_chars
        self.draw_background = draw_background  # Nuevo parámetro
        self.font = pygame.font.Font(None, self.font_size)
        self.lines = []
        self.images = []
        self.update_content()

    def update_content(self):
        self.lines = []

        if self.max_chars is not None and len(self.text) > self.max_chars:
            words = self.text.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) <= self.max_chars:
                    current_line += word + " "
                else:
                    self.lines.append(current_line.rstrip())
                    current_line = word + " "
            self.lines.append(current_line.rstrip())
        else:
            self.lines.append(self.text)

        self.rendered_lines = [self.font.render(line, True, self.font_color) for line in self.lines]
        self.adjust_position()

    def add_image(self, image_path, opacity=255, size=None):
        image = pygame.image.load(image_path).convert_alpha()
        if size is not None:
            image = pygame.transform.scale(image, size)
        image.set_alpha(opacity)
        self.images.append(image)
        self.adjust_position()

    def adjust_position(self):
        total_height = sum(line.get_rect().height for line in self.rendered_lines)
        for image in self.images:
            total_height += image.get_rect().height

        if total_height > self.rect.height:
            self.rect.height = total_height

    def draw(self, screen):
        if self.draw_background:  
            pygame.draw.rect(screen, (0, 0, 0), self.rect)  

        current_y = self.rect.y
        for rendered_line in self.rendered_lines:
            screen.blit(rendered_line, (self.rect.x, current_y))
            current_y += rendered_line.get_rect().height

        for image in self.images:
            screen.blit(image, (self.rect.x, current_y))
            current_y += image.get_rect().height

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.target = None  

    def set_target(self, target):
        self.target = target

    def update(self):
        if self.target:
            self.x = self.target.rect.centerx - self.width / 2
            self.y = self.target.rect.centery - self.height / 2

    def apply(self, rect):
        return pygame.Rect(rect.x * self.zoom - self.x, rect.y * self.zoom - self.y, rect.width * self.zoom, rect.height * self.zoom)
