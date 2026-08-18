from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class BasePlateReport: markdown:str
@dataclass(frozen=True,slots=True)
class BasePlateAdvice: message:str; recommendations:tuple

class BasePlateReportAI:
    def build(self,plate,result,optimization=None):
        lines=["# Base Plate Design Report","",f"- Plate: {plate.plate_id}",f"- Dimensions: {plate.width:.3f} x {plate.length:.3f} x {plate.thickness:.3f} m",f"- Maximum unity: {result.maximum_unity:.4f}",f"- Governing: {result.governing_check}",f"- Status: {'PASS' if result.passed else 'FAIL'}"]
        if optimization and optimization.recommended_dimensions:
            lines += ["",f"- Recommended: {optimization.recommended_dimensions}",f"- Steel reduction: {optimization.steel_reduction_percent:.2f}%"]
        return BasePlateReport("\n".join(lines)+"\n")
    def advise(self,result,optimization=None):
        rec=[]
        if optimization and optimization.recommended_dimensions: rec.append("Aplicar dimensiones optimizadas.")
        msg="La placa base cumple." if result.passed else "La placa base no cumple."
        return BasePlateAdvice(msg,tuple(rec))
