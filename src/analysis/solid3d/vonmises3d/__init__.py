from math import sqrt
class VonMises3DEngine:
    def calculate(self,sx,sy,sz,txy=0,tyz=0,tzx=0):
        return sqrt(.5*((sx-sy)**2+(sy-sz)**2+(sz-sx)**2)+3*(txy*txy+tyz*tyz+tzx*tzx))
