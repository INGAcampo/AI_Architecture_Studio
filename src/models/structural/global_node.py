class GlobalNode:

    def __init__(self, node_id=0, x=0.0, y=0.0, z=0.0):

        self.node_id = node_id

        self.x = x
        self.y = y
        self.z = z

        self.connected_columns = []
        self.connected_beams = []
        self.connected_foundations = []

        self.constraints = []
        self.loads = []
