from aias_regeneration import RegenerationEngine
from aias_building_design_core import BuildingDesignCore

def test_change_invalidates_topological_downstream():
    c=BuildingDesignCore(); a=c.seed_pilot(c.create_project('P')); b=c.seed_pilot(c.create_project('P')); b.nodes[0]['properties']['units']='SI-v2'
    e=RegenerationEngine(); plan=e.plan(a,b,{}); assert plan['changed'] and plan['order'][0]=='standards'
    result=e.execute(plan,{key:(lambda k=key:{'artifact':k}) for key in plan['order']}); assert result['status']=='PASS' and len(result['journal'])==9

def test_abort_rolls_back_artifacts():
    c=BuildingDesignCore(); a=c.seed_pilot(c.create_project('P')); b=c.seed_pilot(c.create_project('P')); b.nodes[0]['properties']['units']='SI-v2'; e=RegenerationEngine(); p=e.plan(a,b,{})
    result=e.execute(p,{key:(lambda k=key: (_ for _ in ()).throw(RuntimeError('fail')) if k=='cad' else {'x':k}) for key in p['order']}); assert result['status']=='ABORTED' and not result['artifacts']
