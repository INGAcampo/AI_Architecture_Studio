from analysis.transient.transient_domain import TransientStep,TransientResult
from analysis.transient.newmark_advanced import NewmarkAdvancedEngine
class TransientSolverPipeline:
    def solve_sdof(self,forces,dt,mass,damping,stiffness):
        u=v=a=0.0;steps=[];engine=NewmarkAdvancedEngine()
        for i,f in enumerate(forces):
            u,v,a=engine.step(u,v,a,f,mass,damping,stiffness,dt)
            steps.append(TransientStep((i+1)*dt,u,v,a))
        return TransientResult(tuple(steps),True,"Newmark-beta")
