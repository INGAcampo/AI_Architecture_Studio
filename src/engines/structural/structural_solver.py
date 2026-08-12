from models.structural.solver_result import SolverResult


class StructuralSolver:

    @staticmethod
    def solve(model, load_case=None):

        result = SolverResult()

        result.load_case = load_case

        return result
