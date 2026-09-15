import pygame

class Camera:
    def __init__ (self, viewport_widht, viewport_height):
        self.position = pygame.Vector2(0, 0)

        self.viewport_widht = viewport_widht
        self.viewport_height = viewport_height
    
    def update(self, target_position, world_widht, world_height):
        # centraliza a câmara no jogador
        self.position.x = target_position.x - self.viewport_widht / 2
        self.position.y = target_position.y - self.viewport_height / 2

        # Limites da câmara
        max_x = world_widht - self.viewport_widht
        max_y = world_height - self.viewport_height

        self.position.x = max(
            0,
        min(self.position.x, max_x)
        )

        self.position.y = max(
            0,
            min(self.position.y, max_y)
        )