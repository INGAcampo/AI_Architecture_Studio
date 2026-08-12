from analysis.composites.composite_damage_domain import CompositeDamageState,CompositeDamageResult
class ProgressiveDamageLoop:
    def run(self,failure_index,max_iterations=20):
        damage=0.0
        for iteration in range(1,max_iterations+1):
            if failure_index<=1.0:
                return CompositeDamageResult(CompositeDamageState(damage,damage*.5,damage*.25,0.0,False),failure_index,iteration,True)
            damage=min(.999999,damage+.1*(failure_index-1)); failure_index*=max(.2,1-damage)
        return CompositeDamageResult(CompositeDamageState(damage,damage*.5,damage*.25,0.0,damage>.95),failure_index,max_iterations,False)
