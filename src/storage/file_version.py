from dataclasses import dataclass
AIAS_FILE_VERSION = "1.0.0"
@dataclass(frozen=True, order=True)
class FileVersion:
    major:int; minor:int; patch:int=0
    @classmethod
    def parse(cls,value:str):
        parts=[int(p) for p in value.strip().split('.')]
        if not 1 <= len(parts) <= 3: raise ValueError(f"Versión AIAS inválida: {value!r}")
        while len(parts)<3: parts.append(0)
        return cls(*parts)
    def is_compatible_with(self,supported): return self.major==supported.major and self<=supported
    def __str__(self): return f"{self.major}.{self.minor}.{self.patch}"
