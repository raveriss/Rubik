import pytest

from solver import get_solver


def test_solve_trivial():
    solver = get_solver()
    solution = solver.solve("")
    assert solution == []
