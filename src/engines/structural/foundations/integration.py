from engines.parametric.parameters import ParameterAccess, ParameterDefinition, ParameterType
from engines.regeneration import RegenerationItem
def foundation_parameter_definitions():
    return (
        ParameterDefinition("length","Longitud",ParameterType.LENGTH,unit="m",minimum=0.01,default_value=1.0),
        ParameterDefinition("width","Ancho",ParameterType.LENGTH,unit="m",minimum=0.01,default_value=1.0),
        ParameterDefinition("depth","Profundidad",ParameterType.LENGTH,unit="m",minimum=0.01,default_value=0.5),
        ParameterDefinition("plan_area","Área",ParameterType.AREA,unit="m²",access=ParameterAccess.CALCULATED,default_value=0.0),
        ParameterDefinition("volume","Volumen",ParameterType.VOLUME,unit="m³",access=ParameterAccess.CALCULATED,default_value=0.0),
    )
class FoundationRegenerationAdapter:
    def __init__(self, engine, regeneration_engine): self.engine=engine; self.regeneration_engine=regeneration_engine
    def register(self, foundation_id):
        item=RegenerationItem(f"foundation:{foundation_id}",lambda:self.engine.calculate(foundation_id),priority=25)
        self.regeneration_engine.register(item); return item
