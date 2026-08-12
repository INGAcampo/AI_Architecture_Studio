class ContactActiveSet:
    def active(self,gaps): return tuple(i for i,g in enumerate(gaps) if g<=0)
