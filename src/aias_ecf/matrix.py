"""Dense matrix algebra and linear solvers for deterministic engineering calculations."""
from __future__ import annotations
import math

class MatrixEngine:
    """Validate shapes and perform products, factorization, inversion and equation solving."""
    @staticmethod
    def shape(a):
        """Return matrix row and column counts while rejecting ragged input."""
        if not a or not a[0]:
            return (0, 0)
        cols = len(a[0])
        if any(len(row) != cols for row in a):
            raise ValueError("ragged_matrix")
        return (len(a), cols)

    @staticmethod
    def transpose(a):
        """Return rows and columns interchanged after shape validation."""
        MatrixEngine.shape(a)
        return [list(row) for row in zip(*a)]

    @staticmethod
    def multiply(a, b):
        """Multiply compatible dense matrices and reject incompatible shapes."""
        ra, ca = MatrixEngine.shape(a)
        rb, cb = MatrixEngine.shape(b)
        if ca != rb:
            raise ValueError("incompatible_shapes")
        return [[sum(a[i][k] * b[k][j] for k in range(ca)) for j in range(cb)] for i in range(ra)]

    @staticmethod
    def determinant(a):
        """Compute a square-matrix determinant using pivoted elimination."""
        n, m = MatrixEngine.shape(a)
        if n != m:
            raise ValueError("matrix_must_be_square")
        mat = [list(map(float, row)) for row in a]
        det = 1.0
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(mat[r][i]))
            if abs(mat[pivot][i]) < 1e-15:
                return 0.0
            if pivot != i:
                mat[i], mat[pivot] = mat[pivot], mat[i]
                det *= -1.0
            pivot_value = mat[i][i]
            det *= pivot_value
            for r in range(i + 1, n):
                factor = mat[r][i] / pivot_value
                for c in range(i + 1, n):
                    mat[r][c] -= factor * mat[i][c]
        return det

    @staticmethod
    def inverse(a):
        """Invert a nonsingular square matrix using Gauss-Jordan elimination."""
        n, m = MatrixEngine.shape(a)
        if n != m:
            raise ValueError("matrix_must_be_square")
        aug = [list(map(float, row)) + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(aug[r][i]))
            if abs(aug[pivot][i]) < 1e-15:
                raise ValueError("singular_matrix")
            aug[i], aug[pivot] = aug[pivot], aug[i]
            pv = aug[i][i]
            aug[i] = [v / pv for v in aug[i]]
            for r in range(n):
                if r == i:
                    continue
                factor = aug[r][i]
                aug[r] = [aug[r][c] - factor * aug[i][c] for c in range(2 * n)]
        return [row[n:] for row in aug]

    @staticmethod
    def solve(a, b):
        """Solve a nonsingular square linear system by pivoted elimination."""
        n, m = MatrixEngine.shape(a)
        if n != m or len(b) != n:
            raise ValueError("invalid_linear_system")
        aug = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(aug[r][i]))
            if abs(aug[pivot][i]) < 1e-15:
                raise ValueError("singular_matrix")
            aug[i], aug[pivot] = aug[pivot], aug[i]
            for r in range(i + 1, n):
                factor = aug[r][i] / aug[i][i]
                for c in range(i, n + 1):
                    aug[r][c] -= factor * aug[i][c]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))) / aug[i][i]
        return x

    @staticmethod
    def lu_decompose(a):
        """Factor a square matrix into lower and upper triangular matrices."""
        n, m = MatrixEngine.shape(a)
        if n != m:
            raise ValueError("matrix_must_be_square")
        l = [[0.0] * n for _ in range(n)]
        u = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for k in range(i, n):
                u[i][k] = a[i][k] - sum(l[i][j] * u[j][k] for j in range(i))
            if abs(u[i][i]) < 1e-15:
                raise ValueError("zero_pivot")
            for k in range(i, n):
                l[k][i] = 1.0 if i == k else (a[k][i] - sum(l[k][j] * u[j][i] for j in range(i))) / u[i][i]
        return l, u

    @staticmethod
    def cholesky(a):
        """Factor a positive-definite matrix into a lower triangular product."""
        n, m = MatrixEngine.shape(a)
        if n != m:
            raise ValueError("matrix_must_be_square")
        l = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                s = sum(l[i][k] * l[j][k] for k in range(j))
                if i == j:
                    value = a[i][i] - s
                    if value <= 0:
                        raise ValueError("matrix_not_positive_definite")
                    l[i][j] = math.sqrt(value)
                else:
                    l[i][j] = (a[i][j] - s) / l[j][j]
        return l
