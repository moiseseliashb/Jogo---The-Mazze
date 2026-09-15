import pygame

class Player:
    def __init__ (self, position):

        self.position = pygame.Vector2(position)
        self.radius = 15
        self.speed = 100
    
    def update(self, dt, maze):
        direction = pygame.Vector2(0, 0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            direction.x -= 1
        
        if keys[pygame.K_s]:
            direction.y -= 1
        
        if keys[pygame.K_z]:
            direction.y += 1
        
        if keys[pygame.K_x]:
            direction.x += 1
        
        # ... Estabilizador de velocidade diagonal
        if direction.length_squared() > 0:
            direction = direction.normalize() * self.speed * dt
        
        movement = direction * self.speed * dt

        new_position = self.position + movement

        if not maze.collides_with_cicrle(new_position, self.radius):

            self.position = new_position

        # .... 
    
    def draw(self, screen, camera_position):
        screen_position = self.position - camera_position

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(screen_position.x), int(screen_position.y)),
            self.radius
        )