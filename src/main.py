import pygame

from entities.player import Player
from camera import Camera
from maze.maze import Maze
from maze.mazes import generate_maze, set_cell_size
from grid import draw_grid
from lighting.lighting_renderer import LightingRenderer

pygame.init()


# --- Inicializando os objetos




maze = Maze(
    generate_maze(),
    set_cell_size()
)

# Set up the display

HEIGHT = 600
WIDTH = 800

WORLD_WIDTH = maze.width * set_cell_size()
WORLD_HEIGHT = maze.height * set_cell_size()


clock = pygame.time.Clock()
print(f"Starting the game...")


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Mazze")

player = Player((WORLD_WIDTH // 2, WORLD_HEIGHT // 2))

camera = Camera(WIDTH, HEIGHT)

lighting_renderer = LightingRenderer(screen, player, maze, camera)



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # --- Delta Time
    dt = clock.tick(60) / 1000
    
    player.update(dt, maze)
    
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
    maze.draw(
        screen,
        camera.position
    )

    player.draw(screen, camera.position)
    lighting_renderer.render()

    # Update the display
    pygame.display.flip()

pygame.quit()

