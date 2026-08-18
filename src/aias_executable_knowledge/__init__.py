"""Safely admitted and reproducibly executable engineering knowledge for AEKS."""
from .admission import KnowledgeAdmission
from .executor import DeclarativeKnowledgeExecutor
__all__=["KnowledgeAdmission","DeclarativeKnowledgeExecutor"]
__version__="1.0.0"
