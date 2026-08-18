import pytest
from ai_kernel.evolutionary import *

@pytest.mark.parametrize("i", range(120))
def test_evolution(i):
    population = (
        Genome("A", (1.0, 2.0)),
        Genome("B", (2.0, 3.0)),
        Genome("C", (3.0, 4.0)),
        Genome("D", (4.0, 5.0)),
    )
    solver = EvolutionarySolver(seed=i)
    result = solver.evolve(population, lambda genome: sum(genome.genes), generations=2)
    assert len(result.population) == 4
    assert result.generation == 2
    assert result.best_fitness == max(sum(g.genes) for g in result.population)
