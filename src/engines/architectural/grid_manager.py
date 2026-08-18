class GridManager:

    def __init__(self):
        self.grids = []

    def add_grid(self, grid):
        self.grids.append(grid)

    def get_grids(self):
        return list(self.grids)
