from dataclasses import dataclass
from analysis.fem2d.adaptive_marking import AdaptiveMarkingEngine
from analysis.fem2d.h_refinement import HRefinementEngine
@dataclass(frozen=True,slots=True)
class AdaptivePipelineResult: marked_elements:tuple; target_sizes:tuple
class AdaptivePipeline:
    def run(self,errors,sizes,target):
        marked=AdaptiveMarkingEngine().mark(errors); return AdaptivePipelineResult(marked,tuple(HRefinementEngine().target_size(sizes[i],errors[i],target) for i in marked))