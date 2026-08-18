from design.steel.domain import *
def seed_default_catalog(pr,mr):
 ps=(SteelProfile('W12X26','W12X26',SteelProfileFamily.W,.00494,38.7,1e-4,2.1e-5,2.2e-4,8.2e-5,2.45e-4,9.1e-5,.142,.065),SteelProfile('W14X38','W14X38',SteelProfileFamily.W,.0072,56.6,2.08e-4,3.4e-5,3.05e-4,9.7e-5,3.42e-4,1.08e-4,.17,.069),SteelProfile('IPE300','IPE300',SteelProfileFamily.IPE,.00538,42.2,8.36e-5,6.04e-6,5.57e-4,8.05e-5,6.28e-4,1.26e-4,.125,.0335),SteelProfile('HEA300','HEA300',SteelProfileFamily.HEA,.01125,88.3,1.826e-4,6.31e-5,1.218e-3,4.21e-4,1.38e-3,6.41e-4,.127,.0749),SteelProfile('HSS200X200X8','HSS200X200X8',SteelProfileFamily.HSS,.00586,46,3.55e-5,3.55e-5,3.55e-4,3.55e-4,4.2e-4,4.2e-4,.0778,.0778))
 ms=(SteelMaterial('ASTM_A36','ASTM A36',250e6,400e6,200e9,7850,'ASTM'),SteelMaterial('ASTM_A992','ASTM A992',345e6,450e6,200e9,7850,'ASTM'),SteelMaterial('S355','S355',355e6,510e6,210e9,7850,'EN'))
 for p in ps: pr.register(p,replace=True)
 for m in ms: mr.register(m,replace=True)
 return ps,ms
