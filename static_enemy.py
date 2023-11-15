import pygame
from animation import Animation

class Staticenemy:
    def __init__(self, x, y, width, height, speed, distance):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.distance = distance
        self.start_y = y
        self.direction = 1
        self.is_life = True
        self.wait_time = 3000  # Tiempo de espera en milisegundos (3 segundos)
        self.last_move_time = pygame.time.get_ticks()
        self.waiting = True  # Indica si el enemigo está esperando

        idle_animation = Animation([pygame.image.load("textures/a.png"), pygame.image.load("textures/a.png")])

        self.animations = {
            "idle": idle_animation,
        }
        self.current_animation = "idle"

    def move(self):
        current_time = pygame.time.get_ticks()

        # Verificar si está esperando y ha pasado el tiempo de espera completo
        if self.waiting and current_time - self.last_move_time >= self.wait_time:
            self.waiting = False  # Dejar de esperar
            self.last_move_time = current_time  # Reiniciar el tiempo de último movimiento

        # Si no está esperando, cambiar la dirección cuando haya pasado la mitad del tiempo de espera
        if not self.waiting and current_time - self.last_move_time >= self.wait_time / 2:
            self.direction *= -1
            self.waiting = True  # Volver a esperar después de cambiar de dirección
            self.last_move_time = current_time  # Reiniciar el tiempo de último movimiento

        # Moverse si no está esperando
        if not self.waiting:
            self.y += self.speed * self.direction

    def update_animation(self):
        self.current_animation = "idle"
        self.animations[self.current_animation].update()

    def draw(self, screen, camera_x):
        enemy_texture = self.animations[self.current_animation].current_frame()
        enemy_texture = pygame.transform.scale(enemy_texture, (self.width, self.height))
        enemy_rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        screen.blit(enemy_texture, enemy_rect)
