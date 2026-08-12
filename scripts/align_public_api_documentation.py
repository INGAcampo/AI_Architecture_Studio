"""Conservatively add semantic docstrings to undocumented multiline public APIs."""
from __future__ import annotations
import ast
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACKAGE_PURPOSE={
 "aias_omega_core":"the Omega application core and shared runtime services",
 "aias_aeps_advanced_v4":"advanced AEPS production, governance and observability",
 "aias_multistudio_shell":"the coordinated multi-studio desktop shell",
 "aias_aeps_autonomous_v5":"autonomous engineering planning and controlled execution",
 "aias_bim_professional_foundation":"professional BIM foundation modeling and exchange",
 "aias_omega_release2":"the second Omega integrated product release",
 "aias_omega_release3":"the third Omega integrated product release",
 "aias_omega_release4":"the fourth Omega integrated product release",
 "aias_omega_release5":"the fifth Omega integrated product release",
 "aias_omega_release6":"the sixth Omega integrated product release",
 "aias_aeps_automation_v3":"AEPS repeatable generation and delivery automation",
 "aias_foundation_documentation":"foundation drawings, schedules and technical documentation",
 "aias_bim_foundation":"foundational BIM entities and relationships",
 "aias_aeps_foundation":"the AEPS foundation production runtime",
 "aias_geometry":"shared geometric operations",
 "aias_generative":"generative engineering workflows",
 "aias_cad_foundation":"foundational CAD services",
 "aias_cad_professional":"professional CAD commands and drawing behavior",
 "aias_cad_viewport":"interactive CAD viewport rendering and navigation",
 "aias_bim_wall":"native BIM wall authoring",
 "aias_bim_door":"native BIM door authoring",
 "aias_bim_window":"native BIM window authoring",
 "aias_documentation":"professional drawing and report production",
 "aias_ai_kernel":"controlled AI-assisted engineering operations",
 "aias_enterprise_v7_v10":"enterprise portfolio, orchestration and governance capabilities",
 "aias_context_engine":"the AIAS continuity and context system",
 "aias_adf":"the AIAS development factory",
 "aias_asset_registry":"the universal engineering asset registry",
 "aias_engineering_system":"the executable AIAS engineering operating system",
 "aias_program_s1_cad":"the S1 professional CAD foundation program",
 "aias_omega_structural_suite":"the Omega structural analysis and design suite",
 "aias_autonomous_cloud":"the cloud-neutral autonomous engineering control plane",
 "aias_cad_bim_integration":"controlled CAD and BIM interchange",
 "aias_capability_factory":"repeatable engineering capability production",
 "aias_central_nervous_system":"event-driven AIAS coordination",
 "aias_continuous_observatory":"continuous technology observation and governed adoption",
 "aias_development_platform":"specification-driven AIAS development workflows",
 "aias_drawing_framework":"professional engineering drawing production",
 "aias_end_to_end":"end-to-end governed engineering project production",
 "aias_engineering_intelligence":"evidence-grounded engineering intelligence",
 "aias_engineering_os":"the AIAS engineering operating system",
 "aias_engineering_wave12":"early-value professional engineering capabilities",
 "aias_enterprise_knowledge_graph":"traceable enterprise engineering knowledge",
 "aias_enterprise_offices":"the AIAS virtual enterprise offices",
 "aias_level5_assurance":"honest Level 5 evidence and maturity assurance",
 "aias_pmo":"portfolio governance and macro-delivery selection",
 "aias_security_recovery":"security, signed backup and recovery assurance",
 "aias_technical_file":"professional technical-file generation",
 "aias_university":"competency-based AIAS learning and certification",
 "aias_virtual_organization":"segregated virtual engineering roles and review",
}

def phrase(name:str,owner:str|None,purpose:str)->str:
 words=name.replace("_"," ")
 subject=f"{owner}.{name}" if owner else name
 if name.startswith(("validate","check","verify")):return f"Validate {words.split(' ',1)[-1] or 'inputs'} for {purpose} and report explicit issues."
 if name.startswith(("create","build","generate","make","new")):return f"Build the {words.split(' ',1)[-1]} required by {purpose} from explicit inputs."
 if name.startswith(("load","read","open","import")):return f"Load {words.split(' ',1)[-1]} for {purpose} while preserving typed state."
 if name.startswith(("save","write","export","serialize")):return f"Persist {words.split(' ',1)[-1]} for {purpose} in its stable external representation."
 if name.startswith(("get","find","list","query","search","resolve")):return f"Return {words.split(' ',1)[-1]} from {purpose} using deterministic lookup rules."
 if name.startswith(("to_","as_")):return f"Project the current value into the stable {words.split(' ',1)[-1]} representation."
 if name.startswith(("add","register","attach","insert")):return f"Add {words.split(' ',1)[-1]} to {purpose} while enforcing identity constraints."
 if name.startswith(("remove","delete","clear","detach")):return f"Remove the requested {words.split(' ',1)[-1]} from {purpose} without affecting unrelated state."
 if name.startswith(("update","set","apply","execute","run","process")):return f"Execute {words} for {purpose} with validated state transitions."
 if name.startswith(("is_","has_","can_")):return f"Return whether {words.replace('is ','').replace('has ','').replace('can ','')} holds for {purpose}."
 return f"Execute the public {subject} operation for {purpose} using explicit caller inputs."

def align(path:Path,purpose:str)->int:
 text=path.read_text(encoding="utf-8");lines=text.splitlines(keepends=True)
 try:tree=ast.parse(text)
 except SyntaxError:return 0
 inserts=[]
 if not ast.get_docstring(tree):
  inserts.append((0,f'"""Public module supporting {purpose}."""\n'))
 for node in tree.body:
  candidates=[]
  if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and not node.name.startswith("_"):
   candidates.append((node,None))
  if isinstance(node,ast.ClassDef):
   candidates.extend((child,node.name) for child in node.body if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)) and not child.name.startswith("_"))
  for target,owner in candidates:
   if ast.get_docstring(target) or not target.body:continue
   first=target.body[0]
   insertion_line=min([first.lineno]+[decorator.lineno for decorator in getattr(first,"decorator_list",[])])
   if insertion_line<=target.lineno:continue
   indent=" "*first.col_offset
   doc=phrase(target.name,owner,purpose).replace('"','\\"')
   inserts.append((insertion_line-1,f'{indent}"""{doc}"""\n'))
 for index,value in sorted(inserts,reverse=True):lines.insert(index,value)
 if inserts:path.write_text("".join(lines),encoding="utf-8")
 return len(inserts)

def main()->None:
 total=0;rows=[]
 for package,purpose in PACKAGE_PURPOSE.items():
  folder=ROOT/"src"/package
  if not folder.is_dir():continue
  count=sum(align(path,purpose) for path in sorted(folder.glob("*.py")))
  rows.append((package,count));total+=count
 print({"inserted":total,"packages":rows})

if __name__=="__main__":main()
