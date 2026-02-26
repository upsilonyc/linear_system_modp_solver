import pytest

from solver.alg import solve_modular_system


def test_basic_2x2():
    matrix = [[1, 1, 2], [1, -1, 0]]
    assert solve_modular_system(matrix, 7) == [1, 1]


def test_3x3():
    matrix = [[1, 1, 1, 1], [1, 2, 3, 4], [2, 3, 1, 5]]
    assert solve_modular_system(matrix, 7) == [5, 3, 0]


def test_no_solution():
    # singular matrix mod 5
    matrix = [[1, 1, 2], [2, 2, 4]]
    with pytest.raises(ArithmeticError):
        solve_modular_system(matrix, 5)


def test_non_square():
    matrix = [[1, 2, 3]]
    with pytest.raises(ValueError):
        solve_modular_system(matrix, 3)
