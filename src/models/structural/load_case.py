class LoadCase:

    DEAD = "dead"
    LIVE = "live"
    WIND = "wind"
    SEISMIC = "seismic"

    def __init__(self, name="", load_type=DEAD, factor=1.0):

        self.name = name
        self.load_type = load_type
        self.factor = factor
        self.loads = []
