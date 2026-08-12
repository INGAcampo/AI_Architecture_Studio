"""Authority hierarchy and contradiction resolution for AIAS artifacts."""
AUTHORITY=("AIAS Charter","AIAS Constitution","AIAS SDD","Architecture Handbook","Program Specification","Generated Evidence")
def authority_rank(name:str)->int:
 """Return the lower-is-stronger authority rank for a canonical artifact type."""
 if name not in AUTHORITY:raise KeyError(name)
 return AUTHORITY.index(name)
def governing_authority(first:str,second:str)->str:
 """Return which of two artifact types governs a contradiction."""
 return first if authority_rank(first)<authority_rank(second) else second
