from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class FrameAdvice:
    summary:str
    warnings:tuple[str,...]
    recommendations:tuple[str,...]

class SteelFrameAIAdvisor:
    def advise(self,dashboard,connectivity,load_path,optimization):
        warnings=[]
        recommendations=[]
        if not connectivity.valid:
            warnings.append("La conectividad del marco no es válida.")
        if not load_path.path_exists:
            warnings.append("No existe una ruta de carga hasta los apoyos.")
        if dashboard.failed_members:
            warnings.append(f"Existen {dashboard.failed_members} miembros que no cumplen.")
        if dashboard.critical_members:
            warnings.append(f"Miembros críticos: {', '.join(c.member_id for c in dashboard.critical_members)}.")
        if optimization.optimized_members:
            recommendations.append(f"Optimizar {optimization.optimized_members} miembros.")
        if optimization.average_weight_reduction_percent>0:
            recommendations.append(f"Reducción media estimada: {optimization.average_weight_reduction_percent:.2f}%.")
        summary="El marco es apto para continuar." if not warnings else "El marco requiere revisión."
        return FrameAdvice(summary,tuple(warnings),tuple(recommendations))
