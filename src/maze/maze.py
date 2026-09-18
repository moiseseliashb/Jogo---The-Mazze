import pygame

class Maze:
    def __init__(self, layout, cell_size):
        self.layout = [list(row) for row in layout]

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

    
    
    # ----- Mutação ------------
    def is_wall(self, row, column):
        if not self.is_valid_cell(row, column):
            return False
        
        return self.layout[row][column] == '#'
    
    def is_open(self, row, column):
        if not self.is_valid_cell(row, column):
            return False
        
        return self.layout[row][column] != '#'
    
    def is_valid_cell(self, row, column):
        return (
            0 <= row < self.height
            and
            0 <= column < self.width
        )

    def is_mutable(self, row, column):
            if not self.is_valid_cell(row, column):
                return False
            
            if row == 0 or row == self.height - 1:
                return False
            
            if column == 0 or column == self.width - 1:
                return False
            
            return True
    
    def set_cell(self, row, column, value):
        if value not in ('#', '.'):
            return

        if not self.is_mutable(row, column):
            return

        self.layout[row][column] = value
        self._rebuild_walls()
    
    def set_cells(self, cells, value):
        if value not in ('#', '.'):
            return

        valid_cells = []

        for row, column in cells:
            if self.is_mutable(row, column):
                valid_cells.append((row, column))

        
        for row, column in valid_cells:
            self.layout[row][column] = value

        if valid_cells:
            self._rebuild_walls()
    

    def mutate_cells(self, cells, value):
        mutable_cells = []

        for row, column in cells:
            if self.is_mutable(row, column):
                mutable_cells.append((row, column))
        
        if not mutable_cells:
            return

        
        self.set_cells(mutable_cells, value)
    

    def _rebuild_walls(self):
        self.walls = self._build_walls()