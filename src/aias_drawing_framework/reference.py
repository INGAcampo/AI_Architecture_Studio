"""Immediate professional foundation-sheet consumer for the drawing framework."""
from .models import Dimension,Drawing,Layer,Line,Sheet,Text,View
def foundation_sheet()->Drawing:
    """Create an A3 reference foundation plan with traceability and review status."""
    sheet=Sheet("SHT-F-001","F-001","FOUNDATION PLAN",420,297,"0","LIGHTHOUSE-001","AIAS","PROFESSIONAL_REVIEWER")
    layers=(Layer("OBJECTS","#000000",.35),Layer("DIMENSIONS","#000000",.18),Layer("TEXT","#000000",.18))
    entities=(Line("L1","OBJECTS",120,90,300,90),Line("L2","OBJECTS",300,90,300,210),Line("L3","OBJECTS",300,210,120,210),Line("L4","OBJECTS",120,210,120,90),Dimension("D1","DIMENSIONS",120,90,300,90,-12,5000,"mm"),Dimension("D2","DIMENSIONS",300,90,300,210,12,4000,"mm"),Text("T1","TEXT",20,280,"LIGHTHOUSE-001 / FOUNDATION PLAN",4),Text("T2","TEXT",20,15,"REFERENCE ONLY - PROFESSIONAL REVIEW REQUIRED",3))
    return Drawing("DRW-FOUND-001","1.0.0",sheet,layers,(View("V1","PLAN",50,100,70,220,160,"ECP-000001D"),),entities,{"source":"ECP-000001D","project":"LIGHTHOUSE-001"},True)
