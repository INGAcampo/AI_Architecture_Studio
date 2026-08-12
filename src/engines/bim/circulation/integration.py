from engines.parametric.parameters import ParameterAccess, ParameterDefinition, ParameterType
from engines.regeneration import RegenerationItem
def circulation_parameter_definitions():
    return (
        ParameterDefinition("rise","Altura",ParameterType.LENGTH,unit="m",access=ParameterAccess.CALCULATED,default_value=0),
        ParameterDefinition("width","Ancho",ParameterType.LENGTH,unit="m",minimum=.5,default_value=1),
        ParameterDefinition("riser_height","Contrahuella",ParameterType.LENGTH,unit="m",minimum=.1,maximum=.22,default_value=.175),
        ParameterDefinition("tread_depth","Huella",ParameterType.LENGTH,unit="m",minimum=.22,default_value=.28),
        ParameterDefinition("path_length","Longitud",ParameterType.LENGTH,unit="m",access=ParameterAccess.CALCULATED,default_value=0),
    )
class CirculationRegenerationAdapter:
    def __init__(self,engine,regeneration_engine):self.engine=engine;self.regeneration_engine=regeneration_engine
    def register(self,item_id):
        item=RegenerationItem(f"circulation:{item_id}",lambda:self.engine.calculate(item_id),priority=50)
        self.regeneration_engine.register(item);return item
