class ReactionRecovery:
 def recover(self,K,u,F): return tuple(sum(a*b for a,b in zip(r,u))-f for r,f in zip(K,F))
