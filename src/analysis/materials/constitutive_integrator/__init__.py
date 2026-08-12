from analysis.materials.return_mapping import RadialReturnMapping
class ConstitutiveIntegrator:
    def integrate_j2(self,trial,G,y):return RadialReturnMapping().integrate(trial,G,y)
