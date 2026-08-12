from analysis.solid3d.solid3d_domain import SolidNode,SolidElement
class VolumetricMeshEngine:
    def unit_tetra(self):
        n=(SolidNode("N1",(0,0,0)),SolidNode("N2",(1,0,0)),SolidNode("N3",(0,1,0)),SolidNode("N4",(0,0,1)))
        return n,(SolidElement("E1",("N1","N2","N3","N4"),"MAT"),)
