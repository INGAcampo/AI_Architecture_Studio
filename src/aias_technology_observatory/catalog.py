"""Curated, attributable initial observation catalog for ATO."""
from .sources import Observation

def initial_observations():
    """Return the first official-source observations shipped with ATO."""
    return [
        Observation("OBS-000001","NIST AI RMF continuous risk lifecycle","https://www.nist.gov/itl/ai-risk-management-framework","NIST","2026-08-03","Operationalize govern, map, measure and manage as a continuous AI risk cycle.","AI_GOVERNANCE",1.0),
        Observation("OBS-000002","NIST AI Resource Center TEVV resources","https://airc.nist.gov/","NIST","2026-08-03","Use testing, evaluation, verification and validation resources to strengthen trustworthy AI evidence.","AI_ASSURANCE",1.0),
        Observation("OBS-000003","NIST Generative AI Profile","https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf","NIST","2026-08-03","Map generative-AI risks and actions across the AI lifecycle.","GENERATIVE_AI_RISK",1.0),
    ]
