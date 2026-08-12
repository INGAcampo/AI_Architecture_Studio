from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class FacadeQuantities:
    gross_area:float
    panel_area:float
    mullion_area:float
    glass_area:float
    opaque_area:float
    panel_count:int
class FacadeQuantityCalculator:
    def calculate(self,facade,catalog):
        panel_area=facade.panel_width*facade.panel_height
        glass=opaque=0.0
        for v in range(facade.grid.v_divisions):
            for u in range(facade.grid.u_divisions):
                type_id=facade.panel_overrides.get((u,v),facade.default_panel_type_id)
                panel=catalog.get(type_id)
                if panel.kind.value=="glass":glass+=panel_area
                else:opaque+=panel_area
        mullion_area=max(0.0,facade.gross_area-glass-opaque)
        return FacadeQuantities(facade.gross_area,panel_area,mullion_area,glass,opaque,facade.grid.panel_count)
