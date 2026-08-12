from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PlatformCommand:
    command_type:str; payload:object=None
@dataclass(frozen=True,slots=True)
class CommandResult:
    completed:bool; value:object=None; error:str|None=None
class CommandBus:
    def __init__(self): self._handlers={}
    def register_handler(self,name,handler,replace=False):
        if name in self._handlers and not replace: raise ValueError("Handler duplicado")
        self._handlers[name]=handler
    def execute(self,command):
        h=self._handlers.get(command.command_type)
        if h is None:return CommandResult(False,None,"Sin handler")
        try:return CommandResult(True,h(command.payload),None)
        except Exception as e:return CommandResult(False,None,str(e))
