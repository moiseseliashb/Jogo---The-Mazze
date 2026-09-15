import pygame

from entities.player import Player
from camera import Camera
from grid import draw_grid

pygame.init()

# Set up the display
HEIGHT = 600
WIDTH = 800

WORLD_WIDTH = 2000
WORLD_HEIGHT = 1200

clock = pygame.time.Clock()
print(f"Starting the game...")


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Mazze")

player = Player((WORLD_WIDTH // 2, WORLD_HEIGHT // 2))
camera = Camera(WIDTH, HEIGHT)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # --- Delta Time
    dt = clock.tick(60) / 1000
    
    player.update(dt)
    
    # Limites do Jogador
    player.position.x = max(
        player.radius, 
        min(WORLD_WIDTH - player.radius, player.position.x)
        )

    player.position.y = max(
        player.radius, 
        min(WORLD_HEIGHT - player.radius, player.position.y)
        )

    
    camera.update(
        player.position,
        WORLD_WIDTH,
        WORLD_HEIGHT
    )
    
    # ----------- Renderizando os objetos na tela
    screen.fill((0, 0, 0))

    draw_grid(
        screen,
        camera,
        WORLD_WIDTH,
        WORLD_HEIGHT,
        HEIGHT,
        WIDTH
    )

    player.draw(screen, camera.position)

    # Update the display
    pygame.display.flip()

pygame.quit()

