from analysis.dynamic.generalized_eigen import GeneralizedEigenEngine
from analysis.dynamic.modal_frequency import ModalFrequencyEngine
from analysis.dynamic.mode_shape import ModeShapeEngine
from analysis.dynamic.dynamic_domain import ModalMode,DynamicAnalysisResult
class ModalAnalysisEngine:
    def solve(self,K,M):
        values,shapes=GeneralizedEigenEngine().solve(K,M);modes=[]
        for i,(v,s) in enumerate(zip(values,shapes),1):
            _,f,t=ModalFrequencyEngine().from_eigenvalue(v)
            modes.append(ModalMode(i,v,f,t,ModeShapeEngine().normalize(s)))
        n=max(len(modes),1)
        ratios=tuple(1/n for _ in modes)
        return DynamicAnalysisResult(tuple(modes),tuple(1.0 for _ in modes),ratios,True)
