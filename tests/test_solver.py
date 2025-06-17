from solver import get_solver
from utils.cube_utils import apply_scramble
import pycuber as pc


def test_solve_trivial():
    solver = get_solver()
    assert solver.solve("") == []


def test_solve_single_move():
    solver = get_solver()
    solution = solver.solve("U")
    cube = apply_scramble("U")
    cube(pc.Formula(' '.join(solution)))
    assert cube == pc.Cube()
