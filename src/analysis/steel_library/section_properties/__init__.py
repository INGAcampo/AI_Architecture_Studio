class SectionPropertiesEngine:
    def rectangular_hollow(self,b,h,t):
        return {"area_mm2":b*h-(b-2*t)*(h-2*t),"ix_mm4":(b*h**3-(b-2*t)*(h-2*t)**3)/12,"iy_mm4":(h*b**3-(h-2*t)*(b-2*t)**3)/12}
