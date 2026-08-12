"""Structural and professional-boundary validation for canonical drawings."""
from __future__ import annotations
from .models import Dimension,Drawing,Line,Text

class DrawingValidator:
    """Validate identity, scale, layers, bounds, text safety and review status."""
    def validate(self,drawing:Drawing)->list[str]:
        """Return deterministic validation issues without modifying the drawing."""
        issues=[];layer_names=[x.name for x in drawing.layers];ids=[]
        if not drawing.drawing_id or not drawing.version or not drawing.provenance.get("source"):issues.append("missing_drawing_identity_or_provenance")
        if len(layer_names)!=len(set(layer_names)):issues.append("duplicate_layers")
        if not drawing.professional_review_required:issues.append("professional_review_boundary_required")
        for view in drawing.views:
            if view.scale_denominator<=0 or min(view.width_mm,view.height_mm)<=0:issues.append(f"invalid_view:{view.view_id}")
            if view.x_mm<0 or view.y_mm<0 or view.x_mm+view.width_mm>drawing.sheet.width_mm or view.y_mm+view.height_mm>drawing.sheet.height_mm:issues.append(f"view_out_of_bounds:{view.view_id}")
        for entity in drawing.entities:
            ids.append(entity.entity_id)
            if entity.layer not in layer_names:issues.append(f"unknown_layer:{entity.entity_id}")
            points=[(entity.x1,entity.y1),(entity.x2,entity.y2)] if isinstance(entity,(Line,Dimension)) else [(entity.x,entity.y)]
            if any(x<0 or y<0 or x>drawing.sheet.width_mm or y>drawing.sheet.height_mm for x,y in points):issues.append(f"entity_out_of_bounds:{entity.entity_id}")
            if isinstance(entity,Text) and (not entity.value.strip() or any(c in entity.value for c in "<>")):issues.append(f"unsafe_text:{entity.entity_id}")
        if len(ids)!=len(set(ids)):issues.append("duplicate_entity_ids")
        return sorted(set(issues))
