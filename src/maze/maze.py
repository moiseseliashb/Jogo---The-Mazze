import pygame

class Maze:
    def __init__(self, layout, cell_size):
        self.layout = layout
        self.cell_size = cell_size

        self.width = len(layout[0])
        self.height = len(layout)

        self.walls = self._build_walls()
    
    def draw(self, surface, camera_position):
        for row_index, row in enumerate(self.layout):
            for column_index, cell in enumerate(row):
                if cell != '#':
                    continue

                world_x = column_index * self.cell_size
                world_y = row_index * self.cell_size

                # ----- Posição das celulas

                screen_x = world_x - camera_position.x
                screen_y = world_y - camera_position.y

                pygame.draw.rect(
                    surface,
                    (255, 255, 255),
                    (
                        int(screen_x),
                        int(screen_y),
                        self.cell_size,
                        self.cell_size
                    )
                )
    
    def collides_with_circle(self, position, radius):
        for row_index, row in enumerate(self.layout):
            for column_index, cell in enumerate(row):
                if cell != '#':
                    continue

                wall_rect = pygame.Rect(
                    column_index * self.cell_size,
                    row_index * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                closest_x = max(
                    wall_rect.left,
                    min(position.x, wall_rect.right)
                )

                closest_y = max(
                    wall_rect.top,
                    min(position.y, wall_rect.bottom)
                )

                distance_squared = (
                    (position.x - closest_x) ** 2 + (position.y - closest_y) ** 2
                )

                if distance_squared < radius ** 2:
                    return True
        
        return False
    
    def _build_walls(self):

        walls = []

        for row_index, row in enumerate(self.layout):
            for column_index, cell in enumerate(row):

                if cell != '#':
                    continue

                wall_rect = pygame.Rect(
                    column_index * self.cell_size,
                    row_index * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                walls.append(wall_rect)
        
        return walls
    
    def raycast(self, start, end):
        closest_point = None
        closest_distance_squared = float('inf')

        for wall in self.walls:
            clipped_line = wall.clipline(start, end)

            if not clipped_line:
                continue

            for point in clipped_line:
                distance_squared = start.distance_squared_to(point)

                if distance_squared < closest_distance_squared:
                    closest_distance_squared = distance_squared
                    closest_point = pygame.Vector2(point)
        
        if closest_point is None:
            return pygame.Vector2(end)
        
        return closest_point
