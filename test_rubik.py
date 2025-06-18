# test_rubik.py
import pytest
from rubik import parse_mix, ParseError, Cube, solve

def test_parse_mix_valide():
    assert parse_mix("U R2 F'") == ["U", "R2", "F'"]

def test_parse_mix_invalide():
    with pytest.raises(ParseError):
        parse_mix("X Y Z")

def test_cube_solved_initialement():
    cube = Cube()
    assert cube.is_solved()

def test_move_inverse():
    cube = Cube()
    cube.apply_moves(["U", "U'", "R", "R'"])
    assert cube.is_solved()

def test_solve_simple_scramble():
    scramble = ["U", "R", "U'", "R'"]
    solution = solve(scramble)
    # Appliquer le scramble puis la solution doit redonner l'état résolu
    cube = Cube()
    cube.apply_moves(scramble)
    cube.apply_moves(solution)
    assert cube.is_solved()

def test_apply_U_changes_state():
    from rubik import Cube
    c = Cube()
    # État non trivial : chaque sticker a un ID unique 0..53
    c.state = list(range(54))
    st0 = c.state.copy()
    c.apply_moves(["U"])
    # On doit voir 20 stickers déplacés (le centre reste fixe)
    assert c.state != st0
    diffs = sum(1 for a,b in zip(st0, c.state) if a != b)
    assert diffs == 20

def test_solve_one_move():
    from rubik import solve, Cube
    scramble = ["U"]
