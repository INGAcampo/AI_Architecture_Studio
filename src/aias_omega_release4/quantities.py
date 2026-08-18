"""Public module supporting the fourth Omega integrated product release."""
class BimQuantityService:
    """Execute the public BimQuantityService operation for the fourth Omega integrated product release using explicit caller inputs."""
    def wall_net_area(self, project, wall_id):
        """Execute the public BimQuantityService.wall_net_area operation for the fourth Omega integrated product release using explicit caller inputs."""
        wall=project.objects[wall_id]
        gross=wall.properties["length_m"]*wall.properties["height_m"]
        openings=0.0
        for rel in project.graph.outgoing(wall_id,"hosts_opening"):
            o=project.objects[rel.target]
            openings += o.properties["width_m"]*o.properties["height_m"]
        return gross-openings

    def wall_net_volume(self, project, wall_id):
        """Execute the public BimQuantityService.wall_net_volume operation for the fourth Omega integrated product release using explicit caller inputs."""
        wall=project.objects[wall_id]
        return self.wall_net_area(project,wall_id)*wall.properties["thickness_m"]
