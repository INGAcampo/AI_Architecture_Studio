"""Public module supporting the fifth Omega integrated product release."""
from .truss import Node,Bar,Truss2DSolver
def solve_demo_truss():
    """Execute the public solve_demo_truss operation for the fifth Omega integrated product release using explicit caller inputs."""
    nodes=[
        Node("N1",0,0,True,True),
        Node("N2",4,0,False,True),
        Node("N3",2,3,False,False,0,-100000),
    ]
    E=200e9; A=0.005
    bars=[Bar("B1","N1","N2",A,E),Bar("B2","N1","N3",A,E),Bar("B3","N2","N3",A,E)]
    return Truss2DSolver().solve(nodes,bars)
