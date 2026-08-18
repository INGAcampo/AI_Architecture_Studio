from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StructuralSection:
    section_id: str
    area: float
    capacity: float
    mass_per_length: float
    cost_per_length: float

@dataclass(frozen=True, slots=True)
class StructuralDemand:
    demand_id: str
    required_capacity: float
    length: float

@dataclass(frozen=True, slots=True)
class StructuralOption:
    demand_id: str
    section_id: str
    utilization: float
    mass: float
    cost: float

class StructuralOptimizationEngine:
    def feasible_options(self, demand, sections):
        options = []
        for section in sections:
            if section.capacity < demand.required_capacity:
                continue
            options.append(StructuralOption(
                demand_id=demand.demand_id,
                section_id=section.section_id,
                utilization=demand.required_capacity / section.capacity,
                mass=section.mass_per_length * demand.length,
                cost=section.cost_per_length * demand.length,
            ))
        return tuple(options)

    def select_minimum_mass(self, demand, sections):
        options = self.feasible_options(demand, sections)
        if not options:
            raise ValueError("No existe una sección factible")
        return min(options, key=lambda option: (option.mass, option.cost))
