from __future__ import annotations

from typing import List, Optional

import pycuber as pc

from utils.cube_utils import apply_scramble


class SimpleSolver:
    """Brute-force solver using iterative deepening DFS."""

    MOVES = [
        "U", "U'", "U2",
        "R", "R'", "R2",
        "F", "F'", "F2",
        "D", "D'", "D2",
        "L", "L'", "L2",
        "B", "B'", "B2",
    ]

    def __init__(self, max_depth: int = 7) -> None:
        self.max_depth = max_depth

    def solve(self, scramble: str) -> List[str]:
        cube = apply_scramble(scramble)
        if cube == pc.Cube():
            return []
        for depth in range(self.max_depth + 1):
            solution = self._dfs(cube, depth, [], None)
            if solution is not None:
                return solution
        raise RuntimeError("Solution not found within depth limit")

    def _dfs(self, cube: pc.Cube, depth: int, path: List[str], last_face: Optional[str]) -> Optional[List[str]]:
        if depth == 0:
            if cube == pc.Cube():
                return path
            return None
        for move in self.MOVES:
            if last_face and move[0] == last_face:
                continue
            new_cube = cube.copy()
            new_cube(pc.Formula(move))
            result = self._dfs(new_cube, depth - 1, path + [move], move[0])
            if result is not None:
                return result
        return None
