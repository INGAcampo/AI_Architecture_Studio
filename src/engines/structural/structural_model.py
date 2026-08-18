class StructuralModel:

    def __init__(self):

        self.nodes = []
        self.columns = []
        self.beams = []
        self.foundations = []

    def add_node(self, node):

        self.nodes.append(node)
