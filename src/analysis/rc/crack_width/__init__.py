class CrackWidthEngine:
    def estimate(self,fs,spacing,cover,Es=200000): return 3*fs/Es*((cover*spacing)**(1/3))
