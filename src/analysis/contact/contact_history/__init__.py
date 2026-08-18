class ContactHistory:
    def __init__(self): self.records=[]
    def add(self,*record): self.records.append(tuple(record))
    def latest(self): return self.records[-1] if self.records else None
