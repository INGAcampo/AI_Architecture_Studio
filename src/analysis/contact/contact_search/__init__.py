class ContactSearchEngine:
    def candidate_pairs(self,slave,master,radius):
        return tuple((i,j) for i,s in enumerate(slave) for j,m in enumerate(master) if sum((s[k]-m[k])**2 for k in range(len(s)))**.5<=radius)
