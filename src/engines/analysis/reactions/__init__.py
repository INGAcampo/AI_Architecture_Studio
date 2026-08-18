from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ReactionResult:
    restrained_equation:int
    value:float

class ReactionSolver:
    def calculate(self,full_stiffness,full_displacements,full_loads,restrained_equations):
        reactions=[]
        for eq in restrained_equations:
            internal=sum(full_stiffness[eq][j]*full_displacements[j] for j in range(len(full_displacements)))
            reactions.append(ReactionResult(eq,internal-full_loads[eq]))
        return tuple(reactions)

    def equilibrium(self,reactions,applied_loads,tolerance=1e-8):
        return abs(sum(r.value for r in reactions)+sum(applied_loads))<=tolerance
