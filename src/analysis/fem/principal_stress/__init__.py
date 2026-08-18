from math import sqrt
class PrincipalStress:
 def plane(self,sx,sy,t):
  a=(sx+sy)/2;r=sqrt(((sx-sy)/2)**2+t*t);return a+r,a-r
