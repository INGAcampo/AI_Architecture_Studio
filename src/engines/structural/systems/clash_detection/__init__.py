from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class BoundingBox:
    object_id:str
    minimum:tuple[float,float,float]
    maximum:tuple[float,float,float]

@dataclass(frozen=True,slots=True)
class StructuralClash:
    object_a_id:str
    object_b_id:str

class StructuralClashDetection:
    def overlaps(self,a,b):
        return all(a.minimum[i]<b.maximum[i] and b.minimum[i]<a.maximum[i] for i in range(3))
    def detect(self,boxes):
        clashes=[]
        boxes=tuple(boxes)
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                if self.overlaps(a,b): clashes.append(StructuralClash(a.object_id,b.object_id))
        return tuple(clashes)
