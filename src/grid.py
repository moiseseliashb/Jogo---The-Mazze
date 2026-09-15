import pygame

def draw_grid(surface, camara, world_widht, world_height, HEIGHT, WIDHT):
    grid_size = 100

    for x in range(0, world_widht + 1, grid_size):
        screen_x = x - camara.position.x

        pygame.draw.line(
            surface,
            (255, 255, 255),
            (int(screen_x), 0),
            (int(screen_x), HEIGHT)
        )

    
    for y in range(0, world_height + 1, grid_size):
        screen_y = y - camara.position.y

        pygame.draw.line(
            surface,
            (255, 255, 255),
            (0, int(screen_y)),
            (WIDHT, int(screen_y))
        )