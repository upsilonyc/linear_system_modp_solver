"""Core solver utilities for modular linear systems.

The solver works on an *augmented matrix* represented as a list of
lists.  Each row should contain the coefficients for the variables
followed by the constant term.  For a system with *n* variables there
must be *n* equations and each row will therefore have length ``n+1``.

We intentionally avoid external dependencies (``numpy``) so the
algorithm can be packaged lightly and even translated to other
languages for the web interface.
"""


def get_input(num_coef: int, num_eqs: int):
    """Interactively prompt the user for the augmented matrix.

    ``num_coef`` is the number of integers per row (including the
    constant), and ``num_eqs`` is the number of equations.  The caller
    is responsible for validating that the two are consistent; the
    routine will raise an ``AssertionError`` if they are not.
    """

    assert num_eqs == num_coef - 1, (
        f"expected {num_coef-1} equations for {num_coef-1} variables, "
        f"but got {num_eqs}"
    )

    matrix = []
    for eq in range(num_eqs):
        row = input(
            f"coefficients & constant for equation {eq} (space separated, "
            "e.g. 1 0 0 1 1): "
        )
        values = [int(x) for x in row.split()]
        if len(values) != num_coef:
            raise ValueError(
                f"expected {num_coef} values on row {eq}, got {len(values)}"
            )
        matrix.append(values)
    return matrix

def modular_inverse(a, p):
    """Finds the multiplicative inverse of 'a' modulo 'p' using Fermat's Little Theorem."""
    return pow(int(a), p - 2, p)

def solve_modular_system(matrix, p):
    """Solve a system of linear equations modulo a prime ``p``.

    ``matrix`` must be a list of ``m`` rows where each row has
    ``n+1`` entries (``n`` coefficients and the constant term).  The
    current implementation requires a square system (``m == n``) and
    will raise ``ValueError`` otherwise.  Returns a list containing the
    solution vector if a unique solution exists or raises an
    ``ArithmeticError`` when there is no unique solution.
    """

    # number of equations / variables
    m = len(matrix)
    if m == 0:
        return []

    n = len(matrix[0]) - 1
    if m != n:
        raise ValueError("only square systems are supported")

    # work on a copy to avoid mutating caller's data
    mat = [row[:] for row in matrix]

    for i in range(n):
        # 1. Find pivot
        pivot_row = i
        while pivot_row < n and mat[pivot_row][i] % p == 0:
            pivot_row += 1

        if pivot_row == n:  # no pivot in this column
            raise ArithmeticError("no unique solution exists")

        # swap into position
        mat[i], mat[pivot_row] = mat[pivot_row], mat[i]

        # scale pivot row to make leading coefficient 1
        inv = modular_inverse(mat[i][i], p)
        mat[i] = [(x * inv) % p for x in mat[i]]

        # eliminate the variable from all other rows
        for j in range(m):
            if i != j:
                factor = mat[j][i]
                mat[j] = [
                    (mat[j][k] - factor * mat[i][k]) % p for k in range(n + 1)
                ]

    return [int(row[-1]) for row in mat]