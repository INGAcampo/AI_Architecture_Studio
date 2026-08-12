class MaterialHistory:
    def __init__(self):self.states=[]
    def add(self,s):self.states.append(s)
    def latest(self):return self.states[-1] if self.states else None
