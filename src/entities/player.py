import pygame
from entities.light import Light

class Player:
    def __init__ (self, position):

        self.position = pygame.Vector2(position)
        self.radius = 15
        self.speed = 150

        self.light = Light(
            max_energy=100,
            idle_consumption=1,
            moving_consumption=2)
    
    def update(self, dt, maze):
        direction = pygame.Vector2(0, 0)

        keys = pygame.key.get_pressed()

        # -------- Luz do jogador -    
        

        if keys[pygame.K_a]:
            direction.x -= 1
        
        if keys[pygame.K_s]:
            direction.y -= 1
        
        if keys[pygame.K_z]:
            direction.y += 1
        
        if keys[pygame.K_x]:
            direction.x += 1

        
        is_moving = direction.length_squared() > 0

        self.light.update(dt, is_moving)

        
        
        # ... Estabilizador de velocidade diagonal
        if direction.length_squared() > 0:
            direction = direction.normalize()
        
        movement = direction * self.speed * dt

        new_position = self.position.copy()
        new_position.x += movement.x

        if not maze.collides_with_circle(new_position, self.radius):

            self.position.x = new_position.x

        
        new_position = self.position.copy()
        new_position.y += movement.y

        if not maze.collides_with_circle(new_position, self.radius):

            self.position.y = new_position.y

        # .... 
    
    def draw(self, screen, camera_position):
        screen_position = self.position - camera_position

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(screen_position.x), int(screen_position.y)),
            self.radius
        )

        font = pygame.font.Font(None, 36)

        light_text = font.render(
            f"Light: {self.light.energy:.1f}",
            True,
            (255, 255, 255))

        screen.blit(light_text, (20, 20))