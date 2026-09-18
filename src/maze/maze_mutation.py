import random
import pygame
from maze.pathfinding import PathFinding

class MazeMutation:
    def __init__(self, maze, mutation_interval = 3.0, mutation_size = 3, player_safe_radius = 150):

        self.maze = maze

        self.mutation_interval = mutation_interval
        self.mutation_timer = 0.0

        self.mutation_size = mutation_size

        self.player_safe_radius = player_safe_radius
        self.player_position = None

        self.pathfinder = PathFinding(maze)

    def update(self, dt, player_position):
        self.player_position = player_position

        self.mutation_timer += dt

        if self.mutation_timer < self.mutation_interval:
            return
        
        self.mutation_timer = 0.0

        self.mutate()
    
    def apply(self, cells, value):
        self.maze.mutate_cells(cells, value)
    
    def open_cells(self, cells):
        self.apply(cells, '.')
    
    def close_cells(self, cells):
        self.apply(cells, '#')
    
    def toggle_cells(self, cells):
        cells_to_open = []
        cells_to_close = []

        for row, column in cells:

            if not self.maze.is_valid_cell(row, column):
                continue

            if not self.maze.is_mutable(row, column):
                continue

            if self.is_near_player(row, column):
                return

            if self.maze.is_wall(row, column):
                cells_to_open.append((row, column))

            else:
                cells_to_close.append((row, column))
        
        self.open_cells(cells_to_open)
        self.close_cells(cells_to_close)
    
    def get_mutable_cells(self):
        cells = []

        for row in range(self.maze.height):
            for column in range(self.maze.width):

                if not self.maze.is_mutable(row, column):
                    continue

                if self.is_near_player(row, column):
                    continue

                cells.append((row, column))

        return cells
    
    def choose_random_cell(self):
        cells = self.get_mutable_cells()

        if not cells:
            return None
        
        return random.choice(cells)
    
    def create_region(self, center):
        center_row, center_column = center

        cells = []

        half_size = self.mutation_size // 2

        for row in range(
            center_row - half_size, center_row + half_size + 1):

            for column in range(center_column - half_size, center_column + half_size + 1):
                
                if not self.maze.is_mutable(row, column):
                    continue

                if self.is_near_player(row, column):
                    continue
                
                cells.append((row, column))
        
        return cells

    def choose_random_region(self):
        center = self.choose_random_cell()

        if center is None:
            return []

        
        return self.create_region(center)
    
    def is_near_player(self, row, column):
        if self.player_position is None:
            return False
        
        cell_center = pygame.Vector2(
            column * self.maze.cell_size + self.maze.cell_size / 2,
            row * self.maze.cell_size + self.maze.cell_size / 2
        )

        distance = cell_center.distance_to(self.player_position)

        return distance < self.player_safe_radius
    
    def get_player_cell(self):
        if self.player_position is None:
            return None

        return self.pathfinder.world_to_cell(
            self.player_position
        )
    
    def find_distant_target(self, start):
        reachable_cells = []

        for row in range(self.maze.height):
            for column in range(self.maze.width):

                cell = (row, column)

                if not self.maze.is_open(row, column):
                    continue
                
                if cell == start:
                    continue

                path = self.pathfinder.find_path(
                    start,
                    cell
                )

                if path is None:
                    continue

                reachable_cells.append(
                    (len(path), cell)
                )
            
        if not reachable_cells:
            return None
        
        reachable_cells.sort(
            key=lambda item: item[0], reverse=True
        )

        return reachable_cells[0][1]

    
    def test_mutation(self, cells):
        player_cell = self.get_player_cell()

        if  player_cell is None:
            return False

        
        if not self.maze.is_open(*player_cell):
            return False

        
        target = self.find_distant_target(
            player_cell
        )

        if target is None:
            return False

        
        original_values = []

        for row, column in cells:
            original_values.append(
                (
                    row,
                    column,
                    self.maze.layout[row][column]
                )
            )
        
        self.toggle_cells(cells)

        path_exists = self.pathfinder.has_path(
            player_cell,
            target
        )

        if path_exists:
            return True

        for row, column, value in original_values:
            self.maze.layout[row][column] = value
        
        self.maze._rebuild_walls()

        return False

    def mutate(self):
        cells = self.choose_random_region()

        if not cells:
            return
        
        self.test_mutation(cells)