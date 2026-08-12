from engines.parametric.parameters import ParameterAccess, ParameterDefinition, ParameterType
from engines.regeneration import RegenerationItem
def facade_parameter_definitions():
    return (
        ParameterDefinition("width","Ancho",ParameterType.LENGTH,unit="m",minimum=.1,default_value=1),
        ParameterDefinition("height","Altura",ParameterType.LENGTH,unit="m",minimum=.1,default_value=1),
        ParameterDefinition("gross_area","Área bruta",ParameterType.AREA,unit="m²",access=ParameterAccess.CALCULATED,default_value=0),
        ParameterDefinition("glass_area","Área vidrio",ParameterType.AREA,unit="m²",access=ParameterAccess.CALCULATED,default_value=0),
        ParameterDefinition("panel_count","Paneles",ParameterType.INTEGER,access=ParameterAccess.CALCULATED,default_value=0),
    )
class FacadeRegenerationAdapter:
    def __init__(self,engine,regeneration_engine):self.engine=engine;self.regeneration_engine=regeneration_engine
    def register(self,facade_id):
        item=RegenerationItem(f"facade:{facade_id}",lambda:self.engine.calculate(facade_id),priority=55)
        self.regeneration_engine.register(item);return item
