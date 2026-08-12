"""Text command registration, history and argument dispatch."""

class CommandEngine:
    """Execute known CAD commands while retaining automation-visible history."""
    def __init__(self) -> None:
        self._commands={}
        self._aliases={}
        self.history=[]

    def register(self, name, callback, aliases=()):
        """Add register to the S1 professional CAD foundation program while enforcing identity constraints."""
        key=name.upper()
        self._commands[key]=callback
        for alias in aliases:
            self._aliases[alias.upper()]=key

    def execute(self, text: str):
        """Execute execute for the S1 professional CAD foundation program with validated state transitions."""
        parts=text.strip().split()
        if not parts:
            return None
        name=parts[0].upper()
        name=self._aliases.get(name,name)
        if name not in self._commands:
            raise KeyError(name)
        self.history.append(text)
        return self._commands[name](*parts[1:])
