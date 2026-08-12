def axial_stiffness(E,A,L):
    if min(E,A,L)<=0: raise ValueError("Valores positivos requeridos")
    k=E*A/L
    return ((k,-k),(-k,k))
