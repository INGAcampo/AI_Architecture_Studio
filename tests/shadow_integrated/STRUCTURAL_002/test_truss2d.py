import math
from structural_platform_ext.truss2d import *

E=200e9; A=0.01

def test_bar_closed_form():
    L=2.; P=10000.
    m=TrussModel((TrussNode("A",0,0,True,True),TrussNode("B",L,0,False,True)),(TrussMember("AB","A","B",A,E),),(TrussLoad("B",P,0),))
    r=solve_truss_2d(m)
    assert math.isclose(r.displacements_m["B"][0],P*L/(A*E),rel_tol=1e-10)
    assert math.isclose(r.member_axial_forces_n["AB"],P,rel_tol=1e-10)
    assert math.isclose(r.reactions_n["A"][0],-P,rel_tol=1e-10)

def test_triangle_equilibrium():
    m=TrussModel(
      (TrussNode("A",0,0,True,True),TrussNode("B",4,0,False,True),TrussNode("C",2,3)),
      (TrussMember("AC","A","C",A,E),TrussMember("BC","B","C",A,E),TrussMember("AB","A","B",A,E)),
      (TrussLoad("C",0,-20000),))
    r=solve_truss_2d(m)
    assert math.isclose(r.reactions_n["A"][1],10000.,rel_tol=1e-9)
    assert math.isclose(r.reactions_n["B"][1],10000.,rel_tol=1e-9)

def test_unstable_fails_closed():
    m=TrussModel((TrussNode("A",0,0,True,False),TrussNode("B",1,0)),(TrussMember("AB","A","B",A,E),),(TrussLoad("B",0,-1000),))
    try: solve_truss_2d(m)
    except ValueError as e:
        assert "singular" in str(e); return
    assert False
