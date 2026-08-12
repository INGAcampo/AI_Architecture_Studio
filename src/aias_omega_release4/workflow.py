"""Public module supporting the fourth Omega integrated product release."""
from aias_omega_core.materials import Material
from aias_omega_core.project import EngineeringProject
from .bim import BimFactory, LevelSpec
from .quantities import BimQuantityService

def build_bim_building():
    """Build the bim building required by the fourth Omega integrated product release from explicit inputs."""
    p=EngineeringProject("Omega BIM Building")
    p.materials.add(Material("CONC_30","Concrete 30 MPa","concrete",{"E_MPa":30000}))
    f=BimFactory(); level=f.create_level(p,LevelSpec("Ground Floor",0.0))
    walls=[
        f.create_wall(p,(0,0),(8,0),3,0.2,"CONC_30",level,"South Wall"),
        f.create_wall(p,(8,0),(8,6),3,0.2,"CONC_30",level,"East Wall"),
        f.create_wall(p,(8,6),(0,6),3,0.2,"CONC_30",level,"North Wall"),
        f.create_wall(p,(0,6),(0,0),3,0.2,"CONC_30",level,"West Wall"),
    ]
    f.create_opening(p,walls[0],1.0,2.1,0.0,"door","Main Door")
    f.create_opening(p,walls[2],1.5,1.2,0.9,"window","Window W01")
    slab=f.create_slab(p,[(0,0),(8,0),(8,6),(0,6)],0.15,"CONC_30",level,"Ground Slab")
    q=BimQuantityService()
    return p, {"walls":walls,"slab":slab,"net_wall_volume_m3":sum(q.wall_net_volume(p,w) for w in walls)}
