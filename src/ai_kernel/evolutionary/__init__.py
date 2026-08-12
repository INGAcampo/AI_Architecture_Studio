from dataclasses import dataclass
from random import Random

@dataclass(frozen=True, slots=True)
class Genome:
    genome_id: str
    genes: tuple[float, ...]

@dataclass(frozen=True, slots=True)
class EvolutionResult:
    generation: int
    population: tuple[Genome, ...]
    best: Genome
    best_fitness: float

class EvolutionarySolver:
    def __init__(self, *, seed=0):
        self.random = Random(seed)

    def mutate(self, genome, *, rate=0.1, scale=1.0):
        genes = []
        for gene in genome.genes:
            if self.random.random() < rate:
                gene += self.random.uniform(-scale, scale)
            genes.append(gene)
        return Genome(genome.genome_id, tuple(genes))

    def crossover(self, left, right, child_id):
        genes = tuple(
            a if index % 2 == 0 else b
            for index, (a, b) in enumerate(zip(left.genes, right.genes))
        )
        return Genome(child_id, genes)

    def evolve(self, population, fitness, *, generations=1):
        population = tuple(population)
        best = max(population, key=fitness)
        for generation in range(1, generations + 1):
            ranked = sorted(population, key=fitness, reverse=True)
            elite = ranked[:max(1, len(ranked)//2)]
            children = list(elite)
            while len(children) < len(population):
                left = elite[len(children) % len(elite)]
                right = elite[(len(children)+1) % len(elite)]
                child = self.crossover(left, right, f"g{generation}-{len(children)}")
                children.append(self.mutate(child, rate=0.5, scale=0.25))
            population = tuple(children)
            best = max(population, key=fitness)
        return EvolutionResult(generations, population, best, fitness(best))
