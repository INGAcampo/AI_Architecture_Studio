"""Public module supporting the AEPS foundation production runtime."""
from pathlib import Path
DIRS=('00_GOVERNANCE','01_CHARTER','02_CONSTITUTION','03_ONTOLOGY','04_KNOWLEDGE_MODEL','05_SDD','06_ARCHITECTURE','07_STANDARDS','08_QUALITY','09_DEVELOPMENT_PLATFORM','10_CERTIFICATION','11_RELEASE','12_KNOWLEDGE_GRAPH','13_AI','14_ENTERPRISE','15_EVOLUTION','adr','schemas','templates','validators','generators','metrics','glossary','examples','roadmap','tests','registry')
def bootstrap(root):
 """Execute the public bootstrap operation for the AEPS foundation production runtime using explicit caller inputs."""
 out=[]
 for n in DIRS:
  p=Path(root)/'engineering'/'aeps'/n; p.mkdir(parents=True,exist_ok=True); (p/'.gitkeep').write_text('',encoding='utf-8'); out.append(p)
 return tuple(out)
