"""Public module supporting professional BIM foundation modeling and exchange."""
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.graph import Relationship

class OmegaBridge:
    """Execute the public OmegaBridge operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def publish_wall(self,project,wall,analytical,quantity):
        """Execute the public OmegaBridge.publish_wall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        a=EngineeringObject(object_type="bim_wall",name=wall.name,
            geometry={"start":[wall.start.x,wall.start.y],"end":[wall.end.x,wall.end.y]},
            properties={"length_m":wall.length_m,"height_m":wall.height_m,
                        "thickness_m":wall.thickness_m,"net_volume_m3":quantity.net_volume_m3},
            material_id=wall.material_id,classification="BIM.Wall")
        aid=project.add_object(a)
        b=EngineeringObject(object_type="structural_wall",name=f"Analytical {wall.name}",
            properties={"length_m":analytical.length_m,"area_m2":analytical.area_m2},
            material_id=wall.material_id,classification="Structural.Wall")
        bid=project.add_object(b)
        project.graph.add(Relationship(aid,bid,"analytical_representation"))
        return aid,bid
