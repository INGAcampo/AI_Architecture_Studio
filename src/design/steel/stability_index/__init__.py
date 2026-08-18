from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StoryStabilityResult:
    story_id: str
    vertical_load: float
    drift: float
    story_shear: float
    height: float
    theta: float
    stable: bool

class StabilityIndexEngine:
    def calculate(self,story_id,vertical_load,drift,story_shear,height,limit=0.10):
        denominator=max(abs(story_shear*height),1e-12)
        theta=abs(vertical_load*drift)/denominator
        return StoryStabilityResult(story_id,vertical_load,drift,story_shear,height,theta,theta<=limit)
