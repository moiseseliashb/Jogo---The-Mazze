from collections import deque

class PathFinding:

    def __init__(self, maze):
        self.maze = maze

    
    def find_path(self, start, target):
        if not self.maze.is_valid_cell(*start):
            return None

        
        if not self.maze.is_valid_cell(*target):
            return None
        
        if not self.maze.is_open(*start):
            return None

        if not self.maze.is_open(*target):
            return None

        
        queue = deque([start])

        previous = {
            start: None
        }

        while queue:
            current = queue.popleft()

            if current == target:
                return self._reconstruct_path(
                    previous,
                    target
                )
            
            row, column = current

            neighbors = [
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1)
            ]

            for neighbor in neighbors:

                if neighbor in previous:
                    continue

                neighbor_row, neighbor_column = neighbor

                if not self.maze.is_valid_cell(
                    neighbor_row,
                    neighbor_column):
                    continue

                if not self.maze.is_open(
                    neighbor_row,
                    neighbor_column):
                    continue

                previous[neighbor] = current

                queue.append(neighbor)
        
        return None
    
    def has_path(self, start, target):
        return self.find_path(start, target) is not None

    
    def _reconstruct_path(self, previous, target):

        path = []

        current = target

        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()

        return path

    
    def world_to_cell(self, position):
        column = int(position.x // self.maze.cell_size)
        row = int(position.y // self.maze.cell_size)

        return row, column