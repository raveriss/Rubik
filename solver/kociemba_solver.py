from __future__ import annotations

from typing import List

import kociemba

from utils.cube_utils import apply_scramble, cube_to_kociemba


class KociembaSolver:
    """Wrapper around the kociemba two-phase solver."""

    def solve(self, scramble: str) -> List[str]:
        if not scramble:
            return []
        cube = apply_scramble(scramble)
        facelets = cube_to_kociemba(cube)
        solution = kociemba.solve(facelets)
        return solution.split()
