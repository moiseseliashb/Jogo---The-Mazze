import pygame

from entities.player import Player
from camera import Camera
from maze.maze import Maze
from maze.mazes import mazes, set_cell_size
from grid import draw_grid

pygame.init()


# --- Inicializando os objetos




maze = Maze(
    mazes(),
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


    visibility_points = player.light.calculate_visibility(
        player.position,
        maze
    )

    screen_points = []
    for light_data in visibility_points:

        points = light_data['position']
        intensity = light_data['intensity']

        screen_point = points - camera.position
        screen_points.append({
            'position': 
            (int(screen_point.x),
            int(screen_point.y)),
            'intensity': intensity
        })
    
    

    # ------- Camada de escuridão
    darkness = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA)
    
    light_gradient = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )
    
    # ------- Camada de máscara de luz
    polygon_points = []

    for light_data in screen_points:
        polygon_points.append(light_data['position'])

    light_mask = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    light_mask.fill((0, 0, 0, 0))

    if len(polygon_points) >= 3:
        pygame.draw.polygon(
            light_mask,
            (255, 255, 255, 255),
            polygon_points
        )
    
    # -------------------------------------

    light_gradient.fill((0, 0, 0, 0))

    light_position = (
        int(player.position.x - camera.position.x),
        int(player.position.y - camera.position.y)
    )

    radius = int(player.light.current_radius)

    for current_radius in range(radius, 0, -2):
        intensity = player.light.get_intensity(current_radius)

        alpha = int(255 * intensity)

        pygame.draw.circle(
            light_gradient,
            (0, 0, 0, alpha),
            light_position,
            current_radius
        )

    darkness.fill((0, 0, 0, 255))

    light_gradient.blit(
        light_mask,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MIN
    )

    darkness.blit(
        light_gradient,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_SUB
    )

    screen.blit(
        darkness,
        (0, 0)
    )


    # Update the display
    pygame.display.flip()

pygame.quit()

