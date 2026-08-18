"""Lighthouse BIM-footprint reference consumer."""
from .models import BimElement,InterchangeModel
def lighthouse_model():
    """Create one attributable foundation and wall model in canonical millimetres."""
    return InterchangeModel("LIGHTHOUSE-BIM-001","1.0.0","mm",(BimElement("FND-001","Footing","Main footing",((80,70),(180,70),(180,150),(80,150)),{"material":"concrete","mark":"F1"},"LIGHTHOUSE-001"),BimElement("WALL-001","Wall","North wall",((80,170),(300,170),(300,180),(80,180)),{"material":"masonry","mark":"W1"},"LIGHTHOUSE-001")),{"source":"LIGHTHOUSE-001"})
