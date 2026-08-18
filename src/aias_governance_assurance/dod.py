"""Definition-of-Done evidence evaluator."""
REQUIRED=("code","tests","integration","documentation","cli","receipt","manifest","example","installer","release","validation")
def evaluate(evidence):
 """Evaluate the complete AIAS Definition of Done evidence map."""
 gates={name:bool(evidence.get(name)) for name in REQUIRED}
 return {"done":all(gates.values()),"gates":gates,"missing":[k for k,v in gates.items() if not v]}
