from aias_structural_codes_program import ComputeJob,DistributedComputePlanner,DocumentAutomationEngine,DocumentEvidence,GovernedOptimizer,OptimizationCandidate,OptimizationPolicy,REQUIRED_DOCUMENTS
H="a"*64
def test_optimizer_filters_constraints_and_proposes_best_score():
 c=(OptimizationCandidate("A",(("weight",100),("cost",90)),(("ratio",.9),),H),OptimizationCandidate("B",(("weight",80),("cost",100)),(("ratio",1.1),),H));p=OptimizationPolicy("P",(("weight",1),("cost",.1)),(("ratio",1),));r=GovernedOptimizer().select(c,p);assert r.selected_id=="A" and r.rejected[0][0]=="B" and r.human_approval_required and not r.global_optimum_claimed
def test_optimizer_reports_no_feasible_candidate():
 r=GovernedOptimizer().select((OptimizationCandidate("X",(("weight",1),),(('ratio',2),),H),),OptimizationPolicy("P",(("weight",1),),(('ratio',1),)));assert r.status=="NO_FEASIBLE_CANDIDATE"
def test_document_package_requires_complete_integrity_evidence():
 d=tuple(DocumentEvidence(k,k,"R1",f"artifact://{k}",H) for k in sorted(REQUIRED_DOCUMENTS));r=DocumentAutomationEngine().assemble("PKG",d);assert r.status=="READY_FOR_PROFESSIONAL_REVIEW" and len(r.manifest_sha256)==64
def test_incomplete_document_package_is_blocked():assert DocumentAutomationEngine().assemble("PKG",()).status=="BLOCKED"
def test_distributed_plan_is_dependency_safe():
 j=(ComputeJob("A","SOLVER",H),ComputeJob("B","REPORT",H,("A",)),ComputeJob("C","REPORT",H,("A",)));r=DistributedComputePlanner().plan("P",j,{"SOLVER","REPORT"});assert r.status=="READY" and r.batches==(("A",),("B","C"))
def test_distributed_cycle_is_blocked():
 j=(ComputeJob("A","X",H,("B",)),ComputeJob("B","X",H,("A",)));r=DistributedComputePlanner().plan("P",j,{"X"});assert r.status=="BLOCKED" and "dependency_cycle" in r.issues
