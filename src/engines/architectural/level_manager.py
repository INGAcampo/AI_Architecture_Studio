class LevelManager:

    def __init__(self):
        self.levels = []

    def add_level(self, level):
        self.levels.append(level)

    def get_levels(self):
        return list(self.levels)

    def active_level(self):
        for level in self.levels:
            if level.active:
                return level
        return None
