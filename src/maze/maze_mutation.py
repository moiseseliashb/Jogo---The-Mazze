class MazeMutation:
    def __init__(self, maze):
        self.maze = maze
    
    def apply(self, cells, value):
        self.maze.mutate_cells(cells, value)
    
    def open_cells(self, cells):
        self.apply(cells, '.')