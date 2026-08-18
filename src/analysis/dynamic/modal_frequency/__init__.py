from math import sqrt,pi
class ModalFrequencyEngine:
    def from_eigenvalue(self,value):
        omega=sqrt(max(value,0));f=omega/(2*pi);t=float("inf") if f==0 else 1/f
        return omega,f,t
