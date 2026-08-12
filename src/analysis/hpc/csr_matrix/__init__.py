class CSRMatrix:
    def __init__(self,nrows,ncols,triplets):
        self.nrows=nrows;self.rows=[[] for _ in range(nrows)]
        for r,c,v in triplets:self.rows[r].append((c,v))
    def matvec(self,x):return tuple(sum(v*x[c] for c,v in row) for row in self.rows)
