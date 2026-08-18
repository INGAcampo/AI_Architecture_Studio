class GlobalNodeEngine:

    SNAP_TOLERANCE = 0.50

    @staticmethod
    def generate(scene):

        return []

    @staticmethod
    def next_id(nodes):

        if not nodes:
            return 1

        return max(node.node_id for node in nodes) + 1
