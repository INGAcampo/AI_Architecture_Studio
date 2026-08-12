# EKG-000001 Enterprise Knowledge Graph

EKG is the persistent golden-thread graph for AIAS. It stores stable typed concepts and relationships, source provenance, versions and temporal metadata. Atomic writes, endpoint validation and conflict detection protect integrity.

Queries cover adjacency, shortest directed paths and transitive downstream impact. Inference is deliberately limited to pre-approved two-hop rules; each inferred edge records its rule and supporting edges. Graph conclusions aid discovery and traceability and never replace licensed professional judgment.

The first production consumer imports the complete AMIR master concept inventory and its dependency network.
