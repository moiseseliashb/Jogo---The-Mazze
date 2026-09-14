import pygame

pygame.init()

# Set up the display
HEIGHT = 600
WIDTH = 800

clock = pygame.time.Clock()
print(f"Starting the game... {clock}")

player = {
    "x": WIDTH // 2,
    "y": HEIGHT // 2,
    "radius": 30,
    "speed": 300,
    "color": (255, 255, 255)  # White color
}


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Mazze")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # --- Delta Time
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player['x'] -= player['speed'] * dt 
    
    if keys[pygame.K_s]:
        player['y'] -= player['speed'] * dt 
    
    if keys[pygame.K_z]:
        player['y'] += player['speed'] * dt 
    
    if keys[pygame.K_x]:
        player['x'] += player['speed'] * dt 

    
    screen.fill((0, 0, 0))
    
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (int(player['x']), int(player['y'])),
        player['radius']
        )

    # Fill the screen with a color (e.g., white)
    

    # Update the display
    pygame.display.flip()

pygame.quit()

